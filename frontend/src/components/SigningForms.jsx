import React, { useEffect, useState } from 'react'
import LoginPage from './LoginPage';
import RegisterPage from './RegisterPage';
import { getUserExists } from '../api';

const SigningForms = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("");
  const [userExists, setUserExists] = useState(false)
  const checkUserExists = async () => {
    
    setLoading(true)
    let response = await getUserExists();
    console.log(response)
    if (response?.status == 200){
      setUserExists(response.data.userExists)
    }
    else{
      setError(response.message)
    }
    setLoading(false)
  }
  useEffect(e =>{
    checkUserExists();

  }, [])
  

  if(loading)
    return(
      <div>Loading...</div>
    )
  return userExists == true ? (
    <LoginPage/>
  ) : (
    <RegisterPage setUserExists={setUserExists}/>
  )
  
  
}

export default SigningForms