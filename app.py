import sys
from google import genai
import subprocess
import os
import shutil
import gradio as gr

def download_subtitles(url):
    # Execute the bash script and capture the output
    result = subprocess.run(
        ['bash', 'download_subtitles.sh', url],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Extract the last line from stdout which is the directory name
    stdout_lines = result.stdout.strip().split('\n')
    directory = stdout_lines[-1].strip()
    
    # Verify the directory exists
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory {directory} does not exist")
    
    # Find the .srt file in the directory
    srt_files = [f for f in os.listdir(directory) if f.endswith('.srt')]
    if not srt_files:
        raise FileNotFoundError(f"No .srt file found in {directory}")
    if len(srt_files) > 1:
        raise RuntimeError(f"Multiple .srt files found in {directory}")
    
    srt_path = os.path.join(directory, srt_files[0])
    return srt_path

def cleanup_directory(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The directory {folder_path} does not exist")
    # Remove the directory and all its contents
    shutil.rmtree(folder_path)
    
    
def srt_to_text(input_file):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)

    entries = content.strip().split("\n\n")
    output_lines = []

    for entry in entries:
        lines = entry.strip().split("\n")
        if len(lines) < 3:
            continue
        text_lines = lines[2:]
        for line in text_lines:
            stripped_line = line.strip()
            if stripped_line:
                if not output_lines or stripped_line != output_lines[-1]:
                    output_lines.append(stripped_line)

    return "\n".join(output_lines)

# url = "https://www.youtube.com/watch?v=B1dWbiXnz_s"
# subtitlesfile = download_subtitles(url)
# video_text = srt_to_text(subtitlesfile)
# cleanup_directory(os.path.dirname(subtitlesfile))

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# client = genai.Client(api_key=GEMINI_API_KEY)
# response = client.models.generate_content(
#     model='gemini-2.0-flash',
#     contents=f"Summarize following text chronollogically, make it long, use markdown: \n{video_text}",
# )

# print(response.text)

def get_transcript_text(url):
    try:
        print("Downloading subtitles...")
        subtitlesfile = download_subtitles(url)
        print("Extracting text from subtitles...")
        video_text = srt_to_text(subtitlesfile)
        print("Cleaning up...")
        cleanup_directory(os.path.dirname(subtitlesfile))
        return video_text
    except Exception as e:
        raise gr.Error(f"Error retrieving transcript: {e}")

def summarize_video(url, prompt):
    try:
        video_text = get_transcript_text(url)
        
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        final_prompt = prompt + "\n" + video_text
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=final_prompt,
        )
        summary = response.text
        
        return summary
    except Exception as e:
        return f"An error occurred: {str(e)}"

with gr.Blocks() as app:
    gr.Markdown("# YouTube Video Summarizer")
    
    with gr.Row():
        with gr.Column(scale=5):
            url_input = gr.Textbox(label="YouTube URL", placeholder="Enter YouTube URL here...")
        with gr.Column(scale=5):
            summarize_btn = gr.Button("Summarize", variant="primary")
    
    default_prompt = """Summarize the following text chronologically, make it long, use markdown:"""
    prompt_input = gr.Textbox(label="Prompt", value=default_prompt, lines=4)
    
    output = gr.Markdown()

    summarize_btn.click(
        fn=summarize_video,
        inputs=[url_input, prompt_input],
        outputs=output
    )

if __name__ == "__main__":
    app.launch()

