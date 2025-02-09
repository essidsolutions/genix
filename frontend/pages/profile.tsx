import { useState } from "react";
import styles from "../styles/Profile.module.css";

export default function Profile() {
  const [provider, setProvider] = useState("AWS");
  const [message, setMessage] = useState("");

  const handleOAuthConnect = async () => {
    const response = await fetch("http://localhost:8000/oauth/connect", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ provider, auth_token: "fake_token" })
    });
    const data = await response.json();
    setMessage(data.message || "Failed to connect");
  };

  return (
    <div className={styles.container}>
      <h1>Profile</h1>
      <p>Connect your cloud provider to fetch real-time cost data.</p>
      <select className={styles.selectDropdown} value={provider} onChange={(e) => setProvider(e.target.value)}>
        <option value="AWS">AWS</option>
        <option value="Azure">Azure</option>
        <option value="GCP">GCP</option>
      </select>
      <button className={styles.connectButton} onClick={handleOAuthConnect}>Connect</button>
      {message && <p>{message}</p>}
    </div>
  );
}