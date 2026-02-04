/*
  Lightweight QA check that does NOT require installing deps.
  It validates that key files exist and JSON is parseable.
*/
import fs from 'fs';
import path from 'path';

const root = process.cwd();

const mustExist = [
  'package.json',
  'next.config.js',
  'prisma/schema.prisma',
  'pages/index.tsx',
  'pages/submit.tsx',
  'pages/dashboard.tsx',
  'pages/api/books/submit.ts',
  'locales/en.json',
  'locales/fr.json',
  '.env.example'
];

const missing = mustExist.filter((p) => !fs.existsSync(path.join(root, p)));
if (missing.length) {
  console.error('Missing required files:');
  missing.forEach((m) => console.error(' - ' + m));
  process.exit(1);
}

for (const l of ['locales/en.json', 'locales/fr.json']) {
  JSON.parse(fs.readFileSync(path.join(root, l), 'utf8'));
}

const pkg = JSON.parse(fs.readFileSync(path.join(root, 'package.json'), 'utf8'));
if (!pkg.scripts || !pkg.scripts.dev || !pkg.scripts.build) {
  console.error('package.json scripts appear incomplete');
  process.exit(1);
}

console.log('OK: smoke checks passed');
