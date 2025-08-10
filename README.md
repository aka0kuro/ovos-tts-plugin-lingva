## Description
OVOS TTS plugin for [Lingva.ml](https://lingva.ml)

### About Lingva.ml

[Lingva.ml](https://lingva.ml) is a privacy-focused alternative to Google Translate that provides translation and text-to-speech services without tracking or storing user data. This plugin uses the Lingva.ml API to convert text to speech in multiple languages.

This plugin is privacy-friendly and does not require any API keys or authentication.

![](./lingva.png)

## Install

pip install git+https://github.com/aka0kuro/ovos-tts-plugin-lingva.git


## Configuration

```json
  "tts": {
    "module": "ovos-tts-plugin-lingva"
  }
 
```

### Extra options

You can configure the Lingva instance and language settings:

```json
  "tts": {
    "module": "ovos-tts-plugin-lingva",
    "ovos-tts-plugin-lingva": {
      "lingva_instance": "https://lingva.ml",
      "lang": "es"
    }
```

### Supported Languages

The plugin supports a wide range of languages including:

- **English**: en, en-US, en-GB, en-AU, en-CA, en-IN, en-IE, en-ZA, en-NG
- **Spanish**: es, es-ES, es-US, es-MX
- **French**: fr, fr-FR, fr-CA
- **Portuguese**: pt, pt-PT, pt-BR
- **German**: de, de-DE, de-AT, de-CH
- **Italian**: it, it-IT
- **Dutch**: nl, nl-NL, nl-BE
- **Russian**: ru, ru-RU
- **Japanese**: ja, ja-JP
- **Korean**: ko, ko-KR
- **Chinese**: zh, zh-CN, zh-TW
- **Arabic**: ar, ar-SA
- **Hindi**: hi, hi-IN
- **Turkish**: tr, tr-TR
- **Polish**: pl, pl-PL
- **Swedish**: sv, sv-SE
- **Danish**: da, da-DK
- **Norwegian**: no, no-NO
- **Finnish**: fi, fi-FI
- **Czech**: cs, cs-CZ
- **Slovak**: sk, sk-SK
- **Hungarian**: hu, hu-HU
- **Romanian**: ro, ro-RO
- **Bulgarian**: bg, bg-BG
- **Croatian**: hr, hr-HR
- **Serbian**: sr, sr-RS
- **Slovenian**: sl, sl-SI
- **Estonian**: et, et-EE
- **Latvian**: lv, lv-LV
- **Lithuanian**: lt, lt-LT
- **Greek**: el, el-GR
- **Hebrew**: he, he-IL
- **Thai**: th, th-TH
- **Vietnamese**: vi, vi-VN
- **Indonesian**: id, id-ID
- **Malay**: ms, ms-MY
- **Catalan**: ca, ca-ES
- **Basque**: eu, eu-ES
- **Galician**: gl, gl-ES
- **Icelandic**: is, is-IS
- **Macedonian**: mk, mk-MK
- **Albanian**: sq, sq-AL
- **Bosnian**: bs, bs-BA
- **Maltese**: mt, mt-MT
- **Welsh**: cy, cy-GB
- **Irish**: ga, ga-IE
- **Scottish Gaelic**: gd, gd-GB
- **Cornish**: kw, kw-GB
- **Breton**: br, br-FR
- **Occitan**: oc, oc-FR
- **Corsican**: co, co-FR
- **Luxembourgish**: lb, lb-LU
- **Romansh**: rm, rm-CH
- **Friulian**: fur, fur-IT
- **Sardinian**: sc, sc-IT
- **Venetian**: vec, vec-IT
- **Lombard**: lmo, lmo-IT
- **Piedmontese**: pms, pms-IT
- **Ligurian**: lij, lij-IT
- **Neapolitan**: nap, nap-IT
- **Sicilian**: scn, scn-IT
- **Sardinian**: srd, srd-IT

### Privacy Features

- No API keys required
- No user tracking
- No data storage on external servers
- Open source and privacy-focused
- Supports multiple Lingva instances

### Alternative Instances

You can use alternative Lingva instances by changing the `lingva_instance` configuration:

```json
{
  "lingva_instance": "https://lingva.ml"
}
```

Other available instances:
- https://lingva.ml (Official)
- https://lingva.pussthecat.org
- https://translate.argosopentech.com
