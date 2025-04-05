import React, { useState, useEffect, useRef } from "react";
import { getAllSensorReports } from "../api"
import { LineChart } from '@mui/x-charts/LineChart';
import { format } from 'date-fns';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Button from '@mui/material/Button';

const ITEM_HEIGHT = 48;

const options = [
  'ph_sensor',
  'ec_sensor',
  'water_temp_sensor',
  'air_temp_sensor',
  'humidity_sensor',
  'water_flow_sensor',
  'tds_sensor',
  'vpd_sensor',
  'water_level_sensor',
  'Pyxis',
];

const Chart = () => {
  const accessToken = localStorage.getItem("token");
  const [sensors, setSensors] = useState({});
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [timeRange, setTimeRange] = useState("7d");

  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  const getCutoffDate = (range) => {
    const now = new Date();
    switch (range) {
      case "2d":
        return new Date(now.setDate(now.getDate() - 2));
      case "7d":
        return new Date(now.setDate(now.getDate() - 7));
      case "1m":
        return new Date(now.setMonth(now.getMonth() - 1));
      case "6m":
        return new Date(now.setMonth(now.getMonth() - 6));
      case "all":
      default:
        return new Date(0); // Unix epoch → include everything
    }
  };
  const filterSensorData = (sensorKey) => {
    const sensor = sensors.result?.[sensorKey];
    if (!sensor) return [];

    const cutoff = getCutoffDate(timeRange);
    const timestamps = sensor.timestamp.map(ts => new Date(ts));

    return timestamps.reduce((acc, ts, i) => {
      if (ts >= cutoff) {
        acc.push(sensor.value[i]);
      }
      return acc;
    }, []);
  };
  const getFilteredTimestamps = () => {
    const sensor = sensors.result?.air_temp_sensor;
    if (!sensor) return [];

    const cutoff = getCutoffDate(timeRange);
    return sensor.timestamp.map(ts => new Date(ts)).filter(ts => ts >= cutoff);
  };

  const sensoDataAll = [
    {
      data: filterSensorData("ph_sensor"),
      showMark: false,
      label: "PH value (pH)"
    },
    {
      data: filterSensorData("ec_sensor"),
      showMark: false,
      label: "EC sensor (mS/cm)"
    },
    {
      data: filterSensorData("water_temp_sensor"),
      showMark: false,
      label: "Water temperature (°C)"
    },
    {
      data: filterSensorData("air_temp_sensor"),
      showMark: false,
      label: "Air temperature (°C)"
    },
    {
      data: filterSensorData("humidity_sensor"),
      showMark: false,
      label: "Humidity (%)"
    },
    {
      data: filterSensorData("water_flow_sensor"),
      showMark: false,
      label: "Water flow (l/min)"
    },
    {
      data: filterSensorData("tds_sensor"),
      showMark: false,
      label: "TDS value (ppm)"
    },
    {
      data: filterSensorData("vpd_sensor"),
      showMark: false,
      label: "VPD value (Pa)"
    },
    {
      data: filterSensorData("water_level_sensor"),
      showMark: false,
      label: "Water level (%)"
    }
  ];



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
    handleAllSensorData();
  }, [])
  return (
    <>
      <select value={timeRange} onChange={(e) => setTimeRange(e.target.value)}>
        <option value="2d">LAST 2 DAYS</option>
        <option value="7d">LAST WEEK</option>
        <option value="1m">LAST MONTH</option>
        <option value="6m">LAST 6 MONTHS</option>
        <option value="all">ALL</option>
      </select>
      <div id="sensor-data-chart-center">
      {
        
        sensors?.result?.air_temp_sensor ? (
          <LineChart id="sensor-data-chart"
            
            xAxis={
              [
                {
                  data: getFilteredTimestamps(),
                  scaleType: 'time',
                  valueFormatter: (value) => format(value, 'MMM d'), // or 'MMM d, HH:mm'
                  label: 'Time'
                }
              ]}
              series={sensoDataAll}
              width={1200}
              height={400}
              slotProps={{
                legend: {
                  direction: 'row', // horizontal legend
                  position: { vertical: 'top', horizontal: 'center' }, // adjust as needed
                  padding: 10,
                  itemGap: 24, // <-- THIS creates spacing between items
                },
              }}
              />
        ) : (
          <div>Loading chart...</div>
        )
      }
      </div>
    </>
  )
}

export default Chart