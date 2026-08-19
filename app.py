import importlib.util
import json
import os
import re
from pathlib import Path

from flask import Flask, jsonify, render_template, request, session
from groq import Groq


BASE_DIR = Path(__file__).resolve().parent
CHATBOT_PATH = Path(
    os.getenv("CHATBOT_MODULE_PATH", r"C:\Users\anjan\SAMSUNG\name.ai\chatbot.py")
)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "travel-planner-dev-secret")


PLACE_IMAGES = {
    "agra": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=1200&q=80",
    "bali": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1200&q=80",
    "bangkok": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?auto=format&fit=crop&w=1200&q=80",
    "delhi": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=1200&q=80",
    "dubai": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1200&q=80",
    "goa": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1200&q=80",
    "jaipur": "https://images.unsplash.com/photo-1603262110263-fb0112e7cc33?auto=format&fit=crop&w=1200&q=80",
    "kerala": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80",
    "kyoto": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=1200&q=80",
    "london": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=1200&q=80",
    "maldives": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=1200&q=80",
    "mumbai": "https://images.unsplash.com/photo-1529253355930-ddbe423a2ac7?auto=format&fit=crop&w=1200&q=80",
    "new york": "https://images.unsplash.com/photo-1485871981521-5b1fd3805eee?auto=format&fit=crop&w=1200&q=80",
    "paris": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1200&q=80",
    "rome": "https://images.unsplash.com/photo-1529260830199-42c24126f198?auto=format&fit=crop&w=1200&q=80",
    "santorini": "https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=1200&q=80",
    "singapore": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=1200&q=80",
    "switzerland": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=1200&q=80",
    "tokyo": "https://images.unsplash.com/photo-1528164344705-47542687000d?auto=format&fit=crop&w=1200&q=80",
}

DEFAULT_PLACE_IMAGE = (
    "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=1200&q=80"
)

DESTINATION_ATTRACTIONS = {
    "agra": ["Taj Mahal", "Agra Fort", "Mehtab Bagh", "Itmad-ud-Daulah"],
    "bali": ["Ubud rice terraces", "Uluwatu Temple", "Tanah Lot", "Tegenungan Waterfall"],
    "bangkok": ["Grand Palace Bangkok", "Wat Arun", "Wat Pho", "Chatuchak Market"],
    "delhi": ["India Gate Delhi", "Red Fort Delhi", "Qutub Minar", "Humayun's Tomb"],
    "dubai": ["Burj Khalifa", "Dubai Marina", "Desert Safari Dubai", "Museum of the Future"],
    "goa": ["Basilica of Bom Jesus Goa", "Fort Aguada Goa", "Baga Beach Goa", "Fontainhas Goa"],
    "jaipur": ["Hawa Mahal", "Amber Fort Jaipur", "City Palace Jaipur", "Jantar Mantar Jaipur"],
    "japan": ["Fushimi Inari Kyoto", "Kiyomizu-dera Kyoto", "Arashiyama Bamboo Grove", "Gion Kyoto"],
    "kashmir": ["Dal Lake Srinagar", "Gulmarg Gondola", "Pahalgam Valley", "Mughal Gardens Srinagar"],
    "kerala": ["Alleppey Backwaters", "Munnar Tea Gardens", "Fort Kochi", "Varkala Cliff"],
    "kyoto": ["Fushimi Inari Shrine", "Kiyomizu-dera Temple", "Arashiyama Bamboo Grove", "Gion Kyoto"],
    "ladakh": ["Pangong Lake", "Thiksey Monastery", "Nubra Valley", "Khardung La"],
    "london": ["Tower Bridge London", "Big Ben London", "British Museum", "Buckingham Palace"],
    "maldives": ["Male Maldives", "Maafushi Island", "Banana Reef Maldives", "Vaadhoo Island"],
    "manali": ["Solang Valley", "Hadimba Devi Temple", "Rohtang Pass", "Old Manali"],
    "mumbai": ["Gateway of India Mumbai", "Marine Drive Mumbai", "Elephanta Caves", "Chhatrapati Shivaji Terminus"],
    "new york": ["Statue of Liberty", "Central Park New York", "Times Square", "Brooklyn Bridge"],
    "paris": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Paris", "Montmartre Paris"],
    "rome": ["Colosseum Rome", "Trevi Fountain", "Roman Forum", "Pantheon Rome"],
    "santorini": ["Oia Santorini", "Santorini Caldera", "Red Beach Santorini", "Fira Santorini"],
    "singapore": ["Marina Bay Sands", "Gardens by the Bay", "Sentosa Island", "Jewel Changi Airport"],
    "switzerland": ["Matterhorn Zermatt", "Lake Lucerne", "Jungfraujoch", "Interlaken Switzerland"],
    "tokyo": ["Senso-ji Temple Tokyo", "Shibuya Crossing", "Tokyo Skytree", "Meiji Shrine Tokyo"],
}

IMAGE_POOLS = {
    "agra": [
        "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1585135497273-1a86b09fe70e?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=900&q=80",
    ],
    "bali": [
        "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1555400038-63f5ba517a47?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1604999333679-b86d54738315?auto=format&fit=crop&w=900&q=80",
    ],
    "dubai": [
        "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1518684079-3c830dcef090?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1512632578888-169bbbc64f33?auto=format&fit=crop&w=900&q=80",
    ],
    "goa": [
        "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1519046904884-53103b34b206?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1520942702018-0862200e6873?auto=format&fit=crop&w=900&q=80",
    ],
    "jaipur": [
        "https://images.unsplash.com/photo-1603262110263-fb0112e7cc33?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1477587458883-47145ed94245?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1598091383021-15ddea10925d?auto=format&fit=crop&w=900&q=80",
    ],
    "kerala": [
        "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1593693397690-362cb9666fc2?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=900&q=80",
    ],
    "kyoto": [
        "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1528164344705-47542687000d?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1545569341-9eb8b30979d9?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1526481280693-3bfa7568e0f3?auto=format&fit=crop&w=900&q=80",
    ],
    "japan": [
        "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1528164344705-47542687000d?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1545569341-9eb8b30979d9?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1526481280693-3bfa7568e0f3?auto=format&fit=crop&w=900&q=80",
    ],
    "paris": [
        "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1499856871958-5b9627545d1a?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1522093007474-d86e9bf7ba6f?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1431274172761-fca41d930114?auto=format&fit=crop&w=900&q=80",
    ],
    "tokyo": [
        "https://images.unsplash.com/photo-1528164344705-47542687000d?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1532236204992-f5e85c024202?auto=format&fit=crop&w=900&q=80",
    ],
}

GENERIC_IMAGE_POOL = [
    "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=900&q=80",
]


def place_image(destination):
    lowered = destination.lower()
    for key, image in PLACE_IMAGES.items():
        if key in lowered:
            return image
    return GENERIC_IMAGE_POOL[0]


def destination_key(destination):
    lowered = destination.lower()
    for key in DESTINATION_ATTRACTIONS:
        if key in lowered:
            return key
    return ""


def image_pool_for(destination):
    key = destination_key(destination)
    if key in IMAGE_POOLS:
        return IMAGE_POOLS[key]
    return GENERIC_IMAGE_POOL


def attraction_names_for(destination):
    key = destination_key(destination)
    if key:
        return DESTINATION_ATTRACTIONS[key]
    return [
        f"{destination} landmark",
        f"{destination} old town",
        f"{destination} local market",
        f"{destination} viewpoint",
    ]


def attraction_image_for(destination, name, index):
    pool = image_pool_for(destination)
    return pool[index % len(pool)]


def normalized_attraction_name(destination, name, index):
    curated_names = attraction_names_for(destination)
    fallback = curated_names[index % len(curated_names)]
    cleaned = (name or "").strip()
    lowered = cleaned.lower()
    generic_names = {
        "iconic landmark",
        "historic district",
        "local market",
        "scenic viewpoint",
        "famous landmark",
        "old town",
        "main attraction",
        "top attraction",
        "landmark",
    }

    if not cleaned or lowered in generic_names:
        return fallback
    if "taj mahal" in lowered and "agra" not in destination.lower():
        return fallback
    return cleaned


def section_images_for(destination):
    pool = image_pool_for(destination)
    return {
        "overview": pool[0],
        "best_time": pool[1 % len(pool)],
        "itinerary": pool[2 % len(pool)],
        "attractions": pool[3 % len(pool)],
        "food": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=900&q=80",
        "transport": "https://images.unsplash.com/photo-1474487548417-781cb71495f3?auto=format&fit=crop&w=900&q=80",
        "accommodation": "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=900&q=80",
        "budget": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=900&q=80",
        "packing": "https://images.unsplash.com/photo-1553531384-cc64ac80f931?auto=format&fit=crop&w=900&q=80",
        "safety": pool[0],
    }


def normalize_plan(plan, destination):
    plan.setdefault("destination_image", place_image(destination))
    if not plan.get("destination_image"):
        plan["destination_image"] = place_image(destination)
    plan["section_images"] = section_images_for(destination)
    plan.setdefault("map_query", destination)

    key = destination_key(destination)
    attractions = plan.get("attractions")
    if key:
        source_attractions = attractions if isinstance(attractions, list) else []
        curated_attractions = []
        for index, name in enumerate(attraction_names_for(destination)[:4]):
            source = source_attractions[index] if index < len(source_attractions) else {}
            why = source.get("why") if isinstance(source, dict) else ""
            curated_attractions.append(
                {
                    "name": name,
                    "why": why or "A destination-specific highlight for photos, culture, and local flavor.",
                }
            )
        attractions = curated_attractions
    elif not isinstance(attractions, list) or not attractions:
        attractions = attraction_names_for(destination)

    if isinstance(attractions, list):
        normalized_attractions = []
        for index, attraction in enumerate(attractions):
            if isinstance(attraction, str):
                name = normalized_attraction_name(destination, attraction, index)
                image = attraction_image_for(destination, name, index)
                normalized_attractions.append(
                    {"name": name, "why": "A worthwhile stop for photos, context, and local flavor.", "image": image}
                )
            else:
                attraction["name"] = normalized_attraction_name(destination, attraction.get("name"), index)
                attraction.setdefault("why", "A worthwhile stop for photos, context, and local flavor.")
                attraction["image"] = attraction_image_for(destination, attraction.get("name"), index)
                normalized_attractions.append(attraction)
        fallback_names = attraction_names_for(destination)
        while len(normalized_attractions) < 4:
            index = len(normalized_attractions)
            name = fallback_names[index % len(fallback_names)]
            normalized_attractions.append(
                {
                    "name": name,
                    "why": "A destination-specific highlight for photos, culture, and local flavor.",
                    "image": attraction_image_for(destination, name, index),
                }
            )
        plan["attractions"] = normalized_attractions

    if not isinstance(plan.get("transport"), list) or len(plan.get("transport", [])) < 3:
        plan["transport"] = demo_itinerary(destination, 3, "Mid-range", 0, "INR", 2, "Culture")["transport"]

    if not isinstance(plan.get("accommodation"), list) or len(plan.get("accommodation", [])) < 3:
        plan["accommodation"] = demo_itinerary(destination, 3, "Mid-range", 0, "INR", 2, "Culture")["accommodation"]

    return plan


def clean_overview_from_raw(raw_text, destination, days, style):
    match = re.search(r'"overview"\s*:\s*"((?:\\.|[^"\\])*)"', raw_text, re.DOTALL)
    if match:
        try:
            return json.loads(f'"{match.group(1)}"')
        except json.JSONDecodeError:
            return match.group(1).replace('\\"', '"')

    if raw_text.lstrip().startswith(("{", "[")):
        return (
            f"Here is a polished {days}-day {style.lower()} plan for {destination}. "
            "The details are organized below into itinerary, attractions, food, transport, stay, budget, packing, and safety cards."
        )

    return raw_text.strip() or f"A personalized {days}-day {style.lower()} escape to {destination}."


def load_existing_chatbot():
    """Load the user's existing chatbot module without changing its code."""
    if not CHATBOT_PATH.exists():
        return None

    spec = importlib.util.spec_from_file_location("existing_chatbot", CHATBOT_PATH)
    if spec is None or spec.loader is None:
        return None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


existing_chatbot = load_existing_chatbot()


def get_groq_client():
    if existing_chatbot is not None and hasattr(existing_chatbot, "client"):
        return existing_chatbot.client

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)


def get_model():
    if existing_chatbot is not None and hasattr(existing_chatbot, "model"):
        return existing_chatbot.model
    return os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


def demo_itinerary(destination, days, budget, budget_amount, currency, travellers, style):
    budget_note = budget.lower()
    if budget_amount:
        budget_note = f"{budget_note} budget around {currency} {budget_amount:,.0f}"
    attraction_names = attraction_names_for(destination)

    return {
        "overview": f"A balanced {days}-day {style.lower()} escape to {destination} for {travellers} traveller(s), tuned for a {budget_note}.",
        "destination_image": place_image(destination),
        "section_images": section_images_for(destination),
        "best_time": "Aim for shoulder season when flights are calmer, queues are shorter, and hotels usually price more kindly.",
        "itinerary": [
            {
                "day": f"Day {day}",
                "title": title,
                "morning": "Start early with a landmark visit and a relaxed local breakfast.",
                "afternoon": "Explore a walkable neighborhood, museum, market, or scenic viewpoint.",
                "evening": "Choose a memorable dinner spot and take a gentle sunset stroll.",
            }
            for day, title in enumerate(
                [
                    "Arrival and first impressions",
                    "Culture, views, and local flavor",
                    "Hidden corners and signature experiences",
                    "Slow travel and souvenir hunting",
                    "Departure with one last highlight",
                ][: int(days)],
                start=1,
            )
        ],
        "attractions": [
            {
                "name": name,
                "why": "A destination-specific highlight for photos, culture, and local flavor.",
                "image": attraction_image_for(destination, name, index),
            }
            for index, name in enumerate(attraction_names[:4])
        ],
        "food": ["Regional street food", "Family-run cafe", "Signature dessert", "Rooftop dinner"],
        "transport": [
            {"mode": "Airport transfer", "details": "Pre-book for late arrivals or first-time visitors."},
            {"mode": "Public transport", "details": "Use metros, buses, or local rail for predictable daily movement."},
            {"mode": "Walking zones", "details": "Cluster attractions by neighborhood to reduce ride time."},
            {"mode": "Ride apps/taxis", "details": "Best for evenings, luggage days, or family travel."},
        ],
        "accommodation": [
            {
                "type": "Central comfort stay",
                "details": "Pick a hotel near transit, safe evening streets, and breakfast options.",
                "link": "https://www.booking.com/",
            },
            {
                "type": "Apartment stay",
                "details": "Good for families, longer trips, laundry, and light cooking.",
                "link": "https://www.airbnb.com/",
            },
            {
                "type": "Premium hotel",
                "details": "Use this when convenience, concierge support, and amenities matter most.",
                "link": "https://www.expedia.com/Hotels",
            },
        ],
        "budget": f"For a {budget_note}, reserve the biggest share for stay and transport, then keep a flexible daily food/activity allowance.",
        "packing": ["Comfortable shoes", "Weather layer", "Reusable bottle", "Power bank", "Day bag"],
        "safety": ["Keep offline maps", "Use licensed transport", "Store backup documents", "Share plans with someone trusted"],
    }


def parse_itinerary(raw_text, destination, days, budget, budget_amount, currency, travellers, style):
    plan = None
    try:
        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1
        if start >= 0 and end > start:
            plan = json.loads(raw_text[start:end])
    except json.JSONDecodeError:
        pass

    if plan is None:
        plan = demo_itinerary(destination, days, budget, budget_amount, currency, travellers, style)
        plan["overview"] = clean_overview_from_raw(raw_text, destination, days, style)

    return normalize_plan(plan, destination)


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/api/plan")
def plan_trip():
    data = request.get_json(silent=True) or {}
    destination = data.get("destination", "").strip()
    days = int(data.get("days") or 3)
    budget = data.get("budget", "Mid-range").strip()
    budget_amount = float(data.get("budget_amount") or 0)
    currency = data.get("currency", "INR").strip()
    travellers = int(data.get("travellers") or 1)
    style = data.get("style", "Culture").strip()

    if not destination:
        return jsonify({"error": "Please enter a destination."}), 400

    client = get_groq_client()
    if client is None:
        return jsonify(
            {
                "source": "demo",
                "plan": demo_itinerary(destination, days, budget, budget_amount, currency, travellers, style),
            }
        )

    prompt = f"""
Create a polished travel itinerary as strict JSON for:
Destination: {destination}
Days: {days}
Budget: {budget}
Specific budget amount: {currency} {budget_amount:,.0f}
Travellers: {travellers}
Travel style: {style}

Return exactly this JSON shape:
{{
  "overview": "short inspiring summary",
  "destination_image": "a direct https image URL if you know a suitable real destination/landmark image, otherwise empty string",
  "best_time": "best months/seasons and why",
  "itinerary": [
    {{"day": "Day 1", "title": "theme", "morning": "...", "afternoon": "...", "evening": "..."}}
  ],
  "attractions": [
    {{"name": "real attraction name", "why": "why it is worth visiting", "image": "direct https image URL if known, otherwise empty string"}}
  ],
  "food": ["..."],
  "transport": [
    {{"mode": "flight/train/metro/bus/taxi/walking/etc", "details": "specific beginner-friendly advice, passes, timings, apps, stations, or areas"}}
  ],
  "accommodation": [
    {{"type": "hotel/hostel/resort/apartment/area", "details": "who it suits and where to stay", "link": "official booking or hotel/tourism website if known, otherwise empty string"}}
  ],
  "budget": "include a practical cost breakdown and mention the entered budget amount",
  "packing": ["..."],
  "safety": ["..."]
}}
Keep it practical, beginner-friendly, destination-specific, and detailed for accommodation and transport.
"""

    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {
                "role": "system",
                "content": "You are a professional travel planner. Return clean JSON only.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=2600,
        temperature=0.75,
    )
    raw_text = response.choices[0].message.content

    return jsonify(
        {
            "source": "groq",
            "plan": parse_itinerary(
                raw_text, destination, days, budget, budget_amount, currency, travellers, style
            ),
        }
    )


@app.post("/api/chat")
def chat_with_trekki():
    data = request.get_json(silent=True) or {}
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"error": "Message cannot be empty."}), 400

    client = get_groq_client()
    if client is None:
        return jsonify(
            {
                "reply": "I need a Groq API key before I can chat live. Try adding GROQ_API_KEY or keeping your chatbot.py path available.",
                "history": session.get("chat_history", []),
            }
        )

    conversation_history = session.get("chat_history", [])
    conversation_history.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model=get_model(),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Tripzy, a friendly travel assistant inside Wanderly. "
                        "Give detailed, practical place information when relevant: best areas, "
                        "highlights, food, transport, safety, budget, accommodation, and useful tips. "
                        "Keep it beginner-friendly and organized. End travel-related answers with: "
                        'Ready to turn this into a day-by-day plan? Tap "Plan from chat".'
                    ),
                },
                *conversation_history,
            ],
            max_tokens=650,
            temperature=0.7,
        )
        ai_output = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": ai_output})
        session["chat_history"] = conversation_history[-20:]
        return jsonify({"reply": ai_output, "history": session["chat_history"]})
    except Exception as exc:
        return jsonify({"error": f"Sorry, I encountered an error: {str(exc)}"}), 500


@app.post("/api/chat/reset")
def reset_chat():
    session["chat_history"] = []
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True)
