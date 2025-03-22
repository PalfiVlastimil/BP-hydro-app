import { useState } from "react";
import {postLogin} from "../api"
import { useNavigate } from "react-router-dom";
function LoginPage() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault()
    const response = await postLogin({username, password})
    const data = await response.data;
    console.log(response)
    if (response?.status == 200) {
      console.log("Hello?")
      localStorage.setItem("token", data.access_token);
      navigate("/dashboard"); // Redirect after login
    } else {
      setError(response.message);
    }

  };

  return (
    <form onSubmit={handleLogin}>
      <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button type="submit">Login</button>
      {error && <p>{error}</p>}
    </form>
  );
}

export default LoginPage;
