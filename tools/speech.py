import subprocess

def call_speech_to_text(input_audio_path, output_text_path):
    # Define the command to run the external process
    command = [
        'python3.10', 'azure-speech.py',
        '--input', input_audio_path,
        '--output', output_text_path,
        '--offline',
        '--key', 'e8d4495bdef04477b4b00f9cc18ab1e9',
        '--region', 'westeurope',
        '--language', 'ru-RU'
    ]
    
    # Run the command as a subprocess
    subprocess.run(command, check=True)
