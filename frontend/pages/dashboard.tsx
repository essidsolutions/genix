import { useState, useEffect } from "react";
import styles from "../styles/Dashboard.module.css";

interface CloudCostData {
  total_cost: number;
  services: Record<string, number>;
}

export default function Dashboard() {
  const [costData, setCostData] = useState<[string, CloudCostData][]>([]);
  const [selectedProvider, setSelectedProvider] = useState("");

  useEffect(() => {
    fetch(`http://localhost:8000/cloud-cost${selectedProvider ? `?provider=${selectedProvider}` : ""}`)
      .then((res) => res.json())
      .then((data) => {
        if (typeof data === "object" && data !== null) {
          setCostData(Object.entries(data) as [string, CloudCostData][]);
        } else {
          setCostData([]); // Ensure it doesn't crash if data is unexpected
        }
      })
      .catch((error) => {
        console.error("Error fetching cloud cost:", error);
        setCostData([]);
      });
  }, [selectedProvider]);

  return (
    <div className={styles.container}>
      <h1>Cloud Cost Dashboard</h1>
      <select className={styles.selectDropdown} onChange={(e) => setSelectedProvider(e.target.value)}>
        <option value="">All Providers</option>
        <option value="AWS">AWS</option>
        <option value="Azure">Azure</option>
        <option value="GCP">GCP</option>
      </select>
      <div className={styles.costGrid}>
        {costData.length > 0 ? (
          costData.map(([provider, details]) => (
            <div key={provider} className={styles.card}>
              <h2>{provider}</h2>
              <p><strong>Total Cost:</strong> ${details?.total_cost ? details.total_cost.toFixed(2) : "N/A"}</p>
              <ul>
                {details?.services
                  ? Object.entries(details.services).map(([service, cost]) => (
                      <li key={service}>
                        {service}: ${cost ? cost.toFixed(2) : "N/A"}
                      </li>
                    ))
                  : <li>No service data available</li>}
              </ul>
            </div>
          ))
        ) : (
          <p>No data available. Please select a provider or try again later.</p>
        )}
      </div>
    </div>
  );
}
