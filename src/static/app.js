// EduTask Frontend Controller
// Baseline v1.1 - Interfacing with FastAPI REST API & CR-101 Analytics

document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const tasksList = document.getElementById("tasks-list");
  const taskCountBadge = document.getElementById("task-count-badge");
  const searchInput = document.getElementById("search-input");
  const filterCourse = document.getElementById("filter-course");
  const filterPriority = document.getElementById("filter-priority");
  const filterStatus = document.getElementById("filter-status");

  // Stat Elements
  const statTotal = document.getElementById("stat-total");
  const statPending = document.getElementById("stat-pending");
  const statCompleted = document.getElementById("stat-completed");
  const statHours = document.getElementById("stat-hours");
  const statRate = document.getElementById("stat-rate");
  const progressBar = document.getElementById("progress-bar");

  // Health Elements
  const healthStatusText = document.getElementById("health-status-text");
  const footerUptime = document.getElementById("footer-uptime");
  const footerVersion = document.getElementById("footer-version");

  // Modal Elements
  const modal = document.getElementById("task-modal");
  const openModalBtn = document.getElementById("open-add-modal-btn");
  const closeModalBtn = document.getElementById("close-modal-btn");
  const cancelModalBtn = document.getElementById("cancel-modal-btn");
  const createTaskForm = document.getElementById("create-task-form");

  // Fetch and render everything
  async function loadData() {
    await Promise.all([fetchTasks(), fetchWorkloadAnalytics(), fetchHealthStatus()]);
  }

  // Fetch tasks with current active filters
  async function fetchTasks() {
    const params = new URLSearchParams();
    if (filterCourse.value) params.append("course_code", filterCourse.value);
    if (filterPriority.value) params.append("priority", filterPriority.value);
    if (filterStatus.value) params.append("status", filterStatus.value);
    if (searchInput.value.trim()) params.append("search", searchInput.value.trim());

    try {
      const response = await fetch(`/api/tasks?${params.toString()}`);
      if (!response.ok) throw new Error("Failed to fetch tasks");
      const tasks = await response.json();
      renderTasks(tasks);
    } catch (err) {
      console.error("Error fetching tasks:", err);
      tasksList.innerHTML = `<p class="error-msg">Failed to load tasks from server.</p>`;
    }
  }

  // Render task cards
  function renderTasks(tasks) {
    taskCountBadge.textContent = `${tasks.length} task${tasks.length === 1 ? '' : 's'}`;

    if (tasks.length === 0) {
      tasksList.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 2rem; color: #64748b;">
          <p>No matching assignments found. Click "+ New Task" to create one!</p>
        </div>
      `;
      return;
    }

    tasksList.innerHTML = tasks.map(task => {
      const isCompleted = task.status === "COMPLETED";
      const isOverdue = task.is_overdue && !isCompleted;
      
      return `
        <div class="task-card ${isCompleted ? 'completed' : ''}" data-id="${task.id}">
          <div>
            <div class="task-top-row">
              <div class="task-badge-group">
                <span class="badge badge-course">${escapeHtml(task.course_code)}</span>
                <span class="badge badge-${task.priority}">${task.priority}</span>
              </div>
              <span style="font-size: 0.75rem; color: #64748b;">${task.estimated_hours}h est.</span>
            </div>
            <h3 class="task-title">${escapeHtml(task.title)}</h3>
            <p class="task-desc">${escapeHtml(task.description || "No description provided.")}</p>
          </div>

          <div>
            <div class="task-meta">
              <span class="${isOverdue ? 'due-warning' : ''}">
                📅 Due: ${task.due_date} ${isOverdue ? '(OVERDUE!)' : ''}
              </span>
              <span>Status: <strong>${task.status}</strong></span>
            </div>
            <div class="task-actions">
              <label class="check-label">
                <input type="checkbox" class="toggle-checkbox" data-id="${task.id}" ${isCompleted ? 'checked' : ''}>
                <span>${isCompleted ? 'Completed' : 'Mark Complete'}</span>
              </label>
              <button class="delete-btn" data-id="${task.id}" title="Delete Task">🗑 Delete</button>
            </div>
          </div>
        </div>
      `;
    }).join("");

    // Attach card event listeners
    attachCardListeners();
  }

  function attachCardListeners() {
    document.querySelectorAll(".toggle-checkbox").forEach(chk => {
      chk.addEventListener("change", async (e) => {
        const taskId = e.target.getAttribute("data-id");
        await toggleTask(taskId);
      });
    });

    document.querySelectorAll(".delete-btn").forEach(btn => {
      btn.addEventListener("click", async (e) => {
        const taskId = e.target.getAttribute("data-id");
        if (confirm("Are you sure you want to delete this task?")) {
          await deleteTask(taskId);
        }
      });
    });
  }

  // Toggle task status
  async function toggleTask(taskId) {
    try {
      const res = await fetch(`/api/tasks/${taskId}/toggle`, { method: "POST" });
      if (res.ok) {
        await fetchTasks();
        await fetchWorkloadAnalytics();
      }
    } catch (err) {
      console.error("Error toggling task:", err);
    }
  }

  // Delete task
  async function deleteTask(taskId) {
    try {
      const res = await fetch(`/api/tasks/${taskId}`, { method: "DELETE" });
      if (res.ok) {
        await fetchTasks();
        await fetchWorkloadAnalytics();
      }
    } catch (err) {
      console.error("Error deleting task:", err);
    }
  }

  // Fetch CR-101 workload analytics
  async function fetchWorkloadAnalytics() {
    try {
      const res = await fetch("/api/tasks/analytics/workload");
      if (!res.ok) return;
      const data = await res.json();

      statTotal.textContent = data.total_tasks;
      statPending.textContent = data.pending_tasks + data.in_progress_tasks;
      statCompleted.textContent = data.completed_tasks;
      statHours.textContent = `${data.remaining_hours} hrs`;
      statRate.textContent = `${data.completion_rate_percentage}%`;
      progressBar.style.width = `${data.completion_rate_percentage}%`;
    } catch (err) {
      console.error("Error fetching analytics:", err);
    }
  }

  // Health and Uptime check
  async function fetchHealthStatus() {
    try {
      const res = await fetch("/api/health");
      if (!res.ok) throw new Error("Health check failed");
      const health = await res.json();
      healthStatusText.textContent = `Health: ${health.status} (${health.service})`;
      footerUptime.textContent = `Uptime: ${health.uptime_seconds}s`;
      footerVersion.textContent = `Release: v${health.version}`;
    } catch (err) {
      healthStatusText.textContent = "Health: DOWN";
      healthStatusText.style.color = "#ef4444";
    }
  }

  // Modal handlers
  openModalBtn.addEventListener("click", () => {
    // Set default due date to tomorrow
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    document.getElementById("task-due-date").value = tomorrow.toISOString().split("T")[0];
    modal.classList.remove("hidden");
  });

  const closeModal = () => modal.classList.add("hidden");
  closeModalBtn.addEventListener("click", closeModal);
  cancelModalBtn.addEventListener("click", closeModal);

  // Form submission
  createTaskForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = {
      title: document.getElementById("task-title").value.trim(),
      course_code: document.getElementById("task-course").value.trim().toUpperCase(),
      due_date: document.getElementById("task-due-date").value,
      priority: document.getElementById("task-priority").value,
      estimated_hours: parseFloat(document.getElementById("task-hours").value),
      description: document.getElementById("task-desc").value.trim()
    };

    try {
      const res = await fetch("/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error("Failed to create task");
      createTaskForm.reset();
      closeModal();
      await fetchTasks();
      await fetchWorkloadAnalytics();
    } catch (err) {
      alert("Error saving task. Please check your inputs.");
    }
  });

  // Filters & search listeners
  let searchTimeout = null;
  searchInput.addEventListener("input", () => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(fetchTasks, 250);
  });
  filterCourse.addEventListener("change", fetchTasks);
  filterPriority.addEventListener("change", fetchTasks);
  filterStatus.addEventListener("change", fetchTasks);

  // Polling for health check every 15s
  setInterval(fetchHealthStatus, 15000);

  // Utility
  function escapeHtml(str) {
    if (!str) return "";
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  // Initial load
  loadData();
});
