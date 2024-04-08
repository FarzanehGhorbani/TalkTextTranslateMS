from typing import Optional
from fastapi import UploadFile
from ... import Application as app


class TalkTextTranslatorRepository:

    async def start_get_text(self, file: UploadFile):
        with open("temp.wav", "wb") as audio_file:
            content = await file.read()
            audio_file.write(content)

    def get_text(self)-> tuple[Optional[str],str]:
        text = app.translated_speech_result
        message=''
        if not text:
            message = "If you have already uploaded the file, please wait for a while"
        return text,message
