import requests
import json
from urllib.parse import quote
from ovos_plugin_manager.templates.tts import TTS
from ovos_utils import classproperty
from ovos_utils.lang import standardize_lang_tag

# Map OVOS language tags to Lingva language codes
LINGVA_LANG_MAP = {
    "en": "en",
    "en-US": "en",
    "en-GB": "en",
    "en-AU": "en",
    "en-CA": "en",
    "en-IN": "en",
    "en-IE": "en",
    "en-ZA": "en",
    "en-NG": "en",
    "es": "es",
    "es-ES": "es",
    "es-US": "es",
    "es-MX": "es",
    "fr": "fr",
    "fr-FR": "fr",
    "fr-CA": "fr",
    "pt": "pt",
    "pt-PT": "pt",
    "pt-BR": "pt",
    "de": "de",
    "de-DE": "de",
    "de-AT": "de",
    "de-CH": "de",
    "it": "it",
    "it-IT": "it",
    "nl": "nl",
    "nl-NL": "nl",
    "nl-BE": "nl",
    "ru": "ru",
    "ru-RU": "ru",
    "ja": "ja",
    "ja-JP": "ja",
    "ko": "ko",
    "ko-KR": "ko",
    "zh": "zh",
    "zh-CN": "zh",
    "zh-TW": "zh",
    "ar": "ar",
    "ar-SA": "ar",
    "hi": "hi",
    "hi-IN": "hi",
    "tr": "tr",
    "tr-TR": "tr",
    "pl": "pl",
    "pl-PL": "pl",
    "sv": "sv",
    "sv-SE": "sv",
    "da": "da",
    "da-DK": "da",
    "no": "no",
    "no-NO": "no",
    "fi": "fi",
    "fi-FI": "fi",
    "cs": "cs",
    "cs-CZ": "cs",
    "sk": "sk",
    "sk-SK": "sk",
    "hu": "hu",
    "hu-HU": "hu",
    "ro": "ro",
    "ro-RO": "ro",
    "bg": "bg",
    "bg-BG": "bg",
    "hr": "hr",
    "hr-HR": "hr",
    "sr": "sr",
    "sr-RS": "sr",
    "sl": "sl",
    "sl-SI": "sl",
    "et": "et",
    "et-EE": "et",
    "lv": "lv",
    "lv-LV": "lv",
    "lt": "lt",
    "lt-LT": "lt",
    "el": "el",
    "el-GR": "el",
    "he": "he",
    "he-IL": "he",
    "th": "th",
    "th-TH": "th",
    "vi": "vi",
    "vi-VN": "vi",
    "id": "id",
    "id-ID": "id",
    "ms": "ms",
    "ms-MY": "ms",
    "ca": "ca",
    "ca-ES": "ca",
    "eu": "eu",
    "eu-ES": "eu",
    "gl": "gl",
    "gl-ES": "gl",
    "is": "is",
    "is-IS": "is",
    "mk": "mk",
    "mk-MK": "mk",
    "sq": "sq",
    "sq-AL": "sq",
    "bs": "bs",
    "bs-BA": "bs",
    "mt": "mt",
    "mt-MT": "mt",
    "cy": "cy",
    "cy-GB": "cy",
    "ga": "ga",
    "ga-IE": "ga",
    "gd": "gd",
    "gd-GB": "gd",
    "kw": "kw",
    "kw-GB": "kw",
    "br": "br",
    "br-FR": "br",
    "oc": "oc",
    "oc-FR": "oc",
    "co": "co",
    "co-FR": "co",
    "lb": "lb",
    "lb-LU": "lb",
    "rm": "rm",
    "rm-CH": "rm",
    "fur": "fur",
    "fur-IT": "fur",
    "sc": "sc",
    "sc-IT": "sc",
    "vec": "vec",
    "vec-IT": "vec",
    "lmo": "lmo",
    "lmo-IT": "lmo",
    "pms": "pms",
    "pms-IT": "pms",
    "lij": "lij",
    "lij-IT": "lij",
    "nap": "nap",
    "nap-IT": "nap",
    "scn": "scn",
    "scn-IT": "scn",
    "srd": "srd",
    "srd-IT": "srd",
    "vec": "vec",
    "vec-IT": "vec",
    "lmo": "lmo",
    "lmo-IT": "lmo",
    "pms": "pms",
    "pms-IT": "pms",
    "lij": "lij",
    "lij-IT": "lij",
    "nap": "nap",
    "nap-IT": "nap",
    "scn": "scn",
    "scn-IT": "scn",
    "srd": "srd",
    "srd-IT": "srd"
}


class LingvaTTS(TTS):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, audio_ext="mp3")
        self.lingva_instance = self.config.get("lingva_instance", "https://lingva.ml")

    def _download_tts_to_file(self, sentence: str, lang_code: str, wav_file: str) -> bool:
        """Try fetching TTS audio using Lingva in two steps:
        1) Primary: /api/tts/{lang}/{text} which should return audio bytes
        2) Fallback: /api/v1/audio/{lang}/{text} which returns JSON with an 'audio' byte array

        Returns True if the file was written successfully, False otherwise.
        """
        encoded_sentence = quote(sentence, safe="")

        # Step 1: try /api/tts
        tts_url = f"{self.lingva_instance}/api/tts/{lang_code}/{encoded_sentence}"
        headers = {
            "User-Agent": "OVOS-LingvaTTS/1.0 (+https://github.com/aka0kuro/ovos-tts-plugin-lingva)",
            "Accept": "audio/*,application/octet-stream;q=0.9,*/*;q=0.8"
        }
        try:
            response = requests.get(tts_url, headers=headers, timeout=30)
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "")
            if content_type.startswith("audio/") or content_type == "application/octet-stream":
                with open(wav_file, "wb") as f:
                    f.write(response.content)
                return True
            else:
                # Log a small snippet to help diagnose HTML/text responses
                try:
                    if content_type.startswith("text/") or "json" in content_type:
                        snippet = response.text[:200]
                        self.log.debug(f"Lingva /api/tts non-audio response (snippet): {snippet}")
                except Exception:
                    pass
        except requests.exceptions.RequestException as e:
            self.log.debug(f"/api/tts request failed: {e}")

        # Step 2: try /api/v1/audio (JSON with byte array)
        v1_url = f"{self.lingva_instance}/api/v1/audio/{lang_code}/{encoded_sentence}"
        json_headers = {
            "User-Agent": "OVOS-LingvaTTS/1.0 (+https://github.com/aka0kuro/ovos-tts-plugin-lingva)",
            "Accept": "application/json"
        }
        try:
            response = requests.get(v1_url, headers=json_headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            audio_arr = data.get("audio")
            if isinstance(audio_arr, list):
                try:
                    audio_bytes = bytes(audio_arr)
                except Exception as e:
                    self.log.error(f"Could not convert audio JSON to bytes: {e}")
                    return False
                with open(wav_file, "wb") as f:
                    f.write(audio_bytes)
                return True
            else:
                self.log.error("Invalid /api/v1/audio response: missing valid 'audio' field")
        except requests.exceptions.RequestException as e:
            self.log.debug(f"/api/v1/audio request failed: {e}")
        except Exception as e:
            self.log.debug(f"Error processing /api/v1/audio response: {e}")

        return False

    @classproperty
    def available_languages(cls) -> set:
        """Return available languages supported by Lingva"""
        return set(LINGVA_LANG_MAP.keys())

    def get_tts(self, sentence, wav_file, lang=None, voice=None):
        """Fetch tts audio using Lingva.ml API.

        Args:
            sentence (str): Sentence to generate audio for
            wav_file (str): output file path
            lang (str): language of sentence
            voice (str): unsupported by this plugin
        Returns:
            Tuple ((str) written file, None)
        """
        lang = lang or self.lang
        lang = standardize_lang_tag(lang, macro=True)
        
        # Map the OVOS language to the Lingva language code
        lingva_lang = LINGVA_LANG_MAP.get(lang, lang.split("-")[0])
        
        # If the language is not mapped, fall back to the base code
        if lingva_lang not in LINGVA_LANG_MAP.values():
            lingva_lang = lang.split("-")[0]
        
        # First attempt: mapped language
        if self._download_tts_to_file(sentence, lingva_lang, wav_file):
            return (wav_file, None)

        # Second attempt: base language if different
        if lang != lingva_lang:
            fallback_lang = lang.split("-")[0]
            if self._download_tts_to_file(sentence, fallback_lang, wav_file):
                return (wav_file, None)

        # If both attempts fail, raise a clear error
        raise ValueError("Failed to obtain TTS audio from Lingva (both /api/tts and /api/v1/audio failed)")


if __name__ == "__main__":
    e = LingvaTTS()
    ssml = "Hello world"
    e.get_tts(ssml, f"en-US.mp3", lang="en-US")

    ssml = "Hello world"
    e.get_tts(ssml, f"pt-BR.mp3", lang="pt-BR")
 
    ssml = "Hello world"
    e.get_tts(ssml, f"es-ES.mp3", lang="es-ES")
