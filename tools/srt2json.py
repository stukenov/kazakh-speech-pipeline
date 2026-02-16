import re
import json
import glob

def parse_subtitle_file(file_path):
    subtitles = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        if file_path.endswith('.srt'):
            pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n', re.DOTALL)
        elif file_path.endswith('.vtt'):
            pattern = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\n(.*?)\n\n', re.DOTALL)
        else:
            raise ValueError("Unsupported file format")
        
        matches = pattern.finditer(content)
        for match_num, match in enumerate(matches):
            if file_path.endswith('.srt'):
                index = int(match.group(1))
                start_time = match.group(2)
                end_time = match.group(3)
                text = match.group(4).replace('\n', ' ')
            elif file_path.endswith('.vtt'):
                index = match_num + 1
                start_time = match.group(1).replace('.', ',')
                end_time = match.group(2).replace('.', ',')
                text = match.group(3).replace('\n', ' ')
            subtitle = {'index': index, 'start_time': start_time, 'end_time': end_time, 'text': text}
            subtitles.append(subtitle)
    return subtitles

def save_subtitles_to_json(directory):
    subtitle_files = glob.glob(f"{directory}/*.srt") + glob.glob(f"{directory}/*.vtt")
    for subtitle_file in subtitle_files:
        subtitles = parse_subtitle_file(subtitle_file)
        json_file_path = subtitle_file.rsplit('.', 1)[0] + '.json'
        json_directory = json_file_path.replace('/captions/', '/captions/json/')
        with open(json_directory, 'w', encoding='utf-8') as json_file:
            json.dump(subtitles, json_file, ensure_ascii=False, indent=4)

# Convert SRT caption files to JSON
captions_folder = 'content/captions'

save_subtitles_to_json(captions_folder)

