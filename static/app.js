// ── State ──────────────────────────────────────────────
let tasks = [];

// ── Boot ───────────────────────────────────────────────
async function boot() {
  const res = await fetch('/api/tasks');
  tasks = await res.json();
  render();
}

// ── Render ─────────────────────────────────────────────
function render() {
  const list   = document.getElementById('taskList');
  const empty  = document.getElementById('emptyState');
  const total  = document.getElementById('totalCount');
  const done   = document.getElementById('doneCount');

  list.innerHTML = '';

  const doneCount = tasks.filter(t => t.completed).length;
  total.textContent = `${tasks.length} task${tasks.length !== 1 ? 's' : ''}`;
  done.textContent  = `${doneCount} done`;

  if (tasks.length === 0) {
    empty.classList.add('visible');
    return;
  }
  empty.classList.remove('visible');

  tasks.forEach(task => {
    const li = document.createElement('li');
    li.className = `task-item${task.completed ? ' done' : ''}`;
    li.dataset.id = task.id;
    li.innerHTML = `
      <button class="check-btn" onclick="toggleTask('${task.id}')" title="Toggle complete"></button>
      <span class="task-title">${escapeHtml(task.title)}</span>
      <button class="delete-btn" onclick="deleteTask('${task.id}')" title="Delete">×</button>
    `;
    list.appendChild(li);
  });
}

// ── Actions ────────────────────────────────────────────
async function addTask() {
  const input = document.getElementById('taskInput');
  const title = input.value.trim();
  if (!title) { input.focus(); return; }

  const res  = await fetch('/api/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
  });
  const task = await res.json();
  tasks.unshift(task);
  input.value = '';
  input.focus();
  render();
}

async function toggleTask(id) {
  const res  = await fetch(`/api/tasks/${id}`, { method: 'PATCH' });
  const updated = await res.json();
  tasks = tasks.map(t => t.id === id ? updated : t);
  render();
}

async function deleteTask(id) {
  const li = document.querySelector(`[data-id="${id}"]`);
  if (li) {
    li.style.transition = 'opacity .2s, transform .2s';
    li.style.opacity    = '0';
    li.style.transform  = 'translateX(20px)';
    await sleep(200);
  }
  await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
  tasks = tasks.filter(t => t.id !== id);
  render();
}

// ── Helpers ────────────────────────────────────────────
function escapeHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// Enter key to add task
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('taskInput').addEventListener('keydown', e => {
    if (e.key === 'Enter') addTask();
  });
  boot();
});
