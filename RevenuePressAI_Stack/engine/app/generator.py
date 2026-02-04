from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Tuple

from langdetect import detect
from rapidfuzz import process, fuzz

from .models import BookInput, LaunchPack, Persona, ChannelMessage, VideoAd, Language

STOPWORDS_EN = {
    "the","a","an","and","or","but","to","of","in","on","for","with","from","by","at","as",
    "is","are","was","were","be","been","being","this","that","these","those","it","its","your","you",
}
STOPWORDS_FR = {
    "le","la","les","un","une","des","et","ou","mais","à","de","du","en","sur","pour","avec","par","au","aux",
    "est","sont","été","être","ce","cet","cette","ces","il","elle","vous","votre","vos","leurs","leur",
}

CHANNELS_BASE = [
    "Amazon","Audible","TikTok","YouTube","Instagram","Facebook","LinkedIn","X","Email","WhatsApp","Website"
]

@dataclass
class LangCfg:
    lang: Language
    stopwords: set
    hashtag_prefix: str


def _safe_detect(text: str) -> Language:
    try:
        code = detect(text)
        if code.startswith("fr"):
            return "fr"
        return "en"
    except Exception:
        return "en"


def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9àâäçéèêëîïôöùûüÿñæœ\s-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _extract_terms(text: str, stopwords: set, max_terms: int = 25) -> List[str]:
    text = _normalize(text)
    tokens = [t for t in re.split(r"[\s-]+", text) if len(t) >= 3]
    tokens = [t for t in tokens if t not in stopwords]

    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1

    terms = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
    return [t for t, _ in terms[:max_terms]]


def _dedupe_ranked(items: List[str], limit: int) -> List[str]:
    # fuzzy de-dupe while preserving order
    out: List[str] = []
    for it in items:
        if not out:
            out.append(it)
            continue
        match = process.extractOne(it, out, scorer=fuzz.token_sort_ratio)
        if match and match[1] >= 90:
            continue
        out.append(it)
        if len(out) >= limit:
            break
    return out


def generate_keywords_and_hashtags(book: BookInput, lang: Language) -> Tuple[List[str], List[str]]:
    cfg = LangCfg(lang=lang, stopwords=STOPWORDS_FR if lang == "fr" else STOPWORDS_EN, hashtag_prefix="#")

    base_text = " ".join([book.title, book.subtitle or "", book.description])
    terms = _extract_terms(base_text, cfg.stopwords, max_terms=40)

    # enrich with common intent terms
    if lang == "fr":
        boosters = ["livre", "auteur", "lecture", "roman", "ebook", "audible", "kindle"]
    else:
        boosters = ["book", "author", "reading", "novel", "ebook", "audible", "kindle"]

    keywords = _dedupe_ranked(terms + boosters, limit=30)

    # hashtags: camel-ish for readability
    def tagify(w: str) -> str:
        w = re.sub(r"[^a-z0-9àâäçéèêëîïôöùûüÿñæœ]", "", w.lower())
        if not w:
            return ""
        return cfg.hashtag_prefix + w

    hashtags = [tagify(k) for k in keywords]
    hashtags = [h for h in hashtags if h]

    # add platform tags
    platform_tags = ["#amazon", "#kindle", "#audible", "#booktok", "#bookstagram"]
    hashtags = _dedupe_ranked(hashtags + platform_tags, limit=35)
    return keywords, hashtags


def generate_personas(book: BookInput, lang: Language) -> List[Persona]:
    title = book.title.strip()
    if lang == "fr":
        return [
            Persona(
                name="Lecteur curieux (découverte)",
                pains=["ne sait pas quoi lire", "a peur d’être déçu"],
                desires=["une histoire forte", "une idée utile immédiatement"],
                triggers=[f"Recommandations autour de: {title}", "avis courts et sincères"],
            ),
            Persona(
                name="Acheteur de cadeaux",
                pains=["cadeau de dernière minute", "pas sûr des goûts"],
                desires=["offrir un cadeau intelligent", "faire plaisir"],
                triggers=["listes cadeaux", "promotions limitées"],
            ),
            Persona(
                name="Auditeur (audio)",
                pains=["manque de temps", "fatigue visuelle"],
                desires=["apprendre en déplacement", "s’inspirer"],
                triggers=["extraits audio", "voix captivante"],
            ),
        ]

    return [
        Persona(
            name="Curious reader (discovery)",
            pains=["doesn’t know what to read next", "fear of wasting time"],
            desires=["a gripping story", "immediate takeaways"],
            triggers=[f"Recommendations around: {title}", "short, honest reviews"],
        ),
        Persona(
            name="Gift buyer",
            pains=["last-minute gift", "unsure about taste"],
            desires=["a smart gift", "to impress"],
            triggers=["gift lists", "limited-time offers"],
        ),
        Persona(
            name="Audio listener",
            pains=["no time", "screen fatigue"],
            desires=["learn while commuting", "feel inspired"],
            triggers=["audio snippets", "a compelling voice"],
        ),
    ]


def generate_channel_messages(book: BookInput, lang: Language) -> List[ChannelMessage]:
    t = book.title.strip()
    a = book.author_name.strip()
    if lang == "fr":
        return [
            ChannelMessage(channel="Amazon", hook=f"{t} — à lire ce week-end.", body=f"Une promesse simple: {book.description[:160].strip()}…", cta="Voir sur Amazon"),
            ChannelMessage(channel="Audible", hook=f"Écoutez {t} en audio.", body="Extrait 60s + voix immersive. Parfait pour trajets et sport.", cta="Écouter l’extrait"),
            ChannelMessage(channel="TikTok", hook="Tu lis ou tu scrolles?", body=f"POV: tu découvres {t} et tu changes d’avis en 10 secondes.", cta="Commente ‘CHAPITRE’ pour l’extrait"),
            ChannelMessage(channel="Instagram", hook=f"{t} en 3 émotions.", body="Carrousel: Problème → Déclic → Transformation.", cta="Sauvegarde & partage"),
            ChannelMessage(channel="WhatsApp", hook="Message à transférer", body=f"Je te recommande {t} de {a}. Si tu veux, je t’envoie le lien.", cta="Réponds ‘OUI’"),
        ]

    return [
        ChannelMessage(channel="Amazon", hook=f"{t} — your next read.", body=f"A simple promise: {book.description[:160].strip()}…", cta="View on Amazon"),
        ChannelMessage(channel="Audible", hook=f"Listen to {t}.", body="60s sample + immersive voice. Perfect for commuting and workouts.", cta="Play the sample"),
        ChannelMessage(channel="TikTok", hook="Read or keep scrolling?", body=f"POV: you discover {t} and your brain goes ‘wait…’", cta="Comment ‘CHAPTER’ for an excerpt"),
        ChannelMessage(channel="Instagram", hook=f"{t} in 3 emotions.", body="Carousel: Pain → Turning point → Transformation.", cta="Save & share"),
        ChannelMessage(channel="WhatsApp", hook="Forwardable text", body=f"Quick rec: {t} by {a}. Want the link?", cta="Reply ‘YES’"),
    ]


def generate_video_ads(book: BookInput, lang: Language) -> List[VideoAd]:
    t = book.title.strip()
    if lang == "fr":
        return [
            VideoAd(
                angle="Problème → Déclic",
                script=f"[0-3s] Question choc: ‘Et si tout ce que tu crois savoir était faux?’\n[3-12s] 2 phrases du livre (sans spoiler)\n[12-20s] ‘{t}’ — lien en bio.",
                overlay_text=["Et si tout était faux?", t, "Lien en bio"],
                footage_keywords=["close-up reading", "city night", "slow walking"],
                music_keywords=["cinematic", "tension", "minimal"],
            ),
            VideoAd(
                angle="Avant/Après",
                script=f"[0-5s] ‘Avant ce livre, je…’\n[5-15s] 3 bullets de transformation\n[15-25s] ‘{t}’ disponible maintenant.",
                overlay_text=["Avant / Après", "3 déclics", "Disponible"],
                footage_keywords=["sunrise", "writing notes", "smiling"],
                music_keywords=["uplifting", "inspiring"],
            ),
        ]

    return [
        VideoAd(
            angle="Problem → breakthrough",
            script=f"[0-3s] Hook: ‘What if everything you were told was wrong?’\n[3-12s] Two punchy lines (no spoiler)\n[12-20s] ‘{t}’ — link in bio.",
            overlay_text=["What if you were wrong?", t, "Link in bio"],
            footage_keywords=["close-up reading", "city night", "slow walk"],
            music_keywords=["cinematic", "tension", "minimal"],
        ),
        VideoAd(
            angle="Before/after",
            script=f"[0-5s] ‘Before this book, I…’\n[5-15s] 3 transformation bullets\n[15-25s] ‘{t}’ available now.",
            overlay_text=["Before / After", "3 breakthroughs", "Available now"],
            footage_keywords=["sunrise", "taking notes", "smiling"],
            music_keywords=["uplifting", "inspiring"],
        ),
    ]


def generate_emotional_angles(lang: Language) -> List[str]:
    if lang == "fr":
        return ["curiosité", "espoir", "révolte", "statut", "soulagement", "identité"]
    return ["curiosity", "hope", "anger", "status", "relief", "identity"]


def generate_gift_ideas(lang: Language) -> List[str]:
    if lang == "fr":
        return [
            "Chapitre bonus PDF (exclusif)",
            "Checklist ‘à appliquer en 7 jours’",
            "Audiogram 60s pour WhatsApp",
            "Pack 10 citations visuelles",
            "Accès à un groupe WhatsApp privé (30 jours)",
        ]
    return [
        "Bonus PDF chapter (exclusive)",
        "7-day action checklist",
        "60s audiogram for WhatsApp",
        "10 quote-image pack",
        "Private WhatsApp group access (30 days)",
    ]


def build_launch_pack(book: BookInput) -> LaunchPack:
    lang: Language = book.language or _safe_detect((book.title or "") + " " + (book.description or ""))

    personas = generate_personas(book, lang)
    keywords, hashtags = generate_keywords_and_hashtags(book, lang)
    channel_messages = generate_channel_messages(book, lang)
    emotional_angles = generate_emotional_angles(lang)
    gift_ideas = generate_gift_ideas(lang)
    video_ads = generate_video_ads(book, lang)

    return LaunchPack(
        language=lang,
        personas=personas,
        channel_messages=channel_messages,
        emotional_angles=emotional_angles,
        gift_ideas=gift_ideas,
        keywords=keywords,
        hashtags=hashtags,
        video_ads=video_ads,
    )
