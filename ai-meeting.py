import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from pytube import YouTube

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")

client = OpenAI(api_key=OPENAI_KEY)


def get_video_id(url):
    return url.split("v=")[1].split("&")[0]


def get_audio(url, audio_directory="./audio/"):
    video_id = get_video_id(url)
    file_path = os.path.join(audio_directory, f"{video_id}.mp3")
    if os.path.exists(file_path):
        print(f"Audio file already exists: {file_path}")
        return file_path

    yt = YouTube(url)
    audio_stream = yt.streams.get_audio_only()
    audio_stream.download(output_path=audio_directory, filename=f"{video_id}.mp3")
    print(f"Download completed and saved as {file_path}")
    return file_path


def transcribe_audio(audio_file_path):
    print("Transcribing audio with OpenAI...")
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file
        )
    print("Transcription complete.")
    return transcription.text


def get_transcript(
    url, transcript_directory="./transcripts/", audio_directory="./audio/"
):
    video_id = get_video_id(url)
    transcript_file_path = os.path.join(transcript_directory, f"{video_id}.txt")

    if os.path.exists(transcript_file_path):
        print(f"Transcript file already exists: {transcript_file_path}")
        with open(transcript_file_path, "r") as transcript_file:
            transcript_text = transcript_file.read()
        return transcript_text

    audio_file_path = os.path.join(audio_directory, f"{video_id}.mp3")
    transcript_text = transcribe_audio(audio_file_path)
    with open(transcript_file_path, "w") as transcript_file:
        transcript_file.write(transcript_text)
    print(f"Transcript file created: {transcript_file_path}")
    return transcript_text


def extract_references(transcription):
    print("Extracting references...")
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are an AI expert in analyzing conversation transcripts and extracting references. Please review the text and identify any software, movies, books, or other reference material referenced.",
            },
            {"role": "user", "content": transcription},
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "extract_references",
                    "description": "Extract all references to software, books, movies, and other reference materials from a meeting transcript.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "software": {
                                "type": "array",
                                "description": "Any software or software tools mentioned in the transcript",
                                "items": {"type": "string"},
                            },
                            "books": {
                                "type": "array",
                                "description": "Any books mentioned in the transcript",
                                "items": {"type": "string"},
                            },
                            "movies": {
                                "type": "array",
                                "description": "Any movies mentioned in the transcript",
                                "items": {"type": "string"},
                            },
                            "other": {
                                "type": "array",
                                "description": "Any other reference material mentioned in the transcript",
                                "items": {"type": "string"},
                            },
                        },
                        "required": ["software", "books", "movies", "other"],
                    },
                },
            }
        ],
        tool_choice="required",
    )

    json_response = json.loads(
        response.choices[0].message.tool_calls[0].function.arguments
    )
    return json_response


def main():
    video_url = input("Enter the YouTube video URL: ")
    get_audio(video_url)
    text = get_transcript(video_url)
    references = extract_references(text)
    print(f"References: {json.dumps(references, indent=4)}")


if __name__ == "__main__":
    main()
