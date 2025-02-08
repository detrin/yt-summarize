# yt-summarize
Summarize YouTube videos.

## Usage

### Local
```
uv venv --python=3.12
source .venv/bin/activate
uv pip install -r requirements.txt
python app.py
```
Now you can visit http://0.0.0.0:3000 and enjoy the app.

### Docker
```
docker build -t yt-summarize-app .
docker run -p 3000:3000 --name yt-summarize -e GEMINI_API_KEY=your_gemini_api_key_here yt-summarize-app
```
Now you can enjoy the app on http://localhost:3000. 

To remove the image
```
docker rm yt-summarize
```