// Create modal automatically
const modal = document.createElement("div");
modal.id = "detail-modal";
modal.className = "modal-overlay";

modal.innerHTML = `
    <div class="modal-card">
        <button class="modal-close" onclick="closeModal()">&times;</button>
        <h2 id="modal-title"></h2>

        <div class="modal-row">
            <span class="modal-label">Readiness</span>
            <span id="modal-readiness" class="modal-status"></span>
        </div>

        <div class="modal-row">
            <span class="modal-label">Risk</span>
            <span id="modal-risk"></span>
        </div>

        <div class="modal-section">
            <h4>Contributing Issues</h4>
            <ul id="modal-issues"></ul>
        </div>

        <div class="modal-section">
            <h4>Recommended Actions</h4>
            <ul id="modal-actions"></ul>
        </div>
    </div>
`;

document.body.appendChild(modal);


function openModal(asset, risk, maintenance) {

    const issueHtml = asset.issues.length
        ? asset.issues.map(i => `<li>${i}</li>`).join("")
        : "<li>No abnormal conditions detected</li>";

    const actionHtml = maintenance.recommendations.length
        ? maintenance.recommendations.map(r => `<li>${r}</li>`).join("")
        : "<li>Continue routine monitoring</li>";

    document.getElementById("modal-title").textContent =
        asset.asset_id + " — " + asset.asset_name;

    const readiness = document.getElementById("modal-readiness");

    readiness.textContent = asset.readiness;
    readiness.className =
        "modal-status " + asset.readiness.replace(/\s+/g, "_");

    document.getElementById("modal-risk").textContent =
        risk.risk_level + " (" + risk.risk_score + " / 100)";

    document.getElementById("modal-issues").innerHTML = issueHtml;
    document.getElementById("modal-actions").innerHTML = actionHtml;

    document.getElementById("detail-modal").classList.add("open");
}


function closeModal() {
    document.getElementById("detail-modal").classList.remove("open");
}


modal.addEventListener("click", function (e) {
    if (e.target === modal) {
        closeModal();
    }
});


async function loadDashboard() {

    let readiness, risks, maintenance;

    try {

        const [rRes, skRes, mRes] = await Promise.all([
            fetch("/api/readiness"),
            fetch("/api/risk"),
            fetch("/api/maintenance")
        ]);

        if (!rRes.ok || !skRes.ok || !mRes.ok) {
            throw new Error("One or more API requests failed.");
        }

        readiness = await rRes.json();
        risks = await skRes.json();
        maintenance = await mRes.json();

    } catch (err) {

        document.getElementById("priority").innerHTML =
            "<strong style='color:red'>Failed to load dashboard data. " +
            "Please check the server and try again.</strong>";

        console.error("MissionGuard AI load error:", err);
        return;
    }


    // Summary
    document.getElementById("total").textContent = readiness.length;

    document.getElementById("ready").textContent =
        readiness.filter(x => x.readiness === "READY").length;

    document.getElementById("caution").textContent =
        readiness.filter(x => x.readiness === "CAUTION").length;

    document.getElementById("notReady").textContent =
        readiness.filter(x => x.readiness === "NOT READY").length;


    // Maps
    const riskMap = Object.fromEntries(
        risks.map(r => [r.asset_id, r])
    );

    const maintenanceMap = Object.fromEntries(
        maintenance.map(m => [m.asset_id, m])
    );


    // Priority assets
    const highRisk = risks
        .filter(x => x.risk_level === "HIGH")
        .sort((a, b) => b.risk_score - a.risk_score);

    const priorityEl = document.getElementById("priority");

    if (highRisk.length) {

        const items = highRisk.map(x => `
            <div class="priority-item">
                <span class="priority-id">${x.asset_id}</span>
                <span class="priority-name">${x.asset_name}</span>
                <span class="priority-score">${x.risk_score}/100</span>
                <span class="priority-badge">HIGH RISK</span>
            </div>
        `).join("");

        priorityEl.innerHTML = `
            <h3 class="priority-heading">
                ⚠ Priority Assets Requiring Attention
            </h3>
            <div class="priority-list">${items}</div>
        `;

    } else {

        priorityEl.innerHTML =
            `<p class="priority-none">✓ No high-risk assets detected.</p>`;
    }


    // Asset table
    const table = document.getElementById("assetTable");

    table.innerHTML = "";

    readiness.forEach(asset => {

        const risk = riskMap[asset.asset_id];
        const maintenanceData = maintenanceMap[asset.asset_id];

        if (!risk || !maintenanceData) return;

        const statusClass =
            asset.readiness.replace(/\s+/g, "_");

        const row = document.createElement("tr");

        row.className = "clickable-row";
        row.title = "Click for details";

        row.innerHTML = `
            <td>
                <strong>${asset.asset_id}</strong><br>
                ${asset.asset_name}
            </td>

            <td class="${statusClass}">
                ${asset.readiness}
            </td>

            <td>${risk.risk_level}</td>

            <td>${risk.risk_score}/100</td>

            <td>
                ${asset.issues.length
                    ? asset.issues.join("<br>")
                    : "No issues detected"}
            </td>

            <td>
                ${maintenanceData.recommendations.join("<br>")}
            </td>
        `;

        row.addEventListener("click", function () {
            openModal(asset, risk, maintenanceData);
        });

        table.appendChild(row);
    });
}


loadDashboard();
