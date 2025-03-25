# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)

import assemblyai as aai
from liulianmao import logger

aai.settings.api_key = input()
transcriber = aai.Transcriber()

transcript = transcriber.transcribe(input())
# transcript = transcriber.transcribe("https://assembly.ai/news.mp4")
# transcript = transcriber.transcribe("./my-local-audio-file.wav")

logger.info(transcript.text)