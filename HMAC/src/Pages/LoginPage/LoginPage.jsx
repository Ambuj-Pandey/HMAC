import React from "react";
import "./LoginPage.css";
import InputWithLabel from "../../Components/InputWithLabel/InputWithLabel";

import { Link } from "react-router-dom";

const LoginPage = () => {
  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Login</h2>
        <form>

          <InputWithLabel
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
          />

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
