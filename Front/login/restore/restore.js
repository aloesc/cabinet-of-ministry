(async () => {
  const email = document.querySelectorAll("#email");
  try {
    const token = localStorage.getItem("token");
    const response = await fetch("http://localhost:8000/auth/forgot_password/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "data": JSON.stringify({ email: email[0].value }),
      },
    });

    if (!response.ok) throw new Error("Ошибка восстановления");

    const result = await response.json();
    alert("Регистрация успешна!");
    console.log(result);

    // Можно перенаправить на логин
    alert("Письмо отправлено");
    window.location.href = "login/login.html";
  } catch (err) {
    console.error(err);
    alert("Не удалось зарегистрироваться");
}
})();