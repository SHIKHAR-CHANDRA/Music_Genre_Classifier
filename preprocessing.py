import os
import librosa
import math
import json

DATASET_PATH="C:/Users/Shikhar/Desktop/dataset"
JSON_PATH="data.json"

SAMPLERATE= 22050
DURATION=30
SAMPLES_PER_TRACK=SAMPLERATE*DURATION

def save_mfcc(dataset_path, json_path, n_mfcc=13, n_fft=2048, hop_length=512, num_segments=5):
    data={
        "mapping":[],
        "mfcc":[],
        'labels':[],
        }
    num_samples_per_segment= int(SAMPLES_PER_TRACK/num_segments)
    expected_num_mffc_vectors_per_segment=math.ceil(num_samples_per_segment/hop_length)
    
    for i, (dirpath,dirnames,filenames) in enumerate(os.walk(dataset_path)):
        if dirpath is not dataset_path:
            dirpath_components=dirpath.split('/')
            semantic_label=dirpath_components[-1]
            data["mapping"].append(semantic_label)
            print("\nProcessing {}".format(semantic_label))
            
            for f in filenames:
                file_path=os.path.join(dirpath,f)
                signal,sr=librosa.load(file_path, sr=SAMPLERATE)
                for s in range(num_segments):
                    start_sample= num_samples_per_segment *s
                    finish_sample=start_sample+num_samples_per_segment
                    
                    
                    mfcc=librosa.feature.mfcc(signal[start_sample:finish_sample],sr=sr,n_fft=n_fft,n_mfcc=n_mfcc,hop_length=hop_length)
                    mfcc=mfcc.T
                    
                    if len(mfcc)==expected_num_mffc_vectors_per_segment:
                        data["mfcc"].append(mfcc.tolist())
                        data["labels"].append(i-1)
                        print("{},segment:{}".format(file_path, s+1))
    
    with open(json_path, "w") as fp:
        json.dump(data, fp, indent=4)
        
if __name__=="__main__":
    save_mfcc(DATASET_PATH, JSON_PATH, num_segments=10)        
        
        
        
        
        
        
        
