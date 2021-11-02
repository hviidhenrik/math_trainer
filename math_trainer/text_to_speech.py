import multiprocessing
from gtts import gTTS
from playsound import playsound
import os
import time

# get the speech from google API and save it locally
tts = gTTS("Hvad er 5 + 5", lang="da")
tts.save("temp.mp3")
#
playsound("temp.mp3")
# p = multiprocessing.Process(target=playsound, args=("temp.mp3",))
# p.start()
# p.terminate()
# os.remove("temp.mp3")

try:
    os.remove("temp.mp3")
except FileNotFoundError:
    pass

time.sleep(2)

# get the speech from google API and save it locally
tts = gTTS("Hvad er 8 + 8", lang="da")
tts.save("temp.mp3")

playsound("temp.mp3")
# p = multiprocessing.Process(target=playsound, args=("temp.mp3",))
# p.start()
# p.terminate()
