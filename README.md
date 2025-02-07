# yt-summarize
Summarize YouTube videos.

```
video_url="https://www.youtube.com/watch?v=LwOITqr_fz4"
yt-dlp --write-auto-subs --sub-lang en --convert-subs srt --skip-download $video_url
yt-dlp --write-subs --sub-lang en --convert-subs srt --skip-download $video_url
```