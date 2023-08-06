import coreaudio
import numpy as np
import soundfile
data, fs = soundfile.read("test.wav")

print(coreaudio.all_speakers())
print(coreaudio.all_microphones())
print(coreaudio.default_speaker())
print(coreaudio.default_microphone())

print('playing...', end='')
with coreaudio.default_speaker().player(fs, channels=1) as p:
    p.play(data)
print(' done.')

print('recording...', end='')
with coreaudio.default_microphone().recorder(fs, channels=1) as r:
    data = r.record(44100)
print(' done.')

print('loopback...', end='')
data = np.zeros(512)
with coreaudio.default_speaker().player(fs, channels=1) as p, \
     coreaudio.default_microphone().recorder(fs, channels=1) as r:
    for n in range(100):
        data = r.record(512)
        p.play(data, wait=False)
print(' done.')
