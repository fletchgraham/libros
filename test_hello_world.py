"""
Hello world test: Generate a Spanish sentence with ElevenLabs TTS and upload to Dropbox.
"""

import os
import requests

ELEVEN_API_KEY = os.environ["ELEVEN_API_KEY"].strip().strip('""\u201c\u201d')
DROPBOX_TOKEN = os.environ["DROPBOX_TOKEN"]

# ElevenLabs TTS - using "Rachel" voice (21m00Tcm4TlvDq8ikWAM)
# A simple pre-intermediate Spanish sentence
text = "Hola, me llamo Carlos y me gusta mucho leer libros en español. Hoy es un buen día para aprender algo nuevo."

print("Generating audio with ElevenLabs...")
voice_id = "21m00Tcm4TlvDq8ikWAM"
url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

resp = requests.post(
    url,
    headers={
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json",
    },
    json={
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    },
)

if resp.status_code != 200:
    print(f"ElevenLabs error {resp.status_code}: {resp.text}")
    raise SystemExit(1)

mp3_data = resp.content
print(f"Got {len(mp3_data)} bytes of audio")

# Save locally as backup
local_path = "/home/user/libros/hello_world.mp3"
with open(local_path, "wb") as f:
    f.write(mp3_data)
print(f"Saved locally to {local_path}")

# Upload to Dropbox
print("Uploading to Dropbox...")
dropbox_path = "/libros/hello_world.mp3"
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

print("Hello world test complete!")
