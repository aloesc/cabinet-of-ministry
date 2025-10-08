document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault(); // чтобы форма не перезагружала страницу

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch("http://localhost:8000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) throw new Error("Ошибка логина");

    const data = await response.json();
    const token = data.access_token;

    // Сохраняем токен
    localStorage.setItem("token", token);

    window.location.href = "../www/index.html";
  } catch (err) {
    console.error(err);
    alert("Не удалось войти");
  }
});


document.querySelector(".restore-btn").addEventListener("click", () => {
  alert("Функция восстановления пароля пока недоступна.");
});

const restore_btn = document.querySelector(".restore-btn");
forgot_btn.addEventListener("click", () => {
  window.location.href = "restore/restore.html";
});