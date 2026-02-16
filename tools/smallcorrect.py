
def split_sentences(text):
    import re
    # Regular expression pattern to match sentence endings followed by a space
    pattern = re.compile(r'(\. |\! |\? )')
    # Find the first occurrence of sentence ending
    match = pattern.search(text)
    if match:
        # Find the index of the first character of the match
        index = match.start()
        # Split the text into two sentences at the index of the sentence ending
        sentence1 = text[:index+1]
        sentence2 = text[index+2:]
        return sentence1, sentence2
    else:
        # If no sentence ending is found, return the original text and None
        return text, None


# split_sentences("This is a sentence. This is another sentence.")
# print(split_sentences("соқпай кету"))

import json

def read_json_to_python_object(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def initialize_text_fields(captions):
    for caption in captions:
        caption['text_1'] = caption.get('text_1', '')  # Initialize 'text_1' if not present
    return captions

def split_and_assign_sentences(captions):
    for i, caption in enumerate(captions):
        text = caption['text']
        sentence1, sentence2 = split_sentences(text)
        if sentence1 and sentence2:
            caption['text_2'] = sentence1
            caption['text_3'] = sentence2
            # If there is a next caption, set its 'text_1' to the current caption's 'text_3'
            if i + 1 < len(captions):
                captions[i + 1]['text_1'] = sentence2
        else:
            caption['text_2'] = text
            caption['text_3'] = None
            # If there is a next caption, set its 'text_1' to None
            if i + 1 < len(captions):
                captions[i + 1]['text_1'] = None
    return captions

def merge_text_fields(captions):
    processed_captions = []
    for caption in captions:
        # Create 'merged_text' by concatenating 'text_1', 'text_2' with spaces, excluding None values
        caption['merged_text'] = ' '.join(filter(None, [caption.get('text_1'), caption.get('text_2')]))
        processed_captions.append(caption)
    return processed_captions

def save_as_srt(captions, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for caption in captions:
            file.write(f"{caption['index']}\n")
            file.write(f"{caption['start_time']} --> {caption['end_time']}\n")
            file.write(f"{caption['text']}\n\n")


captions = read_json_to_python_object('content/captions/grammar/2MJOhrdfhF0.json')


save_as_srt(captions, 'content/captions/2MJOhrdfhF0.srt')



# Example usage:
# python_object = read_json_to_python_object('content/2MJOhrdfhF0.json')
# captions_with_initialized_fields = initialize_text_fields(python_object)
# captions_with_split_sentences = split_and_assign_sentences(captions_with_initialized_fields)
# processed_python_object = merge_text_fields(captions_with_split_sentences)
# save_as_srt(processed_python_object, 'content/captions/2MJOhrdfhF0.srt')
