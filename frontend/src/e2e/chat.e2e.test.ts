// frontend/src/e2e/chat.e2e.test.ts
import { test, expect } from '@playwright/test';

test.describe('Customer Support Chat E2E', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('should display chat interface', async ({ page }) => {
    // Check if chat window is displayed
    await expect(page.locator('.chatWindow')).toBeVisible();
    await expect(page.locator('h2')).toContainText('Customer Support');
  });

  test('should create new session on load', async ({ page }) => {
    // Wait for session to be created
    await page.waitForTimeout(1000);
    
    // Check if session is created by sending a message
    await page.fill('textarea[placeholder="Type your message..."]', 'Hello');
    await page.click('button:has-text("Send")');
    
    // Wait for response
    await page.waitForSelector('.message.assistant');
    await expect(page.locator('.message.assistant')).toBeVisible();
  });

  test('should send and receive messages', async ({ page }) => {
    // Send a message
    await page.fill('textarea[placeholder="Type your message..."]', 'I need help with my order');
    await page.click('button:has-text("Send")');
    
    // Check if user message is displayed
    await expect(page.locator('.message.user')).toContainText('I need help with my order');
    
    // Wait for and check assistant response
    await page.waitForSelector('.message.assistant');
    await expect(page.locator('.message.assistant')).toBeVisible();
  });

  test('should handle file attachments', async ({ page }) => {
    // Send a message with attachment
    await page.fill('textarea[placeholder="Type your message..."]', 'Here is my invoice');
    
    // Upload a file
    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles('test-files/sample.pdf');
    
    // Check if attachment is displayed
    await expect(page.locator('.attachmentPreview')).toBeVisible();
    await expect(page.locator('.fileName')).toContainText('sample.pdf');
    
    // Send message
    await page.click('button:has-text("Send")');
    
    // Check if message is sent
    await expect(page.locator('.message.user')).toBeVisible();
  });

  test('should display typing indicator', async ({ page }) => {
    // Send a message
    await page.fill('textarea[placeholder="Type your message..."]', 'Test typing indicator');
    await page.click('button:has-text("Send")');
    
    // Check if typing indicator appears
    await expect(page.locator('.typingIndicator')).toBeVisible();
    await expect(page.locator('.typingText')).toContainText('Support agent is typing...');
  });

  test('should handle escalation', async ({ page }) => {
    // Send a message that triggers escalation
    await page.fill('textarea[placeholder="Type your message..."]', 'I need to speak to a human agent');
    await page.click('button:has-text("Send")');
    
    // Wait for escalation response
    await page.waitForSelector('.escalationNotice');
    await expect(page.locator('.escalationNotice')).toBeVisible();
    await expect(page.locator('h3')).toContainText('Escalated to Human Agent');
  });

  test('should display source citations', async ({ page }) => {
    // Send a query that should return sources
    await page.fill('textarea[placeholder="Type your message..."]', 'How do I return an item?');
    await page.click('button:has-text("Send")');
    
    // Wait for response with sources
    await page.waitForSelector('.sources');
    await expect(page.locator('.sources')).toBeVisible();
    await expect(page.locator('.sourceCitation')).toBeVisible();
  });

  test('should handle new chat functionality', async ({ page }) => {
    // Send a message
    await page.fill('textarea[placeholder="Type your message..."]', 'First message');
    await page.click('button:has-text("Send")');
    
    // Wait for response
    await page.waitForSelector('.message.assistant');
    
    // Click new chat button
    await page.click('button:has-text("New Chat")');
    
    // Check if chat is cleared
    await expect(page.locator('.message')).toHaveCount(0);
    
    // Send a new message
    await page.fill('textarea[placeholder="Type your message..."]', 'New chat message');
    await page.click('button:has-text("Send")');
    
    // Check if new message is displayed
    await expect(page.locator('.message.user')).toContainText('New chat message');
  });

  test('should handle error states', async ({ page }) => {
    // Mock API error
    await page.route('**/chat/sessions/*/messages', (route) => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal server error' })
      });
    });
    
    // Send a message
    await page.fill('textarea[placeholder="Type your message..."]', 'Test error');
    await page.click('button:has-text("Send")');
    
    // Check if error message is displayed
    await expect(page.locator('.errorMessage')).toBeVisible();
    await expect(page.locator('.errorMessage')).toContainText('Error');
  });

  test('should handle keyboard shortcuts', async ({ page }) => {
    // Focus on textarea
    await page.click('textarea[placeholder="Type your message..."]');
    
    // Type message and press Enter
    await page.fill('textarea[placeholder="Type your message..."]', 'Test Enter key');
    await page.keyboard.press('Enter');
    
    // Check if message is sent
    await expect(page.locator('.message.user')).toContainText('Test Enter key');
    
    // Check if Shift+Enter creates new line
    await page.fill('textarea[placeholder="Type your message..."]', 'Line 1');
    await page.keyboard.press('Shift+Enter');
    await page.type('textarea[placeholder="Type your message..."]', 'Line 2');
    await page.keyboard.press('Enter');
    
    // Check if multi-line message is sent
    await expect(page.locator('.message.user')).toContainText('Line 1');
    await expect(page.locator('.message.user')).toContainText('Line 2');
  });

  test('should be responsive on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    // Check if chat interface is still usable
    await expect(page.locator('.chatWindow')).toBeVisible();
    
    // Send a message
    await page.fill('textarea[placeholder="Type your message..."]', 'Mobile test');
    await page.click('button:has-text("Send")');
    
    // Check if message is displayed
    await expect(page.locator('.message.user')).toContainText('Mobile test');
  });
});
