import React, { useEffect, useState } from "react";
import axios from "axios";
import "./LoginPage.css";

import { Link } from "react-router-dom";

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

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
        { withCredentials: true }
      );

      if (response.status === 200) {
        const data = response.data;
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);

        console.log(data.access_token);

        if (data.is_staff == true) {
          window.location.href = "/Professor";
        } else {
          window.location.href = "/Student";
        }
       
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
