import React, { useState, useEffect } from "react";
import { Card, CardContent, Typography, Button, Grid } from "@mui/material"; // Import Grid here
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";
import { useNavigate } from "react-router-dom";
const Dashboard = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate()
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
        const response = await postLogin({ username, password });
        console.log(response); // Log the response properly

        // Since Axios automatically parses JSON, response.data contains the actual data
        const data = response.data;

        if (response.status === 200) { // Ensure response status is checked correctly
            localStorage.setItem("token", data.access_token);
            navigate("/dashboard"); // Redirect after login
        } else {
            setError("Invalid credentials");
        }
    } catch (error) {
        console.error("Login failed:", error);
        setError("Login failed. Please try again.");
    }
};
  const handleLogout = () => setIsAuthenticated(false);

  return (
    <div style={{ padding: "24px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
        <Typography variant="h4">Sensor Dashboard</Typography>
        <Button variant="contained" color="secondary" onClick={handleLogout}>Logout</Button>
      </div>
      <Grid container spacing={2}>
        {/* Card 1 */}
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">pH Value</Typography>
              <Typography variant="h4" color="primary">7.4</Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Card 2 */}
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">EC Value</Typography>
              <Typography variant="h4" color="primary">1.2</Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Card 3 */}
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">Water Temperature</Typography>
              <Typography variant="h4" color="primary">22°C</Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Card 4 */}
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">Air Temperature</Typography>
              <Typography variant="h4" color="primary">24°C</Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Card 5 */}
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">Humidity</Typography>
              <Typography variant="h4" color="primary">60%</Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Card 6 */}
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">Water Flow</Typography>
              <Typography variant="h4" color="primary">2.5 L/min</Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Card 7 */}
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">TDS (ppm)</Typography>
              <Typography variant="h4" color="primary">450</Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Card 8 */}
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">VPD</Typography>
              <Typography variant="h4" color="primary">1.2</Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Card 9 */}
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">Water Level</Typography>
              <Typography variant="h4" color="primary">75%</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
};

export default Dashboard;