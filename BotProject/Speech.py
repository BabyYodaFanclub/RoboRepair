from gtts import gTTS
import speech_recognition as sr
import time
from pydub import AudioSegment


def current_sec_time():
    return int(round(time.time() * 1000 * 1000))


# https://cloud.google.com/text-to-speech/quotas
TTS_contingent_per_min = 300
STT_contingent_per_min = 300
TTS_text_len = 5000

TMP_FOLDER = '.tmp/'


class ContingentReachedError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class Speech:

    TTS_file = TMP_FOLDER + 'tts.mp3'
    STT_file_wav = TMP_FOLDER + 'stt.wav'
    STT_file_ogg = TMP_FOLDER + 'stt.ogg'

    class __Speech:
        ttsCounter = []

        def __init__(self):
            self.tts_counter = []
            self.stt_counter = []

    instance = None

    def __init__(self):
        if not Speech.instance:
            Speech.instance = Speech.__Speech()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def have_text_to_speech_contingent(self) -> bool:
        current_time = current_sec_time()
        self.instance.tts_counter = list(filter(lambda t: t >= current_time + 60, self.instance.tts_counter))

        return len(self.instance.tts_counter) < TTS_contingent_per_min

    def have_speech_to_text_contingent(self) -> bool:
        current_time = current_sec_time()
        self.instance.stt_counter = list(filter(lambda t: t >= current_time + 60, self.instance.stt_counter))

        return len(self.instance.stt_counter) < STT_contingent_per_min

    def speech_to_text(self, voice_message) -> str:
        if not self.have_speech_to_text_contingent():
            raise ContingentReachedError('speechToText limit reached')

        self.stt_counter.append(current_sec_time())

        r = sr.Recognizer()

        voice_message.get_file().download(self.STT_file_ogg)
        audio = AudioSegment.from_ogg(self.STT_file_ogg)
        audio.export(self.STT_file_wav, format="wav")

        with sr.AudioFile(self.STT_file_wav) as source:
            audio = r.record(source)

        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def text_to_speech(self, text_message):
        if not self.have_text_to_speech_contingent():
            raise ContingentReachedError('textToSpeech limit reached')

        self.tts_counter.append(current_sec_time())
        text_message = text_message[:TTS_text_len]

        tts = gTTS(text_message)
        tts.save(self.TTS_file)
        return open(self.TTS_file, 'rb')
