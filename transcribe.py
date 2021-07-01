import soundfile as sf
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

# load pretrained model
print("Loading STT model...")
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")
print("STT model loaded.")


def transcribe(sound_file):
    # load audio
    audio_input, _ = sf.read(sound_file)

    # transcribe
    input_values = tokenizer(audio_input, return_tensors="pt").input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(predicted_ids)[0]

    return transcription


# transcribe WAV files into folders for each user within a folder: "transcripts"
def transcribe_folder(target_folder):
    # go through all WAV files
    for file in os.listdir(target_folder):
        if file.endswith(".wav"):
            # get the username, output to named folder
            # naming convention - ID2C00_voice_tmp_[guid].wav
            username = str(file).split("_voice_")[0]
            filename = str(target_folder) +"\\"+ "transcripts" + "\\" + username + "\\" + str(file)[:-3]+'txt'
            # output to user folder with same name .txt
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                f.write(transcribe(str(target_folder)+file))