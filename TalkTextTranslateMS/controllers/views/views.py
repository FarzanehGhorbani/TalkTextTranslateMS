import os
import wave
from fastapi import File, UploadFile, BackgroundTasks

from ..model.outcome_models import ContextResponseModel

from ..logics.logics import TalkTextTranslatorRepository
from . import router

from ..tasks.talk_text_translator_tasks import talk_text_translator_tasks
from ... import Application as app

from ...core import Response

@router.post("/set/")
async def transcribe_audio(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., media_type="audio/wav"),
):

    repository = TalkTextTranslatorRepository()
    await repository.start_get_text(file)
    background_tasks.add_task(
        talk_text_translator_tasks,
        audio_file="temp.wav",
        from_language_code="en",
        to_language_code="fa",
        lang="en-us",
    )
    return Response(
        status_code=202, message="Uploaded file. Please wait for a while"
    )


@router.get(path="/get/translated-text", response_model=ContextResponseModel)
async def get_translated_text():
    repository = TalkTextTranslatorRepository()
    text,message = repository.get_text()
    return Response(data={"content": text},message=message)
