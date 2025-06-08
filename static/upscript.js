document.addEventListener("DOMContentLoaded", () => {
  // Password Toggle Functionality
  const togglePassword = document.getElementById("togglePassword");
  const passwordInput = document.getElementById("password");
  const toggleConfirmPassword = document.getElementById(
    "toggleConfirmPassword"
  );
  const confirmPasswordInput = document.getElementById("confirmPassword");

  // Password strength elements
  const passwordStrengthProgress = document.getElementById(
    "passwordStrengthProgress"
  );
  const passwordStrengthBar = document.getElementById("passwordStrengthBar");
  const passwordStrengthText = document.getElementById("passwordStrengthText");
  const passwordMatchIndicator = document.getElementById(
    "passwordMatchIndicator"
  );

  // Toggle password visibility
  togglePassword.addEventListener("click", function () {
    const type =
      passwordInput.getAttribute("type") === "password" ? "text" : "password";
    passwordInput.setAttribute("type", type);
    this.querySelector("i").classList.toggle("bi-eye");
    this.querySelector("i").classList.toggle("bi-eye-slash");
  });

  // Toggle confirm password visibility
  toggleConfirmPassword.addEventListener("click", function () {
    const type =
      confirmPasswordInput.getAttribute("type") === "password"
        ? "text"
        : "password";
    confirmPasswordInput.setAttribute("type", type);
    this.querySelector("i").classList.toggle("bi-eye");
    this.querySelector("i").classList.toggle("bi-eye-slash");
  });

  // Password strength checker
  passwordInput.addEventListener("input", function () {
    const password = this.value;

    if (password.length > 0) {
      passwordStrengthProgress.style.display = "block";
      passwordStrengthText.style.display = "block";

      // Calculate password strength
      let strength = 0;

      // Length check
      if (password.length >= 8) strength += 25;

      // Uppercase check
      if (/[A-Z]/.test(password)) strength += 25;

      // Lowercase check
      if (/[a-z]/.test(password)) strength += 25;

      // Number or special char check
      if (/[0-9!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password))
        strength += 25;

      // Update progress bar
      passwordStrengthBar.style.width = strength + "%";

      // Update text based on strength
      if (strength <= 25) {
        passwordStrengthText.textContent = "Weak";
        passwordStrengthText.style.color = "#ff4d4d";
      } else if (strength <= 50) {
        passwordStrengthText.textContent = "Fair";
        passwordStrengthText.style.color = "#ffaa00";
      } else if (strength <= 75) {
        passwordStrengthText.textContent = "Good";
        passwordStrengthText.style.color = "#ffff00";
      } else {
        passwordStrengthText.textContent = "Strong";
        passwordStrengthText.style.color = "#00ff00";
      }
    } else {
      passwordStrengthProgress.style.display = "none";
      passwordStrengthText.style.display = "none";
    }

    checkPasswordsMatch();
  });

  confirmPasswordInput.addEventListener("input", checkPasswordsMatch);

  function checkPasswordsMatch() {
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;

    if (confirmPassword.length > 0) {
      passwordMatchIndicator.style.display = "block";

      if (password === confirmPassword) {
        passwordMatchIndicator.textContent = "Passwords match";
        passwordMatchIndicator.style.color = "#00ff00";
      } else {
        passwordMatchIndicator.textContent = "Passwords do not match";
        passwordMatchIndicator.style.color = "#ff4d4d";
      }
    } else {
      passwordMatchIndicator.style.display = "none";
    }
  }

  // Form submission
  document
    .getElementById("signupForm")
    .addEventListener("submit", async (e) => {
      e.preventDefault();

      const username = document.getElementById("username").value;
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;

      const response = await fetch("/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password }),
      });

      const data = await response.json();
      alert(data.message);
      if (response.ok) window.location.href = "/templates/form.html";

      // Check if passwords match
      if (password !== confirmPassword) {
        confirmPasswordInput.classList.add("shake");
        setTimeout(() => {
          confirmPasswordInput.classList.remove("shake");
        }, 500);
        return;
      }

      alert("Sign up successful! Redirecting to login page...");
      window.location.href = "index.html";
    });

  // Create animated background particles
  const particlesContainer = document.getElementById("particles-container");
  const particleCount = 20;

  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement("div");
    particle.classList.add("floating-particle");

    // Random size between 50px and 150px
    const size = Math.random() * 100 + 50;
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;

    // Random position
    particle.style.top = `${Math.random() * 100}%`;
    particle.style.left = `${Math.random() * 100}%`;

    // Random opacity
    particle.style.opacity = (Math.random() * 0.5 + 0.1).toString();

    // Animation
    const duration = Math.random() * 10 + 10;
    particle.style.animation = `float ${duration}s linear infinite`;

    particlesContainer.appendChild(particle);
  }

  document.querySelector(".sign-in-link").addEventListener("click", (e) => {
    e.preventDefault();
    document.body.style.opacity = "0";
    setTimeout(() => {
      window.location.href = "/sign-in";
    }, 300);
  });
});
