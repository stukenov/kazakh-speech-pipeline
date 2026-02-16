from speechkit import ShortAudioRecognition

recognizeShortAudio = ShortAudioRecognition(session)
with open(str('/Users/tikhon/Desktop/out.wav'), str('rb')) as f:
    data = f.read()

print(recognizeShortAudio.recognize(data, format='lpcm', sampleRateHertz='48000'))

# Will be printed: 'text that need to be recognized'