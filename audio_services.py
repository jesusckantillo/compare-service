import parselmouth
import scipy.fftpack as fourier
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as pearsonr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import numpy as np
from pydub import AudioSegment
import librosa as lr
import soundfile as sf


class AudioController:
    def __init__(self)->None:
        pass

    def clean_audios(self,audio_1, audio_2): #Audio1 person Audio2Bot
        person_audio = AudioSegment.from_file(audio_1, format="wav")
        silence_umbral = -40
        silent_segments = split_on_silence(person_audio, min_silence_len=100, silence_thresh=silence_umbral)
        clean_audio1 = sum(silent_segments)
        audio1_path ="cleanaudio1.wav"
        clean_audio1.export(audio1_path,format="wav")

        k, pr = lr.load(audio_1)
        y, sr =  lr.load(audio_2)

        original_duration = lr.get_duration(y=y, sr=sr)
        print(original_duration, "duracion original")

        objetive_duration = lr.get_duration(y=k, sr=pr)

        estiramiento_factor = original_duration/objetive_duration

        y_stretched = lr.effects.time_stretch(y=y, rate= estiramiento_factor)
        audio2_path = "cleanaudio2.wav"
        sf.write(audio2_path, y_stretched, sr)
        return [audio1_path, audio2_path]

    def compare_audio(self,audio_1, audio_2):
        audio_1 =parselmouth.Sound(audio_1)
        audio_2 =parselmouth.Sound(audio_2)
        def compare_graphs(intensity1, intensity2):
            len1 = len(intensity1)
            len2 = len(intensity2)
            if len1 > len2:
                intensity1 = intensity1[:len2]
            elif len1 < len2:
                intensity2 = intensity2[:len1]
            intensity1 = intensity1.flatten()
            intensity2 = intensity2.flatten()
            len1 = len(intensity1)
            len2 = len(intensity2)
            if len1 > len2:
                intensity1 = intensity1[:len2]
            elif len1 < len2:
                intensity2 = intensity2[:len1]
            correlation = np.correlate(intensity1, intensity2, mode='valid')[0]
            similarity_percentage = correlation / max(np.sum(intensity1 ** 2), np.sum(intensity2 ** 2))
            error_margin = np.std(intensity1 - intensity2)
            return similarity_percentage * 100, error_margin
        
        intensity1 = audio_1.to_intensity()
        intensity2 = audio_2.to_intensity()
        similarity, error = compare_graphs(intensity1.values, intensity2.values)
        return similarity, error
    


