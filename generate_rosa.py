"""
Generate audiobook: El Nombre de la Rosa
Uses ElevenLabs v3 with audio tags and uploads to Dropbox.

Handles chunking for texts over 5000 chars, concatenates MP3 segments,
and generates glossary audio for each chapter.
"""

import os
import sys
import glob
import requests
import json
import time

ELEVEN_API_KEY = os.environ["ELEVEN_API_KEY"].strip().strip('"\u201c\u201d')
DROPBOX_TOKEN = os.environ["DROPBOX_TOKEN"]
VOICE_ID = "syjZiIvIUSwKREBfMpKZ"  # Jacobo Montoro
MAX_CHARS = 4900  # stay safely under 5000 limit


def tts(text, label="chunk"):
    """Generate MP3 bytes from text via ElevenLabs v3."""
    print(f"  Generating TTS for {label} ({len(text)} chars)...")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    resp = requests.post(
        url,
        headers={
            "xi-api-key": ELEVEN_API_KEY,
            "Content-Type": "application/json",
        },
        json={
            "text": text,
            "model_id": "eleven_v3",
            "language_code": "es",
            "voice_settings": {"stability": 0.4, "similarity_boost": 0.8},
        },
        timeout=300,
    )
    if resp.status_code != 200:
        print(f"  ElevenLabs error {resp.status_code}: {resp.text}")
        raise SystemExit(1)
    print(f"  Got {len(resp.content)} bytes")
    return resp.content


def chunk_text(text):
    """Split text into chunks under MAX_CHARS, breaking at paragraph boundaries."""
    if len(text) <= MAX_CHARS:
        return [text]

    chunks = []
    paragraphs = text.split("\n\n")
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 > MAX_CHARS:
            if current:
                chunks.append(current.strip())
            current = para
        else:
            current = current + "\n\n" + para if current else para

    if current.strip():
        chunks.append(current.strip())

    return chunks


def upload_dropbox(mp3_data, dropbox_path):
    """Upload MP3 data to Dropbox."""
    print(f"  Uploading to Dropbox: {dropbox_path} ({len(mp3_data)} bytes)...")
    resp = requests.post(
        "https://content.dropboxapi.com/2/files/upload",
        headers={
            "Authorization": f"Bearer {DROPBOX_TOKEN}",
            "Dropbox-API-Arg": json.dumps({
                "path": dropbox_path,
                "mode": "overwrite",
            }),
            "Content-Type": "application/octet-stream",
        },
        data=mp3_data,
    )
    if resp.status_code == 200:
        result = resp.json()
        print(f"  Uploaded: {result['path_display']} ({result['size']} bytes)")
    else:
        print(f"  Dropbox error {resp.status_code}: {resp.text}")
        raise SystemExit(1)


def generate_file(text_path, dropbox_name):
    """Generate audio for a text file, handling chunking if needed."""
    with open(text_path) as f:
        text = f.read()

    print(f"\n{'='*60}")
    print(f"Processing: {text_path}")
    print(f"Total length: {len(text)} chars")

    chunks = chunk_text(text)
    print(f"Split into {len(chunks)} chunk(s)")

    mp3_parts = []
    for i, chunk in enumerate(chunks):
        label = f"chunk {i+1}/{len(chunks)}" if len(chunks) > 1 else "full text"
        mp3_parts.append(tts(chunk, label))
        if i < len(chunks) - 1:
            time.sleep(1)  # brief pause between API calls

    mp3_data = b"".join(mp3_parts)

    # Save locally
    local_name = dropbox_name.split("/")[-1]
    with open(local_name, "wb") as f:
        f.write(mp3_data)
    print(f"  Saved locally: {local_name}")

    upload_dropbox(mp3_data, dropbox_name)
    return mp3_data


def main():
    # With naming like 001_cap1, 001g_cap1_glosario, 002_cap2, etc.,
    # a simple sorted glob gives the right order: chapter then glossary.
    all_files = sorted(glob.glob("texts/[0-9]*_el_nombre_de_la_rosa_*.txt"))

    print(f"Found {len(all_files)} file(s)")

    for text_path in all_files:
        basename = os.path.basename(text_path).replace(".txt", "")
        dropbox_name = f"/libros/{basename}.mp3"
        generate_file(text_path, dropbox_name)

    print(f"\n{'='*60}")
    print("All done!")


if __name__ == "__main__":
    main()
