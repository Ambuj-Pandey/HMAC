import React, { useEffect, useState } from "react";
import axios from "axios";
import "./LoginPage.css";
import InputWithLabel from "../../Components/InputWithLabel/InputWithLabel";

import { Link } from "react-router-dom";

const LoginPage = () => {
  const [Email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  useEffect(() => {
    users();
  }, []);

  let users = async () => {
    let response = await fetch("http://127.0.0.1:8000")
    let data = await response.json()
    console.log(data)
  }

  // const submit = async (e) => {
  //   e.preventDefault();
  //   const user = {
  //     Email: Email,
  //     password: password,
  //   };
  //   // Create the POST requuest
  //   const { data } = await axios.post(
  //     "http://127.0.0.1:8000/token/",
  //     user,
  //     { headers: { "Content-Type": "application/json" } },
  //     { withCredentials: true }
  //   );

  //   // Initialize the access & refresh token in localstorage.
  //   localStorage.clear();
  //   localStorage.setItem("access_token", data.access);
  //   localStorage.setItem("refresh_token", data.refresh);
  //   axios.defaults.headers.common["Authorization"] = `Bearer ${data["access"]}`;
  //   window.location.href = "/";
  // };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Login</h2>
        <form 
        // onSubmit={submit}
        >
          {/* <InputWithLabel
            type="text"
            id="email"
            name="email"
            label="Email"
            required
          />
          
          <InputWithLabel
            type="password"
            id="password"
            name="password"
            label="Password"
            required
          /> */}

          <div className="inputBox">
            <input
              type="text"
              name="email"
              required
              value={Email}
              // onChange={(e) => setEmail(e.target.value)}
            />
            <span>Email</span>
          </div>

          <div className="inputBox">
            <input
              type="password"
              name="password"
              required
              value={password}
              // onChange={(e) => setPassword(e.target.value)}
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
