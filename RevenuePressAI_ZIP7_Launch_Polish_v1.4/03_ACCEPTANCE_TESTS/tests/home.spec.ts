import { test, expect } from '@playwright/test';

test('Homepage loads and shows core value proposition', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('body')).toBeVisible();
  // Look for the 7-second clarity hero keyword
  await expect(page.getByText(/Turn any book into a movement|Transformez votre livre en mouvement/i)).toBeVisible();
  await expect(page.getByRole('button', { name: /Start Free|Démarrer gratuitement|Get Started|Commencer/i })).toBeVisible();
});

