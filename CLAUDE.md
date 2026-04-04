# Libros

Generate audiobooks in pre-intermediate to intermediate Spanish for language learning through comprehensible input.

## Services

- **ElevenLabs** - Text-to-speech generation. Use the `eleven_multilingual_v2` model for Spanish. API key is in `ELEVEN_API_KEY` env var (note: the value may be wrapped in curly/smart quotes that need stripping).
- **Dropbox** - Storage for generated MP3 files. Token is in `DROPBOX_TOKEN` env var. Upload to `/libros/` path.

## Notes

- The ElevenLabs API is working and tested. See `test_hello_world.py` for a minimal example.
- The Dropbox app (ID: 6619331) needs `files.content.write` scope enabled, and the token must be regenerated after changing permissions for new scopes to take effect.
