document.getElementById("registerForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    username: document.getElementById("username").value,
    full_name: document.getElementById("first_name").value + " " +document.getElementById("last_name").value + " " + document.getElementById("middle_name").value,
    email: document.getElementById("email").value,
    phonenumber: document.getElementById("phone").value,
    password: document.getElementById("password").value,
    date_of_birth: document.getElementById("birth_date").value,
    gender: document.getElementById("gender").value,
  };

  try {
    const response = await fetch("http://localhost:8000/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!response.ok) throw new Error("Ошибка регистрации");

    const result = await response.json();
    alert("Регистрация успешна!");
    console.log(result);

    // Можно перенаправить на логин
    window.location.href = "../login/login.html";
  } catch (err) {
    console.error(err);
    alert("Не удалось зарегистрироваться");
  }
});
