document.getElementById("menuBtn").addEventListener("click", () => {
  alert("Меню в разработке");
});

const searchInput = document.querySelector(".search-section input");
searchInput.addEventListener("input", () => {
  const filter = searchInput.value.toLowerCase();
  document.querySelectorAll(".agenda-item").forEach(item => {
    const text = item.innerText.toLowerCase();
    item.style.display = text.includes(filter) ? "block" : "none";
  });
});

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
