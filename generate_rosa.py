"""
Generate audiobook: El Nombre de la Rosa, Chapter 1
Uses ElevenLabs v3 with audio tags and Dropbox upload.
"""

import os
import requests

ELEVEN_API_KEY = os.environ["ELEVEN_API_KEY"].strip().strip('""\u201c\u201d')
DROPBOX_TOKEN = os.environ["DROPBOX_TOKEN"]

# Read the text
with open("texts/el_nombre_de_la_rosa_cap1.txt") as f:
    text = f.read()

print(f"Text length: {len(text)} characters")

# ElevenLabs v3 TTS - Jacobo Montoro (warm male, Andalusian Spanish)
voice_id = "syjZiIvIUSwKREBfMpKZ"
url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

# v3 has a 5000 char limit, our text should fit
assert len(text) <= 5000, f"Text too long: {len(text)} chars (max 5000)"

print("Generating audio with ElevenLabs v3...")
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
    print(f"ElevenLabs error {resp.status_code}: {resp.text}")
    raise SystemExit(1)

mp3_data = resp.content
print(f"Got {len(mp3_data)} bytes of audio")

# Save locally
local_path = "el_nombre_de_la_rosa_cap1.mp3"
with open(local_path, "wb") as f:
    f.write(mp3_data)
print(f"Saved locally to {local_path}")

# Upload to Dropbox
print("Uploading to Dropbox...")
dropbox_path = "/libros/el_nombre_de_la_rosa_cap1.mp3"
resp2 = requests.post(
    "https://content.dropboxapi.com/2/files/upload",
    headers={
        "Authorization": f"Bearer {DROPBOX_TOKEN}",
        "Dropbox-API-Arg": '{"path": "' + dropbox_path + '", "mode": "overwrite"}',
        "Content-Type": "application/octet-stream",
    },
    data=mp3_data,
)

if resp2.status_code == 200:
    result = resp2.json()
    print(f"Uploaded to Dropbox: {result['path_display']} ({result['size']} bytes)")
else:
    print(f"Dropbox error {resp2.status_code}: {resp2.text}")
    raise SystemExit(1)

print("Done!")
