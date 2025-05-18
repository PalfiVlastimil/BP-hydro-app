import { useState } from "react";
import { postLogin } from "../api"
import { useNavigate } from "react-router-dom";
import { TextField, Button, Typography, Paper, Box } from "@mui/material";
import { useForm } from 'react-hook-form';

function LoginPage() {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const { handleSubmit, register } = useForm();

  const onSubmit = async (data) => {
    //e.preventDefault()
    let email = data.email;
    let username = data.username;
    let password = data.password;
    const response = await postLogin({ email, username, password });
    console.log(response)
    if (response?.status == 200) {
      localStorage.setItem("token", response.data.access_token);
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

        <form onSubmit={handleSubmit(onSubmit)}>
          <TextField
            fullWidth
            id="email"
            label="Email"
            variant="outlined"
            margin="normal"
            {...register("email", {
              required: "Email is required."
            })}
          />
          <TextField
            fullWidth
            id="username"
            label="Username"
            variant="outlined"
            margin="normal"
            {...register("username", {
              required: "Username is required."
            })}
          />
          <TextField
            fullWidth
            id="password"
            label="Password"
            type="password"
            variant="outlined"
            margin="normal"
            {...register("password", {
              required: "Password is required."
            })}
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
