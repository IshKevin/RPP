import re
import math
from collections import Counter, defaultdict

STOP_EN = set("""a an the and or but if then else for to of in on at by with from into over under is are was were be been being this that these those it its as not can will would should could you your we our they their i me my""".split())
STOP_FR = set("""un une le la les des du de d' et ou mais si alors sinon pour à au aux en sur chez par avec depuis dans vers est sont était étaient être été étant ce cette ces ceux cela il elle ils elles je tu vous nous votre vos notre nos leur leurs mon ma mes""".replace("d'", "d").split())

EMOTIONS = {
  "curiosity": ["secret","mystery","hidden","unknown","why","how","reveal","unlock","discover","curieux","mystère","secret","révèle","découvre"],
  "hope": ["hope","transform","change","breakthrough","new","future","reborn","espoir","changer","nouveau","avenir","renaître"],
  "fear": ["danger","risk","warning","dark","lose","threat","peur","danger","risque","alerte","sombre","perdre","menace"],
  "trust": ["proven","tested","evidence","guide","steps","method","fiable","prouvé","testé","preuve","guide","étapes","méthode"],
  "belonging": ["community","together","tribe","join","we","famille","communauté","ensemble","tribu","rejoindre","nous"]
}

CHANNELS = [
  ("tiktok", ["short hook","visual proof","fast CTA"]),
  ("instagram", ["carousel","reel","story CTA"]),
  ("youtube", ["long-form","tutorial","review"]),
  ("facebook", ["groups","community","events"]),
  ("linkedin", ["authority","case study","B2B"]),
  ("email", ["nurture","launch sequence","offers"]),
  ("whatsapp", ["direct","group pitch","fast conversion"]),
  ("amazon", ["keywords","blurb","A+ content"])
]

CTA_TEMPLATES = {
  "en": {
    "tiktok": "Comment 'BOOK' and I’ll send you the launch pack.",
    "instagram": "DM me 'LAUNCH' for the free checklist.",
    "youtube": "Grab the full launch pack via the link below.",
    "facebook": "Join the reader group and get the bonus gift.",
    "linkedin": "Message me for the executive summary + campaign kit.",
    "email": "Reply 'YES' and I’ll send the next step.",
    "whatsapp": "Tap to join our WhatsApp pitch group and get your bonus.",
    "amazon": "Download the sample and read Chapter 1 today."
  },
  "fr": {
    "tiktok": "Commente 'LIVRE' et je t’envoie le pack de lancement.",
    "instagram": "DM 'LANCEMENT' pour recevoir la checklist gratuite.",
    "youtube": "Télécharge le pack complet via le lien en description.",
    "facebook": "Rejoins le groupe lecteurs et reçois le bonus.",
    "linkedin": "Écris-moi pour le résumé exécutif + kit campagne.",
    "email": "Réponds 'OUI' et je t’envoie l’étape suivante.",
    "whatsapp": "Clique pour rejoindre le groupe WhatsApp et recevoir ton bonus.",
    "amazon": "Télécharge l’extrait et lis le Chapitre 1 aujourd’hui."
  }
}

def _normalize(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9àâçéèêëîïôûùüÿñæœ\s-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_keywords(text: str, lang: str, top_k: int = 15):
    text = _normalize(text)
    tokens = text.split()
    stop = STOP_FR if lang == "fr" else STOP_EN
    tokens = [t for t in tokens if len(t) > 2 and t not in stop]
    if not tokens:
        return []
    # bigrams + unigrams
    unig = Counter(tokens)
    big = Counter([f"{tokens[i]} {tokens[i+1]}" for i in range(len(tokens)-1)])
    scored = Counter()
    for w,c in unig.items():
        scored[w] += c
    for b,c in big.items():
        scored[b] += c * 1.6
    # normalize by log length to avoid long manuscripts dominating
    norm = math.log(1+len(tokens))
    items = [(k, v/norm) for k,v in scored.items()]
    items.sort(key=lambda x: x[1], reverse=True)
    return [k for k,_ in items[:top_k]]

def make_hashtags(keywords, lang: str, top_k: int = 20):
    tags = []
    for k in keywords:
        h = re.sub(r"\s+", "", k.title())
        h = re.sub(r"[^A-Za-z0-9À-ÿ]", "", h)
        if len(h) >= 3:
            tags.append("#" + h)
    # add a few platform tags
    base = ["#BookTok","#Bookstagram","#Kindle","#AmazonBooks","#AuthorLife"] if lang=="en" else ["#Livre","#Auteur","#AmazonKDP","#Lecture","#BookTokFR"]
    for b in base:
        if b not in tags:
            tags.append(b)
    return tags[:top_k]

def infer_audiences(title, category, description, lang):
    text = _normalize(" ".join([title or "", category or "", description or ""]))
    audiences = []
    if any(k in text for k in ["business","money","finance","startup","entrepreneur","marketing","ai","tech","entreprise","argent","finance","startup","entrepreneur","ia"]):
        audiences.append({"persona":"Ambitious builders","need":"clear steps + proof","objection":"skeptical of hype","hook":"Stop guessing. Follow a proven playbook."})
    if any(k in text for k in ["health","diet","diabetes","weight","fitness","santé","diabète","poids","fitness"]):
        audiences.append({"persona":"Health improvers","need":"simple daily actions","objection":"overwhelmed","hook":"Small daily steps that compound."})
    if any(k in text for k in ["love","relationship","romance","couple","amour","relation","romance"]):
        audiences.append({"persona":"Relationship seekers","need":"emotion + identification","objection":"fear of vulnerability","hook":"You’re not alone—this story mirrors you."})
    if any(k in text for k in ["thriller","mystery","secret","crime","enquête","mystère","secret","police"]):
        audiences.append({"persona":"Thrill & mystery fans","need":"hooks + suspense","objection":"predictable plots","hook":"One secret changes everything."})
    if not audiences:
        audiences.append({"persona":"Curious readers","need":"a strong reason to care","objection":"too many choices","hook":"Give me 60 seconds—this will surprise you."})
    return audiences[:4]

def recommend_channels(audiences, lang):
    # Simple heuristic: map personas to channels
    out = []
    for a in audiences:
        p = a["persona"].lower()
        if "thrill" in p or "curious" in p:
            out += ["tiktok","instagram","youtube","amazon"]
        elif "builders" in p:
            out += ["linkedin","youtube","email","whatsapp","amazon"]
        elif "health" in p:
            out += ["youtube","instagram","facebook","email","amazon"]
        else:
            out += ["tiktok","facebook","email","amazon"]
    # de-dupe keeping order
    seen = set()
    final = []
    for c in out:
        if c not in seen:
            final.append(c); seen.add(c)
    # ensure whatsapp exists
    if "whatsapp" not in final:
        final.append("whatsapp")
    return final[:7]

def generate_messages(title, subtitle, description, keywords, channels, lang):
    t = title or ""
    sub = subtitle or ""
    desc = description or ""
    lines = []
    if lang == "fr":
        hook = f"3 mots et tout bascule : {t}. {sub}".strip()
        proof = f"Ce livre vous donne : {', '.join(keywords[:5])}." if keywords else "Ce livre vous donne une méthode claire."
    else:
        hook = f"Three words changed everything: {t}. {sub}".strip()
        proof = f"This book gives you: {', '.join(keywords[:5])}." if keywords else "This book gives you a clear method."

    for ch in channels:
        cta = CTA_TEMPLATES[lang].get(ch, CTA_TEMPLATES[lang]["email"])
        if ch in ("tiktok","instagram"):
            msg = f"{hook}\n{proof}\n{cta}"
        elif ch == "linkedin":
            msg = (f"{t}: a practical, no-fluff breakdown.\n"
                   f"Key themes: {', '.join(keywords[:7])}.\n{cta}") if lang=="en" else (
                   f"{t} : une analyse concrète, sans blabla.\n"
                   f"Thèmes clés : {', '.join(keywords[:7])}.\n{cta}")
        elif ch == "email":
            msg = (f"Subject: {t} — your next 7-day plan\n\nHi,\n\n{desc[:220]}...\n\n{cta}") if lang=="en" else (
                   f"Objet : {t} — votre plan sur 7 jours\n\nBonjour,\n\n{desc[:220]}...\n\n{cta}")
        else:
            msg = f"{t}\n{desc[:200]}...\n{cta}"
        lines.append({"channel": ch, "message": msg})
    return lines

def emotion_map(text, lang):
    t = _normalize(text)
    scores = {}
    for emo, kws in EMOTIONS.items():
        scores[emo] = sum(1 for k in kws if k in t)
    # keep top 3
    items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top = [ {"emotion": k, "score": v} for k,v in items[:3] ]
    return top

def suggest_gift(category, keywords, lang):
    # Gifts (lead magnets) tuned to conversion
    if lang=="fr":
        options = [
          "Un extrait PDF + Chapitre 1",
          "Une checklist 1 page 'Lancement en 7 jours'",
          "Un modèle de message (WhatsApp/Email)",
          "Une mini-vidéo 'Pourquoi ce livre va changer votre trajectoire'",
        ]
    else:
        options = [
          "PDF sample + Chapter 1",
          "1-page '7-day launch checklist'",
          "Message templates (WhatsApp/Email)",
          "Mini video: 'Why this book changes your trajectory'",
        ]
    # add keyword themed gift
    if keywords:
        kw = keywords[0]
        options.insert(0, (f"A printable cheat-sheet: {kw}" if lang=="en" else f"Une fiche imprimable : {kw}"))
    return options[:5]

def build_intelligence(book: dict):
    lang = book.get("language","en")
    text = " ".join([book.get("title",""), book.get("subtitle",""), book.get("category",""), book.get("description",""), (book.get("manuscript_text") or "")[:5000]])
    keywords = extract_keywords(text, lang)
    hashtags = make_hashtags(keywords, lang)
    audiences = infer_audiences(book.get("title"), book.get("category"), book.get("description"), lang)
    channels = recommend_channels(audiences, lang)
    messages = generate_messages(book.get("title"), book.get("subtitle"), book.get("description"), keywords, channels, lang)
    emotional = emotion_map(text, lang)
    gift = suggest_gift(book.get("category"), keywords, lang)
    return {
      "keywords": keywords,
      "hashtags": hashtags,
      "audiences": audiences,
      "channels": channels,
      "messages": messages,
      "emotional": emotional,
      "gift": gift
    }
