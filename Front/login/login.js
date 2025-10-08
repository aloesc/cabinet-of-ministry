document.getElementById("loginForm").addEventListener("submit", (e) => {
  e.preventDefault();
  alert("Вы успешно вошли в систему!");
});

document.querySelector(".restore-btn").addEventListener("click", () => {
  alert("Функция восстановления пароля пока недоступна.");
});
