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
