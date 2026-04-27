// Function to handle public stock searches on the landing page
async function searchPublicStock(event) {
    event.preventDefault();
    const ticker = document.getElementById("public-ticker").value.trim();
    const resultDiv = document.getElementById("public-search-result");

    if (!ticker) {
        return;
    }

    resultDiv.innerHTML = `<p>Loading data for ${ticker.toUpperCase()}...</p>`;

    try {
        const response = await fetch(`/prices/${ticker}`);
        if (!response.ok) {
            throw new Error("Ticker not found");
        }
        const data = await response.json();
        resultDiv.innerHTML = `
            <h3>${data.ticker}</h3>
            <p><strong>Current Price:</strong> $${data.price.toFixed(2)}</p>
            <p><strong>Source:</strong> yfinance</p>
        `;
    } catch (err) {
        resultDiv.innerHTML = `<p>Sorry, we could not find that ticker.</p>`;
    }
}

async function loadDashboard() {
    const holdingsTable = document.getElementById("holdings-table");
    const summaryBox = document.getElementById("portfolio-summary");
    const token = localStorage.getItem("token");

    if (!holdingsTable || !summaryBox) {
        return;
    }

    if (!token) {
        summaryBox.innerHTML = "<p>Please login to see your dashboard.</p>";
        holdingsTable.innerHTML = "";
        return;
    }

    const headers = { Authorization: `Bearer ${token}` };
    try {
        const [holdingsRes, summaryRes] = await Promise.all([
            fetch("/portfolio", { headers }),
            fetch("/portfolio/analytics", { headers }),
        ]);

        if (!holdingsRes.ok || !summaryRes.ok) {
            throw new Error("Unauthorized");
        }

        const holdings = await holdingsRes.json();
        const summary = await summaryRes.json();

        summaryBox.innerHTML = `
            <div class="summary-card">
                <h3>Total Invested</h3>
                <p>$${summary.total_invested.toFixed(2)}</p>
            </div>
            <div class="summary-card">
                <h3>Current Value</h3>
                <p>$${summary.current_value.toFixed(2)}</p>
            </div>
            <div class="summary-card">
                <h3>Unrealized P&L</h3>
                <p>$${summary.unrealized_pnl.toFixed(2)} (${summary.return_pct.toFixed(2)}%)</p>
            </div>
        `;

        if (holdings.length === 0) {
            holdingsTable.innerHTML = "<tr><td colspan=\"3\">No holdings yet.</td></tr>";
        } else {
            holdingsTable.innerHTML = holdings
                .map(
                    (h) => `
                <tr>
                    <td>${h.ticker}</td>
                    <td>${h.quantity}</td>
                    <td>$${h.avg_buy_price.toFixed(2)}</td>
                </tr>
            `
                )
                .join("");
        }
    } catch (err) {
        summaryBox.innerHTML = "<p>Please login to see your dashboard.</p>";
        holdingsTable.innerHTML = "";
    }
}

async function addHolding(event) {
    event.preventDefault();
    const input = document.getElementById("add-ticker");
    const token = localStorage.getItem("token");

    if (!token) {
        alert("Please login first.");
        return;
    }

    const ticker = input.value.trim();
    if (!ticker) {
        return;
    }

    const response = await fetch("/portfolio/holdings", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ ticker }),
    });

    if (response.ok) {
        input.value = "";
        loadDashboard();
    } else {
        const data = await response.json();
        alert(data.detail || "Could not add holding");
    }
}

async function loginUser(event) {
    event.preventDefault();
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;
    const response = await fetch("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        window.location.href = "/dashboard";
    } else {
        alert("Login failed");
    }
}

async function registerUser(event) {
    event.preventDefault();
    const name = document.getElementById("register-name").value;
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;
    const response = await fetch("/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        window.location.href = "/dashboard";
    } else {
        alert("Registration failed");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadDashboard();
});
