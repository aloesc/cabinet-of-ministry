function createAgendaItem(number, description, committee) {
  const item = document.createElement("div");
  item.className = "agenda-item";

  const h3 = document.createElement("h3");
  h3.textContent = `№ ${number}`;
  item.appendChild(h3);

  const p = document.createElement("p");
  p.textContent = description;
  item.appendChild(p);

  if (committee) {
    const small = document.createElement("small");
    small.textContent = `Главный комитет: ${committee}`;
    item.appendChild(small);
  }

  const dot = document.createElement("span");
  dot.className = "dot";
  item.appendChild(dot);

  return item;
}

// ===== Основная логика =====
(async () => {
  const mainContainer = document.querySelector(".agenda-container");
  mainContainer.innerHTML = "<p>Загрузка...</p>";

  try {
    const token = localStorage.getItem("token");

    const response = await fetch("http://localhost:8000/documents/?type_of_doc=string", {
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
    console.log(userData);

    mainContainer.innerHTML = ""; // очищаем «Загрузка...»

    for (let i = 0; i < userData.length; i++) {
      const newItem = createAgendaItem(
        i + 1,
        userData[i].title || "Без названия",
        userData[i].description || "Без описания"
      );
      mainContainer.appendChild(newItem);
    }

  } catch (err) {
    console.error(err);
    mainContainer.innerHTML = "<p>Ошибка при загрузке данных</p>";
  }
})();

// ===== Открытие/закрытие бокового меню =====
const menuBtn = document.getElementById("menuBtn");
const sideMenu = document.getElementById("sideMenu");

menuBtn.addEventListener("click", (event) => {
  event.stopPropagation();
  sideMenu.classList.toggle("open");
});

document.addEventListener("click", (event) => {
  if (sideMenu.classList.contains("open") && !sideMenu.contains(event.target)) {
    sideMenu.classList.remove("open");
  }
});

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