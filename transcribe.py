import soundfile as sf
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import os
import speech_recognition as sr

# transcribe audio using 'tokenizer' in this case Wav2Vec
def transcribe_tokenizer(sound_file):
    # load audio
    audio_input, _ = sf.read(sound_file)

    # transcribe
    input_values = tokenizer(audio_input, return_tensors="pt").input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(predicted_ids)[0]

    return transcription

# transcribe WAV files into folders for each user within a folder: "transcripts"
def transcribe_tokenizer_folder(target_folder):
    # go through all WAV files
    for file in os.listdir(target_folder):
        if file.endswith(".wav"):
            # get the username, output to named folder
            # naming convention - ID2C00_voice_tmp_[guid].wav
            username = str(file).split("_voice_")[0]
            filename = str(target_folder) +"/"+ "transcripts" + "/" + username + "/" + str(file)[:-3]+'txt'
            # output to user folder with same name .txt
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                f.write(transcribe_tokenizer(str(target_folder)+file))
                
                
# transcribe audio using 'tokenizer' in this case Wav2Vec
def transcribe_google(sound_file):
    # define speech recognizer object
    r = sr.Recognizer()
    # load audio
    audio_file= sr.AudioFile(sound_file)
    with audio_file as source:
        audio = r.record(source)
        
    # transcribe
    transcription = r.recognize_google(audio)
    
    return transcription

# transcribe WAV files into folders for each user within a folder: "transcripts"
def transcribe_google_folder(target_folder):
    # go through all WAV files
    for file in os.listdir(target_folder):
        if file.endswith(".wav"):
            # get the username, output to named folder
            # naming convention - ID2C00_voice_tmp_[guid].wav
            username = str(file).split("_voice_")[0]
            filename = str(target_folder) +"/"+ "transcripts" + "/" + username + "/" + str(file)[:-3]+'txt'
            # output to user folder with same name .txt
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                f.write(transcribe_google(str(target_folder)+file))
                print(str(target_folder)+file)