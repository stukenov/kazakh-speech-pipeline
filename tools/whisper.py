# Let's see how to use a user-managed pool for batch decoding multiple audios
from multiprocessing import get_context
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from datasets import load_dataset
import torch

# import model, feature extractor, tokenizer
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base")
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base")

# load example dataset
dataset = load_dataset("patrickvonplaten/librispeech_asr_dummy", "clean", split="validation")
dataset = dataset.cast("audio", "float32")

def map_to_pred(batch):
    inputs = processor(batch["speech"], sampling_rate=16_000, return_tensors="pt")
    inputs = {k: v for k, v in inputs.items()}

    with torch.no_grad():
        logits = model(**inputs).logits

    transcription = processor.batch_decode(logits.cpu().numpy(), skip_special_tokens=True)
    batch["transcription"] = transcription
    return batch

# prepare speech data for batch inference
dataset = dataset.map(map_to_pred, batched=True, batch_size=2, remove_columns=["audio"])

result = dataset["transcription"][:2]
