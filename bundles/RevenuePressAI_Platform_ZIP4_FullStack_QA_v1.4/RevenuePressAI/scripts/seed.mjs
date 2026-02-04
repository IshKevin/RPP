import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  const demoAuthor = await prisma.author.upsert({
    where: { email: 'demo@author.com' },
    update: {},
    create: {
      displayName: 'Demo Author',
      email: 'demo@author.com',
      bio: 'Sample author used for demo data.',
      website: 'https://revenuepressai.com',
      languages: 'en,fr'
    }
  });

  const book = await prisma.book.create({
    data: {
      authorId: demoAuthor.id,
      title: 'Ship ChatGPT Apps',
      subtitle: 'From idea to launch assets',
      language: 'en',
      description: 'A demo book to showcase RevenuePress AI workflows.',
      genre: 'Business/Tech',
      coverUrl: '',
      status: 'ACTIVE'
    }
  });

  await prisma.assetPack.create({
    data: {
      bookId: book.id,
      language: 'en',
      packJson: JSON.stringify({
        targetAudiences: ['Indie founders', 'Creators & coaches', 'Aspiring app builders'],
        bestChannels: [
          { channel: 'TikTok', why: 'Fast reach & discovery', message: 'Build and ship faster with AI — start today.', cta: 'Download the book' },
          { channel: 'LinkedIn', why: 'High-intent professionals', message: 'A practical playbook to launch with AI.', cta: 'Get the launch pack' }
        ],
        keywords: ['ChatGPT apps', 'AI business', 'prompting', 'launch plan'],
        hashtags: ['#AI', '#ChatGPT', '#BookTok', '#IndieHackers'],
        adScripts: [
          { angle: 'Pain → solution', script: 'Still stuck on page 1? This book gives you a complete AI launch kit.', footageIdeas: ['Typing on laptop', 'Busy creator workspace', 'Simple motion graphics'] }
        ],
        visualsBrief: ['Clean hero banner', '3 benefit cards', 'Book mockup + CTA button'],
        gifts: ['Free checklist PDF', 'Launch calendar template'],
        emotionalReach: ['Confidence', 'Momentum', 'Belonging']
      })
    }
  });

  console.log('Seeded demo author + book');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
