import assemblyai as aai
from liulianmao import logger

aai.settings.api_key = input("Please input assemblyai apikey")
transcriber = aai.Transcriber()
config = aai.TranscriptionConfig(speaker_labels=True)
transcript = transcriber.transcribe(input("Please input URI you want to transcribe"),config=config)

# demo
# transcriber.transcribe("https://assembly.ai/news.mp4")
# transcriber.transcribe("./my-local-audio-file.wav")


if transcript.status == aai.TranscriptStatus.error:
    print(transcript.error)
else:
    # logger.info(transcript.text) # 如果没带config
    for utterance in transcript.utterances:
        logger.info(f"Speaker {utterance.speaker}: {utterance.text}")