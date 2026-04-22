from flask import Flask, render_template, request, jsonify
import random
import re
from datetime import datetime

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# ─── KNOWLEDGE BASE ──────────────────────────────────────────────────────────
KNOWLEDGE = [
    # GREETINGS
    ([r'\b(hi|hello|hey|howdy|sup)\b'],
     ["Hey there! 😊 How can I help you today?",
      "Hello! Great to see you. What's on your mind?",
      "Hi! I'm ready to chat. Ask me anything!"]),

    ([r'\bhow are you\b', r'\bhow do you do\b'],
     ["I'm doing great, thanks for asking! 😄 How about you?",
      "Perfectly fine and ready to help! 🌟",
      "All systems running smoothly! What can I do for you?"]),

    ([r'\bwhat is your name\b', r'\bwho are you\b', r'\bwhat are you\b'],
     ["I'm ChatBot 🤖 — your friendly AI assistant built with Python & Flask!",
      "I go by ChatBot! I'm here to answer your questions.",
      "I'm your AI ChatBot, powered by Python. Ask me anything!"]),

    # FAREWELL
    ([r'\b(bye|goodbye|see you|take care|cya|farewell)\b'],
     ["Goodbye! Have a wonderful day! 👋",
      "See you soon! Come back anytime. 😊",
      "Take care! It was nice chatting with you! 🌟"]),

    # THANKS
    ([r'\b(thanks|thank you|thx|ty|cheers)\b'],
     ["You're very welcome! 😊",
      "Happy to help! Ask me anything else.",
      "My pleasure! Feel free to ask more questions. 🌟"]),

    # SCIENCE
    ([r'\bwhat is (the )?sun\b', r'\btell me about (the )?sun\b'],
     ["☀️ The Sun is a star at the center of our Solar System. It's a massive ball of hot plasma, mainly hydrogen and helium. Its energy comes from nuclear fusion in its core, providing the light and heat needed for life on Earth."]),

    ([r'\bwhat is (the )?moon\b', r'\btell me about (the )?moon\b'],
     ["🌕 The Moon is Earth's only natural satellite. It orbits Earth every ~27 days, influences ocean tides, and is about 384,400 km away from Earth. It's the fifth-largest moon in the Solar System."]),

    ([r'\bwhat is gravity\b', r'\bexplain gravity\b'],
     ["🍎 Gravity is a fundamental force that attracts objects with mass toward each other. On Earth it gives weight to objects and causes them to fall. Einstein described gravity as the curvature of space-time caused by mass."]),

    ([r'\bwhat is photosynthesis\b', r'\bexplain photosynthesis\b'],
     ["🌿 Photosynthesis is the process by which plants use sunlight, water, and CO₂ to produce glucose and oxygen. The equation: 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂. It is the foundation of life on Earth."]),

    ([r'\bwhat is dna\b', r'\bexplain dna\b'],
     ["🧬 DNA (Deoxyribonucleic Acid) carries the genetic instructions for all living organisms. Shaped like a double helix, it contains four bases: Adenine, Thymine, Guanine, and Cytosine. Every cell in your body has ~6 feet of DNA packed inside it!"]),

    ([r'\bwhat is an atom\b', r'\bexplain atom\b'],
     ["⚛️ An atom is the basic unit of matter. It has a nucleus (protons + neutrons) surrounded by electrons. Atoms are incredibly tiny — a human hair is about 1 million atoms wide!"]),

    ([r'\bwhat is electricity\b', r'\bexplain electricity\b'],
     ["⚡ Electricity is the flow of electric charge through electrons moving in a conductor. It powers our homes and devices. Static electricity is a buildup of charge; current electricity is flowing charge."]),

    ([r'\b(speed of light|how fast is light)\b'],
     ["💡 The speed of light in a vacuum is ~299,792,458 m/s (186,282 miles/s). Denoted as 'c', it is the ultimate speed limit in the universe, as established by Einstein's Theory of Relativity."]),

    ([r'\bwhat is evolution\b', r'\bexplain evolution\b'],
     ["🦕 Evolution is the process of change in species over generations through natural selection. Charles Darwin proposed that organisms with better-suited traits survive and reproduce more, passing those traits to offspring."]),

    ([r'\bwhat is climate change\b', r'\bglobal warming\b'],
     ["🌍 Climate change refers to long-term shifts in global temperatures. Human activities — especially burning fossil fuels — increase greenhouse gases (CO₂, methane), warming the planet. Effects include rising sea levels and extreme weather."]),

    ([r'\bwater cycle\b', r'\bhydrological cycle\b'],
     ["💧 The water cycle: evaporation from oceans → condensation into clouds → precipitation as rain/snow → runoff back to oceans. Powered by the Sun and driven by gravity."]),

    ([r'\bblack hole\b'],
     ["🕳️ A black hole is a region where gravity is so strong that nothing — not even light — can escape. They form when massive stars collapse. The boundary is called the event horizon. Stephen Hawking discovered they emit radiation (Hawking Radiation)."]),

    # MATH
    ([r'\bpythagorean theorem\b'],
     ["📐 The Pythagorean Theorem: in a right-angled triangle, a² + b² = c² where c is the hypotenuse. One of the most important theorems in mathematics, proven by Pythagoras."]),

    ([r'\bwhat is pi\b', r'\bvalue of pi\b'],
     ["🔵 Pi (π) ≈ 3.14159265... It is the ratio of a circle's circumference to its diameter. An irrational, non-repeating decimal that appears throughout mathematics, physics, and engineering."]),

    ([r'\bwhat is calculus\b', r'\bexplain calculus\b'],
     ["📊 Calculus deals with continuous change. Differential Calculus handles rates of change (derivatives); Integral Calculus handles areas (integrals). Invented independently by Newton and Leibniz in the 17th century."]),

    # HISTORY
    ([r'\bmahatma gandhi\b', r'\bgandhi\b'],
     ["🕊️ Mahatma Gandhi (1869–1948) was an Indian independence activist who pioneered non-violent civil disobedience. He led India's independence movement against British colonial rule and is called the 'Father of the Nation' in India."]),

    ([r'\balbert einstein\b', r'\beinstein\b'],
     ["🧠 Albert Einstein (1879–1955) developed the theory of relativity (E=mc²). He won the Nobel Prize in Physics in 1921 and is widely regarded as one of the greatest scientists in history."]),

    ([r'\bisaac newton\b', r'\bnewton\b'],
     ["🍎 Isaac Newton (1643–1727) formulated the Laws of Motion and Universal Gravitation, invented calculus, and made major contributions to optics. His work laid the foundation for classical mechanics."]),

    ([r'\bworld war (1|one|i)\b', r'\bwwi\b', r'\bfirst world war\b'],
     ["⚔️ World War I (1914–1918) involved most world powers. Triggered by the assassination of Archduke Franz Ferdinand, it caused ~20 million deaths and ended with the Treaty of Versailles."]),

    ([r'\bworld war (2|two|ii)\b', r'\bwwii\b', r'\bsecond world war\b'],
     ["⚔️ World War II (1939–1945) was the deadliest conflict in history (~70–85 million deaths). Caused by Nazi Germany's aggression under Hitler. It ended with Germany's and Japan's surrender, leading to the United Nations."]),

    ([r'\bchristopher columbus\b', r'\bwho discovered america\b'],
     ["⛵ Christopher Columbus (1451–1506) was an Italian explorer who sailed from Spain in 1492, reaching the Americas. His voyage began an era of European exploration, though Indigenous peoples had lived there for thousands of years."]),

    # GEOGRAPHY
    ([r'\bcapital of india\b'],
     ["🇮🇳 The capital of India is New Delhi. It's the seat of all three branches of the Government of India."]),

    ([r'\bcapital of (usa|united states|america)\b'],
     ["🇺🇸 The capital of the United States is Washington, D.C. — home to the White House, Capitol Building, and Supreme Court."]),

    ([r'\bcapital of (uk|united kingdom|england|britain)\b'],
     ["🇬🇧 The capital of the United Kingdom is London — a global hub for finance, culture, and history."]),

    ([r'\bcapital of france\b'],
     ["🇫🇷 The capital of France is Paris — the 'City of Light', home to the Eiffel Tower, the Louvre, and Notre-Dame Cathedral."]),

    ([r'\bcapital of china\b'],
     ["🇨🇳 The capital of China is Beijing. It has been the political center of China for centuries and is home to the Forbidden City and Tiananmen Square."]),

    ([r'\bcapital of japan\b'],
     ["🇯🇵 The capital of Japan is Tokyo — one of the world's largest and most modern cities."]),

    ([r'\b(largest|biggest) country\b'],
     ["🌍 Russia is the largest country by land area, covering ~17.1 million km² — about 11% of Earth's total land area, spanning both Europe and Asia."]),

    ([r'\bsmallest country\b'],
     ["🏛️ Vatican City is the world's smallest country — 0.44 km² with ~800 people — an independent city-state within Rome, Italy."]),

    ([r'\b(longest|biggest) river\b'],
     ["🌊 The Nile River (~6,650 km) is traditionally the longest river. The Amazon River is sometimes cited as longer depending on how its source is measured."]),

    ([r'\b(highest|tallest) mountain\b'],
     ["🏔️ Mount Everest is the highest mountain above sea level at 8,848.86 m (29,031.7 ft), located in the Himalayas on the Nepal–Tibet border."]),

    # TECHNOLOGY & PROGRAMMING
    ([r'\bwhat is python\b', r'\btell me about python\b', r'\bexplain python\b'],
     ["🐍 Python is a high-level, versatile programming language known for its readable syntax. Created by Guido van Rossum in 1991, it's widely used in web development (Django, Flask), data science, AI/ML, and automation. This chatbot runs on Python!"]),

    ([r'\bwhat is (artificial intelligence|ai)\b', r'\bexplain (ai|artificial intelligence)\b'],
     ["🤖 Artificial Intelligence (AI) is the simulation of human intelligence by computers. AI systems can learn, reason, solve problems, understand language, and recognize patterns. Key areas: Machine Learning, Deep Learning, NLP, and Computer Vision."]),

    ([r'\bwhat is machine learning\b', r'\bexplain machine learning\b'],
     ["🧠 Machine Learning (ML) is a subset of AI where systems learn from data without being explicitly programmed. They find patterns and improve with experience. Types: Supervised, Unsupervised, and Reinforcement Learning."]),

    ([r'\bwhat is deep learning\b', r'\bexplain deep learning\b'],
     ["🔬 Deep Learning uses multi-layered neural networks to excel at image recognition, speech, and NLP tasks. It powers ChatGPT, self-driving cars, and face recognition systems."]),

    ([r'\bwhat is (the )?internet\b'],
     ["🌐 The Internet is a global network of interconnected computers using TCP/IP protocols. Developed from ARPANET in the 1960s, it enables the Web, email, streaming, social media, and cloud computing."]),

    ([r'\bwhat is html\b', r'\bexplain html\b'],
     ["📄 HTML (HyperText Markup Language) is the standard language for creating web pages. Tags like <h1>, <p>, <img>, and <a> structure content. Every website is built on HTML."]),

    ([r'\bwhat is css\b', r'\bexplain css\b'],
     ["🎨 CSS (Cascading Style Sheets) styles HTML — controlling layout, colors, fonts, animations, and responsiveness. Without CSS, all websites would look like plain text!"]),

    ([r'\bwhat is javascript\b', r'\bexplain javascript\b'],
     ["⚡ JavaScript (JS) is the programming language of the web. It makes websites interactive. Runs in browsers and on servers (Node.js). Frameworks like React and Vue are built on it."]),

    ([r'\bwhat is flask\b', r'\bexplain flask\b'],
     ["🔥 Flask is a lightweight Python web framework. It's simple, flexible, and great for building web apps and APIs. This chatbot you're using is powered by Flask!"]),

    ([r'\bwhat is (a )?database\b', r'\bexplain database\b'],
     ["🗄️ A database is an organized collection of structured data stored electronically. Relational databases (MySQL, PostgreSQL) use tables; NoSQL databases (MongoDB) use flexible formats. They power almost every app you use."]),

    ([r'\bcloud computing\b'],
     ["☁️ Cloud computing delivers computing services over the internet (servers, storage, databases, software). Providers like AWS, Google Cloud, and Azure let you scale on demand instead of owning hardware."]),

    ([r'\bblockchain\b'],
     ["🔗 Blockchain is a distributed ledger where data is stored in tamper-resistant blocks chained together across many computers. Bitcoin and Ethereum use blockchain; it's also used in supply chains and healthcare."]),

    # HEALTH
    ([r'\bwhat is (a )?virus\b', r'\bexplain virus\b'],
     ["🦠 A virus is a microscopic infectious agent that replicates inside living cells. Unlike bacteria, viruses are not alive on their own. They cause flu, COVID-19, and the common cold. Vaccines help the immune system fight them."]),

    ([r'\bwhat is (a )?vaccine\b', r'\bexplain vaccine\b'],
     ["💉 A vaccine trains the immune system to fight a specific pathogen using a weakened/dead version or its proteins. Vaccines have eradicated smallpox and nearly eliminated polio."]),

    ([r'\bhow much water (should|do) (i|we) drink\b', r'\bdaily water intake\b'],
     ["💧 Most experts recommend ~8 glasses (2 liters) of water per day, though needs vary by body weight, activity, and climate. Aim for light yellow urine as a hydration guide."]),

    ([r'\bhow (to|do you) lose weight\b', r'\bweight loss\b'],
     ["⚖️ Healthy weight loss: eat a balanced diet with fewer processed foods, maintain a moderate caloric deficit, exercise regularly (cardio + strength), get 7–9 hours of sleep, and stay hydrated. Always consult a doctor before major changes."]),

    ([r'\bhow (many|much) sleep\b', r'\bhow long to sleep\b'],
     ["😴 Adults need 7–9 hours of sleep per night. Teenagers need 8–10 hours. Good sleep improves memory, mood, and immune function. Tips: regular schedule, avoid screens before bed, keep your room cool and dark."]),

    # FUN & MISC
    ([r'\btell me a joke\b', r'\bsay a joke\b', r'\bgive me a joke\b', r'\bjoke\b'],
     ["😄 Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
      "😂 Why did the mathematician break up with the calendar? Too many dates!",
      "😆 What do you call a fish without eyes? A fsh! 🐟",
      "🤣 Why can't you trust an atom? Because they make up everything!"]),

    ([r'\bmeaning of life\b', r'\bpurpose of life\b'],
     ["🌟 42 — according to The Hitchhiker's Guide to the Galaxy! 😄 Seriously though, philosophers debate this endlessly. Many believe it's about happiness, meaningful relationships, and pursuing what brings you fulfillment."]),

    ([r'\bwho (made|created|built) you\b'],
     ["👨‍💻 I was built by a developer using Python and Flask! I'm a rule-based chatbot with a rich knowledge base. Pretty cool, right? 😊"]),

    ([r'\bwhat (can you do|do you know)\b', r'\byour capabilities\b'],
     ["💡 I can answer questions about:\n📚 Science & Nature\n🧮 Math (including calculations)\n🌍 Geography\n📖 History\n💻 Technology & Programming\n❤️ Health & Lifestyle\n😄 Fun & Trivia\n\nJust ask me anything!"]),

    ([r'\b(current )?time\b', r'\bwhat time is it\b'],
     [f"⏰ The current time is {datetime.now().strftime('%I:%M %p')}."]),

    ([r'\b(today.?s? )?date\b', r'\bwhat day is (it|today)\b'],
     [f"📅 Today is {datetime.now().strftime('%A, %B %d, %Y')}."]),
]


def try_math(text):
    """Safely evaluate simple arithmetic"""
    text = (text.replace('plus', '+').replace('minus', '-')
                .replace('times', '*').replace('multiplied by', '*')
                .replace('divided by', '/').replace(' x ', '*'))
    m = re.search(r'(\d+\.?\d*)\s*([\+\-\*\/])\s*(\d+\.?\d*)', text)
    if m:
        a, op, b = m.group(1), m.group(2), m.group(3)
        try:
            result = eval(f"{a}{op}{b}")  # safe: only numbers + operator
            result = int(result) if isinstance(result, float) and result.is_integer() else round(result, 4)
            return f"🧮 {a} {op} {b} = {result}"
        except Exception:
            return None
    return None


def get_response(user_input):
    text = user_input.lower().strip()

    math_result = try_math(text)
    if math_result:
        return math_result

    for patterns, answers in KNOWLEDGE:
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return random.choice(answers)

    if re.search(r'\bwhat is\b|\bwhat are\b|\bexplain\b|\btell me about\b|\bdefine\b', text):
        return "🔍 I don't have specific info on that yet. Try asking about science, math, history, geography, technology, or health!"
    if re.search(r'\bhow (do|does|to|can|should)\b', text):
        return "🤔 Great 'how' question! I might not have that specific answer — try asking about health tips, programming concepts, or scientific processes!"
    if re.search(r'\bwho (is|was|are|were)\b', text):
        return "👤 I know many historical figures! Try asking about Einstein, Newton, Gandhi, Columbus, and more."
    if re.search(r'\bwhere is\b|\bwhere are\b', text):
        return "📍 I can help with geography! Ask me about capitals, countries, rivers, or mountains."

    fallbacks = [
        "🤔 Hmm, not sure about that one. Try asking about science, history, math, or technology!",
        "💡 Great question! I might not know that yet — ask me about programming, AI, world history, or health tips!",
        "😊 I don't have that answer yet. Try 'What is AI?' or 'Tell me a joke'!",
        "📚 My knowledge covers science, math, geography, history, and tech. Give those a try!",
    ]
    return random.choice(fallbacks)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()
        if not user_message:
            return jsonify({"reply": "Please type a message! 💬"})
        return jsonify({"reply": get_response(user_message)})
    except Exception:
        return jsonify({"reply": "Oops! Something went wrong. Please try again. 🔧"}), 400


@app.route("/health")
def health():
    return jsonify({"status": "ok", "time": datetime.now().isoformat()})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
