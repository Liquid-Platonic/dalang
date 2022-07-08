from speechbrain.pretrained.interfaces import foreign_class

classifier = foreign_class(
    source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
    pymodule_file="custom_interface.py",
    classname="CustomEncoderWav2vec2Classifier",
)

# Example 1
out_prob, score, index, text_lab = classifier.classify_file(
    "speechbrain/emotion-recognition-wav2vec2-IEMOCAP/anger.wav"
)
print(out_prob)
print(text_lab)

# Example 2
out_prob, score, index, text_lab = classifier.classify_file(
    "speechbrain/emotion-recognition-wav2vec2-IEMOCAP/hap.wav"
)
print(out_prob)
print(text_lab)

# Example 3
out_prob, score, index, text_lab = classifier.classify_file(
    "speechbrain/emotion-recognition-wav2vec2-IEMOCAP/neutral.wav"
)
print(out_prob)
print(text_lab)

# Example 4
out_prob, score, index, text_lab = classifier.classify_file(
    "speechbrain/emotion-recognition-wav2vec2-IEMOCAP/sad.wav"
)  # or classifier.classify_batch(wavs: torch.Tensor)

print(out_prob)
print(text_lab)

# Labels
# ["neutral", "anger", "hap", "sad"]
