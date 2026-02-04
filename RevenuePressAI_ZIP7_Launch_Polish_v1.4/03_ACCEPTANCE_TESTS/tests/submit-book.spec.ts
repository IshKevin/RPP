import { test, expect } from '@playwright/test';

test('Submit Book entry point exists', async ({ page }) => {
  await page.goto('/');
  const btn = page.getByRole('link', { name: /Submit a Book|Soumettre un livre/i }).first();
  await expect(btn).toBeVisible();
});
