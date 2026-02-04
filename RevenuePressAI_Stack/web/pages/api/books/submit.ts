import type { NextApiRequest, NextApiResponse } from 'next';
import { prisma } from '../../../lib/db';
import { generateLaunchPack } from '../../../lib/generator';

function bad(res: NextApiResponse, msg: string, status = 400) {
  return res.status(status).json({ ok: false, error: msg });
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return bad(res, 'POST only', 405);
  const { authorName, authorEmail, bookTitle, bookLanguage, description, genre, amazonLink } = (req.body || {}) as Record<string, string>;
  if (!authorName || !authorEmail || !bookTitle || !description || !genre) {
    return bad(res, 'Missing required fields');
  }

  const author = await prisma.author.upsert({
    where: { email: authorEmail.toLowerCase().trim() },
    update: { displayName: authorName.trim() },
    create: { displayName: authorName.trim(), email: authorEmail.toLowerCase().trim(), languages: bookLanguage === 'fr' ? 'fr' : 'en' }
  });

  const book = await prisma.book.create({
    data: {
      title: bookTitle.trim(),
      language: bookLanguage === 'fr' ? 'fr' : 'en',
      description,
      genre,
      amazonLink: amazonLink || null,
      authorId: author.id
    }
  });

  const pack = generateLaunchPack({ title: book.title, genre: book.genre, description: book.description, lang: book.language as any });

  await prisma.assetPack.create({
    data: {
      bookId: book.id,
      language: book.language,
      payloadJson: JSON.stringify(pack)
    }
  });

  return res.status(200).json({ ok: true, bookId: book.id });
}
