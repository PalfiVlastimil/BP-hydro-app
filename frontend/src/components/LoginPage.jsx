import { useState } from "react";
import { postLogin } from "../api"
import { useNavigate } from "react-router-dom";
import { TextField, Button, Typography, Paper, Box } from "@mui/material";
function LoginPage() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault()
    const response = await postLogin({ username, password })
    const data = await response.data;
    console.log(response)
    if (response?.status == 200) {
      localStorage.setItem("token", data.access_token);
      navigate("/dashboard"); // Redirect after login
    } else {
      setError(response.message);
    }
  };

  return (

    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "radial-gradient(circle, rgba(16,51,152,1) 0%, rgba(17,14,59,1) 50%, rgba(13,13,56,1) 95%);", // Blue gradient
      }}
    >
      <Paper
        elevation={6}
        sx={{
          padding: 4,
          width: 320,
          textAlign: "center",
          borderRadius: 3,
        }}
      >
        <Typography variant="h5" color="primary" gutterBottom>
          Login
        </Typography>

        <form onSubmit={handleLogin}>
          <TextField
            fullWidth
            label="Username"
            variant="outlined"
            margin="normal"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <TextField
            fullWidth
            label="Password"
            type="password"
            variant="outlined"
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          {error && (
            <Typography color="error" variant="body2" sx={{ mt: 1 }}>
              {error}
            </Typography>
          )}

          <Button
            type="submit"
            variant="contained"
            color="secondary"
            fullWidth
            sx={{ mt: 2, borderRadius: 2 }}
          >
            Login
          </Button>
        </form>
      </Paper>
    </Box>
  );
}

export default LoginPage;
