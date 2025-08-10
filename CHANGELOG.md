# Changelog

## [1.0.5](https://github.com/aka0kuro/ovos-tts-plugin-lingva/tree/1.0.5) (2025-08-10)

**Chores:**
- Añadir `.gitignore` y limpiar artefactos locales de desarrollo

## [1.0.4](https://github.com/aka0kuro/ovos-tts-plugin-lingva/tree/1.0.4) (2025-08-05)

**BREAKING CHANGES:**
- Migrated from Google Translate (gTTS) to Lingva.ml API
- Changed plugin name from `ovos-tts-plugin-google-tx` to `ovos-tts-plugin-lingva`
- Removed dependency on gTTS library
- Added requests library dependency
- Updated configuration options

**New Features:**
- Privacy-focused TTS using Lingva.ml
- No API keys required
- Support for multiple Lingva instances
- Wide language support (100+ languages)
- Fallback mechanism for unsupported languages

**Configuration Changes:**
- Replaced `tld` and `slow` options with `lingva_instance`
- Simplified configuration structure
- Added support for custom Lingva instances

