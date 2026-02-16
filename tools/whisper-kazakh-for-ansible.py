import argparse
from transformers import pipeline
import soundfile as sf
import torch
import numpy as np
import sys
import json
import subprocess
import os

def transcribe_audio(file_path, output_file):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # Specify the language as 'kz' for Kazakh
    transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3", device=device, lang='kz')  
    
    # Check if the audio file is not in flac format
    if not file_path.endswith('.flac'):
        # Transcode the audio file to flac format
        flac_file_path = file_path.rsplit('.', 1)[0] + '.flac'
        subprocess.run(['ffmpeg', '-i', file_path, flac_file_path])
        file_path = flac_file_path
    
    data, samplerate = sf.read(file_path)
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)
    data = data.astype('float32')
    # Split the data into chunks of 1 minute (assuming samplerate of 44100 Hz)
    chunks = np.array_split(data, max(1, len(data) // (60 * samplerate)))  # Ensure at least one chunk
    result = []
    for chunk in chunks:
        result.append(transcriber(chunk))
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in result:
                f.write(json.dumps(item, ensure_ascii=False))  # Convert the result to string before writing to file
                f.write('\n')  # Write each transcription to a new line
    except Exception as e:
        sys.stderr.write(str(e))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transcribe Kazakh audio file.')
    parser.add_argument('file_path', type=str, help='Path of the audio file to transcribe.')
    parser.add_argument('output_file', type=str, help='Path of the output file to save the transcription.')
    args = parser.parse_args()
    transcribe_audio(args.file_path, args.output_file)
