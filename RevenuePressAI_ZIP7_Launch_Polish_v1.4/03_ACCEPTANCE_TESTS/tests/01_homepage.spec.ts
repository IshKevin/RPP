import { test, expect } from '@playwright/test';

test('Homepage loads and shows 7-second clarity hero', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading')).toBeVisible();
  // Accept either EN or FR hero depending on language detection
  await expect(
    page.locator('text=Turn any book into a movement').or(page.locator('text=Transformez votre livre en mouvement'))
  ).toBeVisible();
});
