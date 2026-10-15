// Date helpers. Dates are plain strings in the form YYYY-MM-DD.

export function parseDate(text) {
  const [y, m, d] = text.split('-').map(Number);
  return new Date(y, m, d);
}

export function formatDate(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

export function isOverdue(due, today) {
  return parseDate(due) < parseDate(today);
}
