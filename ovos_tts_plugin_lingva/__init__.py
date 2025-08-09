import requests
import json
from urllib.parse import quote
from ovos_plugin_manager.templates.tts import TTS
from ovos_utils import classproperty
from ovos_utils.lang import standardize_lang_tag

# Mapeo de idiomas de OVOS a códigos de idioma de Lingva
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
        
        # Mapear el idioma de OVOS al código de idioma de Lingva
        lingva_lang = LINGVA_LANG_MAP.get(lang, lang.split("-")[0])
        
        # Si el idioma no está en el mapeo, usar el código base
        if lingva_lang not in LINGVA_LANG_MAP.values():
            lingva_lang = lang.split("-")[0]
        
        try:
            # Construir la URL de la API de Lingva para TTS
            encoded_sentence = quote(sentence, safe="")
            tts_url = f"{self.lingva_instance}/api/tts/{lingva_lang}/{encoded_sentence}"

            # Realizar la petición a la API de Lingva
            headers = {
                "User-Agent": "OVOS-LingvaTTS/1.0 (+https://github.com/OpenVoiceOS/ovos-tts-plugin-lingva)",
                "Accept": "audio/*,application/octet-stream;q=0.9,*/*;q=0.8"
            }
            response = requests.get(tts_url, headers=headers, timeout=30)
            response.raise_for_status()

            # Validar tipo de contenido devuelto
            content_type = response.headers.get("Content-Type", "")
            if not (content_type.startswith("audio/") or content_type == "application/octet-stream"):
                # Registrar un fragmento de respuesta si es texto para facilitar diagnóstico
                try:
                    if content_type.startswith("text/") or "json" in content_type:
                        snippet = response.text[:200]
                        self.log.debug(f"Respuesta Lingva (fragmento): {snippet}")
                except Exception:
                    pass
                self.log.error(f"Contenido inesperado de Lingva: {content_type} - URL: {tts_url}")
                raise ValueError(f"Lingva devolvió contenido no-audio: {content_type}")

            # Guardar el audio recibido
            with open(wav_file, 'wb') as f:
                f.write(response.content)

            return (wav_file, None)  # No phonemes

        except requests.exceptions.RequestException as e:
            self.log.error(f"Error fetching TTS from Lingva: {e}")
            # Fallback: intentar con el idioma base si falla
            if lang != lingva_lang:
                try:
                    encoded_sentence = quote(sentence, safe="")
                    fallback_lang = lang.split("-")[0]
                    fallback_url = f"{self.lingva_instance}/api/tts/{fallback_lang}/{encoded_sentence}"
                    headers = {
                        "User-Agent": "OVOS-LingvaTTS/1.0 (+https://github.com/OpenVoiceOS/ovos-tts-plugin-lingva)",
                        "Accept": "audio/*,application/octet-stream;q=0.9,*/*;q=0.8"
                    }
                    response = requests.get(fallback_url, headers=headers, timeout=30)
                    response.raise_for_status()

                    content_type = response.headers.get("Content-Type", "")
                    if not (content_type.startswith("audio/") or content_type == "application/octet-stream"):
                        try:
                            if content_type.startswith("text/") or "json" in content_type:
                                snippet = response.text[:200]
                                self.log.debug(f"Respuesta Lingva fallback (fragmento): {snippet}")
                        except Exception:
                            pass
                        self.log.error(f"Contenido inesperado de Lingva (fallback): {content_type} - URL: {fallback_url}")
                        raise ValueError(f"Lingva devolvió contenido no-audio (fallback): {content_type}")

                    with open(wav_file, 'wb') as f:
                        f.write(response.content)

                    return (wav_file, None)
                except requests.exceptions.RequestException as fallback_e:
                    self.log.error(f"Fallback TTS also failed: {fallback_e}")
                    raise e
            else:
                raise e


if __name__ == "__main__":
    e = LingvaTTS()
    ssml = "Hello world"
    e.get_tts(ssml, f"en-US.mp3", lang="en-US")

    ssml = "Olá Mundo! Bom dia alegria"
    e.get_tts(ssml, f"pt-BR.mp3", lang="pt-BR")

    ssml = "Hola mundo"
    e.get_tts(ssml, f"es-ES.mp3", lang="es-ES")
