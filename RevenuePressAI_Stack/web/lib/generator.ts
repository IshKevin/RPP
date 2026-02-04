import type { Lang } from './i18n';

export type LaunchPack = {
  targetAudiences: string[];
  bestChannels: { channel: string; why: string; cta: string; message: string }[];
  emotionalReach: string[];
  gifts: string[];
  keywords: string[];
  hashtags: string[];
  adScripts: { angle: string; script: string; footageIdeas: string[] }[];
  visualsBrief: string[];
  pricing: { tier: string; includes: string[]; priceUSD: number }[];
};

function tokensFromTitle(title: string) {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 12);
}

export function generateLaunchPack(input: {
  title: string;
  description: string;
  language: Lang;
  genres: string[];
}): LaunchPack {
  const tt = input.language;
  const tokens = Array.from(new Set([...tokensFromTitle(input.title), ...tokensFromTitle(input.description)]));

  const baseKeywords = tokens.filter((t) => t.length >= 4).slice(0, 18);
  const keywords = [...baseKeywords, ...input.genres].filter(Boolean).slice(0, 25);
  const hashtags = keywords.map((k) => `#${k.replace(/\s+/g, '')}`).slice(0, 25);

  const targetAudiences = tt === 'fr'
    ? [
        'Lecteurs qui veulent une solution claire et pratique',
        'Professionnels qui cherchent à progresser rapidement',
        'Étudiants et jeunes actifs motivés par des résultats',
        'Diaspora et entrepreneurs (si le contexte est africain)',
        'Fans du genre (selon vos catégories)'
      ]
    : [
        'Readers who want a clear, practical solution',
        'Professionals seeking fast progress',
        'Students and young professionals hungry for results',
        'Diaspora & entrepreneurs (if Africa context)',
        'Fans of the genre (based on your categories)'
      ];

  const bestChannels = tt === 'fr'
    ? [
        { channel: 'TikTok', why: 'Découverte rapide via vidéos courtes', cta: 'Télécharger l’extrait', message: '3 idées fortes du livre en 20 secondes.' },
        { channel: 'Instagram Reels', why: 'Audience qualité + partage', cta: 'Précommander', message: 'Une phrase choc + bénéfice concret.' },
        { channel: 'YouTube Shorts', why: 'Longue traîne et crédibilité', cta: 'Voir la vidéo complète', message: 'Mini‑histoire avant/après.' },
        { channel: 'LinkedIn', why: 'Idéal pour non‑fiction & business', cta: 'Demander le plan', message: 'Post structure “problème → solution → preuve”.' },
        { channel: 'WhatsApp', why: 'Conversion forte via groupes', cta: 'Recevoir le lien', message: 'Message court + lien + preuve sociale.' }
      ]
    : [
        { channel: 'TikTok', why: 'Fast discovery via short-form video', cta: 'Download the excerpt', message: '3 powerful ideas from the book in 20 seconds.' },
        { channel: 'Instagram Reels', why: 'High-quality audience + sharing', cta: 'Preorder', message: 'A punchy line + a concrete benefit.' },
        { channel: 'YouTube Shorts', why: 'Evergreen reach + credibility', cta: 'Watch the full video', message: 'Mini before/after story.' },
        { channel: 'LinkedIn', why: 'Best for non-fiction & business', cta: 'Request the plan', message: 'Post: “problem → solution → proof”.' },
        { channel: 'WhatsApp', why: 'High conversion through groups', cta: 'Get the link', message: 'Short message + link + social proof.' }
      ];

  const emotionalReach = tt === 'fr'
    ? ['Espoir', 'Contrôle', 'Fierté', 'Urgence', 'Soulagement']
    : ['Hope', 'Control', 'Pride', 'Urgency', 'Relief'];

  const gifts = tt === 'fr'
    ? ['Checklist PDF (1 page)', 'Template prêt à copier/coller', 'Bonus chapitre audio', 'Accès à un groupe WhatsApp privé', 'Réduction de lancement 48h']
    : ['1-page PDF checklist', 'Copy/paste template', 'Bonus audio chapter', 'Access to private WhatsApp group', '48h launch discount'];

  const visualsBrief = tt === 'fr'
    ? [
        'Visuels minimalistes (fond crème), titres navy, accents bleu électrique.',
        'Avant/Après (problème → résultat) en 2 écrans.',
        'Carrousel 5 slides : douleur, erreur, solution, preuve, CTA.',
        'Badge “Hot Book of the Month” + compteur social.',
        'Mockups 3D de couverture (gratuit: smartmockups/Canva)'
      ]
    : [
        'Minimal visuals (cream background), navy titles, electric-blue accents.',
        'Before/After (problem → result) in 2 frames.',
        '5-slide carousel: pain, mistake, solution, proof, CTA.',
        '“Hot Book of the Month” badge + social counter.',
        '3D cover mockups (free: smartmockups/Canva)'
      ];

  const adScripts = tt === 'fr'
    ? [
        {
          angle: 'Problème → Solution',
          script: 'Si vous luttez avec [problème], ce livre vous donne une méthode simple en 3 étapes. Voici l’étape #1… (CTA: extrait gratuit).',
          footageIdeas: ['Écriture dans un carnet', 'Personne frustrée puis soulagée', 'Plan de travail minimaliste']
        },
        {
          angle: 'Preuve sociale',
          script: '“J’ai appliqué une idée du chapitre 2 et j’ai obtenu [résultat].” Voici exactement ce que j’ai fait… (CTA: lien).',
          footageIdeas: ['Avis/étoiles animées', 'Capture de notes', 'Main sur clavier']
        },
        {
          angle: 'Défi 7 jours',
          script: 'Défi: appliquez une idée par jour pendant 7 jours. Jour 1: … (CTA: rejoins le groupe).',
          footageIdeas: ['Calendrier', 'To-do list', 'Compteur 7 jours']
        },
        {
          angle: 'Mythe à casser',
          script: 'Tout le monde croit que [mythe]. Faux. Dans ce livre, je montre pourquoi… (CTA: précommande).',
          footageIdeas: ['Texte “MYTHE” barré', 'Système/graphique simple', 'Personne qui explique face caméra (stock)']
        },
        {
          angle: 'Moment émotion',
          script: 'J’ai écrit ce livre après [histoire courte]. Si vous vous reconnaissez, ce livre est pour vous. (CTA: extrait).',
          footageIdeas: ['Ville nuit', 'Lecture silencieuse', 'Plan serré sur livre']
        }
      ]
    : [
        {
          angle: 'Problem → Solution',
          script: 'If you’re struggling with [problem], this book gives a simple 3-step method. Here’s step #1… (CTA: free excerpt).',
          footageIdeas: ['Writing in a notebook', 'Frustrated → relieved person', 'Minimal desk setup']
        },
        {
          angle: 'Social proof',
          script: '“I used one idea from chapter 2 and got [result].” Here’s exactly what I did… (CTA: link).',
          footageIdeas: ['Animated reviews/stars', 'Notes screenshot', 'Hands typing']
        },
        {
          angle: '7-day challenge',
          script: 'Challenge: apply one idea per day for 7 days. Day 1: … (CTA: join the group).',
          footageIdeas: ['Calendar', 'To-do list', '7-day counter']
        },
        {
          angle: 'Myth-busting',
          script: 'Everyone thinks [myth]. Wrong. In this book, I show why… (CTA: preorder).',
          footageIdeas: ['MYTH text crossed out', 'Simple chart', 'Explainer stock clip']
        },
        {
          angle: 'Emotional origin',
          script: 'I wrote this book after [short story]. If you relate, this is for you. (CTA: excerpt).',
          footageIdeas: ['City at night', 'Quiet reading', 'Close-up on a book']
        }
      ];

  const pricing = tt === 'fr'
    ? [
        { tier: 'Gratuit', priceUSD: 0, includes: ['Profil auteur', '1 pack keywords/hashtags', '1 script pub'] },
        { tier: 'Premium', priceUSD: 49, includes: ['Pack complet', '5 scripts pub', 'Plan 30 jours', 'Widgets viraux'] },
        { tier: 'Done-for-you', priceUSD: 299, includes: ['Montage vidéo (stock)', 'Publication multi-canal', 'Optimisation 14 jours'] }
      ]
    : [
        { tier: 'Free', priceUSD: 0, includes: ['Author profile', '1 keywords/hashtags pack', '1 ad script'] },
        { tier: 'Premium', priceUSD: 49, includes: ['Full launch pack', '5 ad scripts', '30-day plan', 'Viral widgets'] },
        { tier: 'Done-for-you', priceUSD: 299, includes: ['Stock-footage edit', 'Multi-channel posting', '14-day optimisation'] }
      ];

  return {
    targetAudiences,
    bestChannels,
    emotionalReach,
    gifts,
    keywords,
    hashtags,
    adScripts,
    visualsBrief,
    pricing
  };
}
