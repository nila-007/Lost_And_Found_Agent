const API = "http://127.0.0.1:8000";


async function reportLost() {

    const data = {
        item_name: document.getElementById("lostName").value,
        description: document.getElementById("lostDescription").value,
        location: document.getElementById("lostLocation").value,
        lost_date_time: document.getElementById("lostDate").value
    };

    const response = await fetch(`${API}/report-lost`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    document.getElementById("lostResult").innerHTML =
        `✅ Lost item reported! Case ID: <b>${result.case_id}</b>`;
}


async function reportFound() {

    const data = {
        item_name: document.getElementById("foundName").value,
        category: document.getElementById("foundCategory").value,
        description: document.getElementById("foundDescription").value,
        location: document.getElementById("foundLocation").value,
        found_date_time: document.getElementById("foundDate").value
    };

    const response = await fetch(`${API}/report-found`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    document.getElementById("foundResult").innerHTML =
        `✅ Found item added! Item ID: <b>${result.item_id}</b>`;
}


async function investigate() {

    const caseId = document.getElementById("caseId").value;

    if (!caseId) {
        document.getElementById("investigationResult").innerHTML =
            `<div class="warning">⚠️ Please enter a Case ID.</div>`;
        return;
    }

    document.getElementById("investigationResult").innerHTML =
        "🤖 LOSTIQ AI is investigating... Please wait.";

    try {

        const response = await fetch(`${API}/ai-investigate/${caseId}`, {
            method: "POST"
        });

        const result = await response.json();

        if (result.error) {
            document.getElementById("investigationResult").innerHTML =
                `<div class="warning">❌ ${result.error}</div>`;
            return;
        }

        const agent = result.agent_result;

        document.getElementById("investigationResult").innerHTML = `
            <div class="success">

                <h3>🤖 AI INVESTIGATION COMPLETE</h3>

                <hr>

                <p>📦 <b>Item:</b> ${agent.item_name}</p>

                <p>📋 <b>Description:</b> ${agent.description}</p>

                <p>🔐 <b>Status:</b> ${agent.status}</p>

                <hr>

                <p>🔎 AI Agent has completed the investigation.</p>

            </div>
        `;

        document.getElementById("verifyCaseId").value = caseId;

    } catch (error) {

        document.getElementById("investigationResult").innerHTML = `
            <div class="warning">
                ❌ Could not connect to LOSTIQ server.
            </div>
        `;

        console.error(error);
    }
}
async function verifyOwnership() {

    const caseId = document.getElementById("verifyCaseId").value;
    const detail = document.getElementById("verifyDetail").value;

    const response = await fetch(`${API}/verify/${caseId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_detail: detail
        })
    });

    const result = await response.json();

    if (result.status === "verified") {

        document.getElementById("verifyResult").innerHTML = `
            <div class="success">
                <h3>✅ OWNERSHIP VERIFIED</h3>
                ${result.message}
            </div>
        `;

    } else {

        document.getElementById("verifyResult").innerHTML = `
            <div class="warning">
                ⚠️ Verification failed. Case remains under verification.
            </div>
        `;
    }
}