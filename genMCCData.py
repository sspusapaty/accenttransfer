from pydub import AudioSegment
import numpy as np
import python_speech_features as psf
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt

def get_aligned_mfccs(file_pair, output_length):
    """
    Takes a pair of file paths, returns aligned MFCC coefficients for the two
    audio clips
    """
    mfccs = []
    
    for file in file_pair:  
    
        sound = AudioSegment.from_file(file)   
        samples = np.array(list(sound.get_array_of_samples()))
    
        mfcc_samples = psf.mfcc(samples,
                    samplerate=16000,
                    winlen=0.025,
                    winstep=0.01,
                    numcep=13,
                    nfilt=26,
                    nfft=512,
                    lowfreq=0,
                    highfreq=None,
                    preemph=0.97,
                    ceplifter=22,
                    appendEnergy=True)
    
        mfccs.append(mfcc_samples)
    
    sample = mfccs[0]
    target = mfccs[1]
    
    distance, path = fastdtw(sample, target, dist=euclidean)
    
    sample_aligned = [sample[i] for (i, j) in path]
    target_aligned = [target[j] for (i, j) in path]
    
    aligned_length = len(sample_aligned)
    
    head_padding = [np.zeros(13) for i in range((output_length - aligned_length) // 2)]
    tail_padding = [np.zeros(13) for i in range((output_length - aligned_length) // 2)]
    
    padded_sample = head_padding + sample_aligned + tail_padding
    padded_target = head_padding + target_aligned + tail_padding
    
    return (np.array(padded_sample), np.array(padded_target))

def reconstruct_from_mfcc(coeffs):
    pass


print(get_aligned_mfccs(("Data/kaggle_cuts/bosnian3/Wednesday.mp3","Data/kaggle_cuts/english368/Wednesday.mp3"), 250)[0][125])