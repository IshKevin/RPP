import { test, expect } from '@playwright/test';

test('Language toggle switches EN/FR (if toggle exists)', async ({ page }) => {
  await page.goto('/');

  const toggle = page.getByRole('button', { name: /EN|FR|English|Français/i }).first();
  if (await toggle.count()) {
    await toggle.click();
    // After toggle click, we expect one of the FR hero lines to appear
    await expect(page.getByText(/Transformez votre livre en mouvement/i)).toBeVisible();
  }
});
