import logging
import collections, queue, os, os.path
import numpy as np
import pyaudio
import wave
import webrtcvad
from halo import Halo
from scipy import signal
import websockets
import asyncio
import traceback
import transcribe
import translate
import punctuate

logging.basicConfig(level=20)

def make_iter():
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()
    def put(*args):
        loop.call_soon_threadsafe(queue.put_nowait, args)
    return queue, put

def main(source_lang, target_lang):
    # Start audio with VAD
    async def translator():
        async for file in transcribe.transcribe_tokenizer_folder("C:/Program Files (x86)/Steam/steamapps/common/NeosVR/data/tmp/"):
            # naming convention - ID2C00_voice_tmp_[guid].wav
            if file is not None:
                username = str(file).split("_voice_")[0]
                text = transcribe.transcribe_tokenizer(file)
                punctuated = punctuate.punctuate(text.lower())
                print("Recognized: %s" % punctuated)
                yield punctuated
                # translation = translate.translate(punctuated, source_lang, target_lang)
                # translation = punctuated
                # print("Translation: %s" % translation)
                # yield translation
                # os.remove(vad_file)
    # #
    async def send_result(websocket, path):
        result = translator()
        async for msg in result:
            try:
                print(msg)
                await websocket.send(msg)
                await websocket.send("hi")
            except Exception:
                traceback.print_exc()

    # async def test():
    #     result = translator()
    #     async for msg in result:
    #         print(msg)

    async def test2():
        frames = vad_audio.vad_collector()
        print(frames)
        async for frame in frames:
            if frame is not None:
                print(frame)
    # asyncio.get_event_loop().run_until_complete(test2())

    ##To connect with Neos websockets
    asyncio.get_event_loop().run_until_complete(websockets.serve(send_result, 'localhost', 8765))

    # asyncio.get_event_loop().run_until_complete(test())
    asyncio.get_event_loop().run_forever()
    # translator()
