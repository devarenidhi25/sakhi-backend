document.addEventListener("DOMContentLoaded", () => {
  // Initialize AOS Animation Library
  AOS.init({
    duration: 800,
    easing: "ease-in-out",
    once: true,
    mirror: false,
  });

  // Navbar Scroll Effect
  const navbar = document.querySelector(".navbar");

  function toggleNavbarBackground() {
    if (window.scrollY > 50) {
      navbar.classList.add("scrolled");
    } else {
      navbar.classList.remove("scrolled");
    }
  }

  window.addEventListener("scroll", toggleNavbarBackground);

  // Initialize scrolling immediately
  toggleNavbarBackground();

  // Counter Animation for Statistics
  const counters = document.querySelectorAll(".counter");
  const speed = 200;

  const animateCounter = () => {
    counters.forEach((counter) => {
      const target = +counter.dataset.target;
      const count = +counter.innerText;
      const increment = target / speed;

      if (count < target) {
        counter.innerText = Math.ceil(count + increment);
        setTimeout(animateCounter, 1);
      } else {
        counter.innerText = target;
      }
    });
  };

  // Start counter animation when the statistics section is visible
  const statsSection = document.querySelector(".statistics-section");

  const statsObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateCounter();
          statsObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.5 }
  );

  if (statsSection) {
    statsObserver.observe(statsSection);
  }

  // Replace the old FAQ toggle function with Bootstrap's built-in functionality
  // The accordion from Bootstrap 5 handles the toggle automatically

  // Add smooth scrolling for navigation
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();

      const targetId = this.getAttribute("href");
      if (targetId === "#") return;

      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop - 80,
          behavior: "smooth",
        });
      }
    });
  });
});
