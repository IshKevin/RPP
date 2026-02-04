import type { NextApiRequest, NextApiResponse } from 'next';
import { prisma } from '../../../lib/db';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') return res.status(405).json({ ok: false, error: 'GET only' });
  const books = await prisma.book.findMany({
    orderBy: { createdAt: 'desc' },
    include: { author: true },
    take: 50
  });
  return res.status(200).json({ ok: true, books: books.map(b => ({
    id: b.id,
    title: b.title,
    language: b.language,
    createdAt: b.createdAt.toISOString(),
    authorName: b.author.displayName
  })) });
}
