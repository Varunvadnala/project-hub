const form = document.getElementById("decisionForm");
const optionA = document.getElementById("optionA");
const optionB = document.getElementById("optionB");
const profile = document.getElementById("profile");
const dayType = document.getElementById("dayType");
const timeOfDay = document.getElementById("timeOfDay");
const energy = document.getElementById("energy");
const budget = document.getElementById("budget");
const weather = document.getElementById("weather");
const notes = document.getElementById("notes");
const autoContextBtn = document.getElementById("autoContextBtn");

const decisionTitle = document.getElementById("decisionTitle");
const decisionReason = document.getElementById("decisionReason");
const resultCard = document.getElementById("resultCard");
const scoreboard = document.getElementById("scoreboard");

function inferCurrentContext() {
    const now = new Date();
    const hours = now.getHours();
    const day = now.getDay();

    if (hours >= 5 && hours < 12) {
        timeOfDay.value = "morning";
    } else if (hours >= 12 && hours < 17) {
        timeOfDay.value = "afternoon";
    } else if (hours >= 17 && hours < 21) {
        timeOfDay.value = "evening";
    } else {
        timeOfDay.value = "night";
    }

    dayType.value = day === 0 || day === 6 ? "weekend" : "weekday";
}

// Lightweight keyword model for context-sensitive scoring.
const keywordWeights = [
    { tags: ["study", "read", "learn", "course", "exam", "coding", "work", "project"], focus: 1.8, relax: -0.8, cost: 0.4, outdoors: -0.2, indoors: 0.8 },
    { tags: ["gym", "run", "walk", "sport", "football", "yoga", "workout", "exercise"], focus: 1.2, relax: 0.2, cost: 0.2, outdoors: 0.8, indoors: 0.1 },
    { tags: ["movie", "netflix", "game", "gaming", "music", "sleep", "nap", "rest"], focus: -0.7, relax: 1.9, cost: -0.1, outdoors: -0.5, indoors: 1.0 },
    { tags: ["party", "club", "trip", "travel", "shopping", "restaurant", "cafe"], focus: -0.8, relax: 1.1, cost: 1.7, outdoors: 0.9, indoors: 0.2 },
    { tags: ["clean", "home", "family", "cook", "meal", "self care", "routine"], focus: 0.7, relax: 0.9, cost: -0.3, outdoors: -0.4, indoors: 1.1 }
];

function buildTraitScore(text) {
    const normalized = text.toLowerCase();
    const traits = { focus: 0.4, relax: 0.4, cost: 0, outdoors: 0, indoors: 0 };

    keywordWeights.forEach((group) => {
        const hit = group.tags.some((tag) => normalized.includes(tag));
        if (hit) {
            traits.focus += group.focus;
            traits.relax += group.relax;
            traits.cost += group.cost;
            traits.outdoors += group.outdoors;
            traits.indoors += group.indoors;
        }
    });

    return traits;
}

function contextBias(ctx, traits) {
    let score = 0;
    const why = [];

    if (ctx.timeOfDay === "morning") {
        score += traits.focus * 1.2;
        why.push("Morning favors focused choices");
    }
    if (ctx.timeOfDay === "afternoon") {
        score += traits.focus * 0.7 + traits.relax * 0.3;
        why.push("Afternoon balances productivity and comfort");
    }
    if (ctx.timeOfDay === "evening") {
        score += traits.relax * 0.9;
        why.push("Evening often supports winding down");
    }
    if (ctx.timeOfDay === "night") {
        score += traits.relax * 1.1 - traits.outdoors * 0.5;
        why.push("Night rewards calm and indoor options");
    }

    if (ctx.dayType === "weekday") {
        score += traits.focus * 0.7;
        why.push("Weekday gives extra value to useful tasks");
    } else {
        score += traits.relax * 0.8;
        why.push("Weekend gives extra value to enjoyment");
    }

    if (ctx.energy === "high") {
        score += traits.outdoors * 0.9 + traits.focus * 0.4;
        why.push("High energy fits active or ambitious plans");
    }
    if (ctx.energy === "medium") {
        score += traits.focus * 0.3 + traits.relax * 0.3;
    }
    if (ctx.energy === "low") {
        score += traits.relax * 1.0 - traits.focus * 0.5;
        why.push("Low energy favors simpler options");
    }

    if (ctx.budget === "save") {
        score += (-traits.cost) * 1.1;
        why.push("Saving mode prefers lower-cost choices");
    }
    if (ctx.budget === "balanced") {
        score += (-traits.cost) * 0.2;
    }
    if (ctx.budget === "spend") {
        score += traits.cost * 0.6;
        why.push("Spend mode allows premium experiences");
    }

    if (ctx.weather === "rainy") {
        score += traits.indoors * 0.9 - traits.outdoors * 0.7;
        why.push("Rainy weather supports indoor choices");
    }
    if (ctx.weather === "hot") {
        score += traits.indoors * 0.4;
    }
    if (ctx.weather === "cold") {
        score += traits.indoors * 0.8;
    }
    if (ctx.weather === "pleasant") {
        score += traits.outdoors * 0.6;
    }

    // Tiny profile personalization to match user request.
    if (ctx.profile === "girl") {
        score += traits.relax * 0.1;
    }
    if (ctx.profile === "boy") {
        score += traits.outdoors * 0.1;
    }
    if (ctx.profile === "other") {
        score += (traits.focus + traits.relax) * 0.05;
    }

    return { score, why };
}

function evaluateOption(text, ctx, extraNotes) {
    const traits = buildTraitScore(`${text} ${extraNotes}`);
    const { score, why } = contextBias(ctx, traits);
    return {
        text,
        score,
        why
    };
}

function displayResult(a, b) {
    const winner = a.score === b.score ? null : (a.score > b.score ? a : b);
    const loser = winner === a ? b : a;
    const badge = resultCard.querySelector(".badge");

    if (!winner) {
        badge.textContent = "Tie";
        badge.style.background = "rgba(200, 92, 63, 0.14)";
        badge.style.borderColor = "rgba(200, 92, 63, 0.35)";
        badge.style.color = "#8f3f2b";
        decisionTitle.textContent = "Both choices feel equally right for me.";
        decisionReason.textContent = "My current context gives almost the same score to both. I can choose the one I feel more excited about right now.";
    } else {
        badge.textContent = "Recommended";
        badge.style.background = "rgba(47, 125, 93, 0.15)";
        badge.style.borderColor = "rgba(47, 125, 93, 0.35)";
        badge.style.color = "#205640";
        decisionTitle.textContent = `Best pick for me: ${winner.text}`;
        const topReasons = winner.why.slice(0, 3).join(". ");
        decisionReason.textContent = `${topReasons}. For my current situation, this looks better than "${loser.text}".`;
    }

    scoreboard.innerHTML = `
        <div class="score"><strong>${a.text}</strong><br>Score: ${a.score.toFixed(2)}</div>
        <div class="score"><strong>${b.text}</strong><br>Score: ${b.score.toFixed(2)}</div>
    `;
}

form.addEventListener("submit", (event) => {
    event.preventDefault();

    const choiceA = optionA.value.trim();
    const choiceB = optionB.value.trim();

    if (!choiceA || !choiceB) {
        decisionTitle.textContent = "I need to enter both choices first.";
        decisionReason.textContent = "This tool compares two choices, so I should fill both fields.";
        return;
    }

    const ctx = {
        profile: profile.value,
        dayType: dayType.value,
        timeOfDay: timeOfDay.value,
        energy: energy.value,
        budget: budget.value,
        weather: weather.value
    };

    const a = evaluateOption(choiceA, ctx, notes.value.trim());
    const b = evaluateOption(choiceB, ctx, notes.value.trim());
    displayResult(a, b);
});

autoContextBtn.addEventListener("click", inferCurrentContext);

// Initialize with current local day/time.
inferCurrentContext();
