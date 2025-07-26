document.addEventListener("DOMContentLoaded", function () {
  const stars = document.querySelectorAll("#stars i");
  const avgSpan = document.getElementById("avg");
  const countSpan = document.getElementById("count");

  stars.forEach(star => {
    star.addEventListener("mouseover", () => {
      highlightStars(star.dataset.value);
    });
    star.addEventListener("mouseout", () => {
      resetStars();
    });
    star.addEventListener("click", () => {
      submitRating(star.dataset.value);
    });
  });

  function highlightStars(val) {
    stars.forEach(star => {
      star.classList.toggle("hovered", star.dataset.value <= val);
    });
  }

  function resetStars() {
    stars.forEach(star => star.classList.remove("hovered"));
  }

  function submitRating(value) {
    fetch("/submit-rating", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ rating: value })
    })
    .then(res => res.json())
    .then(data => {
      // After submitting, fetch updated rating
      fetch("/get-rating")
        .then(res => res.json())
        .then(data => {
          avgSpan.textContent = data.average.toFixed(1);
          countSpan.textContent = data.count;
        });
    });
  }

  // Load average rating on first load
  fetch("/get-rating")
    .then(res => res.json())
    .then(data => {
      avgSpan.textContent = data.average.toFixed(1);
      countSpan.textContent = data.count;
    });
});
