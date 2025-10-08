const monthYear = document.getElementById("monthYear");
const calendarDays = document.getElementById("calendarDays");
const modal = document.getElementById("listTaskModal");
const closeModal = document.getElementById("closeModal");
const modalTitle = document.getElementById("modalTitle");
const taskList = document.getElementById("taskList");
const newTaskInput = document.getElementById("newTaskInput");
const addTaskBtn = document.getElementById("addTaskBtn");

let currentDate = new Date();
let selectedDate = null;
function renderCalendar() {
  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();

  monthYear.textContent = currentDate.toLocaleString("ru-RU", { month: "long", year: "numeric" });
  calendarDays.innerHTML = "";

  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const offset = firstDay === 0 ? 6 : firstDay - 1;

  for (let i = 0; i < offset; i++) {
    const empty = document.createElement("div");
    calendarDays.appendChild(empty);
  }

  for (let day = 1; day <= daysInMonth; day++) {
    const div = document.createElement("div");
    div.classList.add("day");
    div.innerHTML = `<div class="number">${day}</div>`;

    const today = new Date();
    if (day === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
      div.classList.add("today");
    }


    const key = `${year}-${month}-${day}`;
    const tasksJSON = localStorage.getItem(key);
    const tasks = tasksJSON ? JSON.parse(tasksJSON) : [];

    if (tasks.length > 0) {
      div.classList.add("has-task");
      const taskCount = tasks.length;
      // Правильные склонения для слова "задача"
      let taskWord = 'задач';
      if (taskCount === 1) taskWord = 'задача';
      else if (taskCount > 1 && taskCount < 5) taskWord = 'задачи';
      div.innerHTML += `<div class="task-preview">${taskCount} ${taskWord}</div>`;
    }

    div.addEventListener("click", () => openModal(key, day));
    calendarDays.appendChild(div);
  }
}

function openModal(key, day) {
  selectedDate = key;
  modal.style.display = "flex";
  modalTitle.textContent = `Планы на ${day} число`;
  renderTasks();
}

function renderTasks() {
  taskList.innerHTML = "";
  const tasksJSON = localStorage.getItem(selectedDate);
  const tasks = tasksJSON ? JSON.parse(tasksJSON) : [];

  tasks.forEach(task => {
    const li = document.createElement("li");
    li.textContent = task.text;
    li.dataset.taskId = task.id;

    li.addEventListener("click", () => editTask(li, tasks));
    taskList.appendChild(li);
  });
}

function editTask(li, tasks) {
  // Если поле для редактирования уже существует, ничего не делаем.
  if (li.querySelector('.edit-task-input')) {
    return;
  }

  const taskId = Number(li.dataset.taskId);
  const task = tasks.find(t => t.id === taskId);
  const originalText = task.text;

  li.innerHTML = `
    <input type="text" class="edit-task-input" value="${originalText}">
    <button class="save-edit-btn">💾</button>
    <button class="delete-edit-btn">🗑</button>
  `;
  const input = li.querySelector(".edit-task-input");
  input.focus();

  // Предотвращаем "всплытие" клика от поля ввода к элементу списка `li`.
  // Это и есть исправление проблемы.
  input.addEventListener('click', (e) => e.stopPropagation());

  li.querySelector(".save-edit-btn").addEventListener("click", (e) => {
    e.stopPropagation();
    const newText = li.querySelector(".edit-task-input").value.trim();
    if (newText) {
      task.text = newText;
      saveTasks(tasks);
    }
  });

  li.querySelector(".delete-edit-btn").addEventListener("click", (e) => {
    e.stopPropagation();
    const updatedTasks = tasks.filter(t => t.id !== taskId);
    saveTasks(updatedTasks);
  });
}

function saveTasks(tasks) {
  if (tasks.length > 0) {
    localStorage.setItem(selectedDate, JSON.stringify(tasks));
  } else {
    localStorage.removeItem(selectedDate);
  }
  renderTasks();
  renderCalendar();
}

addTaskBtn.addEventListener("click", () => {
  const text = newTaskInput.value.trim();
  if (!text || !selectedDate) return;

  const tasksJSON = localStorage.getItem(selectedDate);
  const tasks = tasksJSON ? JSON.parse(tasksJSON) : [];
  
  tasks.push({ id: Date.now(), text: text });
  saveTasks(tasks);
  newTaskInput.value = "";
});

closeModal.addEventListener("click", closeModalWindow);
modal.addEventListener("click", e => { if (e.target === modal) closeModalWindow(); });

function closeModalWindow() {
  modal.style.display = "none";
  selectedDate = null;
}

document.getElementById("prevMonth").addEventListener("click", () => {
  currentDate.setMonth(currentDate.getMonth() - 1);
  renderCalendar();
});

document.getElementById("nextMonth").addEventListener("click", () => {
  currentDate.setMonth(currentDate.getMonth() + 1);
  renderCalendar();
});

renderCalendar();

// --- Логика для бокового меню ---
const menuBtn = document.getElementById('menuBtn');
const sideMenu = document.getElementById('sideMenu');
const overlay = document.getElementById('overlay');

function toggleMenu() {
  sideMenu.classList.toggle('open');
  overlay.style.display = sideMenu.classList.contains('open') ? 'block' : 'none';
}

menuBtn.addEventListener('click', toggleMenu);
overlay.addEventListener('click', toggleMenu);

(async () => {
  const user = document.querySelectorAll("#username");
  try {
    const token = localStorage.getItem("token");
    const response = await fetch("http://localhost:8000/users/whoami/", {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      throw new Error(`Ошибка запроса: ${response.status}`);
    }
    const userData = await response.json();
    for (let i = 0; i < user.length; i++) {
      user[i].textContent = userData.full_name;
    }
  } catch (err) {
    console.error(err);
    user.textContent = "Пользователь";
  }
})();
const logoutBtn = document.getElementsByClassName("logout-btn")[0];
document.addEventListener("click", (event) => {
  localStorage.clear()
});