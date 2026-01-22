



from flask import Flask, render_template_string, request, redirect, url_for, session , render_template 
from datetime import datetime
import time

all_orders = []


# --- ADD THIS AFTER YOUR IMPORTS ---
from functools import wraps


app = Flask(__name__)
app.secret_key = "change_me_for_production"

app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_PERMANENT=False  # This tells the browser to delete the cookie on close
)



bracelets = [
    {
        "name": "Tiger Eye Power",
        "image": "images/tiger_eye.jpg",
        "price": 299,
        "description": "Tiger Eye is known for strength, protection, and boosting confidence.",
        "benefits": [
            "Strengthens willpower",
            "Enhances courage and focus",
            "Protects against negativity",
        ],
    },
    {
        "name": "Howlite Calm",
        "image": "images/howlite.jpg",
        "price": 349,
        "description": "Howlite brings calm, patience, and emotional control to your life.",
        "benefits": [
            "Reduces stress and anger",
            "Promotes restful sleep",
            "Improves communication",
        ],
    },
    {
        "name": "Green Aventurine Wealth",
        "image": "images/green_aventurine.jpg",
        "price": 299,
        "description": "Green Aventurine attracts abundance, luck, and prosperity.",
        "benefits": [
            "Attracts money and opportunities",
            "Promotes emotional healing",
            "Encourages optimism and personal growth",
        ],
    },
    {
        "name": "Amethyst Royal",
        "image": "images/amethyst.jpg",
        "price": 499,
        "description": "Amethyst enhances spiritual awareness and balances emotions.",
        "benefits": [
            "Enhances intuition",
            "Reduces anxiety",
            "Supports meditation and spiritual growth",
        ],
    },
    {
        "name": "Rose Quartz Love",
        "image": "images/rose_quartz.jpg",
        "price": 399,
        "description": "Rose Quartz opens your heart to love, compassion, and confidence.",
        "benefits": [
            "Promotes self-love",
            "Soothes heartbreak",
            "Encourages healthy relationships",
        ],
    },
    {
        "name": "Lapis Lazuli Wisdom",
        "image": "images/lapis_lazuli.jpg",
        "price": 599,
        "description": "Lapis Lazuli improves wisdom, intellect, and creativity.",
        "benefits": [
            "Enhances intuition",
            "Supports mental clarity",
            "Boosts self-expression",
        ],
    },
    {
        "name": "Black Onyx Shield",
        "image": "images/black_onyx.jpg",
        "price": 299,
        "description": "Black Onyx shields against negativity and relieves stress.",
        "benefits": [
            "Strong protection from bad energy",
            "Promotes grounding",
            "Reduces anxiety and fears",
        ],
    },
    {
        "name": "Lava Stone Energy",
        "image": "images/lava_stone.jpg",
        "price": 199,
        "description": "Lava Stone brings grounding energy and is perfect for diffuser bracelets.",
        "benefits": [
            "Natural energy balance",
            "Perfect for essential oils",
            "Promotes strength and courage",
        ],
    },
    {
        "name": "Citrine Success",
        "image": "images/citrine.jpg",
        "price": 799,
        "description": "Citrine is the stone of wealth, success, and positivity.",
        "benefits": [
            "Attracts prosperity",
            "Boosts self-confidence",
            "Clears negative energy",
        ],
    },
    {
        "name": "Blue Apatite Motivation",
        "image": "images/blue_apatite.jpg",
        "price": 799,
        "description": "Blue Apatite enhances motivation and creativity for daily challenges.",
        "benefits": [
            "Boosts inspiration",
            "Improves focus",
            "Clears confusion",
        ],
    },
    {
        "name": "Sunstone Joy",
        "image": "images/sunstone.jpg",
        "price": 599,
        "description": "Sunstone brings joy, leadership, and energy to your life.",
        "benefits": [
            "Encourages positivity",
            "Supports leadership",
            "Boosts vitality",
        ],
    },
    {
        "name": "Red Jasper Vitality",
        "image": "images/red_jasper.jpg",
        "price": 399,
        "description": "Red Jasper increases stamina, balance, and courage.",
        "benefits": [
            "Promotes endurance",
            "Enhances determination",
            "Stabilizes emotions",
        ],
    },

    # New bracelets to add:
    {
        "name": "Chalcedony Bracelet",
        "image": "images/chalcedony.jpg",
        "price": 299,
        "description": "Chalcedony promotes harmony, amplifies love, and calms emotions.",
        "benefits": [
            "Promotes harmony",
            "Amplifies feelings of love",
            "Calms emotions",
        ],
    },
    {
        "name": "Orange Quartz Bracelet",
        "image": "images/orange_quartz.jpg",
        "price": 299,
        "description": "Orange Quartz energizes creativity and enhances joy and vitality.",
        "benefits": [
            "Energizes creativity",
            "Enhances joy and vitality",
            "Releases fear",
        ],
    },
    {
        "name": "Pink Rhodonite Bracelet",
        "image": "images/pink_rhodonite.jpg",
        "price": 599,
        "description": "Pink Rhodonite encourages emotional healing and promotes compassion.",
        "benefits": [
            "Encourages emotional healing",
            "Promotes compassion",
            "Clears emotional wounds",
        ],
    },
    {
        "name": "Hematite Bracelet",
        "image": "images/hematite.jpg",
        "price": 279,
        "description": "Hematite grounds energy, absorbs negativity, and enhances focus.",
        "benefits": [
            "Grounds energy",
            "Absorbs negativity",
            "Enhances focus",
        ],
    },
    {
        "name": "Sodalite Bracelet",
        "image": "images/sodalite.jpg",
        "price": 299,
        "description": "Sodalite promotes rational thought and enhances communication.",
        "benefits": [
            "Promotes rational thought",
            "Enhances communication",
            "Calms mind",
        ],
    },
    {
        "name": "Rudraksha Bracelet",
        "image": "images/rudraksha.jpg",
        "price": 379,
        "description": "Rudraksha reduces stress, increases serenity, and offers spiritual protection.",
        "benefits": [
            "Reduces stress",
            "Increases serenity",
            "Spiritual protection",
        ],
    },
    {
        "name": "Garnet Bracelet",
        "image": "images/garnet.jpg",
        "price": 599,
        "description": "Garnet boosts energy, courage, and stimulates metabolism.",
        "benefits": [
            "Boosts energy and passion",
            "Enhances courage",
            "Stimulates metabolism",
        ],
    },
    {
        "name": "Labradorite Bracelet",
        "image": "images/labradorite.jpg",
        "price": 769,
        "description": "Labradorite protects aura, increases intuition, and relieves anxiety.",
        "benefits": [
            "Protects aura",
            "Increases intuition",
            "Relieves anxiety",
        ],
    },
    {
        "name": "Amazonite Bracelet",
        "image": "images/amazonite.jpg",
        "price": 599,
        "description": "Amazonite soothes emotional trauma and enhances creativity.",
        "benefits": [
            "Soothes emotional trauma",
            "Calms nervous system",
            "Enhances creativity",
        ],
    },
    {
        "name": "Turquoise Bracelet",
        "image": "images/turquoise.jpg",
        "price": 399,
        "description": "Turquoise promotes communication and offers protection against negativity.",
        "benefits": [
            "Heals emotional wounds",
            "Promotes communication",
            "Protects against negative energy",
        ],
    },
    {
        "name": "Pyrite Bracelet",
        "image": "images/pyrite.jpg",
        "price": 599,
        "description": "Pyrite attracts wealth, shields from negativity, and boosts confidence.",
        "benefits": [
            "Attracts wealth",
            "Shields from negativity",
            "Boosts confidence",
        ],
    },
    {
        "name": "White Agate",
        "image": "images/White_Agate.jpg",
        "price": 399,
        "description": "White Agate has calming energy and protects from negative influences.",
        "benefits": [
            "Calms anger and anxiety",
            "Boosts happiness and focus",
            "Protects against nightmares",
            "Enhances emotional healing",
        ],
    },
    {
        "name": "Picture Jasper",
        "image": "images/picture_jasper.jpg",
        "price": 399,
        "description": "Picture Jasper nurtures and grounds you, helping clear negative energy.",
        "benefits": [
            "Clears toxins and electromagnetic smog",
            "Enhances creativity",
            "Provides grounding and stability",
            "Aids spiritual healing",
        ],
    },
    {
        "name": "Chakra Bracelet",
        "image": "images/chakra.jpg",
        "price": 599,
        "description": "Chakra Bracelet aligns and balances all 7 chakras for vitality and clarity.",
        "benefits": [
            "Balances energy flow",
            "Boosts vitality and focus",
            "Emotional healing and inner peace",
            "Strengthens spiritual connection",
        ],
    },
    {
        "name": "Black Tiger Eye",
        "image": "images/black_tiger_eye.jpg",
        "price": 499,
        "description": "Black Tiger Eye protects and boosts energy with mental clarity.",
        "benefits": [
            "Blocks negative energy",
            "Enhances intuition and confidence",
            "Strengthens immune and reproductive systems",
            "Improves courage and focus",
        ],
    },
    {
        "name": "Purple Amethyst",
        "image": "images/purple_amethyst.jpg",
        "price": 599,
        "description": "Purple Amethyst reduces stress and aids meditation and spiritual growth.",
        "benefits": [
            "Relieves anxiety and tension",
            "Promotes restful sleep",
            "Enhances intuition and spiritual awareness",
            "Balances hormonal and metabolic functions",
        ],
    },
    {
        "name": "Crystal",
        "image": "images/crystal.jpg",
        "price": 649,
        "description": "Crystal bracelets help clear thoughts and promote calmness and healing.",
        "benefits": [
            "Clears negative energy",
            "Promotes mental clarity",
            "Supports emotional balance",
            "Boosts healing and vitality",
        ],
    },
    {
        "name": "Obsidian",
        "image": "images/obsidian.jpg",
        "price": 399,
        "description": "Obsidian provides grounding, protection, and helps explore inner self.",
        "benefits": [
            "Absorbs negative energy",
            "Calms stress and tension",
            "Helps with chakra cleansing",
            "Encourages self-reflection",
        ],
    },
    {
        "name": "Dark Green Aventurine",
        "image": "images/dark_green_aventurine.jpg",
        "price": 579,
        "description": "Dark Green Aventurine attracts prosperity and promotes emotional healing.",
        "benefits": [
            "Attracts wealth and luck",
            "Promotes optimism and growth",
            "Improves emotional well-being",
            "Supports physical healing",
        ],
    }
]



message_html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Messages | Admin</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body style="background: #faf9f7; padding: 20px;">
    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2>✉️ Customer Messages</h2>
            <a href="/admin/dashboard" class="btn btn-outline-secondary">← Back to Dashboard</a>
        </div>
        <table class="table table-bordered bg-white">
            <thead class="table-dark">
                <tr><th>Name</th><th>Email</th><th>Message</th><th>Date</th></tr>
            </thead>
            <tbody>
                {% for msg in messages %}
                <tr>
                    <td>{{ msg[1] }}</td>
                    <td>{{ msg[2] }}</td>
                    <td>{{ msg[3] }}</td>
                    <td>{{ msg[4] }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
'''

# --- STEP 1: DEFINE THE ADMIN DESIGN (TOP OF FILE) ---
admin_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Admin Dashboard | Treasures Jewels</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f7f6; padding: 40px; }
        .admin-card { background: white; border-radius: 15px; padding: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
        .table thead { background-color: #3a491d; color: white; }
        .badge-paid { background-color: #d1e7dd; color: #0f5132; }
    </style>
</head>
<body>
    <div class="admin-card">
       <div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="mb-0">💎 Treasures Jewels Admin</h2>
    <a href="/admin/logout" class="btn btn-danger">Logout</a>
</div>

  <div class="mb-3">
    <a href="/admin/orders" class="btn btn-sm btn-secondary text-white">View Orders</a>
</div>

     <table class="table table-bordered table-hover">
    <thead class="table-dark">
        <tr>
            <th>ID</th><th>Name</th><th>Phone</th><th>Address</th><th>Total</th><th>Status</th>
        </tr>
    </thead>
    <tbody>
        {% for order in orders %}
        <tr>
            <td>#{{ order.id }}</td>
            <td>{{ order.name }}</td>
            <td>{{ order.phone }}</td>
            <td>{{ order.address }}</td>
            <td>₹{{ order.total }}</td>
            <td>
                {% if order.status == 'Shipped' %}
                    <span class="badge bg-success">Shipped</span>
                {% else %}
                    <span class="badge bg-warning text-dark">Pending</span>
                    <a href="/mark_shipped/{{ order.id }}" class="btn btn-sm btn-primary ms-2">Mark Shipped</a>
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>  
    </div>
</body>
</html>
'''


html_template = '''
 <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Treasures Jewels</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"/>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet"/>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet"/>
    <style>
      /* Your existing styles */
      html { scroll-behavior: smooth; }
      body { background-color: #faf9f7; font-family: 'Playfair Display', serif; }
      .navbar { background: #fffbe7 !important; }
      .navbar-brand { font-weight: 700; font-size: 2.4rem; color: #1d473a !important; font-family: 'Playfair Display', serif !important; }
      .nav-link { color: #402323 !important; font-weight: 600; font-family: 'Playfair Display', serif; }
      .header-section { padding: 80px 0; background: linear-gradient(135deg,#ccffdd 0%,#f8dbda 100%); text-align: center; }
      .header-section h1 { font-weight: 900; font-size: 3rem; margin-bottom: 18px; color: #231942; font-family: 'Playfair Display', serif; }
      .header-section p { font-size: 1.4rem; color: #444; font-family: 'Playfair Display', serif; }
      .bracelet-card { border-radius: 22px; box-shadow: 0 10px 32px rgba(50,70,90,0.08); background: #fff; transition: box-shadow 0.2s, transform 0.2s; height: 100%; }
      .bracelet-card:hover { box-shadow: 0 20px 44px rgba(50,70,90,0.18); transform: scale(1.05); }
      .bracelet-img { width: 100%; height: 240px; object-fit: cover; border-top-left-radius: 22px; border-top-right-radius: 22px;}
      .card-body { padding: 1.7rem; }
      .card-title { color: #1d473a; font-weight: 700; font-size: 1.48rem; margin-bottom: 5px; font-family: 'Playfair Display', serif; }
      .bracelet-price { font-weight: 700; color: #c53211; font-size: 1.22rem; margin-bottom: 7px; font-family: 'Playfair Display', serif; }
      .benefits-list { list-style: none; padding: 0; margin-bottom: 0; color: #555; font-family: 'Playfair Display', serif; }
      .benefits-list li { position: relative; margin-bottom: 8px; padding-left: 22px; }
      .benefits-list li::before { content: "\\2713"; position: absolute; left: 0; color: #1d473a; font-weight: bold; }
      .about-section, .contact-section { background: #eef4f3; padding: 60px 0; margin: 60px 0 0 0 }
      .section-title { color: #1d473a; font-weight: 700; margin-bottom: 2.2rem; font-family: 'Playfair Display', serif; }
      footer { background: #19191b; color: #dccca3; padding: 32px 0; text-align: center; margin-top: 60px; font-size: 1.25rem; font-family: 'Playfair Display', serif;}
      .contact-section input, .contact-section textarea {
          border: 1.5px solid #64a8e3;
          border-radius: 9px;
          margin-bottom: 18px;
          padding: 10px;
          width: 100%;
          max-width: 540px;
          font-family: 'Playfair Display', serif;
          font-size: 1.05rem;
      }
      .contact-section button {
          background: #1d473a;
          color: #fff;
          font-weight: 700;
          padding: 10px 34px;
          border-radius: 10px;
          border: none;
          font-family: 'Playfair Display', serif;
          font-size: 1.1rem;
      }

      /* Enhanced loading animation styles */
      .loading-overlay {
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        background: linear-gradient(120deg,#eafafc 0%,#fef7e0 50%,#e8f5f0 100%);
        background-size: 200% 200%;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        opacity: 1;
        animation: bgMove 4s alternate infinite;
        transition: opacity 1s ease, transform 1s cubic-bezier(.74,.18,.18,.99);
      }
      @keyframes bgMove {
        0% {background-position: 0 0;}
        100% {background-position: 130% 130%;}
      }
      .loading-overlay.hidden {
        opacity: 0;
        pointer-events: none;
        transform: scale(0.85);
      }
      .loading-center {
        text-align:center;
        position: relative;
      }
      .gem-wrapper {
        position:relative;
        display:inline-block;
        font-size: 7rem;
        padding: 16px;
        animation: bob 2.6s infinite cubic-bezier(.4,1.8,.4,.9), pulse 2.4s infinite;
      }
      @keyframes bob {
        0%,100% { transform:translateY(0);}
        30% { transform:translateY(-11px);}
        60% { transform:translateY(7px);}
      }
      @keyframes pulse {
        0%,100% { transform: scale(1);}
        50% { transform: scale(1.12);}
      }
      .gem-wrapper svg {
        display: block;
        margin: 0 auto;
        animation: rotateGem 5s linear infinite;
        filter: drop-shadow(0 0 10px #ffd700a3);
        cursor: default;
        width: 120px;
        height: 120px;
      }
      @keyframes rotateGem {
        0% { transform: rotate(0deg);}
        100% { transform: rotate(480deg);}
      }
      .gem-shine {
        position:absolute;
        top:0; left:0; width:100%; height:100%;
        border-radius:50%;
        background: radial-gradient(circle at 40% 20%, #fff9a8cc 0%, transparent 60%);
        opacity:0.6;
        animation: shine 3s infinite;
        pointer-events:none;
      }
      @keyframes shine {
        0%,100% { opacity:0.3;}
        50% { opacity:0.65;}
      }
      .gem-sparkles {
        position:absolute;
        left:50%;
        top:58%;
        width:175px;
        height:175px;
        pointer-events:none;
        transform:translate(-50%,-50%);
        z-index:10;
      }
      .sparkle {
        position:absolute;
        width:22px; height:22px;
        background: radial-gradient(#fffbe7,#ffd70088,#fff0);
        border-radius:50%;
        opacity:0.7;
        animation: sparkle-move 1.9s infinite;
      }
      .sparkle1 { left:5px; top:7px; animation-delay:0s;}
      .sparkle2 { left:69px; top:15px; animation-delay:.7s;}
      .sparkle3 { left:38px; top:70px; animation-delay:.4s;}
      @keyframes sparkle-move {
        0%,100% { opacity:0.9; transform: scale(1);}
        50% { opacity:0.2; transform: scale(1.27);}
      }
      .loading-logo {
        font-size: 3.7rem;
        font-weight: 900;
        color: #ffd700;
        margin: 22px 0 10px 0;
        letter-spacing: 0.5px;
        font-family: 'Playfair Display', serif;
        background: linear-gradient(90deg,#ffe841,#fffde4,#ffd700 80%);
        background-size: 300px 100%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmerText 2.7s linear infinite, fadeInLogo 1.9s 0.5s both;
      }
      @keyframes shimmerText {
        0% { background-position: 0 0;}
        100% { background-position: 300px 0;}
      }
      @keyframes fadeInLogo {
        from { opacity: 0; transform: scaleY(0.7);}
        to { opacity: 1; transform: scaleY(1);}
      }
      .loading-text {
        font-size: 1.21rem;
        color: #816a21;
        margin-bottom: 17px;
        font-family: 'Playfair Display', serif;
        animation: fadeInText 2.2s 1s both;
      }
      @keyframes fadeInText {
        from { opacity: 0;}
        to { opacity: 1;}
      }
      .loading-dots {
        margin-top: 8px;
        font-family: 'Playfair Display', serif;
        font-size: 5rem;
        color: #cfc05b;
        letter-spacing: 0.17em;
      }
      .loading-dots span {
        opacity: 0.2;
        animation: blink 1.4s infinite;
        margin: 0 2px;
      }
      .loading-dots span:nth-child(2) {
        animation-delay: 0.3s;
      }
      .loading-dots span:nth-child(3) {
        animation-delay: 0.4s;
      }
      @keyframes blink {
        0%, 80%, 100% { opacity: 0.2; }
        40% { opacity: 0.97; }
      }
    </style>
</head>
<body>
    <!-- Loading Animation Overlay -->
    <div id="loading-overlay" class="loading-overlay">
      <div class="loading-center">
        <span class="gem-wrapper">
          <svg version="1.1" xmlns="http://www.w3.org/2000/svg" 
               viewBox="0 0 64 64" fill="none" stroke="#ffd700" stroke-width="1.3" stroke-linejoin="round" stroke-linecap="round">
            <defs>
              <radialGradient id="gemGradient" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#fffacd" stop-opacity="1"/>
                <stop offset="100%" stop-color="#ffcc00" stop-opacity="0.6"/>
              </radialGradient>
              <filter id="glow" x="-50%" y="-50%" width="200%" height="200%" >
                <feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="#ffe700" flood-opacity="0.8"/>
              </filter>
            </defs>
            <polygon points="10,2 54,2 62,20 54,58 10,58 2,20"
                     fill="url(#gemGradient)" filter="url(#glow)"/>
            <polygon points="10,2 31,30 54,2" fill="#ffe841" opacity="0.85"/>
            <polygon points="54,58 31,30 10,58" fill="#ffcc00" opacity="0.9"/>
            <polygon points="2,20 31,30 10,58" fill="#fffacd" opacity="0.7"/>
            <polygon points="31,30 62,20 54,58" fill="#fffacd" opacity="0.7"/>
          </svg>
          <span class="gem-shine"></span>
          <div class="gem-sparkles">
            <span class="sparkle sparkle1"></span>
            <span class="sparkle sparkle2"></span>
            <span class="sparkle sparkle3"></span>
          </div>
        </span>
        <div class="loading-logo">Treasures Jewels</div>
        <div class="loading-text">Loading your treasures...</div>
        <div class="loading-dots"><span>.</span><span>.</span><span>.</span></div>
      </div>
    </div>

     <!-- Rest of your existing HTML (complete as you provided) -->
    <nav class="navbar navbar-expand-lg shadow-sm">
      <div class="container">
        <a class="navbar-brand" href="{{ url_for('home') }}">
          <i class="bi bi-house-door"></i> Treasures Jewels
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item"><a class="nav-link" href="#home"><i class="bi bi-house"></i> Home</a></li>
            <li class="nav-item"><a class="nav-link" href="#collection"><i class="bi bi-gem"></i> Collection</a></li>
            <li class="nav-item"><a class="nav-link" href="#about"><i class="bi bi-person-heart"></i> About Us</a></li>
            <li class="nav-item"><a class="nav-link" href="#contact"><i class="bi bi-envelope-at"></i> Contact</a></li>
            <li class="nav-item"><a class="nav-link" href="{{ url_for('cart') }}"><i class="bi bi-cart"></i> Your Orders</a></li>
          </ul>
        </div>
      </div>
    </nav>

    <header class="header-section" id="home">
      <div class="container">
        <h1>Elevate Your Style with Authentic Treasures Jewels</h1>
        <p>Premium collections hand-crafted for healing, confidence, and abundance.</p>
      </div>
    </header>

    <section id="collection" class="container my-5">
      <h2 class="section-title text-center">Our Exclusive Gemstone Bracelets</h2>
      <div class="row g-4">
        {% for b in bracelets %}
        <div class="col-md-6 col-lg-4">
          <div class="card bracelet-card h-100">
            <img src="{{ url_for('static', filename=b.image) }}" class="bracelet-img" alt="{{ b.name }}">
            <div class="card-body">
              <h5 class="card-title">{{ b.name }}</h5>
              <div class="bracelet-price">&#x20B9; {{ b.price }}</div>
              <div class="card-text mb-2" style="font-size:1rem; color:#3e3e3e;">{{ b.description }}</div>
              <ul class="benefits-list">
                {% for ben in b.benefits %}
                <li>{{ ben }}</li>
                {% endfor %}
              </ul>
              <button type="button" class="btn btn-success mt-3 w-100" data-bs-toggle="modal" data-bs-target="#modal{{ loop.index }}">
                <i class="bi bi-cart-plus"></i> View & Add to Cart
              </button>
            </div>
          </div>
        </div>
        <div class="modal fade" id="modal{{ loop.index }}" tabindex="-1" aria-hidden="true">
          <div class="modal-dialog modal-lg modal-dialog-centered">
            <div class="modal-content" style="border-radius:2em; overflow:hidden;">
              <button type="button" class="btn-close position-absolute top-0 end-0 m-4" data-bs-dismiss="modal" aria-label="Close"></button>
              <div class="row g-0">
                <div class="col-md-6" style="background:#f7fafd;">
                  <img src="{{ url_for('static', filename=b.image) }}" class="img-fluid w-100" style="max-height:440px;object-fit:cover;" alt="{{ b.name }} image">
                </div>
                <div class="col-md-6 d-flex align-items-center">
                  <form class="modal-body w-100"
                        method="POST"
                        action="{{ url_for('add_to_cart') }}"
                        onsubmit="return updateHiddenFields({{ b.price }}, '{{ b.name }}', {{ loop.index }})">
                    <h4 class="mb-0">{{ b.name }}</h4>
                    <div class="text-secondary mb-2">&#x20B9; <span id="price{{ loop.index }}">{{ b.price }}</span></div>
                    <div class="mb-2">{{ b.description }}</div>
                    <div>
                      <label for="qty{{ loop.index }}" class="form-label">Quantity:</label>
                      <div class="input-group mb-3" style="max-width:200px;">
                        <button type="button" class="btn btn-outline-secondary" onclick="decreaseQty({{ loop.index }}, {{ b.price }})">-</button>
                        <input id="qty{{ loop.index }}" type="text" class="form-control text-center" value="1" readonly style="font-weight:600; font-size:1.1rem;">
                        <button type="button" class="btn btn-outline-secondary" onclick="increaseQty({{ loop.index }}, {{ b.price }})">+</button>
                      </div>
                      <input type="hidden" name="bracelet_name" id="bracename{{ loop.index }}" value="{{ b.name }}">
                      <input type="hidden" name="bracelet_price" id="braceprice{{ loop.index }}" value="{{ b.price }}">
                      <input type="hidden" name="quantity" id="qtyinput{{ loop.index }}" value="1">
                      <div><b>Total: ₹<span id="total{{ loop.index }}">{{ b.price }}</span></b></div>
                    </div>
                    <button type="submit" class="btn btn-success w-100 mt-3">Add to Cart</button>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
        {% endfor %}
      </div>
    </section>

    <section id="about" class="about-section">
      <div class="container text-center">
        <h2 class="section-title"><i class="bi bi-person-heart"></i> About Treasures Jewels</h2>
        <div class="row justify-content-center">
          <div class="col-lg-8">
            <p class="lead" style="color: #3d3d4f;">
              <b>Treasures Jewels</b> is your trusted source for authentic gemstone bracelets, handcrafted in Jaipur.<br><br>
              Our passion is to blend modern style with ancient tradition, bringing the energy of real, powerful stones to your everyday life. Every bracelet is thoughtfully strung, lovingly inspected, and ethically sourced.<br><br>
              <span style="font-weight:700;color:#1d473a;">Why choose us?</span><br>
              - 100% genuine gemstones<br>
              - Unique and meaningful designs<br>
              - Secure shopping and quick shipping across India<br>
              - Friendly, accessible support<br>
              - Easy returns & delightful experiences<br><br>
              Thank you for supporting a Jaipur-grown, customer-loved business. Wear your energy, every day!
            </p>
          </div>
        </div>
      </div>
    </section>

    <section id="contact" class="contact-section">
      <div class="container">
        <h2 class="section-title text-center"><i class="bi bi-envelope-at"></i> Contact Us</h2>
        <form class="mx-auto" style="max-width:540px;" method="POST" action="/contact">
  <input type="text" name="name" class="form-control" placeholder="Your Name*" required><br>
  <input type="email" name="email" class="form-control" placeholder="Your Email*" required><br>
  <textarea name="message" class="form-control" rows="4" placeholder="Message*" required></textarea><br>
  <button type="submit">Send Message</button>
     </form>
      </div>
    </section>

    <footer>
      &copy; 2025 Treasures Jewels. All rights reserved. Designed in Jaipur. <span style="font-size:1.2em;">💎</span>
    </footer>

   <script>
    // 1. Quantity and Form Functions
    function increaseQty(idx, price) {
      var qtyInput = document.getElementById('qty'+idx);
      var qty = parseInt(qtyInput.value);
      qtyInput.value = qty + 1;
      document.getElementById('total'+idx).innerText = (price * (qty + 1)).toString();
      document.getElementById('qtyinput'+idx).value = qty + 1;
    }
    function decreaseQty(idx, price) {
      var qtyInput = document.getElementById('qty'+idx);
      var qty = parseInt(qtyInput.value);
      if (qty > 1) {
        qtyInput.value = qty - 1;
        document.getElementById('total'+idx).innerText = (price * (qty - 1)).toString();
        document.getElementById('qtyinput'+idx).value = qty - 1;
      }
    }
    function updateHiddenFields(price, name, idx) {
      document.getElementById('bracename'+idx).value = name;
      document.getElementById('braceprice'+idx).value = price;
      document.getElementById('qtyinput'+idx).value = document.getElementById('qty'+idx).value;
      return true;
    }

    // 2. Integrated Loader Logic
    document.addEventListener('DOMContentLoaded', () => {
        const overlay = document.getElementById('loading-overlay');
        
        // CHECK: Have they seen the animation already in this session?
        if (sessionStorage.getItem('animationPlayed')) {
            // Hide overlay IMMEDIATELY
            if (overlay) {
                overlay.style.display = 'none';
                overlay.style.opacity = '0';
            }
        } else {
            // FIRST TIME VISIT: Play animation, then hide
            setTimeout(() => {
                if (overlay) {
                    overlay.classList.add('hidden'); // This triggers your CSS fade
                    
                    // Mark as played and fully remove from view after fade completes
                    setTimeout(() => {
                        overlay.style.display = 'none';
                        sessionStorage.setItem('animationPlayed', 'true');
                    }, 1000); 
                }
            }, 3000); 
        }
    });
    </script>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>

'''


cart_template = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<title>Your Cart - Treasures Jewels</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet" />
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
<style>
/* Logo shimmer animation */
.logo-shimmer {
  position: relative;
  color: #1d473a;
  font-weight: 700;
  font-size: 2.4rem;
  font-family: 'Playfair Display', serif;
  overflow: hidden;
}
.logo-shimmer::before {
  content: "";
  position: absolute;
  top: 0; left: -75%;
  width: 50%;
  height: 100%;
  background: linear-gradient(120deg, transparent, #f7e568aa, transparent);
  animation: shimmer 2s 1 forwards;
  filter: drop-shadow(0 0 3px #ffd85b);
  z-index: 1;
}
@keyframes shimmer {
  0% { left: -75%; }
  100% { left: 110%; }
}

/* Your full CSS styling as before */
body { background: #ebe4f5; font-family: 'Playfair Display', serif; margin: 0; }
.cart-main { max-width: 900px; margin: 46px auto; display: flex; flex-direction: column; gap: 38px;}
.cart-row { background: #fff; border-radius: 24px; box-shadow: 0 8px 36px rgba(60,50,70,0.09); border: 2.3px solid #d3c486; display:flex; overflow:hidden; min-height:290px; align-items:center;}
.cart-img-section { flex: 1.7; text-align: center; display:flex; justify-content:center; align-items:center; min-width:140px; max-width:340px; background:#f8f8f2; min-height:100%; overflow:hidden;}
.cart-img { max-width:97%; width:285px; min-width:120px; height:auto; margin:auto; border-radius:18px; object-fit:contain; display:block;}
.cart-content { flex: 2.1; padding:10px 38px; display:flex; flex-direction:column; gap:10px;}
.cart-title { font-size:1.31rem; font-weight:700; color:#232323; margin-bottom:4px;}
.cart-qty-section { display:flex; align-items:center; gap:14px; font-size:1.11rem; color:#544f48; margin-bottom:10px; flex-wrap:wrap;}
.qty-btn { background:#f3eed7; border:1.5px solid #ceb83a; color:#b8a248; width:34px; height:34px; border-radius:50%; font-size:1.22rem; font-weight:900; cursor:pointer; transition: all 0.14s;}
.qty-btn:hover { background:#fff5c2; color:#856a1b;}
.cart-sizes, .cart-beadsizes { margin:10px 0 0 0; display:flex; gap:6px; align-items:center; flex-wrap:wrap; min-width:0;}
.size-btn, .beadsize-btn { border:1.5px solid #b9a749; background:#f8f7e8; color:#7a6a2e; font-size:1.04rem; border-radius:7px; padding:6px 13px; cursor:pointer; user-select:none; min-width:49px;}
.size-btn.active, .size-btn:hover, .beadsize-btn.active, .beadsize-btn:hover { background:#ede098; color:#232323; font-weight:700;}
.cart-label { font-size:1.13rem; color:#8c7b1b; font-weight:700;}
.cart-price {color:#a18a22; font-size:1.29rem; font-weight:700;}
.cart-details { font-size:1.03rem; color:#5e5641; margin: 6px 0 10px 0;}
.cart-actions { margin-top:18px; display:flex; gap:13px; flex-wrap:wrap;}
.btn-custom { background:linear-gradient(90deg,#f5e3ab,#e7d8f7 110%); color:#3a491d; border-radius:8px; font-weight:700; font-size:1.11rem; border:none; padding:11px 26px; font-family: 'Playfair Display', serif; cursor:pointer;}
.btn-custom:hover { background:linear-gradient(90deg,#ede098,#d3c486 110%); color:#756a26;}
.remove-btn { border:1.5px solid #ceb83a; border-radius:50%; width:38px;height:38px;display:flex;align-items:center;justify-content:center;font-size:1.1rem; }
.remove-btn:hover { background:#ede098 !important; }
.cart-total-summary { background:#fffdf3; border:2px solid #d3c486; border-radius:18px; max-width:900px; margin:0 auto 30px auto; padding:22px 55px 55px 45px; display:flex; justify-content:space-between; align-items:flex-end; font-size:1.35rem; color:#a18a22; font-weight:800; box-shadow: 0 4px 15px #efe8d4a8; gap: 35px;}
.cart-summary-actions { padding-top:0px; text-align:right; display:flex; gap:20px;}
.empty-cart { 
  background: linear-gradient(135deg, #f8f7e8, #fffdf3); 
  border: 2px dashed #d3c486; 
  border-radius: 24px; 
  padding: 60px 40px; 
  text-align: center; 
  color: #8c7b1b; 
  font-size: 1.3rem; 
  margin: 38px auto; 
  max-width: 500px; 
  box-shadow: 0 8px 36px rgba(60,50,70,0.09);
}
.empty-icon { font-size: 4rem; color: #ceb83a; margin-bottom: 20px; animation: bounce 2s infinite; }
@keyframes bounce { 0%,20%,50%,80%,100%{transform:translateY(0);} 40%{transform:translateY(-10px);} 60%{transform:translateY(-5px);} }

</style>
<script>
window.addEventListener('load', () => {
  const logo = document.querySelector('.logo-shimmer');
  if (!logo) return;
  logo.addEventListener('animationend', () => {
    logo.style.setProperty('animation', 'none');
  }, { once: true });
});


function adjustQty(idx, delta, maxQty) {
  const qtyInput = document.getElementById('qty' + idx);
  let newQty = parseInt(qtyInput.value, 10) + delta;
  if (newQty < 1) newQty = 1;
  if (maxQty && newQty > maxQty) newQty = maxQty;
  qtyInput.value = newQty;
  document.getElementById('qtyinput' + idx).value = newQty;
  document.getElementById('itemtotal' + idx).innerText = '₹' + (parseInt(qtyInput.dataset.price, 10) * newQty);
  updateGrandTotal();
}

function updateGrandTotal() {
  let total = 0;
  document.querySelectorAll('[id^=qty]').forEach(inp => {
    const price = parseInt(inp.dataset.price, 10) || 0;
    const qty = parseInt(inp.value, 10) || 1;
    total += price * qty;
  });
  const grandTotalEl = document.getElementById('grandtotal');
  if(grandTotalEl) grandTotalEl.innerText = '₹' + total;
}
window.onload = updateGrandTotal;
function removeItem(index) {
  const rows = document.querySelectorAll('.cart-row');
  rows[index-1].style.transition = 'opacity 0.3s ease';
  rows[index-1].style.opacity = '0';
  setTimeout(() => {
    rows[index-1].remove();
    updateGrandTotal();
    if (rows.length === 1) {  // Was last bracelet
      document.querySelector('.cart-main').innerHTML = `
        <div class="empty-cart">
          <i class="fas fa-shopping-cart empty-icon"></i>
          <h3 style="color:#544f48; font-weight:700; margin-bottom:15px;">Your cart is empty</h3>
          <a href="{{ url_for('home') }}" class="btn btn-custom" style="font-size:1.1rem;">
            <i class="fas fa-gem me-2"></i>Shop Gemstone Bracelets
          </a>
        </div>`;
      document.querySelector('.cart-total-summary').style.display = 'none';
    }
  }, 300);
}

function saveQty(itemIndex, delta) {
  const qtyInput = document.getElementById('qty' + (itemIndex + 1));
  let newQty = parseInt(qtyInput.value, 10) + delta;
  if (newQty < 1) newQty = 1;

  const form = document.createElement('form');
  form.method = 'POST';
  form.action = '/update_cart';

  const nameInput = document.createElement('input');
  nameInput.type = 'hidden';
  nameInput.name = 'bracelet_name';
  nameInput.value = document.querySelectorAll('.cart-title')[itemIndex].textContent.trim();

  const qtyHidden = document.createElement('input');
  qtyHidden.type = 'hidden';
  qtyHidden.name = 'quantity';
  qtyHidden.value = newQty;

  form.appendChild(nameInput);
  form.appendChild(qtyHidden);
  document.body.appendChild(form);
  form.submit();
}


</script>
</head>
<body>
<nav class="navbar navbar-expand-lg shadow-sm">
  <div class="container">
    <a class="navbar-brand logo-shimmer" href="{{ url_for('home') }}">
      <i class="bi bi-house-door"></i> Treasures Jewels
    </a>
  </div>
</nav>

<div class="cart-main">
{% if cart and cart|length > 0 %}
  {% for item in cart %}
  <div class="cart-row">
    <div class="cart-img-section">
      {% for b in bracelets if b.name == item.name %}
      <img src="{{ url_for('static', filename=b.image) }}" class="cart-img" alt="{{ b.name }} image"/>
      {% endfor %}
    </div>

    <div class="cart-content">
      <form action="{{ url_for('add_to_cart') }}" method="post">
        <div class="cart-title">{{ item.name }}</div>
        
        <div class="cart-qty-section">
          Quantity:
          <button type="button" class="qty-btn" onclick="saveQty({{ loop.index0 }}, -1)">-</button>
          <input id="qty{{ loop.index }}" type="text" value="{{ item.quantity }}" readonly style="width:36px; text-align:center; border:none; background:#f6f6f3;" data-price="{{ item.price }}" />
          <button type="button" class="qty-btn" onclick="saveQty({{ loop.index0 }}, 1)">+</button>
          <input type="hidden" name="quantity" id="qtyinput{{ loop.index }}" value="{{ item.quantity }}"/>
          <input type="hidden" name="bracelet_name" value="{{ item.name }}"/>
          <input type="hidden" name="bracelet_price" value="{{ item.price }}"/>
        </div>

        <div class="cart-sizes">
          Size:
          {% for sz in ['S', 'M', 'L', 'XL', 'XXL'] %}
          <button type="button" class="size-btn{% if item.size == sz %} active{% endif %}">{{ sz }}</button>
          {% endfor %}
          <input type="hidden" name="size" class="size-input" value="{{ item.size or '' }}" />
        </div>

        <div class="cart-beadsizes">
          Beads Size:
          {% for bsize in ['6mm', '8mm', '10mm'] %}
          <button type="button" class="beadsize-btn{% if item.beadsize == bsize %} active{% endif %}">{{ bsize }}</button>
          {% endfor %}
          <input type="hidden" name="beadsize" class="beadsize-input" value="{{ item.beadsize or '' }}" />
        </div>

        <div class="cart-label">
          Price: <span class="cart-price">&#8377;{{ item.price }}</span>
        </div>

        <div class="cart-details">
          {% for b in bracelets if b.name == item.name %}
          {{ b.description }}<br/>
          {% endfor %}
        </div>

        <div class="cart-label">Total:</div>
        <div class="cart-price" id="itemtotal{{ loop.index }}">&#8377;{{ item.price * item.quantity }}</div>

        <div class="cart-actions">
           <a href="{{ url_for('remove_item', item_index=loop.index0) }}" class="btn-custom btn-sm remove-btn" style="text-decoration:none;">
              <i class="fas fa-trash"></i>
           </a>
        </div>
      </form> </div> </div> {% endfor %}

      <!-- SINGLE Size Guide Button + Modal (OUTSIDE LOOP) -->
        <div style="text-align: center; margin-top: 30px; margin-bottom: 20px;">
    <button type="button" class="btn-custom" data-bs-toggle="modal" data-bs-target="#sizeChartModal" 
            style="width: auto; min-width: 250px; padding: 10px 30px; font-size: 1.1rem; background: #fdfaf0; border: 1.5px solid #d3c486; color: #8c7b1b; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
        📏 Size Chart Guide
    </button>
</div>
  
 <div style="background-color: #fff3cd; color: #856404; padding: 15px; border-radius: 5px; margin-top: 20px; text-align: center; border: 1px solid #ffeeba;">
    <strong>Stall Notice:</strong> Online payment is currently unavailable. 
    Please show this cart to the staff at the stall to pay in person!
</div>

 <div class="cart-total-summary" style="display: flex; justify-content: space-between; align-items: center; padding: 25px; background: #fffdf3; border: 2px solid #d3c486; border-radius: 18px; margin-top: 20px;">
    
    <div style="font-size: 1.4rem; color: #a18a22; font-weight: 800; margin: 0;">
        Grand Total: <span id="grandtotal">₹{{ total }}</span>
    </div>
    
    <div class="cart-summary-actions" style="display: flex; gap: 10px; align-items: center;">
        
     <div style="display: flex; gap: 10px;">
    <a href="{{ url_for('clear_cart') }}" class="btn-custom" style="...">
        <i class="fas fa-trash-alt me-2"></i>Clear All
    </a>

    <a href="/" class="btn-custom" style="...">
        Browse More
    </a>
</div>
        
       
   <div style="background-color: #f8d7da; color: #721c24; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #f5c6cb; margin-top: 20px;">
    <h3 style="margin: 0 0 10px 0;">✨ Ready to Purchase? ✨</h3>
    <p style="font-size: 1.1rem; margin-bottom: 0;">
        Please <strong>visit our stall counter</strong> to pay and collect your bracelets. 
        Show us your screen so we can see your selection!
    </p>
</div>
       
    
       
    </div>
</div>  



  {% else %}
    <div class="empty-cart">
      <i class="fas fa-shopping-cart empty-icon"></i>
      <h3 style="color:#544f48; font-weight:700; margin-bottom:15px;">Your cart is empty</h3>
      <a href="{{ url_for('home') }}" class="btn btn-custom" style="font-size:1.1rem;">
        <i class="fas fa-gem me-2"></i>Shop Gemstone Bracelets
      </a>
    </div>
  {% endif %}
  </div>
            
           <!-- Size Chart Modal -->
          <!-- FIXED Modal - Inline Styles (No CSS Needed) -->
<div class="modal fade" id="sizeChartModal" tabindex="-1">
  <div class="modal-dialog modal-xl modal-dialog-centered">
    <div class="modal-content" style="background:#ffffff;border-radius:20px;box-shadow:0 30px 80px rgba(0,0,0,0.5);border:none;">
      <div class="modal-header" style="background:linear-gradient(135deg,#b8a248,#d4af37);color:white;border-radius:20px 20px 0 0;border-bottom:none;padding:20px;">
        <h5 class="modal-title" style="font-family:'Playfair Display',serif;font-weight:700;font-size:1.4rem;margin:0;"><i class="bi bi-rulers me-2"></i>📏 Bracelet Size Chart</h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" style="filter:invert(1);"></button>
      </div>
      <div class="modal-body" style="padding:30px;background:#fafafa;">
        <h3 style="font-family:'Playfair Display',serif;color:#2c1810;font-size:1.6rem;text-align:center;margin-bottom:25px;font-weight:700;">Measure Wrist + 2cm Comfort</h3>
        <div class="table-responsive">
          <table class="table" style="background:white;border-radius:15px;box-shadow:0 10px 30px rgba(0,0,0,0.1);margin:0 auto;font-family:'Poppins',sans-serif;">
            <thead>
              <tr>
                <th style="background:linear-gradient(135deg,#b8a248,#d4af37);color:white;font-weight:700;padding:15px 12px;text-align:center;font-size:1rem;">Size</th>
                <th style="background:linear-gradient(135deg,#b8a248,#d4af37);color:white;font-weight:700;padding:15px 12px;text-align:center;font-size:1rem;">CM</th>
                <th style="background:linear-gradient(135deg,#b8a248,#d4af37);color:white;font-weight:700;padding:15px 12px;text-align:center;font-size:1rem;">Inches</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="font-weight:700;font-size:1.2rem;color:#b8a248;padding:14px;text-align:center;border-color:#e8e8e8;">S</td>
                <td style="font-weight:700;font-size:1.1rem;color:#1a1a1a;padding:14px;text-align:center;border-color:#e8e8e8;">15-16.5</td>
                <td style="font-weight:700;font-size:1.1rem;color:#1a1a1a;padding:14px;text-align:center;border-color:#e8e8e8;">5.9-6.5"</td>

              </tr>
              <tr>
                <td style="font-weight:700;font-size:1.2rem;color:#b8a248;padding:14px;text-align:center;border-color:#e8e8e8;">M</td>
                <td style="font-weight:700;font-size:1.1rem;color:#1a1a1a;padding:14px;text-align:center;border-color:#e8e8e8;">16.5-18</td>
                <td style="font-weight:700;font-size:1.1rem;color:#1a1a1a;padding:14px;text-align:center;border-color:#e8e8e8;">6.5-7.1"</td>
                
              </tr>
              <tr>
                <td style="font-weight:700;font-size:1.2rem;color:#b8a248;padding:14px;text-align:center;border-color:#e8e8e8;">L</td>
                <td style="font-weight:700;font-size:1.1rem;color:#1a1a1a;padding:14px;text-align:center;border-color:#e8e8e8;">18-19.5</td>
                <td style="font-weight:700;font-size:1.1rem;color:#1a1a1a;padding:14px;text-align:center;border-color:#e8e8e8;">7.1-7.7"</td>
               
              </tr>
              <tr>
                <td style="font-weight:700;font-size:1.2rem;color:#b8a248;padding:14px;text-align:center;border-color:#e8e8e8;">XL</td>
                <td style="font-weight:700;font-size:1.1rem;color:#1a1a1a;padding:14px;text-align:center;border-color:#e8e8e8;">19.5-21</td>
                <td style="font-weight:700;font-size:1.1rem;color:#1a1a1a;padding:14px;text-align:center;border-color:#e8e8e8;">7.7-8.3"</td>
               
              </tr>
              <tr>
                <td style="font-weight:700;font-size:1.2rem;color:#b8a248;padding:14px;text-align:center;border-color:#e8e8e8;">XXL</td>
                <td style="font-weight:700;font-size:1.1rem;color:#1a1a1a;padding:14px;text-align:center;border-color:#e8e8e8;">21+</td>
                <td style="font-weight:700;font-size:1.1rem;color:#1a1a1a;padding:14px;text-align:center;border-color:#e8e8e8;">8.3"+</td>
               
              </tr>
            </tbody>
          </table>
        </div>
        <div style="background:rgba(184,162,72,0.1);border-radius:12px;padding:15px;margin-top:20px;border-left:5px solid #b8a248;">
          <strong style="color:#2c1810;">All bracelets fully adjustable</strong> with premium stretch cord.
        </div>
      </div>
    </div>
  </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

 <script>
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.cart-row').forEach(row => {
        const beadsizeBtns = row.querySelectorAll('.beadsize-btn');
        const beadsizeInput = row.querySelector('input.beadsize-input');
        const sizeBtns = row.querySelectorAll('.size-btn');
        const sizeInput = row.querySelector('input.size-input');

        // Logic for Bead Size Buttons
        beadsizeBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                beadsizeBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                beadsizeInput.value = btn.textContent.trim();
            });
        });

        // Logic for Size Buttons
        sizeBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                sizeBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                sizeInput.value = btn.textContent.trim();
            });
        });
    });
});
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template, bracelets=bracelets)

@app.route('/update_cart', methods=['POST'])
def update_cart():
    data = request.form
    cart = session.get('cart', [])
    name = data.get('bracelet_name')
    qty = int(data.get('quantity', 1))
    
    for i, item in enumerate(cart):
        if item['name'] == name:
            item['quantity'] = qty
            if qty <= 0:
                del cart[i]
            break
    
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('cart'))


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    bracelet_name = request.form.get('bracelet_name', '').strip()
    bracelet_price = int(request.form.get('bracelet_price', 0))
    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', [])
    for item in cart:
        if item['name'] == bracelet_name and item['price'] == bracelet_price:
            item['quantity'] += quantity
            break
    else:
        cart.append({'name': bracelet_name, 'price': bracelet_price, 'quantity': quantity})
    session['cart'] = cart
    return redirect(url_for('cart'))



@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = sum(item.get('price', 0) * item.get('quantity', 1) for item in cart)
    return render_template_string(cart_template, cart=cart, total=total, bracelets=bracelets)


@app.route('/remove_item/<int:item_index>', methods=['GET', 'POST'])
def remove_item(item_index):
    cart = session.get('cart', [])

    if isinstance(cart, list) and 0 <= item_index < len(cart):
        cart.pop(item_index)
        session['cart'] = cart
        session.modified = True   # critical for delete

    # if cart becomes empty, still a list
    if not isinstance(session.get('cart', []), list):
        session['cart'] = []
        session.modified = True

    return redirect(url_for('cart'))

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None) # Removes the cart from session
    session.modified = True
    return redirect(url_for('cart'))


if __name__ == "__main__":
    app.run(debug=True)











































