document.addEventListener("DOMContentLoaded", function () {
  const cards = document.querySelectorAll(".card");
  cards.forEach((card, index) => {
    setTimeout(() => {
      card.classList.add("animate-fade");
    }, index * 100); // Staggered animation
  });
});
document.addEventListener("DOMContentLoaded", function () {
  const img = document.querySelector(".animate-fade");
  img.classList.add("animate-fade");

  const fadeIn = () => {
    img.style.opacity = "0";
    img.style.transition = "opacity 0.5s ease-in-out";
    setTimeout(() => {
      img.style.opacity = "1";
    }, 100); // Delay for fade-in effect
  };

  fadeIn();
});
document.addEventListener("DOMContentLoaded", function () {
  const leftCards = document.querySelectorAll(".animate-fade-left");
  const rightCards = document.querySelectorAll(".animate-fade-right");

  leftCards.forEach((card, index) => {
    setTimeout(() => {
      card.style.transform = "translateX(0)";
      card.style.opacity = "1";
      card.style.transition =
        "transform 0.5s ease-in-out, opacity 0.5s ease-in-out";
    }, index * 300); // Staggered animation for left cards
  });

  rightCards.forEach((card, index) => {
    setTimeout(() => {
      card.style.transform = "translateX(0)";
      card.style.opacity = "1";
      card.style.transition =
        "transform 0.5s ease-in-out, opacity 0.5s ease-in-out";
    }, index * 300 + 150); // Staggered animation for right cards
  });
});
function updateFileName(event) {
  const fileInput = document.getElementById("image");
  const fileNameDisplay = document.getElementById("file-name");
  const uploadedImage = document.getElementById("uploaded-image");

  // Update the file name displayed on the button
  const file = fileInput.files[0];
  if (file) {
    fileNameDisplay.textContent = file.name;

    // Display the selected image
    const reader = new FileReader();
    reader.onload = function (e) {
      uploadedImage.src = e.target.result;
    };
    reader.readAsDataURL(file);
  } else {
    fileNameDisplay.textContent = "Choose File";
    uploadedImage.src = ""; // Reset the image if no file is selected
  }
}
document.getElementById("calculateBtn").addEventListener("click", function () {
  const seedDensity = document.getElementById("seedDensity").value;
  const area = document.getElementById("area").value;
  const result = document.getElementById("result");

  if (seedDensity && area) {
    const seedsNeeded = seedDensity * area;
    result.textContent = `You will need approximately ${seedsNeeded} seeds.`;
  } else {
    result.textContent = "Please enter valid values.";
  }
});
document.getElementById("menu-toggle").addEventListener("click", function () {
  const mobileMenu = document.getElementById("mobile-menu");
  mobileMenu.classList.toggle("hidden");
});
document.addEventListener("DOMContentLoaded", function () {
  const navbar = document.querySelector("nav"); // Select your navbar
  const toggleNavbar = () => {
    if (window.scrollY > 50) {
      // Change 50 to adjust when the navbar should change
      navbar.classList.add("navbar-scrolled");
      navbar.classList.remove("navbar-transparent");
    } else {
      navbar.classList.add("navbar-transparent");
      navbar.classList.remove("navbar-scrolled");
    }
  };

  // Listen for scroll events
  window.addEventListener("scroll", toggleNavbar);
  toggleNavbar(); // Initial check
});
