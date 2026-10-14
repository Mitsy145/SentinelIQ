import { useEffect, useState } from "react";

export default function App() {
  const [status, setStatus] = useState("checking...");

  useEffect(() => {
    fetch("/api/v1/health/ready")
      .then((r) => r.json())
      .then((d) => setStatus(d.status))
      .catch(() => setStatus("API unreachable"));
  }, []);

  return (
    <main style={{ fontFamily: "system-ui", padding: 24 }}>
      <h1>SentinelIQ</h1>
      <p>
        API status: <strong>{status}</strong>
      </p>
    </main>
  );
}