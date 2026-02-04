import { test, expect } from '@playwright/test';

test('Author can reach book submission and see required fields', async ({ page }) => {
  await page.goto('/submit');
  await expect(page.locator('text=Submit a Book').or(page.locator('text=Soumettre un livre'))).toBeVisible();
  await expect(page.locator('input[name="title"]')).toBeVisible();
  await expect(page.locator('textarea[name="description"]')).toBeVisible();
  await expect(page.locator('select[name="language"]')).toBeVisible();
});
