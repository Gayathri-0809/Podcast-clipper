import os
import json
import httpx
import yt_dlp
from faster_whisper import WhisperModel
from moviepy import VideoFileClip
from moviepy.video.fx import Crop

# --- CONFIGURATION ---
# Using a short public domain video URL for testing
YOUTUBE_URL = "https://www.youtube.com/watch?v=jNQXAC9IVRw"

def download_youtube_media(url):
    print("Step 1: Downloading video and audio from YouTube...")
    
    # 1. Download audio for transcription
    ydl_opts_audio = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
        ydl.download([url])
        
    # 2. Download single merged MP4 video file
    ydl_opts_video = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'downloaded_video.mp4',
        'merge_output_format': 'mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
        ydl.download([url])
        
    print("Download complete!")
    return "temp_audio.mp3", "downloaded_video.mp4"

def transcribe_audio(audio_path):
    print("Step 2: Transcribing audio with timestamps using Faster-Whisper...")
    # Runs locally on your computer for free
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path, beam_size=5)
    
    transcript_segments = []
    for segment in segments:
        transcript_segments.append({
            "start": round(segment.start, 2),
            "end": round(segment.end, 2),
            "text": segment.text.strip()
        })
    print(f"Transcription complete! Found {len(transcript_segments)} segments.")
    return transcript_segments

def find_best_clips_locally(transcript_segments):
    print("Step 3: Asking local Ollama (Llama 3.2) to find the viral highlight...")
    
    prompt = f"""
    Analyze this transcript with timestamps. Find 1 engaging, standalone segment (up to 30 seconds long) that makes a great short clip.
    Return ONLY a valid JSON object in this exact format (no extra text):
    {{
      "title": "Short catchy title",
      "start": 0.0,
      "end": 10.0,
      "reason": "Why this is interesting"
    }}

    Transcript data:
    {json.dumps(transcript_segments[:30])}
    """
    
    # Talk to local Ollama server running on your PC for FREE
    response = httpx.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False,
            "format": "json"
        },
        timeout=120.0
    )
    
    result_data = response.json()
    clip_data = json.loads(result_data["response"])
    print(f"AI Selected Clip: {clip_data['title']} ({clip_data['start']}s to {clip_data['end']}s)")
    return clip_data

def cut_vertical_clip(video_path, start_time, end_time, output_name):
    print("Step 4: Slicing video and cropping to vertical 9:16 format...")
    clip = VideoFileClip(video_path).subclipped(start_time, end_time)
    
    # Convert widescreen (16:9) to vertical mobile format (9:16)
    w, h = clip.size
    target_width = int(h * (9 / 16))
    
    # Ensure width and height are even numbers for Windows Media Player compatibility
    if target_width % 2 != 0:
        target_width -= 1
    if h % 2 != 0:
        h -= 1

    x_center = w / 2
    x1 = int(x_center - (target_width / 2))
    
    vertical_clip = clip.with_effects([Crop(x1=x1, y1=0, width=target_width, height=h)])
    
    # ffmpeg_params ensures yuv420p encoding for 100% Windows compatibility
    vertical_clip.write_videofile(
        output_name, 
        codec="libx264", 
        audio_codec="aac", 
        fps=24,
        ffmpeg_params=["-pix_fmt", "yuv420p"]
    )
    print(f"Successfully saved your clip to {output_name}!")

if __name__ == "__main__":
    audio_file, video_file = download_youtube_media(YOUTUBE_URL)
    transcript = transcribe_audio(audio_file)
    best_clip = find_best_clips_locally(transcript)
    cut_vertical_clip(video_file, best_clip["start"], best_clip["end"], "viral_short.mp4")