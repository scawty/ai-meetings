# Feature: "Notable References" Extraction

### tl;dr

This is a demo of a new feature idea for Fathom's meeting notetaker product that automatically extracts and lists software, books, movies, and other notable references from the transcript. The idea is to make these references available via the post-meeting page.

## Problem

One reason why a user might put pen to paper during a meeting is to remember a specific reference or resource that was mentioned. For instance, if a mentor recommends their mentee a book, an engineer mentions a new software tool that may be useful for solving a problem, or a prospect mentions a competitor's product which you haven't heard of during a discovery meeting.

## Solution Idea

- A new "Notable References" (or "Resources"? Haven't nailed the name down) section on the post-meeting page
- Users see a list of notable references, each tagged appropriately (e.g. book, software, blog post, etc.)
- Each reference links to a timestamp and/or snippet where the reference was mentioned

## Demo Script

The demo is a python script that takes as input a youtube URL containing the meeting that you want to be transcribed and prints a JSON object containing the categorized references.

The script does the following:

1. Prompts the user for the youtube URL
2. Checks if the audio for this particular video has already been downloaded
3. If not, retrieves the audio via pytube and saves it named by video id
4. Uses OpenAI's Whisper to transcribe the audio and save it as .txt (if it doesn't yet exist)
5. Makes a call to GPT-4-turbo using [Function Calling](https://platform.openai.com/docs/guides/function-calling) to extract references
6. Prints JSON containing the extracted references

### examples

Two example audios/transcripts are provided. Enter them with "https://www.youtube.com/watch?v=" preceeding the video id (file name)

### limitations

The transcript is used in context, meaning very large transcripts may be outside the given context window.

## How I would improve it

This works fine as a demo, but the reliability is untested, we could probably improve the prompt to rename the references to be clearer, and the categorization could be more accurate. Here's one way I might test this feature and improve on it:

1. Assemble a dataset of meeting transcripts and high quality, categorized references. This could be done manually for a smaller dataset or by using fiverr for a larger set. The dataset itself could come from open data such as GitLab's [Unfiltered Meetings YouTube Channel](https://www.youtube.com/@GitLabUnfiltered) or from an internal transcripts
2. Split the dataset into test/validation sets where we can fine-tune with half and validate the results on the other half (manually through random selection, brute force, or through a 3rd party LLM-experimentation tool) using a few pre-defined metrics

### Other ideas

- Use embeddings search on the transcript to increase reliability (instead of function calling) and reduce any hallucinations
- Explore cheaper traditional NLP methods (Eg. Named Entity Recognition)- LLM might be overkill
