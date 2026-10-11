# AI Podcast Clipper 🎬🤖

An end-to-end, local-only AI pipeline that transcribes video content, identifies viral highlights using a local Large Language Model, and automatically cuts and crops widescreen videos into 9:16 vertical short-form content (TikTok, Reels, Shorts).

Built with **Python**, **Whisper**, **Llama 3.2**, and **FFmpeg** to run completely offline without relying on expensive cloud APIs.

---

## 🌟 Key Features

* **Local Transcription**: Uses `faster-whisper` for fast, accurate speech-to-text with word-level timestamps.
* **Semantic Highlight Selection**: Leverages `Llama 3.2` running locally via **Ollama** to analyze transcript context and identify high-engagement segments.
* **Automated Vertical Cropping**: Converts widescreen (16:9) video clips into vertical mobile-friendly clips (9:16) using `moviepy` and `ffmpeg`.
* **Zero Cloud Costs**: 100% private and runs locally on standard consumer hardware.

---

## 🛠️ Tech Stack

* **Language**: Python 3.11+
* **Audio/Video Extraction**: `yt-dlp`, `FFmpeg`
* **Transcription**: `faster-whisper`
* **AI Engine**: `Ollama` running `llama3.2`
* **Video Processing**: `moviepy`

---

## 🚀 Getting Started & Usage

### System Requirements & Full Installation
Make sure you have [FFmpeg](https://ffmpeg.org/) installed and added to your system PATH, and [Ollama](https://ollama.com/) installed on your machine. 

Open your terminal and run the following commands sequentially:

```bash
# 1. Pull the Llama 3.2 model
ollama pull llama3.2

# 2. Clone the repository
git clone [https://github.com/YOUR_USERNAME/podcast-clipper.git](https://github.com/YOUR_USERNAME/podcast-clipper.git)
cd podcast-clipper

# 3. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# 4. Install required dependencies
pip install yt-dlp faster-whisper moviepy httpx "av<14.0.0"

# 5. Start Ollama server (in a separate terminal tab if needed)
ollama serve

# 6. Run the pipeline script
python main.py
```
Small steps, big code, endless possibilities. On to the next project! 💡⚡
