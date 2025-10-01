 function changeImage(src) {
      document.getElementById('pd-img').src = src;
    }

    document.getElementById('add-to-cart-btn').addEventListener('click', () => {
      const name   = document.getElementById('pd-name').innerText;
      const price  = parseInt(document.getElementById('pd-price').innerText.match(/\d+/)[0], 10);
      const rating = document.getElementById('pd-rating').innerText;
      const img    = document.getElementById('pd-img').src;

      let items = JSON.parse(localStorage.getItem('cartItems')) || [];
      const idx = items.findIndex(i => i.name === name);
      if (idx > -1) items[idx].quantity += 1;
      else items.push({ name, price, rating, img, quantity:1 });
      localStorage.setItem('cartItems', JSON.stringify(items));
      alert(name + " cart mein add ho gaya!");
    });

    document.querySelectorAll('.accordion').forEach(a => {
      a.addEventListener('click', () => {
        const panel = a.nextElementSibling;
        panel.classList.toggle('open');
      });
    });

    document.querySelectorAll('#size-options .option, #color-options .option').forEach(opt => {
      opt.addEventListener('click', () => {
        const siblings = opt.parentElement.querySelectorAll('.option');
        siblings.forEach(s => s.classList.remove('selected'));
        opt.classList.add('selected');
      });
    });

    function buyNow() {
      alert("Buy Now button clicked!");
    }

    // Function to load and display reviews from localStorage
    function loadReviews() {
        const reviews = JSON.parse(localStorage.getItem('reviews')) || [];
        const reviewList = document.getElementById('reviewList');
        reviewList.innerHTML = ''; // Clear existing reviews

        reviews.forEach((review, index) => {
            const li = document.createElement('li');
            li.textContent = review;

            // Create a "Remove" button for each review
            const removeBtn = document.createElement('button');
            removeBtn.textContent = 'Remove';
            removeBtn.style.marginLeft = '10px';
            removeBtn.addEventListener('click', () => removeReview(index));

            li.appendChild(removeBtn);
            reviewList.appendChild(li);
        });
    }

    // Function to remove a review
    function removeReview(index) {
        const reviews = JSON.parse(localStorage.getItem('reviews')) || [];
        reviews.splice(index, 1); // Remove the review at the given index
        localStorage.setItem('reviews', JSON.stringify(reviews)); // Update localStorage
        loadReviews(); // Reload the review list
    }

    // Function to add a new review
    function addReview(reviewText) {
        const reviews = JSON.parse(localStorage.getItem('reviews')) || [];
        reviews.push(reviewText);
        localStorage.setItem('reviews', JSON.stringify(reviews));
        loadReviews(); // Update the review list
    }

    // Event listener for the submit button
    document.getElementById('submitReview').addEventListener('click', () => {
        const reviewText = document.getElementById('reviewText').value.trim();
        if (reviewText) {
            addReview(reviewText); // Add the new review
            document.getElementById('reviewText').value = ''; // Clear the input
        } else {
            alert('Please write a review before submitting.');
        }
    });

    // Load reviews when the page is loaded
    window.onload = loadReviews;
