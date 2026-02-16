
import json
import re

def load_subtitles(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def trim_text(subtitle):
    subtitle['text'] = subtitle['text'].strip()
    subtitle['line_ended'] = subtitle['text'][-1] in {'.', '!', '?'} if subtitle['text'] else False

def parse_and_trim_subtitles(file_path):
    subtitles = load_subtitles(file_path)
    for subtitle in subtitles:
        trim_text(subtitle)
    return subtitles

def time_to_ms(time_str):
    
    hours, minutes, seconds, milliseconds = map(int, re.split('[:,]', time_str))
    return (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds

    
def calculate_duration(start_time, end_time):
    start_ms = time_to_ms(start_time)
    end_ms = time_to_ms(end_time)
    return end_ms - start_ms

def calculate_time_per_word(subtitle, duration_ms):
    num_words = len(subtitle['text'].split())
    return duration_ms // num_words if num_words else float('inf')

def format_time(duration_ms):
    milliseconds = duration_ms % 1000
    seconds = (duration_ms // 1000) % 60
    minutes = (duration_ms // (1000 * 60)) % 60
    hours = (duration_ms // (1000 * 60 * 60))
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def process_subtitles_for_timing(subtitles):
    for subtitle in subtitles:
        
        duration_ms = calculate_duration(subtitle['start_time'], subtitle['end_time'])
        time_per_word_ms = calculate_time_per_word(subtitle, duration_ms)
        subtitle['time_per_word'] = format_time(time_per_word_ms)
    
       
def find_sentence_end(text):
    return re.search(r'[.!?]', text)

def merge_texts(text1, text2, end_pos):
    return text1 + ' ' + text2[:end_pos+1], text2[end_pos+1:].strip()

def calculate_new_time(original_time, additional_ms):
    original_ms = time_to_ms(original_time)
    new_ms = original_ms + additional_ms
    return ms_to_time(new_ms)

def ms_to_time(milliseconds):
    hours = milliseconds // (1000 * 60 * 60)
    milliseconds -= hours * (1000 * 60 * 60)
    minutes = milliseconds // (1000 * 60)
    milliseconds -= minutes * (1000 * 60)
    seconds = milliseconds // 1000
    milliseconds -= seconds * 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def merge_subtitles(subtitles):
    for i in range(len(subtitles) - 1):
        if not subtitles[i].get('line_ended', True):
            next_text = subtitles[i + 1].get('text', '')
            first_sentence_end = find_sentence_end(next_text)
            if first_sentence_end:
                end_pos = first_sentence_end.start()
                merged_text, remaining_text = merge_texts(subtitles[i]['text'], next_text, end_pos)
                
                time_per_word_ms = time_to_ms(subtitles[i]['time_per_word'])
                num_words_merged_text = len(merged_text.split())
                duration_ms_for_merged_text = num_words_merged_text * time_per_word_ms
                
                merged_start_time = subtitles[i]['start_time']
                merged_end_time = calculate_new_time(merged_start_time, duration_ms_for_merged_text)
                
                subtitles[i]['merged_text'] = merged_text
                subtitles[i]['merged_start_time'] = merged_start_time
                subtitles[i]['merged_end_time'] = merged_end_time
                
                if remaining_text:
                    subtitles[i + 1]['text'] = remaining_text
                    num_words_next_text = len(next_text[:end_pos+1].split())
                    duration_ms_for_next_text = num_words_next_text * time_per_word_ms
                    subtitles[i + 1]['start_time'] = calculate_new_time(subtitles[i]['end_time'], duration_ms_for_next_text)
                else:
                    subtitles[i + 1]['start_time'] = merged_end_time

file_path = 'content/captions/json/68VwEkf7ahA.json'
try:
    trimmed_subtitles = parse_and_trim_subtitles(file_path)
    process_subtitles_for_timing(trimmed_subtitles)
    merge_subtitles(trimmed_subtitles)
    print(json.dumps(trimmed_subtitles, ensure_ascii=False, indent=2))
except (FileNotFoundError, ValueError, KeyError) as e:
    print(f"An error occurred: {e}")
