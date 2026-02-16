import re

class Subtitle:
    def __init__(self, index, start_time, end_time, text):
        self.index = index
        self.start_time = start_time
        self.end_time = end_time
        self.text = text

def parse_srt(srt_file_path, start_index, end_index):
    subtitles = []
    with open(srt_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n', re.DOTALL)
        matches = pattern.finditer(content)
        for match in matches:
            index = int(match.group(1))
            if start_index <= index <= end_index:
                start_time = match.group(2)
                end_time = match.group(3)
                text = match.group(4).replace('\n', ' ')
                subtitles.append(Subtitle(index, start_time, end_time, text))
    return subtitles

import datetime
import re

def timecode_to_timedelta(timecode):
    """Converts a SRT timecode to a timedelta object."""
    hours, minutes, seconds = map(float, timecode.replace(',', '.').split(':'))
    return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

def find_long_gaps(srt_file_path, min_gap_nanoseconds=1e9):
    """Finds gaps between subtitles longer than min_gap_nanoseconds and returns their indices and lengths."""
    gaps = []
    with open(srt_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')
        matches = pattern.finditer(content)
        previous_end_time = None
        previous_index = None
        
        for match in matches:
            index = int(match.group(1))
            start_time = match.group(2)
            end_time = match.group(3)
            start_td = timecode_to_timedelta(start_time)
            
            if previous_end_time is not None:
                gap = start_td - previous_end_time
                gap_nanoseconds = gap.total_seconds() * 1e9
                if gap_nanoseconds >= min_gap_nanoseconds:
                    gaps.append((previous_index, index, gap_nanoseconds))
            
            previous_end_time = timecode_to_timedelta(end_time)
            previous_index = index
            
    return gaps

# Example usage:
gaps = find_long_gaps('video.srt', 1e9)
for gap in gaps:
    print(f"Gap between subtitle {gap[0]} and {gap[1]}: {gap[2]} nanoseconds")

# Example usage:
# subtitles = parse_srt('video.srt', 20, 30)
# for subtitle in subtitles:
#     print(subtitle.index, subtitle.start_time, subtitle.end_time, subtitle.text)
