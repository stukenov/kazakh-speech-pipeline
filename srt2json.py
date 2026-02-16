import re
import json
import glob

def parse_srt(srt_file_path):
    subtitles = []
    with open(srt_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n', re.DOTALL)
        matches = pattern.finditer(content)
        for match in matches:
            index = int(match.group(1))
            start_time = match.group(2)
            end_time = match.group(3)
            text = match.group(4).replace('\n', ' ')
            subtitle = {'index': index, 'start_time': start_time, 'end_time': end_time, 'text': text}
            subtitles.append(subtitle)
    return subtitles

def save_subtitles_to_json(directory):
    srt_files = glob.glob(f"{directory}/*.srt")
    for srt_file in srt_files:
        subtitles = parse_srt(srt_file)
        json_file_path = srt_file.replace('.srt', '.json')
        json_directory = json_file_path.replace('/captions/', '/captions/json/')
        with open(json_directory, 'w', encoding='utf-8') as json_file:
            json.dump(subtitles, json_file, ensure_ascii=False, indent=4)
