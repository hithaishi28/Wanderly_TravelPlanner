const plannerForm = document.querySelector("#plannerForm");
const resultGrid = document.querySelector("#resultGrid");
const emptyState = document.querySelector("#emptyState");
const chatLauncher = document.querySelector("#chatLauncher");
const chatPanel = document.querySelector("#chatPanel");
const closeChat = document.querySelector("#closeChat");
const chatForm = document.querySelector("#chatForm");
const chatMessages = document.querySelector("#chatMessages");
const destinationCards = document.querySelectorAll(".destination-card");
const placeModal = document.querySelector("#placeModal");
const placeImage = document.querySelector("#placeImage");
const placeVibe = document.querySelector("#placeVibe");
const placeTitle = document.querySelector("#placeTitle");
const placeAbout = document.querySelector("#placeAbout");
const placeHighlights = document.querySelector("#placeHighlights");
const planThisPlace = document.querySelector("#planThisPlace");
const currencySelect = document.querySelector("#currencySelect");
const budgetAmount = document.querySelector("#budgetAmount");
const budgetPreview = document.querySelector("#budgetPreview");
const themeToggle = document.querySelector("#themeToggle");
const mapSearch = document.querySelector("#mapSearch");
const mapSearchButton = document.querySelector("#mapSearchButton");
const googleMapFrame = document.querySelector("#googleMapFrame");
const openGoogleMaps = document.querySelector("#openGoogleMaps");

const icons = {
  overview: "🌍",
  best_time: "☀️",
  itinerary: "🗓️",
  attractions: "📍",
  food: "🍜",
  transport: "🚆",
  accommodation: "🏨",
  budget: "💳",
  packing: "🎒",
  safety: "🛟",
};

const labels = {
  overview: "Overview",
  best_time: "Best time",
  itinerary: "Day-by-day itinerary",
  attractions: "Attractions",
  food: "Food",
  transport: "Transport",
  accommodation: "Accommodation",
  budget: "Budget",
  packing: "Packing",
  safety: "Safety",
};

const sectionArt = {
  overview: "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80",
  best_time: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=80",
  itinerary: "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=1200&q=80",
  attractions: "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=900&q=80",
  food: "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=900&q=80",
  transport: "https://images.unsplash.com/photo-1474487548417-781cb71495f3?auto=format&fit=crop&w=900&q=80",
  accommodation: "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=900&q=80",
  budget: "https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=900&q=80",
  packing: "https://images.unsplash.com/photo-1553531384-cc64ac80f931?auto=format&fit=crop&w=900&q=80",
  safety: "https://images.unsplash.com/photo-1488085061387-422e29b40080?auto=format&fit=crop&w=900&q=80",
};

const imageFallbacks = [
  "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80",
  "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=900&q=80",
  "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=80",
  "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=900&q=80",
];

const inrRates = {
  INR: 1,
  USD: 83,
  EUR: 90,
  GBP: 105,
  AED: 23,
  JPY: 0.56,
};

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function listHtml(items) {
  if (!Array.isArray(items)) {
    return `<p>${escapeHtml(items)}</p>`;
  }
  return `<ul>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
}

function externalLink(url, label) {
  if (!url) return "";
  return `<a class="inline-link" href="${escapeHtml(url)}" target="_blank" rel="noopener">${escapeHtml(label)}</a>`;
}

function detailedListHtml(items, key) {
  if (!Array.isArray(items)) {
    return listHtml(items);
  }

  if (key === "attractions") {
    return `
      <div class="attraction-gallery">
        ${items
          .map((item, index) => {
            const name = typeof item === "string" ? item : item.name;
            const why = typeof item === "string" ? "A must-see stop for your route." : item.why;
            const image = typeof item === "string" ? sectionArt.attractions : item.image || sectionArt.attractions;
            return `
              <article class="mini-visual-card">
                <img src="${escapeHtml(image)}" alt="${escapeHtml(name)}" onerror="this.onerror=null;this.src='${imageFallbacks[index % imageFallbacks.length]}'">
                <div>
                  <strong>${escapeHtml(name || `Attraction ${index + 1}`)}</strong>
                  <span>${escapeHtml(why)}</span>
                </div>
              </article>
            `;
          })
          .join("")}
      </div>
    `;
  }

  if (key === "accommodation") {
    return `
      <div class="option-stack">
        ${items
          .map((item) => {
            if (typeof item === "string") return `<div class="option-row"><strong>Stay option</strong><span>${escapeHtml(item)}</span></div>`;
            return `
              <div class="option-row">
                <strong>${escapeHtml(item.type || item.name || "Stay option")}</strong>
                <span>${escapeHtml(item.details || item.description || "")}</span>
                ${externalLink(item.link, "Booking link")}
              </div>
            `;
          })
          .join("")}
      </div>
    `;
  }

  if (key === "transport") {
    return `
      <div class="option-stack">
        ${items
          .map((item) => {
            if (typeof item === "string") return `<div class="option-row"><strong>Transport tip</strong><span>${escapeHtml(item)}</span></div>`;
            return `
              <div class="option-row">
                <strong>${escapeHtml(item.mode || item.type || "Transport")}</strong>
                <span>${escapeHtml(item.details || item.description || "")}</span>
              </div>
            `;
          })
          .join("")}
      </div>
    `;
  }

  return listHtml(items);
}

function readableOverview(value) {
  if (typeof value !== "string") {
    return value;
  }

  const trimmed = value.trim();
  if (!trimmed.startsWith("{") && !trimmed.startsWith("[")) {
    return value;
  }

  try {
    const parsed = JSON.parse(trimmed);
    if (parsed && typeof parsed.overview === "string") {
      return parsed.overview;
    }
  } catch (error) {
    const match = trimmed.match(/"overview"\\s*:\\s*"([^"]+)/);
    if (match) {
      return match[1];
    }
  }

  return "Your itinerary is ready. Explore the organized cards below for the best time, day-by-day plan, attractions, food, transport, stays, budget, packing, and safety.";
}

function itineraryHtml(days) {
  if (!Array.isArray(days)) {
    return `<p>${escapeHtml(days)}</p>`;
  }

  return `
    <div class="day-list">
      ${days
        .map(
          (day) => `
            <div class="day-plan">
              <div class="day-badge">${escapeHtml(day.day)}</div>
              <strong>${escapeHtml(day.title)}</strong>
              <span><b>Morning:</b> ${escapeHtml(day.morning)}</span>
              <span><b>Afternoon:</b> ${escapeHtml(day.afternoon)}</span>
              <span><b>Evening:</b> ${escapeHtml(day.evening)}</span>
            </div>
          `
        )
        .join("")}
    </div>
  `;
}

function renderCard(key, value, className = "") {
  const displayValue = key === "overview" ? readableOverview(value) : value;
  const body = key === "itinerary" ? itineraryHtml(displayValue) : detailedListHtml(displayValue, key);
  const image =
    key === "overview" && window.latestPlanImage
      ? window.latestPlanImage
      : window.latestSectionImages?.[key] || sectionArt[key];
  const visual = image ? `<img src="${image}" alt="" class="result-art" onerror="this.onerror=null;this.src='${imageFallbacks[0]}'">` : "";
  return `
    <article class="result-card ${className}">
      ${visual}
      <div class="sticker">${icons[key] || "✨"}</div>
      <div class="result-content">
        <h3>${labels[key] || key}</h3>
        ${body}
      </div>
    </article>
  `;
}

function renderPlan(plan) {
  window.latestPlanImage = plan.destination_image || sectionArt.overview;
  window.latestSectionImages = plan.section_images || {};
  const order = [
    ["overview", "feature"],
    ["best_time", ""],
    ["itinerary", "wide-card feature"],
    ["attractions", ""],
    ["food", ""],
    ["transport", ""],
    ["accommodation", ""],
    ["budget", ""],
    ["packing", ""],
    ["safety", ""],
  ];

  resultGrid.innerHTML = order
    .filter(([key]) => plan[key])
    .map(([key, className]) => renderCard(key, plan[key], className))
    .join("");
  emptyState.hidden = true;
  document.querySelectorAll(".result-card").forEach((card, index) => {
    card.style.animationDelay = `${index * 70}ms`;
  });
}

function setTheme(theme) {
  document.body.dataset.theme = theme;
  themeToggle.textContent = theme === "dark" ? "☾" : "☀";
  localStorage.setItem("wanderly-theme", theme);
}

function toggleTheme() {
  setTheme(document.body.dataset.theme === "dark" ? "light" : "dark");
}

function updateMap(place) {
  const query = (place || mapSearch.value || plannerForm.destination.value || "World").trim();
  if (!query) return;
  const encoded = encodeURIComponent(query);
  googleMapFrame.src = `https://www.google.com/maps?q=${encoded}&output=embed`;
  openGoogleMaps.href = `https://www.google.com/maps/search/?api=1&query=${encoded}`;
  mapSearch.value = query;
}

function formatMoney(value, currency) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency,
    maximumFractionDigits: 0,
  }).format(value || 0);
}

function updateBudgetPreview() {
  const amount = Number(budgetAmount.value || 0);
  const currency = currencySelect.value;
  const inrValue = amount * (inrRates[currency] || 1);
  const primary = formatMoney(amount, currency);
  budgetPreview.textContent =
    currency === "INR" ? `Approx. ${primary}` : `Approx. ${primary} (₹${Math.round(inrValue).toLocaleString("en-IN")})`;
}

plannerForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const button = plannerForm.querySelector("button");
  button.classList.add("loading");
  button.disabled = true;

  const payload = Object.fromEntries(new FormData(plannerForm).entries());
  payload.inr_budget = Math.round(Number(payload.budget_amount || 0) * (inrRates[payload.currency] || 1));

  try {
    const response = await fetch("/api/plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Could not generate itinerary.");
    }

    renderPlan(data.plan);
    updateMap(payload.destination);
    document.querySelector("#results").scrollIntoView({ behavior: "smooth" });
  } catch (error) {
    emptyState.hidden = false;
    emptyState.innerHTML = `<strong>Something needs attention.</strong><p>${escapeHtml(error.message)}</p>`;
  } finally {
    button.classList.remove("loading");
    button.disabled = false;
  }
});

function openPlaceModal(card) {
  const place = card.dataset.place;
  placeImage.src = card.dataset.image;
  placeImage.alt = `${place} travel inspiration`;
  placeVibe.textContent = card.dataset.vibe;
  placeTitle.textContent = place;
  placeAbout.textContent = card.dataset.about;
  placeHighlights.innerHTML = card.dataset.highlights
    .split("|")
    .map((item) => `<span>${escapeHtml(item)}</span>`)
    .join("");
  planThisPlace.dataset.place = place;
  placeModal.classList.add("open");
  placeModal.setAttribute("aria-hidden", "false");
}

function closePlaceModal() {
  placeModal.classList.remove("open");
  placeModal.setAttribute("aria-hidden", "true");
}

destinationCards.forEach((card) => {
  card.addEventListener("click", () => openPlaceModal(card));
  card.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      openPlaceModal(card);
    }
  });
});

document.querySelectorAll("[data-close-modal]").forEach((control) => {
  control.addEventListener("click", closePlaceModal);
});

planThisPlace.addEventListener("click", () => {
  plannerForm.destination.value = planThisPlace.dataset.place;
  updateMap(planThisPlace.dataset.place);
  closePlaceModal();
  document.querySelector("#planner").scrollIntoView({ behavior: "smooth" });
  plannerForm.destination.focus({ preventScroll: true });
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closePlaceModal();
    closeChatPanel();
  }
});

currencySelect.addEventListener("change", updateBudgetPreview);
budgetAmount.addEventListener("input", updateBudgetPreview);
updateBudgetPreview();

themeToggle.addEventListener("click", toggleTheme);
setTheme(localStorage.getItem("wanderly-theme") || "light");

mapSearchButton.addEventListener("click", () => updateMap());
mapSearch.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    updateMap();
  }
});

document.querySelectorAll("[data-map-place]").forEach((button) => {
  button.addEventListener("click", () => updateMap(button.dataset.mapPlace));
});

document.querySelectorAll("[data-trending-place]").forEach((button) => {
  button.addEventListener("click", () => {
    plannerForm.destination.value = button.dataset.trendingPlace;
    updateMap(button.dataset.trendingPlace);
    document.querySelector("#planner").scrollIntoView({ behavior: "smooth" });
  });
});

function openChat() {
  if (!chatMessages.children.length) {
    addMessage("Welcome to Wanderly! I’m Tripzy, your travel buddy. Tell me a destination or ask about places, food, routes, packing, or your itinerary.", "bot");
  }
  chatPanel.classList.add("open");
  chatPanel.setAttribute("aria-hidden", "false");
  chatForm.message.focus();
}

function closeChatPanel() {
  chatPanel.classList.remove("open");
  chatPanel.setAttribute("aria-hidden", "true");
}

function addMessage(text, sender) {
  const message = document.createElement("div");
  message.className = `message ${sender}`;
  message.textContent = text;
  chatMessages.appendChild(message);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return message;
}

function addPlanFromChatButton(destination) {
  const wrapper = document.createElement("div");
  wrapper.className = "chat-cta";
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = "Plan from chat";
  button.addEventListener("click", () => {
    plannerForm.destination.value = destination;
    closeChatPanel();
    document.querySelector("#planner").scrollIntoView({ behavior: "smooth" });
    plannerForm.destination.focus({ preventScroll: true });
  });
  wrapper.appendChild(button);
  chatMessages.appendChild(wrapper);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatLauncher.addEventListener("click", openChat);
closeChat.addEventListener("click", closeChatPanel);

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const input = chatForm.message;
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";
  const thinking = addMessage("Tripzy is thinking...", "bot");

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Tripzy could not reply.");
    }
    thinking.textContent = data.reply;
    addPlanFromChatButton(text);
  } catch (error) {
    thinking.textContent = error.message;
  }
});

const observer = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    }
  },
  { threshold: 0.14 }
);

document.querySelectorAll(".reveal").forEach((element) => observer.observe(element));
