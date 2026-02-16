import json
import glob

def load_subtitles_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def convert_to_srt(subtitles):
    srt_content = ""
    for subtitle in subtitles:
        srt_content += f"{subtitle['index']}\n"
        srt_content += f"{subtitle['start_time'].replace('.', ',')} --> {subtitle['end_time'].replace('.', ',')}\n"
        srt_content += subtitle['text'] + "\n\n"
    return srt_content  # Return the srt_content string

def convert_to_vtt(subtitles):
    vtt_content = "WEBVTT\n\n"
    for subtitle in subtitles:
        vtt_content += f"{subtitle['start_time']} --> {subtitle['end_time']}\n"
        vtt_content += subtitle['text'] + "\n\n"
    return vtt_content  # Return the vtt_content string

def save_subtitles(subtitles, file_path, format):
    if format == 'srt':
        content = convert_to_srt(subtitles)
    elif format == 'vtt':
        content = convert_to_vtt(subtitles)
    else:
        raise ValueError("Unsupported format")
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def convert_json_to_subtitles(directory):
    json_files = glob.glob(f"{directory}/*.json")
    for json_file in json_files:
        subtitles = load_subtitles_from_json(json_file)
        base_file_path = json_file.rsplit('.', 1)[0]
        save_subtitles(subtitles, f"{base_file_path}.srt", 'srt')
        save_subtitles(subtitles, f"{base_file_path}.vtt", 'vtt')

# Convert from JSON to SRT and VTT
captions_folder = 'content/captions/done_json'

convert_json_to_subtitles(captions_folder)
