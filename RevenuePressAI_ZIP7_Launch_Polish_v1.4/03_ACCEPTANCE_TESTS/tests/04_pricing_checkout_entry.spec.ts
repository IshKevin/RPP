import { test, expect } from '@playwright/test';

test('Pricing page renders plans and payment methods section', async ({ page }) => {
  await page.goto('/pricing');
  await expect(page.locator('text=Plans').or(page.locator('text=Offres'))).toBeVisible();
  await expect(page.locator('text=Payment methods').or(page.locator('text=Moyens de paiement'))).toBeVisible();
});
