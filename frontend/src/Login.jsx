import { useState } from "react";
import { local } from "./App";
export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleLogin(e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    try {
    const res = await local.post("/auth/login", formData, {
      headers: { "Content-Type": "multipart/form-data" }
    });

    localStorage.setItem("token", res.data.token);
    window.location.href = "/maintenance";
  } catch (err) {
    setError("Invalid username or password");
  }
}
  return (
    <div>
      <h1>Maintenance Login</h1>

      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />

        <button type="submit" className="submit-btn">Login</button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
