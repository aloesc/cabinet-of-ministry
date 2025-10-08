const menuBtn = document.getElementById("menuBtn");
const sideMenu = document.getElementById("sideMenu");

menuBtn.addEventListener("click", (event) => {
  event.stopPropagation(); // Предотвращаем "всплытие" события
  sideMenu.classList.toggle("open");
});

document.addEventListener("click", (event) => {
  // Закрываем меню, если клик был вне его
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