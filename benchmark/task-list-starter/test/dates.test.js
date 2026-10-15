import test from 'node:test';
import assert from 'node:assert/strict';
import { parseDate, formatDate, isOverdue } from '../src/dates.js';

test('parseDate keeps the day of the month', () => {
  assert.equal(parseDate('2026-01-15').getDate(), 15);
});

test('formatDate pads month and day', () => {
  assert.equal(formatDate(new Date(2026, 0, 5)), '2026-01-05');
});

test('isOverdue is false for the same day', () => {
  assert.equal(isOverdue('2026-01-15', '2026-01-15'), false);
});
