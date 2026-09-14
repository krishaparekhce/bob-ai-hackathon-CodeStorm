
async function loadDashboard() {
    const readiness = await (await fetch("/api/readiness")).json();
    const risks = await (await fetch("/api/risk")).json();
    const maintenance = await (await fetch("/api/maintenance")).json();

    document.getElementById("total").textContent = readiness.length;

    document.getElementById("ready").textContent =
        readiness.filter(x => x.readiness === "READY").length;

    document.getElementById("caution").textContent =
        readiness.filter(x => x.readiness === "CAUTION").length;

    document.getElementById("notReady").textContent =
        readiness.filter(x => x.readiness === "NOT READY").length;

    const table = document.getElementById("assetTable");

    readiness.forEach((asset, index) => {
        const risk = risks[index];
        const maintenanceData = maintenance[index];

        const row = document.createElement("tr");

        let statusClass = asset.readiness.replace(" ", "");

        row.innerHTML = `
            <td>
                <strong>${asset.asset_id}</strong><br>
                ${asset.asset_name}
            </td>

            <td class="${statusClass}">
                ${asset.readiness}
            </td>

            <td>
                ${risk.risk_level}
            </td>

            <td>
                ${risk.risk_score}/100
            </td>

            <td>
                ${asset.issues.length
                    ? asset.issues.join("<br>")
                    : "No issues detected"}
            </td>

            <td>
                ${maintenanceData.recommendations.join("<br>")}
            </td>
        `;

        row.onclick = () => showDetails(
            asset,
            risk,
            maintenanceData
        );

        table.appendChild(row);
    });
}


function showDetails(asset, risk, maintenance) {

    alert(
        "MISSIONGUARD AI\n\n" +
        asset.asset_id + " — " + asset.asset_name +
        "\n\nREADINESS: " + asset.readiness +
        "\nRISK: " + risk.risk_level +
        " (" + risk.risk_score + "/100)" +
        "\n\nWHY?\n" +
        (asset.issues.length
            ? asset.issues.join("\n")
            : "No abnormal conditions detected") +
        "\n\nRECOMMENDED ACTIONS\n" +
        maintenance.recommendations.join("\n")
    );
        const highRisk = risks
        .filter(x => x.risk_level === "HIGH")
        .sort((a, b) => b.risk_score - a.risk_score);

    document.getElementById("priority").innerHTML =
        highRisk.length
        ? "<strong>Priority Assets:</strong> " +
          highRisk.map(x =>
              x.asset_id + " — " + x.asset_name +
              " (" + x.risk_score + "/100)"
          ).join(" | ")
        : "No high-risk assets detected.";
}


loadDashboard();
