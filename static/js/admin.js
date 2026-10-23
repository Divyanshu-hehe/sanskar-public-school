/**
 * SANSKAR PUBLIC SCHOOL — Admin Dashboard Interactive Script
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Table Quick Filter Search
  const searchInputs = document.querySelectorAll('.admin-table-search');
  searchInputs.forEach(input => {
    input.addEventListener('keyup', (e) => {
      const query = e.target.value.toLowerCase();
      const targetTable = document.querySelector(input.dataset.targetTable || '.admin-table');
      if (!targetTable) return;

      const rows = targetTable.querySelectorAll('tbody tr');
      rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(query) ? '' : 'none';
      });
    });
  });

  // 2. Delete Confirmation Prompt
  const deleteForms = document.querySelectorAll('.form-delete-confirm');
  deleteForms.forEach(form => {
    form.addEventListener('submit', (e) => {
      const itemTitle = form.dataset.itemTitle || 'this item';
      if (!confirm(`Are you sure you want to permanently delete ${itemTitle}? This action cannot be undone.`)) {
        e.preventDefault();
      }
    });
  });
});
