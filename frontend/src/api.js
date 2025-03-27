import axios from 'axios';
const BASE_URL = `http://10.0.1.53:5000`;

export const postLogin = async(userParams) => {
  const {username, password} = userParams;
  try {
    const response = await axios.post(`${BASE_URL}/login`, {
      username,
      password
    },
    {
      headers: {
        'Content-Type': 'application/json',
      }
    }
  );
    // Vrátíme response data
    return response;
  } catch (error) {
    // Vrátíme chybu, pokud k ní dojde
    console.error("Error during login:", error);
    return error.response ? error.response.data : { message: 'Unknown error' };
  }
}
export const getSensorData = async(userParams) => {
  const {accessToken} = userParams;
  try {
    const response = await axios.get(`${BASE_URL}/get_recent_data`, 
    {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      }
    }
  );
    // Vrátíme response se statusem
    return response;
  } catch (error) {
    // Vrátíme chybu, pokud k ní dojde
    console.error("Error during retrieving recent sensor data:", error);
    return error.response ? error.response.data : { message: 'Unknown error' };
  }
}
export const sendSensorData = async(userParams) => {
  const {accessToken} = userParams;
  try {
    const response = await axios.post(`${BASE_URL}/save_sensor_data`,{},
    {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      }
    }
  );
    // Vrátíme response data
    return response;
  } catch (error) {
    // Vrátíme chybu, pokud k ní dojde
    console.error("Error during saving sensor data:", error);
    return error.response ? error.response.data : { message: 'Unknown error' };
  }
}
export const createImageFile = async(userParams) => {
  const {accessToken} = userParams;
  try {
    const response = await axios.post(`${BASE_URL}/create_image`, {
      username,
      password
    },
    {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      }
    }
  );
    // Vrátíme response data
    return response;
  } catch (error) {
    // Vrátíme chybu, pokud k ní dojde
    console.error("Error during creating image:", error);
    return error.response ? error.response.data : { message: 'Unknown error' };
  }
}
export const getImageFile = async(userParams) => {
  const {accessToken} = userParams;
  try {
    const response = await axios.get(`${BASE_URL}/get_image`,
    {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      }
    }
  );
    // Vrátíme response data
    return response;
  } catch (error) {
    // Vrátíme chybu, pokud k ní dojde
    console.error("Error during getting image:", error);
    return error.response ? error.response.data : { message: 'Unknown error' };
  }
}