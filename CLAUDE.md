# Libros

Generate audiobooks in pre-intermediate to intermediate Spanish for language learning through comprehensible input.

## Services

- **ElevenLabs** - Text-to-speech generation. Use the `eleven_v3` model with `language_code: "es"`. Supports inline audio tags like `[sighs]`, `[whispers]`, `[curious]` for expressive narration. 5,000 character limit per request. API key is in `ELEVEN_API_KEY` env var (strip smart quotes if present).
- **Dropbox** - Storage for generated MP3 files. Token is in `DROPBOX_TOKEN` env var. Upload to `/libros/` path.

## Voice

Using **Jacobo Montoro** (`syjZiIvIUSwKREBfMpKZ`) — warm male Andalusian Spanish narrator. Settings: stability 0.4, similarity_boost 0.8.

## Project Structure

- `texts/` — Source text files, numbered with zero-padded prefixes for sort order (e.g. `001_el_nombre_de_la_rosa_cap1.txt`). Target A2-B1 Spanish level: short sentences, controlled vocabulary, rich detail.
- `*.mp3` files are generated artifacts and not committed (see `.gitignore`).
- `generate_rosa.py` — Generation script for El Nombre de la Rosa. Reads text, calls ElevenLabs v3, uploads to Dropbox.
- `test_hello_world.py` — Minimal end-to-end test of ElevenLabs + Dropbox.

## Notes

- The ElevenLabs v3 API uses the same `/v1/text-to-speech/{voice_id}` endpoint — just set `model_id` to `eleven_v3`.
- v3 audio tags (square brackets) are NOT SSML. Use `[sighs]`, `[whispers]`, `[curious]`, etc. For pauses, use ellipses (`...`).
- The Dropbox app (ID: 6619331) needs `files.content.write` scope enabled, and the token must be regenerated after changing permissions for new scopes to take effect.
- For long texts exceeding 5,000 chars, chunk into multiple API calls and concatenate the MP3s.
