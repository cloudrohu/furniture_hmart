// ====== ELEMENTS ======
const overlay       = document.getElementById('overlay');
const menu          = document.getElementById('menu');
const submenuShell  = document.getElementById('submenuShell');
const openMenuBtn   = document.getElementById('openMenu');
const closeMenuBtn  = document.getElementById('closeMenu');

// ====== MENU OPEN/CLOSE ======
const openMenu = () => {
  menu.classList.remove('-translate-x-full');
  overlay.classList.remove('hidden');
};
const closeMenu = () => {
  menu.classList.add('-translate-x-full');
  overlay.classList.add('hidden');
  // close any open panel & hide submenu
  submenuShell.classList.add('translate-x-full');
  document.querySelectorAll('#submenuShell > div').forEach(p => p.classList.add('hidden'));
};

openMenuBtn.addEventListener('click', openMenu);
closeMenuBtn.addEventListener('click', closeMenu);
overlay.addEventListener('click', closeMenu);

// ====== CATEGORY -> SUBCATEGORY (ALL HTML-BASED) ======
document.querySelectorAll('.catBtn').forEach(btn => {
  btn.addEventListener('click', () => {
    const target = btn.getAttribute('data-target'); // e.g. "living"
    // hide all panels
    document.querySelectorAll('#submenuShell > div').forEach(p => p.classList.add('hidden'));
    // show required panel
    const panel = document.getElementById(`panel-${target}`);
    if (panel) {
      panel.classList.remove('hidden');
      submenuShell.classList.remove('translate-x-full'); // slide in
    }
  });
});

// Back buttons
document.querySelectorAll('.backBtn').forEach(btn => {
  btn.addEventListener('click', () => {
    submenuShell.classList.add('translate-x-full'); // slide out
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const deliveryText = document.getElementById('deliveryText');
  const pinModal     = document.getElementById('pinModal');
  const openPinModal = document.getElementById('openPinModal');
  const cancelPin    = document.getElementById('cancelPin');
  const savePin      = document.getElementById('savePin');
  const pinInput     = document.getElementById('pinInput');

  function safeParseJSON(str, fallback) {
    try { return JSON.parse(str); } catch { return fallback; }
  }

  function loadLocation() {
    const loc = safeParseJSON(localStorage.getItem('deliveryLocation'), null);
    if (loc && loc.city && loc.pincode) {
      deliveryText.textContent = `Delivery to ${loc.city} (${loc.pincode})`;
    } else {
      deliveryText.textContent = 'Delivery to —';
    }
  }

  function showPinModal() {
    const loc = safeParseJSON(localStorage.getItem('deliveryLocation'), {});
    pinInput.value = loc.pincode || '';
    pinModal.classList.remove('hidden');
  }

  function hidePinModal() {
    pinModal.classList.add('hidden');
  }

  function saveLocation() {
    const pincode = (pinInput.value || '').trim();

    if (!/^\d{6}$/.test(pincode)) {
      alert('Please enter a valid 6-digit pincode.');
      return;
    }

    fetch(`https://api.postalpincode.in/pincode/${pincode}`)
      .then(res => res.json())
      .then(data => {
        if (data[0].Status === "Success" && data[0].PostOffice.length > 0) {
          const city = data[0].PostOffice[0].District;
          const locationData = { city, pincode };
          localStorage.setItem('deliveryLocation', JSON.stringify(locationData));
          loadLocation();
          hidePinModal();
        } else {
          alert('Invalid pincode. Please try again.');
        }
      })
      .catch(() => {
        alert('Error fetching city. Please check your internet.');
      });
  }

  // Event Listeners
  openPinModal.addEventListener('click', showPinModal);
  cancelPin.addEventListener('click', hidePinModal);
  savePin.addEventListener('click', saveLocation);

  // Load on page start
  loadLocation();
});


// Initialize on first load

  const searchPopup = document.getElementById('searchPopup');
  const openSearch = document.getElementById('openSearch');
  const closeSearch = document.getElementById('closeSearch');

  openSearch.addEventListener('click', () => {
    searchPopup.classList.remove('hidden');
    searchPopup.classList.add('flex');
  });

  closeSearch.addEventListener('click', () => {
    searchPopup.classList.add('hidden');
    searchPopup.classList.remove('flex');
  });

  // Close popup on clicking outside
  searchPopup.addEventListener('click', (e) => {
    if (e.target === searchPopup) {
      searchPopup.classList.add('hidden');
      searchPopup.classList.remove('flex');
    }
  });

  
  