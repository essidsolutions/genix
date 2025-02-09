import { useState } from "react";
import styles from "../styles/Dashboard.module.css";

export default function Dashboard() {
  const [provider, setProvider] = useState("AWS");
  const [clientId, setClientId] = useState("");
  const [clientSecret, setClientSecret] = useState("");
  const [authToken, setAuthToken] = useState("");
  const [message, setMessage] = useState("");

  const handleOAuthConnect = async () => {
    const response = await fetch("http://localhost:8000/oauth/connect", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        provider,
        client_id: clientId,
        client_secret: clientSecret,
        auth_token: authToken,
      }),
    });

    const data = await response.json();
    setMessage(data.message || "Failed to connect");
  };

  return (
    <div className={styles.container}>
      <h1>Cloud Cost Dashboard</h1>
      <p>Connect your cloud provider to fetch real-time cost data.</p>

      <select className={styles.selectDropdown} value={provider} onChange={(e) => setProvider(e.target.value)}>
        <option value="AWS">AWS</option>
        <option value="Azure">Azure</option>
        <option value="GCP">GCP</option>
      </select>

      <input
        className={styles.inputField}
        type="text"
        placeholder="Client ID"
        value={clientId}
        onChange={(e) => setClientId(e.target.value)}
      />
      
      <input
        className={styles.inputField}
        type="password"
        placeholder="Client Secret"
        value={clientSecret}
        onChange={(e) => setClientSecret(e.target.value)}
      />

      <input
        className={styles.inputField}
        type="text"
        placeholder="OAuth Token"
        value={authToken}
        onChange={(e) => setAuthToken(e.target.value)}
      />

      <button className={styles.connectButton} onClick={handleOAuthConnect}>Connect</button>
      {message && <p>{message}</p>}
    </div>
  );
}
