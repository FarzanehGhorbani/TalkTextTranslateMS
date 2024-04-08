import json
import logging
import os
import vosk
import wave
import time

import argostranslate.package
import argostranslate.translate

from ... import Application as app


class SpeechRecognizer:
    def __init__(self, lang, sample_rate=16000, log_level=0):
        """
        Initialize the SpeechRecognizer with the specified Vosk model.

        Args:
            model_path (str): Path to the Vosk model directory.
            sample_rate (int): Sampling rate of the audio data (default: 16000).
        """
        self.model = vosk.Model(lang=lang)
        self.recognizer = vosk.KaldiRecognizer(self.model, sample_rate)
        vosk.SetLogLevel(log_level)  # Set Vosk's internal log level

    def recognize_audio_file(self, audio_file, frame_size: int = 4000):
        """
        Recognize speech from an audio file using Vosk.

        Args:
            audio_file (str): Path to the input audio file (WAV format).
            frame_size (int): Number of audio frames to process per iteration

        Returns:
            str: Recognized text from the audio.
        """

        wf = wave.open(audio_file, "rb")
        print(wf)
        while True:
            data = wf.readframes(frame_size)
            if len(data) == 0:
                break
            data = self.recognizer.AcceptWaveform(data)

        os.remove("temp.wav")
        return self.recognizer.FinalResult()


class Translator:
    from_code: str = "en"  # Default source language code is English
    to_code: str = "fa"  # Default target language code is Persian
    translation = None  # This will hold the translation engine

    def __init__(self, from_code: str, to_code: str):
        # Constructor to initialize the translation setup if different language codes are provided
        if from_code != "en" or to_code != "fa":
            self.translation = (
                None  # Reset translation to None if codes are not default
            )
            self.from_code = from_code
            self.to_code = to_code

    @classmethod
    def setup_translation(cls):
        # Class method to set up translation engine if not already set
        if not cls.translation:
            argostranslate.package.update_package_index()
            available_packages = argostranslate.package.get_available_packages()
            # Find the appropriate translation package matching source and target language codes
            package = next(
                (
                    p
                    for p in available_packages
                    if p.from_code == cls.from_code and p.to_code == cls.to_code
                ),
                None,
            )
            if package:
                download_path = package.download()  # Download the translation package
                argostranslate.package.install_from_path(
                    download_path
                )  # Install the package

    @classmethod
    def load_translation(cls):
        """Class method to load translation engine"""
        if not cls.translation:
            installed_languages = argostranslate.translate.get_installed_languages()
            # Find source language
            from_lang = next(
                (lang for lang in installed_languages if lang.code == cls.from_code),
                None,
            )
            # Find target language
            to_lang = next(
                (lang for lang in installed_languages if lang.code == cls.to_code),
                None,
            )
            if from_lang and to_lang:
                cls.translation = from_lang.get_translation(
                    to_lang
                )  # Create translation engine

    def translate(self, text: str)-> str:
        """Method to translate text using the translation engine


        Args:
            text (str): _description_

        Returns:
            str: translated text
        """

        try:
            if self.translation:
                return self.translation.translate(text)  # Translate the text
            else:
                return None  # Return None if translation engine is not available
        except Exception as e:
            logging.info(f"Error translating text: {e}")
            return None


def talk_text_translator_tasks(
    audio_file: str, from_language_code: str, to_language_code: str, **model_kwargs
):
    # fetch text
    start_time = time.time()
    recognizer = SpeechRecognizer(**model_kwargs)
    recognized_text = recognizer.recognize_audio_file(audio_file)
    text = json.loads(recognized_text)["text"]
    # start translator
    translator = Translator(from_code=from_language_code, to_code=to_language_code)
    translator.setup_translation()
    translator.load_translation()
    translated_text: str | None = translator.translate(text)
    app.translated_speech_result = translated_text
    logging.info(f"text: {translated_text}, duration: {time.time()-start_time}")
