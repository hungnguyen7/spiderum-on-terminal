import platform
import uuid
import os
import pyttsx3
from gtts import gTTS
import playsound

class TTS:
    def __init__(self):
        self.tts_engine = None
        self.gtts = None
        
        if platform.system() == "Windows":
            self.tts_engine = pyttsx3.init()
            vietnamese_voice_found = False
            for voice in self.tts_engine.getProperty("voices"):
                if "Vietnamese" in voice.name:
                    print(f"Using voice: {voice.name}")
                    self.tts_engine.setProperty("voice", voice.id)
                    vietnamese_voice_found = True
                    break
            if not vietnamese_voice_found:
                raise RuntimeError("No Vietnamese voice found in pyttsx3 on Windows")
        else:
            self.gtts = gTTS

    def speak(self, text):
        if self.tts_engine:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        elif self.gtts:
            self._speak_with_gtts(text)
        else:
            raise RuntimeError("No TTS engine available")

    def _speak_with_gtts(self, text):
        tts = self.gtts(text, lang="vi")
        id = str(uuid.uuid4())
        filename = f"/tmp/{id}.mp3"  # Using /tmp for temporary files
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)  # Clean up the temporary file
