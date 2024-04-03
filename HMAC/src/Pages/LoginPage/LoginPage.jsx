import React, { useEffect, useState } from "react";
import axios from "axios";
import "./LoginPage.css";

import { Link } from "react-router-dom";


const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // useEffect(() => {
  //   users();
  // }, []);

  // let users = async () => {
  //   let response = await fetch("http://127.0.0.1:8000");
  //   let data = await response.json();
  //   console.log(data);
  // };

  // const handleLogin = async (e) => {
  //   e.preventDefault();

  //   const user = {
  //     email: email,
  //     password: password,
  //   };

  //   const requestOptions = {
  //     method: "POST",
  //     headers: {
  //       "Content-Type": "application/json",
  //     },
  //     credentials: "include", // Send credentials with the request
  //     body: JSON.stringify(user),
  //   };

  //   try {
  //     const response = await fetch(
  //       "http://127.0.0.1:8000/login/",
  //       requestOptions
  //     );

  //     if (response.ok) {
  //       // Handle a successful login here
  //       const data = await response.json();
  //       localStorage.setItem("access_token", data.access);
  //       localStorage.setItem("refresh_token", data.refresh);
  //       // Redirect or perform any other actions upon successful login
  //       window.location.href = "/";
  //     } else {
  //       // Handle errors or invalid login credentials here
  //       console.error("Login failed:", response.statusText);
  //     }
  //   } catch (error) {
  //     // Handle network errors here
  //     console.error("Network error:", error);
  //   }
  // };

  const handleLogin = async (e) => {
    e.preventDefault();

    const user = {
      email: email,
      password: password,
    };

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/v1/login/",
        user,
        { withCredentials: true } // Include credentials
      );

      if (response.status === 200) {
        const data = response.data;
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);
        
        console.log(data.access_token);

        if (data.is_staff == true) {
          // Redirect staff users to a staff page
          window.location.href = "/Professor"; 
        
        } else {
          // Redirect regular users to a different page
          window.location.href = "/Student"; 
        }
        // Redirect or perform any other actions upon successful login
        // window.location.href = "/";   ---> this reloads which we dont want
      } else {
        console.error("Login failed:", response.statusText);
      }
    } catch (error) {
      console.error("Network error:", error);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Login</h2>
        <form onSubmit={handleLogin}>
          <div className="inputBox">
            <input
              type="text"
              name="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <span>Email</span>
          </div>

          <div className="inputBox">
            <input
              type="password"
              name="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <span>Password</span>
          </div>

          <button className="submitbutton">login</button>
          <p className="message">
            Not registered? <Link to="/register">Create an account</Link>
          </p>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
