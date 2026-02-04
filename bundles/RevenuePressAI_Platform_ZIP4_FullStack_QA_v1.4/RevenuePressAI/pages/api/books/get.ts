import type { NextApiRequest, NextApiResponse } from 'next';
import { prisma } from '../../../lib/db';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') return res.status(405).json({ ok: false, error: 'GET only' });
  const id = String(req.query.id || '');
  if (!id) return res.status(400).json({ ok: false, error: 'Missing id' });
  const book = await prisma.book.findUnique({
    where: { id },
    include: { author: true, packs: { orderBy: { version: 'desc' }, take: 1 } }
  });
  if (!book) return res.status(404).json({ ok: false, error: 'Not found' });
  const latest = book.packs[0] || null;
  return res.status(200).json({
    ok: true,
    book: {
      id: book.id,
      title: book.title,
      subtitle: book.subtitle,
      language: book.language,
      description: book.description,
      genre: book.genre,
      author: {
        displayName: book.author.displayName,
        website: book.author.website,
        email: book.author.email
      }
    },
    pack: latest ? {
      version: latest.version,
      createdAt: latest.createdAt.toISOString(),
      data: latest.data
    } : null
  });
}
