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