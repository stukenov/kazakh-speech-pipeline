import os
import sys
import subprocess

def print_error(message):
    sys.stderr.write(message)

def print_success(message):
    sys.stdout.write(message)

def exit_with_error():
    sys.exit(1)

def check_directory_exists(directory, directory_type):
    if not os.path.isdir(directory):
        print_error(f"The {directory_type} folder {directory} does not exist.\n")
        exit_with_error()

def is_video_file(file):
    return file.lower().endswith(('.mp4', '.mov', '.mkv', '.flv', '.wmv'))

def get_video_files(video_folder):
    return [f for f in os.listdir(video_folder) if os.path.isfile(os.path.join(video_folder, f)) and is_video_file(f)]

def run_subprocess(command):
    subprocess.run(command, check=True)

def handle_conversion_error(input_file_path, error):
    print_error(f"Failed to convert {os.path.basename(input_file_path)}: {error}\n")

def load_openai_api_key():
    return os.getenv('OPENAI_API_KEY')

def get_api_key():
    return load_openai_api_key()

def load_azure_speech_key():
    return os.getenv('AZURE_SPEECH_KEY')

def load_azure_speech_region():
    return os.getenv('AZURE_SPEECH_REGION')
