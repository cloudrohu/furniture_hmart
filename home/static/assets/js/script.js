// Cetegory Start Here //
// Cetegory Start Here //
const slider = document.getElementById("categorySlider");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");

// --- 1. Button Scroll (Infinite) ---
function scrollSlider(amount) {
  slider.scrollBy({ left: amount, behavior: "smooth" });

  // agar end pe pohch gaye to dobara start se set kar do
  if (slider.scrollLeft + slider.offsetWidth >= slider.scrollWidth) {
    setTimeout(() => {
      slider.scrollTo({ left: 0, behavior: "smooth" });
    }, 500);
  }
  // agar start pe gaye aur prev dabaya to last pe bhej do
  if (slider.scrollLeft === 0 && amount < 0) {
    setTimeout(() => {
      slider.scrollTo({ left: slider.scrollWidth, behavior: "smooth" });
    }, 500);
  }
}

prevBtn.addEventListener("click", () => scrollSlider(-300));
nextBtn.addEventListener("click", () => scrollSlider(300));

// --- 2. Mouse Drag / Touch Scroll ---
let isDown = false;
let startX;
let scrollLeft;

slider.addEventListener("mousedown", (e) => {
  isDown = true;
  slider.classList.add("active");
  startX = e.pageX - slider.offsetLeft;
  scrollLeft = slider.scrollLeft;
});

slider.addEventListener("mouseleave", () => {
  isDown = false;
  slider.classList.remove("active");
});

slider.addEventListener("mouseup", () => {
  isDown = false;
  slider.classList.remove("active");
});

slider.addEventListener("mousemove", (e) => {
  if (!isDown) return;
  e.preventDefault();
  const x = e.pageX - slider.offsetLeft;
  const walk = (x - startX) * 2; // drag speed
  slider.scrollLeft = scrollLeft - walk;
});

// Touch support (mobile)
let startTouchX = 0;
slider.addEventListener("touchstart", (e) => {
  startTouchX = e.touches[0].pageX;
});

slider.addEventListener("touchmove", (e) => {
  const touchX = e.touches[0].pageX;
  const walk = (touchX - startTouchX) * 2;
  slider.scrollLeft -= walk;
  startTouchX = touchX;
});
// Cetegory END Here //

// PRODUCT START HERE 
  // Tab switching
    const buttons = document.querySelectorAll('.tab-btn');
    const panels  = document.querySelectorAll('.tab-panel');

    buttons.forEach(btn=>{
      btn.addEventListener('click', ()=>{
        buttons.forEach(b=>b.classList.remove('active'));
        btn.classList.add('active');
        panels.forEach(p=>p.classList.remove('active'));

        const id = btn.dataset.tab;
        document.getElementById(id).classList.add('active');
        // smooth scroll if needed:
        // document.getElementById(id).scrollIntoView({behavior:'smooth',block:'start'});
      });
    });


    const openBtn = document.getElementById("openPopup");
  const closeBtn = document.getElementById("closePopup");
  const popup = document.getElementById("popup");

  openBtn.addEventListener("click", () => {
    popup.classList.remove("hidden"); // Show popup
  });

  closeBtn.addEventListener("click", () => {
    popup.classList.add("hidden"); // Hide popup
  });

  // Popup ke bahar click karne par close
  popup.addEventListener("click", (e) => {
    if (e.target === popup) {
      popup.classList.add("hidden");
    }
  });
// PRODUCT END HERE 


document.addEventListener("DOMContentLoaded", function () {
  // Check if current page exists
  fetch(window.location.pathname, { method: "HEAD" })
    .then(response => {
      if (!response.ok) {
        window.location.href = "/404.html"; // Redirect to 404 page
      }
    })
    .catch(() => {
      window.location.href = "/404.html"; // Agar koi error aaya to bhi redirect
    });
});
