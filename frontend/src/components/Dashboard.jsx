import React, { useState, useEffect, useRef } from "react";
import { Card, CardContent, Typography, Button, Box } from "@mui/material"; // Import Grid here
import Grid from '@mui/material/Grid2';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";
import { getSensorData, sendSensorData, getLatestImageFile, captureImageFile } from "../api"
import { useNavigate } from "react-router-dom";
import { toast, Bounce } from 'react-toastify';


const Dashboard = () => {
  const accessToken = localStorage.getItem("token");
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [imgSrc, setImgSrc] = useState("");
  const [sensors, setSensors] = useState(
    {
      "ph_sensor": {},
      "ec_sensor": {},
      "water_temp_sensor": {},
      "air_temp_sensor": {},
      "humidity_sensor": {},
      "water_flow_sensor": {},
      "tds_sensor": {},
      "vpd_sensor": {},
      "water_level_sensor": {},
    }

  );
  const showTokenExpireToast = async (message) => {
    toast.error(message, {
      position: "top-right",
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: false,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "dark",
      transition: Bounce,
    });
    localStorage.removeItem("token")
    navigate("/login")
  }
  const showSuccessToast = async (message) => {
    toast.success(message, {
      position: "top-right",
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: false,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "dark",
      transition: Bounce,
    });
  }
  const logoutButton = async () => {
    localStorage.removeItem("token");
    navigate("/login")
    showSuccessToast("Successfully logged out")
  }
  const sendSensorDataButton = async () => {
    const response = await sendSensorData({ accessToken });
    if (response.status == 201) {
      showSuccessToast("Data successfuly requested")
    }
    if (response.msg == "Token has expired") {
      showTokenExpireToast(response.msg)
    }
    console.log(response)
    

  }
  const sendImageDataButton = async () => {
    const response = await captureImageFile({ accessToken })
    console.log(response)
    if (response.status == 201) {
      showSuccessToast("Data successfuly requested")
    }
    if (response.msg == "Token has expired") {
      showTokenExpireToast(response.msg)
    }

  }
  const handleSensors = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getSensorData({ accessToken });
      console.log(response);
      const data = response.data;

      if (response?.status == 200) {

        const sensorMapping = { ...sensors };

        data.sensors.forEach((sensor, index) => {
          if (sensorMapping[sensor.sensor_id]) {
            Object.assign(sensorMapping[sensor.sensor_id], sensor.report);
          }
          else {
            console.warn(`Sensor "${sensor.sensor_id}" not found.`);
          }
        });
        console.log(sensorMapping);
        setSensors(sensorMapping);
        console.log(sensors);
      }
      else if (response.msg == "Token has expired") {
        showTokenExpireToast(response.msg)
      }
      else {
        setError(response.message);
      }
    }
    catch (err) {
      setError(err.message);
    }
    finally {
      setLoading(false);
    }
  };
  const handleImage = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getLatestImageFile({ accessToken });


      if (response?.status == 200) {
        setImgSrc(`data:image/jpeg;base64,${response.data.data}`);
      }
      else if (response.msg == "Token has expired") {
        showTokenExpireToast(response.msg)
      }
      else {
        setError(response.message);
      }
    }
    catch (err) {
      setError(err.message);
    }
    finally {
      setLoading(false);
    }

  }
  useEffect(() => {
    handleSensors();
    handleImage();
  }, [accessToken])

  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        background: "radial-gradient(circle, rgba(16,51,152,1) 0%, rgba(17,14,59,1) 50%, rgba(13,13,56,1) 95%);", // Blue gradient
      }}
    >

      <div style={{ padding: "24px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
          <Typography variant="h4">Sensor Dashboard</Typography>
          <Button variant="contained" color="secondary" onClick={logoutButton}>Logout</Button>
        </div>
        <Grid container spacing={2}>
          {Object.keys(sensors).map((sensorKey) => {
            const sensorData = sensors[sensorKey]; // Access the sensor data by key
            const sensorValue = sensorData.value || 0; // Example of extracting a specific property from sensor data, defaulting to 0 if not present
            const sensorUnit = sensorData.unit || 0;
            const sensorTime = sensorData.timestamp

            return (
              <Grid item size={{ xs: 12, md: 4, sm: 6 }} key={sensorKey}>
                <Card>
                  <CardContent>
                    <Typography variant="h6">{sensorKey}</Typography>
                    <Typography variant="h4" color="primary">{sensorValue.toFixed(2)} {sensorUnit}</Typography>
                    <Typography variant="h7" color="primary">{sensorTime}</Typography>
                  </CardContent>
                </Card>
              </Grid>
            );
          })}
        </Grid>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
          <Button variant="contained" color="secondary" onClick={sendSensorDataButton}>Request sensor data</Button>
          <Button variant="contained" color="secondary" onClick={sendImageDataButton}>Request new image</Button>
        </div>
        <Typography variant="h4">Camera</Typography>
        <img id="latest-image" src={imgSrc} alt="Latest Image" width="500"></img>
      </div>
    </Box>
  );
};

export default Dashboard;