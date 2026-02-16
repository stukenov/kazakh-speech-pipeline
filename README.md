# Kazakh Speech Pipeline

> End-to-end Kazakh speech recognition and grammar correction pipeline powered by Whisper and GPT-4

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## Overview

**Kazakh Speech Pipeline** is a comprehensive solution for converting Kazakh audio/video content into accurate, grammatically correct text. It combines the power of OpenAI's Whisper model for speech recognition with GPT-4 for intelligent grammar correction, specifically optimized for the Kazakh language.

This pipeline is ideal for:
- Transcribing Kazakh news broadcasts
- Creating subtitles for Kazakh video content
- Converting audio interviews to text
- Processing large batches of Kazakh media files

## Features

- **Automatic Speech Recognition**: Uses Whisper (including Kazakh-optimized models) for high-quality transcription
- **Azure Speech Services Integration**: Alternative recognition option with Azure Cognitive Services
- **Grammar Correction**: GPT-4-powered grammar correction tailored for Kazakh language
- **Subtitle Generation**: Supports both WebVTT and SubRip (SRT) formats
- **Video/Audio Processing**: Automatic conversion from video to audio format
- **Batch Processing**: Process multiple files efficiently
- **Flexible Pipeline**: Use individual components or the full end-to-end workflow

## Architecture

```
Input (Video/Audio) → Audio Extraction → Speech Recognition → Grammar Correction → Output (Text/Subtitles)
```

### Pipeline Components

1. **convert.py**: Converts video files to WAV audio (16kHz, mono)
2. **azure-speech.py**: Azure-based speech recognition with timing
3. **2-whisper-kazakh.py**: Whisper model-based transcription
4. **srt2json.py**: Converts SRT subtitles to JSON format
5. **grammar.py**: Grammar correction using GPT-4
6. **onegrammar.py**: Batch grammar correction
7. **correct.py**: Advanced subtitle merging and timing correction

## Installation

### Prerequisites

- Python 3.9 or higher
- FFmpeg (for video/audio conversion)
- CUDA-capable GPU (optional, for faster Whisper inference)

### Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

### Install Python Dependencies

```bash
# Clone the repository
git clone https://github.com/stukenov/kazakh-speech-pipeline.git
cd kazakh-speech-pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configure API Keys

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```ini
[DEFAULT]
OPENAI_API_KEY=your_openai_api_key_here

[AZURESPEECH]
AZURE_SUBSCRIPTION_KEY=your_azure_subscription_key_here
AZURE_SERVICE_REGION=westeurope
```

## Usage

### Quick Start

Process a complete pipeline from video to corrected text:

```python
python main.py
```

Edit `main.py` to uncomment the desired pipeline steps.

### Individual Components

#### 1. Convert Video to Audio

```python
from convert import convert_videos_in_folder

convert_videos_in_folder('content/video', 'content/audio')
```

#### 2. Transcribe with Whisper

```python
from transformers import pipeline
import soundfile as sf
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
transcriber = pipeline(model="anuragshas/whisper-large-v2-kk", device=device)

audio_data, samplerate = sf.read('audio.wav')
result = transcriber(audio_data.astype('float32'))
print(result)
```

#### 3. Transcribe with Azure Speech Services

```bash
python azure-speech.py \
  --input content/audio/sample.wav \
  --output output.srt \
  --offline \
  --key YOUR_AZURE_KEY \
  --region westeurope \
  --language kk-KZ \
  --srt
```

#### 4. Convert SRT to JSON

```python
from srt2json import save_subtitles_to_json

save_subtitles_to_json('content/captions')
```

#### 5. Apply Grammar Correction

```python
from onegrammar import process_json_file

process_json_file('content/captions/json/transcript.json')
```

### Advanced: Subtitle Timing Correction

The `correct.py` module provides advanced functionality for merging subtitle segments and correcting timing:

```python
from correct import parse_and_trim_subtitles, process_subtitles_for_timing, merge_subtitles

subtitles = parse_and_trim_subtitles('captions.json')
process_subtitles_for_timing(subtitles)
merge_subtitles(subtitles)
```

## Project Structure

```
kazakh-speech-pipeline/
├── 1-test-pipeline.py      # Pipeline testing script
├── 2-whisper-kazakh.py     # Whisper Kazakh model example
├── azure-speech.py         # Azure Speech Services integration
├── convert.py              # Video to audio conversion
├── correct.py              # Subtitle merging and timing
├── grammar.py              # Grammar correction (multi-file)
├── onegrammar.py           # Grammar correction (single file)
├── main.py                 # Main pipeline orchestrator
├── srt2json.py             # SRT to JSON converter
├── utils.py                # Utility functions
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## API Keys and Services

### OpenAI API
Required for grammar correction features. Get your API key from [OpenAI Platform](https://platform.openai.com/).

### Azure Speech Services (Optional)
Alternative to Whisper for speech recognition. More information at [Azure Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/speech-services/).

**Note**: The `azure-speech.py` script is based on Microsoft's sample code and requires additional helper modules (`caption_helper.py`, `helper.py`, `user_config_helper.py`) from the [Azure Cognitive Services Speech SDK samples](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/python/console). Download these files if you plan to use Azure Speech Services.

## Models

### Whisper Models
- **openai/whisper-large-v2**: General-purpose multilingual model
- **anuragshas/whisper-large-v2-kk**: Kazakh-optimized Whisper model (recommended)

### GPT-4
Used for intelligent grammar correction of Kazakh text while preserving timing information.

## Performance Tips

1. **GPU Acceleration**: Use CUDA-enabled GPU for 10-20x faster Whisper inference
2. **Batch Processing**: Process multiple files in parallel when possible
3. **Model Selection**: Use the Kazakh-optimized Whisper model for better accuracy
4. **Audio Quality**: 16kHz WAV format provides optimal balance between quality and processing speed

## Troubleshooting

### Common Issues

**FFmpeg not found:**
```bash
# Verify FFmpeg installation
ffmpeg -version
```

**CUDA out of memory:**
```python
# Use CPU instead
device = torch.device('cpu')
```

**API rate limits:**
- Implement delays between API calls
- Use batch processing for grammar correction

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI Whisper team for the speech recognition model
- Anurag Shas for the Kazakh-optimized Whisper model
- Azure Cognitive Services for speech recognition capabilities
- OpenAI GPT-4 for grammar correction

## Author

**Saken Tukenov** - [@stukenov](https://github.com/stukenov)

## Support

If you find this project helpful, please consider:
- Giving it a star on GitHub
- Sharing it with others working on Kazakh NLP
- Contributing improvements and bug fixes

---

Made with ❤️ for the Kazakh language community
