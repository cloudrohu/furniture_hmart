    const chatToggle = document.getElementById("chat-toggle");
    const chatbox = document.getElementById("chatbox");
    const chatClose = document.getElementById("chat-close");
    const chatMessages = document.getElementById("chat-messages");
    const chatInput = document.getElementById("chat-input");
    const chatSend = document.getElementById("chat-send");
    const inquiryForm = document.getElementById("inquiry-form");

    chatToggle.addEventListener("click", () => {
      chatbox.classList.toggle("hidden");
    });

    chatClose.addEventListener("click", () => {
      chatbox.classList.add("hidden");
    });

    // Predefined Furniture Q&A
    const responses = {
      "Yes": "✅ Great! Please provide more details so I can assist better.",
      "hello": "Hi there! How can I assist you with furniture?",
      "hi": "Hello! Looking for furniture today?",
      "sofa": "We have a wide range of sofas – leather, fabric, recliners. Would you like to see options?",
      "bed": "Our beds come in king, queen, and single sizes. Do you prefer wooden or upholstered?",
      "chair": "We offer dining chairs, office chairs, and lounge chairs. Which type do you want?",
      "table": "We have dining tables, coffee tables, and study tables. What are you looking for?",
      "wardrobe": "We have sliding door and hinged door wardrobes in different sizes. Do you want a compact or large one?",
      "price": "Our furniture pricing starts from very affordable to premium luxury range. Do you have a budget in mind?",
      "delivery": "We provide free home delivery within the city. Outside city deliveries are chargeable.",
      "custom": "Yes, we also provide customized furniture as per your design and space requirement.",
      "inquiry": "Sure! Please fill out the inquiry form below 👇",
      "contact": "I'd love to help! Please provide your details below 👇",
      "thanks": "You're most welcome! 😊 Anything else I can help you with?"

    };

    // Send message function
    function sendMessage() {
      const msg = chatInput.value.trim().toLowerCase();
      if (!msg) return;

      // User message
      const userMsg = document.createElement("div");
      userMsg.className = "bg-green-100 p-2 rounded-md text-gray-800 w-fit ml-auto";
      userMsg.textContent = chatInput.value;
      chatMessages.appendChild(userMsg);

      // Auto reply
      setTimeout(() => {
        const botMsg = document.createElement("div");
        botMsg.className = "bg-gray-100 p-2 rounded-md text-gray-800 w-fit";

        if (responses[msg]) {
          botMsg.textContent = responses[msg];
          chatMessages.appendChild(botMsg);

          // Show form if asked for inquiry/contact
          if (msg.includes("inquiry") || msg.includes("contact")) {
            inquiryForm.classList.remove("hidden");
          }
        } else {
          botMsg.textContent = "Sorry, I didn’t understand that. Can you ask about sofa, bed, chair, table, or wardrobe?";
          chatMessages.appendChild(botMsg);
        }

        chatMessages.scrollTop = chatMessages.scrollHeight;
      }, 500);

      chatInput.value = "";
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    chatSend.addEventListener("click", sendMessage);
    chatInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") sendMessage();
    });

    // Inquiry Form Submit
    function submitInquiry() {
      const name = document.getElementById("name").value;
      const phone = document.getElementById("phone").value;
      const email = document.getElementById("email").value;
      const message = document.getElementById("message").value;

      if (!name || !phone) {
        alert("Please enter at least Name and Phone Number.");
        return;
      }

      alert(`✅ Thank you ${name}! We will contact you soon at ${phone} or ${email}.`);

      // Clear form
      document.getElementById("name").value = "";
      document.getElementById("phone").value = "";
      document.getElementById("email").value = "";
      document.getElementById("message").value = "";
    }