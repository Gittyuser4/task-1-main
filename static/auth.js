const apiUrl = "http://localhost:5000";

// username must contain a symbol
const usernameRegex = /^(?=.*[^a-zA-Z0-9])[a-zA-Z0-9_.@\- ]{2,50}$/;

// Show login form
function showLogin() {
    document.getElementById("loginForm").classList.add("show");
    document.getElementById("registerForm").classList.remove("show");

    document.getElementById("loginTab").classList.add("active");
    document.getElementById("registerTab").classList.remove("active");

    clearMessage();
}

// Show register form
function showRegister() {
    document.getElementById("loginForm").classList.remove("show");
    document.getElementById("registerForm").classList.add("show");

    document.getElementById("registerTab").classList.add("active");
    document.getElementById("loginTab").classList.remove("active");

    clearMessage();
}

// Clear message
function clearMessage() {
    document.getElementById("message").innerText = "";
}


// Login API call
function login() {
    const usernameField = document.getElementById("loginUsername");
    const passwordField = document.getElementById("loginPassword");
    const message = document.getElementById("message");

    const username = usernameField.value.trim();
    const password = passwordField.value.trim();

    fetch(apiUrl + "/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            message.innerText = "Login successful!";
            message.style.color = "green";
        } else {
            message.innerText = data.message;
            message.style.color = "red";
        }

        usernameField.value = "";
        passwordField.value = "";
    });
}


// Register API call
function register() {
    const usernameField = document.getElementById("registerUsername");
    const passwordField = document.getElementById("registerPassword");
    const message = document.getElementById("message");

    const username = usernameField.value.trim();
    const password = passwordField.value.trim();

    if (!usernameRegex.test(username)) {
        message.innerText = "Username must contain at least one symbol";
        message.style.color = "red";
        return;
    }

    fetch(apiUrl + "/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            message.innerText = "Registration successful. Please login.";
            message.style.color = "green";
            showLogin();
        } else {
            message.innerText = data.message;
            message.style.color = "red";
        }

        usernameField.value = "";
        passwordField.value = "";
    });
}


// Show / hide password
function toggleLoginPassword() {
    const passwordField = document.getElementById("loginPassword");
    passwordField.type = passwordField.type === "password" ? "text" : "password";
}

function toggleRegisterPassword() {
    const passwordField = document.getElementById("registerPassword");
    passwordField.type = passwordField.type === "password" ? "text" : "password";
}
