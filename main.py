from fastapi import FastAPI, File, UploadFile, Form
from pydub import AudioSegment
import tempfile
import json
import os
from audio_services import AudioController
from generate_ai import sound_generator
audio_manager = AudioController()

app = FastAPI()

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@app.post("/clean_audios/")
async def procces_audios(audio_file: UploadFile = File(...), word:str = Form()):
    if audio_file.content_type.startswith("audio/"):
        file_path = os.path.join(UPLOAD_DIR, audio_file.filename)
        with open(file_path, "wb") as file_object:
            file_object.write(await audio_file.read())


        sound_generator(word)
        bot_sound = AudioSegment.from_mp3('bot_sound.mp3')
        bot_sound.export('bot_sound.wav',format='wav')
        
        audios_clean = audio_manager.clean_audios("bot_sound.wav", file_path)
        plots_comparative = audio_manager.compare_audio(audios_clean[0],audios_clean[1])
        return {"result": plots_comparative}
    else:
        return {"error": "El archivo no es un archivo de audio válido."}