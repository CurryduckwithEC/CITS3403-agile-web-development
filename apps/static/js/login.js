document.addEventListener('DOMContentLoaded', function() {
    const signInBtn = document.getElementById("signIn");
    const signUpBtn = document.getElementById("signUp");
    const registrationForm = document.getElementById("registrationForm");
    const loginForm = document.getElementById("loginForm");
    const container = document.querySelector(".container");

    signInBtn.addEventListener("click", () => {
        container.classList.remove("right-panel-active");
    });

    signUpBtn.addEventListener("click", () => {
        container.classList.add("right-panel-active");
    });

    registrationForm.addEventListener("submit", (e) => {
        e.preventDefault();
        registrationForm.submit();
    });

    loginForm.addEventListener("submit", (e) => {
        e.preventDefault();
        loginForm.submit();
    });
});