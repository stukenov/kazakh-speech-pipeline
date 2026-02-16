
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main_conversion_process():
    from convert import convert_videos_in_folder

    # Convert videos to audios
    video_folder = 'content/video'
    output_folder = 'content/audio'
    try:
        logging.info(f'Starting conversion from videos in {video_folder} to audios in {output_folder}')
        convert_videos_in_folder(video_folder, output_folder)
        logging.info('Conversion process completed')
    except Exception as e:
        logging.error(f'Error during video to audio conversion: {e}')

def main_speech_to_text_process():
    from speech import call_speech_to_text

    # Convert audio to text
    audio_folder = 'content/audio'
    output_folder = 'content/captions'
    try:
        os.makedirs(output_folder, exist_ok=True)  # Ensure the output folder exists
        logging.info(f'Output folder {output_folder} created or already exists')
        audio_files = [f for f in os.listdir(audio_folder) if os.path.isfile(os.path.join(audio_folder, f)) and f.lower().endswith('.wav')]

        for audio_file in audio_files:
            input_audio_path = os.path.join(audio_folder, audio_file)
            output_text_path = os.path.join(output_folder, os.path.splitext(audio_file)[0] + '.txt')
            logging.info(f'Converting {input_audio_path} to text and saving to {output_text_path}')
            call_speech_to_text(input_audio_path, output_text_path)
        logging.info('Speech to text conversion process completed')
    except Exception as e:
        logging.error(f'Error during speech to text conversion: {e}')

def convert_captions_to_json():
    from srt2json import save_subtitles_to_json
    # Convert SRT caption files to JSON
    captions_folder = 'content/captions'
    try:
        logging.info(f'Converting captions in {captions_folder} to JSON format')
        save_subtitles_to_json(captions_folder)
        logging.info('Conversion to JSON format completed')
    except Exception as e:
        logging.error(f'Error during captions to JSON conversion: {e}')

if __name__ == "__main__":
    try:
        main_conversion_process()
        # main_speech_to_text_process()
        # convert_captions_to_json()
        pass
    except Exception as e:
        logging.error(f'Error in main execution: {e}')
