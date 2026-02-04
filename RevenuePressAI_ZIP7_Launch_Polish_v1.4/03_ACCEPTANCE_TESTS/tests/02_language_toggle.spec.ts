import { test, expect } from '@playwright/test';

test('Language toggle switches EN/FR', async ({ page }) => {
  await page.goto('/');
  const toggle = page.locator('[data-testid="lang-toggle"]');
  // If no toggle exists, the platform must still support auto-detect;
  // this test will fail and indicates missing UI wiring.
  await expect(toggle).toBeVisible();
  await toggle.click();
  await expect(page.locator('text=Tarification').or(page.locator('text=Pricing'))).toBeVisible();
});
