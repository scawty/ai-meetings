# Feature: "Notable References" Extraction

### tl;dr

This is a prototype of a new feature idea for Fathom's meeting notetaker product that automatically extracts and lists software, books, movies, and other notable references from the transcript. The idea is to make these references available via the post-meeting page.

## Problem

One reason why a user might put pen to paper during a meeting is to remember a specific reference or resource that was mentioned. For instance, if a mentor recommends their mentee a book, an engineer mentions a new software tool that may be useful for solving a problem, or a prospect mentions a competitor's product which you haven't heard of during a discovery meeting.

## Solution Idea

- A new "Notable References" (or "Resources"? Haven't nailed the name down) section on the post-meeting page
- Users see a list of notable references, each tagged appropriately (e.g. book, software, blog post, etc.)
- Each reference links to a timestamp and/or snippet where the reference was mentioned

## Prototype Script

The prototype is a python script that takes as input a youtube URL containing the meeting that you want to be transcribed and prints a JSON object containing the categorized references.

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

This works fine as a demo, but the reliability is untested, we could probably improve the prompt to rename the references to be clearer, and the categorization could be more accurate. Here's a few ways I might test this feature and improve on it:

### Prompt engineering

- First, try the OpenAI playground/3rd party playground to experiment with prompt variations, eyeballing a few key examples for accuracy and quality. This could get us a significant improvement for lower effort, but it'd be hard to tell without building out evals.
- Get better defined category definitions for the function call to reduce junk results and miscategorization
- Try removing the strict category definitions and let the LLM choose how to categorize results (this would probably result in less consistency across meetings but a wider and more accurate set of categorizations)
- Use few-shot prompting by providing a couple of examples in context. We could try using transcript excerpts instead of full transcript to use less tokens

### Evaluations

- A more robust way of improving would be to assemble a dataset of meeting transcripts and high quality, categorized references. The labeling could be done manually for a smaller dataset or by using fiverr for a larger set (100ish would probably be sufficient based on this [guide](https://platform.openai.com/docs/guides/prompt-engineering/strategy-test-changes-systematically). The transcripts could come from public data such as GitLab's [Unfiltered Meetings YouTube Channel](https://www.youtube.com/@GitLabUnfiltered) or from internal transcripts. Then, split the dataset into test/validation sets where we can experiment and/or fine-tune with half and validate the results on the other half (manually through random selection, brute force, or through a 3rd party LLM-experimentation tool) using a few pre-defined metrics. One eval which may apply here is [basic/json_match.py:JsonMatch](https://github.com/openai/evals/blob/main/docs/eval-templates.md)

### Other ideas

- Use embeddings search on the transcript to increase reliability (instead of function calling) and reduce any hallucinations
- Explore cheaper traditional NLP methods (Eg. Named Entity Recognition)- LLM might be overkill
- Search mentions semantically, so I can find things like "book that Mike mentioned" or "CI tool that Jane recommended"
