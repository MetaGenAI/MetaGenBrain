import soundfile as sf
import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import os
import speech_recognition as sr
from pathlib import Path
import asyncio


# transcribe audio using 'tokenizer' in this case Wav2Vec
def transcribe_tokenizer(sound_file):
    # load audio
    # audio_input, _ = sf.read(sound_file)
    audio_input, _ = librosa.load(sound_file, sr=16000) # Downsample 44.1kHz to 8kHz

    # transcribe
    input_values = tokenizer(audio_input, return_tensors="pt").input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(predicted_ids)[0]

    return transcription

# sound_file = "C:/Program Files (x86)/Steam/steamapps/common/NeosVR/data/tmp/ID2C00_voice_tmp_b11162cd-756d-404e-846b-c0783c95676f.wav"
# transcribe_tokenizer(sound_file)

# load pretrained model
# print("Loading STT model...")
# tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")
# model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")
# print("STT model loaded.")

# transcribe WAV files into folders for each user within a folder: "transcripts"
async def transcribe_tokenizer_folder(target_folder):
    #check which WAV files are in the folder
    while True:
        files = sorted(Path(target_folder).glob("*voice_tmp*.wav"), key=os.path.getmtime, reverse=False)
        try:
            for file in files:
                new_file = str(file).replace("voice_tmp","voice")
                os.rename(file,new_file)
                yield new_file
        except:
            pass
        await asyncio.sleep(0.1)
        # yield None


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
