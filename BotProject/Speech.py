from gtts import gTTS
import speech_recognition as sr
import time
from pydub import AudioSegment

current_sec_time = lambda: int(round(time.time() * 1000 * 1000))

# https://cloud.google.com/text-to-speech/quotas
TTS_contigent_per_min = 300
TTS_text_len = 5000

class ContigentReachedError(Exception): 
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class Speech():
    class __Speech:
        ttsCounter = []

        def __init__(self):
            self.ttsCounter = []

    instance = None

    def __init__(self):
        if not Speech.instance:
            Speech.instance = Speech.__Speech()


    def __getattr__(self, name):
        return getattr(self.instance, name)


    def haveSpeechToTextContigent(self) -> bool:
        currentTime = current_sec_time()
        self.ttsCounter = list(filter(lambda time : time >= currentTime + 60, self.ttsCounter ) )

        return len(self.ttsCounter) < TTS_contigent_per_min



    def speechToText(self, voice_message) -> str:
        r = sr.Recognizer()

        voice_message.get_file().download('tmp/voice_message.ogg')
        audio = AudioSegment.from_ogg('tmp/voice_message.ogg')
        audio.export("tmp/voice_message.wav", format="wav")

        with sr.AudioFile("tmp/voice_message.wav") as source:
            audio = r.record(source)  # read the entire audio file

        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


    def textToSpeech(self, text_message):
        if not self.haveSpeechToTextContigent():
            raise ContigentReachedError('speechToText limit reached')

        self.ttsCounter.append(current_sec_time)
        text_message = text_message[:TTS_text_len]

        tts = gTTS(text_message)
        tts.save('tmp/voice.mp3')
        return open('tmp/voice.mp3', 'rb')
