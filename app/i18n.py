from flask import request, g, session
import re

SUPPORTED = ("en", "fr")

def detect_lang():
    # priority: explicit ?lang= , session, then Accept-Language
    q = request.args.get("lang", "").lower().strip()
    if q in SUPPORTED:
        return q
    s = session.get("lang")
    if s in SUPPORTED:
        return s
    header = request.headers.get("Accept-Language", "")
    m = re.match(r"\s*([a-zA-Z-]+)", header)
    if m:
        code = m.group(1).split("-")[0].lower()
        if code in SUPPORTED:
            return code
    return "en"

def set_locale_before_request(app):
    def _hook():
        lang = detect_lang()
        g.lang = lang
        session["lang"] = lang
        # make translator available
        g.t = lambda key: TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
        g.lang_label = "English" if lang == "en" else "Français"
        g.other_lang = "fr" if lang == "en" else "en"
        g.other_lang_label = "Français" if lang == "en" else "English"
        g.brand = {
            "primary": app.config.get("BRAND_PRIMARY", "#001E3C"),
            "accent": app.config.get("BRAND_ACCENT", "#1991DF"),
        }
    return _hook

TRANSLATIONS = {
  "en": {
    "nav_home": "Home",
    "nav_features": "Features",
    "nav_pricing": "Pricing",
    "nav_login": "Login",
    "nav_register": "Register",
    "nav_dashboard": "Dashboard",
    "nav_admin": "Admin",
    "hero_title": "You wrote the book. We ignite the movement.",
    "hero_sub": "In 7 seconds: Upload your book → Get audience + channels + messages + hashtags → Launch campaigns that sell.",
    "cta_start": "Get Started",
    "cta_demo": "Request a Demo",
    "value_1": "Book Intelligence",
    "value_2": "Campaign Assets",
    "value_3": "Hot Lists + Viral Widgets",
    "footer_privacy": "Privacy Policy",
    "footer_conf": "Confidentiality",
  },
  "fr": {
    "nav_home": "Accueil",
    "nav_features": "Fonctionnalités",
    "nav_pricing": "Tarifs",
    "nav_login": "Connexion",
    "nav_register": "Inscription",
    "nav_dashboard": "Tableau de bord",
    "nav_admin": "Admin",
    "hero_title": "Vous avez écrit le livre. Nous déclenchons le mouvement.",
    "hero_sub": "En 7 secondes : Soumettez votre livre → Audience + canaux + messages + hashtags → Campagnes qui vendent.",
    "cta_start": "Commencer",
    "cta_demo": "Demander une démo",
    "value_1": "Intelligence Livre",
    "value_2": "Assets de Campagne",
    "value_3": "Tendances + Widgets Viraux",
    "footer_privacy": "Politique de confidentialité",
    "footer_conf": "Confidentialité",
  }
}
