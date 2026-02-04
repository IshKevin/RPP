import { test, expect } from '@playwright/test';

test('Hot books and hot authors widgets are reachable', async ({ page }) => {
  await page.goto('/discover');
  await expect(page.locator('text=Hot Books').or(page.locator('text=Livres chauds'))).toBeVisible();
  await expect(page.locator('text=Hot Authors').or(page.locator('text=Auteurs chauds'))).toBeVisible();
});
