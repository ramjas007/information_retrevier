from information_retrevier.finding_mp4_paths import get_video_files
import os
import json
import shutil
from speech_recognition import Recognizer, AudioFile, UnknownValueError, RequestError
from pydub import AudioSegment
from pydub.utils import make_chunks
from tqdm import tqdm

# Initialize the recognizer
r = Recognizer()

def folder_delete(folder):
    """Delete the specified folder and its contents."""
    if os.path.exists(folder):
        shutil.rmtree(folder)

def create_directory(directory_path):
    """Create directory if it does not exist."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def extract_audio_chunks(video_path, audio_folder_path, chunk_length_ms=60000):
    """Extract audio from the video and split it into chunks."""
    video_file_name = os.path.splitext(os.path.basename(video_path))[0]
    video_audio_folder = os.path.join(audio_folder_path, video_file_name)
    
    create_directory(video_audio_folder)
    
    try:
        audio = AudioSegment.from_file(video_path, format="mp4")
    except Exception as e:
        print(f"Error loading audio from {video_path}: {e}")
        return []
    
    chunks = make_chunks(audio, chunk_length_ms)
    
    chunk_paths = []
    for i, chunk in enumerate(chunks):
        chunk_name = f"chunk_{i + 1}.wav"
        chunk_path = os.path.join(video_audio_folder, chunk_name)
        chunk.export(chunk_path, format="wav")
        chunk_paths.append(chunk_path)
    
    return chunk_paths

def transcribe_audio_chunks(audio_chunk_paths, text_folder_path, video_file_name):
    """Transcribe each audio chunk and save the transcriptions."""
    video_text_folder = os.path.join(text_folder_path, video_file_name)
    create_directory(video_text_folder)
    
    transcriptions = {}
    for chunk_path in audio_chunk_paths:
        try:
            with AudioFile(chunk_path) as source:
                audio_data = r.record(source)
                try:
                    text = r.recognize_google(audio_data)
                except UnknownValueError:
                    text = "Google Speech Recognition could not understand audio"
                except RequestError as e:
                    text = f"Could not request results from Google Speech Recognition service; {e}"
                except Exception as e:
                    text = f"Error transcribing audio: {str(e)}"
                
                chunk_name = os.path.basename(chunk_path)
                transcriptions[chunk_name] = text
                
                text_file_path = os.path.join(video_text_folder, f"{chunk_name}.txt")
                with open(text_file_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(text)
        except Exception as e:
            print(f"Error processing chunk {chunk_path}: {e}")
    
    return transcriptions

def process_videos(root_folder, audio_folder_path, text_folder_path):
    """Process each video file: extract audio and transcribe it."""
    video_file_paths = get_video_files(root_folder)

    create_directory(audio_folder_path)
    create_directory(text_folder_path)

    # Initialize a dictionary with root_folder as the parent node
    transcription_data = {}

    for path in tqdm(video_file_paths):
        if os.path.exists(path):
            print(f"Processing: {path}")
            
            # Extract and save audio in chunks
            video_file_name = os.path.splitext(os.path.basename(path))[0]
            audio_chunk_paths = extract_audio_chunks(path, audio_folder_path)
            
            if audio_chunk_paths:
                # Transcribe audio chunks
                transcriptions = transcribe_audio_chunks(audio_chunk_paths, text_folder_path, video_file_name)
                
                # Save transcription data to the JSON structure
                transcription_data[video_file_name] = {
                    "text_folder": os.path.join(text_folder_path, video_file_name),
                    "transcriptions": transcriptions
                }
            else:
                print(f"No audio chunks created for: {path}")
        else:
            print(f"File not found: {path}")

    # Delete the audio and root folder after processing
    folder_delete(audio_folder_path)
    
    # Save the transcription data to a JSON file in the parent directory of root_folder
    parent_directory = os.path.dirname(root_folder)
    json_file_path = os.path.join(parent_directory, "transcriptions.json")
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(transcription_data, json_file, indent=4)

    folder_delete(root_folder)
    
    print(f"Transcriptions JSON saved to: {json_file_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Process videos: extract audio chunks and transcribe.")
    parser.add_argument('root_folder', type=str, help="Root folder containing the videos.")
    parser.add_argument('audio_folder', type=str, help="Folder to save the audio chunks.")
    parser.add_argument('text_folder', type=str, help="Folder to save the transcriptions.")

    args = parser.parse_args()

    process_videos(args.root_folder, args.audio_folder, args.text_folder)
