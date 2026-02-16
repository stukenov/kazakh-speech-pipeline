from transformers import pipeline
import soundfile as sf
import torch
import requests
from io import BytesIO

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
transcriber = pipeline(model="openai/whisper-large-v2", device=device)
response = requests.get("https://speech.qazcorpora.kz/storage/2023/11/01//2ntV0B8ygb2Gi3LLbUMc1N21VHkYJnLLuSUkJbw0.wav")
audio_data = BytesIO(response.content)
audio_data, samplerate = sf.read(audio_data)
audio_data = audio_data.astype('float32')
result = transcriber(audio_data)
print(result)

# The model is designed to transcribe audio files, but it responds in English even for Kazakh audio files,
# although it appears to recognize the Kazakh text correctly.
