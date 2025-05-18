import React, { useState, useEffect, useRef } from "react";
import { Card, CardContent, Typography, Button, Box } from "@mui/material"; // Import Grid here
import Grid from '@mui/material/Grid2';
import { getSensorData, sendSensorData, getLatestImageFile, captureImageFile, getAllSensorReports } from "../api"
import { useNavigate } from "react-router-dom";
import Chart from "./Chart";
import { showTokenExpireToast, showSuccessToast } from "./toasts";


const Dashboard = () => {
  const accessToken = localStorage.getItem("token");
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [imgSrc, setImgSrc] = useState("");
  const [sensors, setSensors] = useState({});
  const [recSensors, setRecSensors] = useState(
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
  
  const logoutButton = async () => {
    localStorage.removeItem("token");
    navigate("/")
    showSuccessToast("Successfully logged out")
  }
  const sendSensorDataButton = async () => {
    const response = await sendSensorData({ accessToken });
    if (response.status == 201) {
      showSuccessToast("Data successfuly requested")
      await handleSensors();
      await handleAllSensorData();
    }
    if (response.msg == "Token has expired") {
      localStorage.removeItem("token")
      navigate("/")
      showTokenExpireToast(response.msg)
    }
    console.log(response)


  }
  const sendImageDataButton = async () => {
    const response = await captureImageFile({ accessToken })
    console.log(response)
    if (response.status == 201) {
      showSuccessToast("Data successfuly requested")
      await handleImage()
    }
    if (response.msg == "Token has expired") {
      localStorage.removeItem("token")
      navigate("/")
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

        const sensorMapping = { ...recSensors };

        data.sensors.forEach((sensor, index) => {
          sensorMapping[sensor.sensor_id] = { ...sensor.report };
        });
        console.log(sensorMapping);
        setRecSensors(sensorMapping);
        console.log(recSensors);
      }
      else if (response.msg == "Token has expired") {
        localStorage.removeItem("token")
        navigate("/")
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
        localStorage.removeItem("token")
        navigate("/")
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
    const handleAllSensorData = async () => {
    setLoading(true);
    setError(null);
    const response = await getAllSensorReports({ accessToken });
    console.log(response)
    try {
      if (response?.status == 200) {
        setSensors(response.data)
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
    handleAllSensorData();
  }, [])

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
        <Grid container spacing={2} >
          {Object.keys(recSensors).map((sensorKey) => {
            const sensorData = recSensors[sensorKey]; // Access the sensor data by key
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
        
        <Typography variant="h4">Sensor Chart</Typography>
        <Chart sensors={sensors}/>
        
        
        <Typography variant="h4">Camera</Typography>
        <img id="latest-image" src={imgSrc} alt="Latest Image" width="800"></img>
      </div>
    </Box>
  );
};

export default Dashboard;