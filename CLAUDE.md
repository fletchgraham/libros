# Libros

Generate audiobooks in pre-intermediate to intermediate Spanish for language learning through comprehensible input.

## Services

- **ElevenLabs** - Text-to-speech generation. Use the `eleven_v3` model with `language_code: "es"`. Supports inline audio tags like `[sighs]`, `[whispers]`, `[curious]` for expressive narration. 5,000 character limit per request. API key is in `ELEVEN_API_KEY` env var (strip smart quotes if present).
- **Dropbox** - Storage for generated MP3 files. Token is in `DROPBOX_TOKEN` env var. Upload to `/libros/` path.

## Voice

Using **Jacobo Montoro** (`syjZiIvIUSwKREBfMpKZ`) — warm male Andalusian Spanish narrator. Settings: stability 0.4, similarity_boost 0.8.

## Project Structure

- `texts/` — Source text files, numbered with zero-padded prefixes for sort order (e.g. `001_el_nombre_de_la_rosa_cap1.txt`). Target A2-B1 Spanish level: short sentences, controlled vocabulary, rich detail.
- Glossaries use a `g` suffix on the number so they sort after their chapter: `001_...cap1.txt`, `001g_...cap1_glosario.txt`, `002_...cap2.txt`, etc.
- `*.mp3` files are generated artifacts and not committed (see `.gitignore`). They live in Dropbox under `/libros/`.
- `generate_rosa.py` — Generation script. Auto-discovers text files, chunks long texts at paragraph boundaries, concatenates MP3 segments, and uploads to Dropbox.
- `test_hello_world.py` — Minimal end-to-end test of ElevenLabs + Dropbox.

## Writing Conventions

- **Target ~8 hours per book.** These are meant to reduce friction of finding something new to listen to — long enough to live in the setting.
- **Don't simplify too heavily.** Include rich sensory detail: food, smells, weather, architecture, daily routines. The listener should feel like they inhabit the world, not just follow the plot.
- **A2-B1 Spanish level:** short sentences, controlled vocabulary, but rich description. Complexity comes from detail, not grammar.
- Each chapter opens with `Capítulo uno... [Title].` followed by a `...` pause.
- Each chapter ends with a `[quietly]` tag on the final lines, extra ellipses for slower delivery, and a trailing `...` for a few seconds of silence.
- Glossaries give ~10 key words per chapter with concise Spanish-only definitions — no English translations.
- Audio tags on dialogue must be separated from narrator attribution. Put the attribution first, then the tag on the dialogue:
  - **Wrong:** `[whispers] "Ha habido una muerte" ... dijo el abad`
  - **Right:** `El abad bajó la voz. [whispers] "Ha habido una muerte."`
  - This prevents the narrator voice from whispering "dijo el abad" along with the dialogue.

## El Nombre de la Rosa

Adapted from Umberto Eco's *The Name of the Rose*. A murder mystery in a medieval Italian monastery, 1327.

- Follows the book's 7-day structure, ~10 chapters per day, ~5 min each.
- Each day follows the canonical hours (Matins, Lauds, Prime, Terce, Sext, None, Vespers, Compline).
- Day 1 (chapters 001–010) is complete. Key characters introduced: Adso, Guillermo, Abad Abbone, Malaquías, Berengario, Jorge de Burgos, Severino, Salvatore, Benno. Central mystery: Adelmo's death, the forbidden library, a poisoned book about laughter.
- Day 2 (chapters 011–020) is complete. The library labyrinth and Finis Africae. Second death: Venantius. Aristotle's lost book on comedy revealed as the forbidden text. Jorge's sermon against laughter. Political subplot: Franciscan poverty debate.

## Notes

- The ElevenLabs v3 API uses the same `/v1/text-to-speech/{voice_id}` endpoint — just set `model_id` to `eleven_v3`.
- v3 audio tags (square brackets) are NOT SSML. Use `[sighs]`, `[whispers]`, `[curious]`, etc. For pauses, use ellipses (`...`).
- The Dropbox app (ID: 6619331) needs `files.content.write` scope enabled, and the token must be regenerated after changing permissions for new scopes to take effect.
- For long texts exceeding 5,000 chars, `generate_rosa.py` chunks at paragraph boundaries and concatenates the MP3 segments.
