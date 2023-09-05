import React from "react";
import "./RegistrationPage.css";
import InputWithLabel from "../../Components/InputWithLabel/InputWithLabel";

import { Link } from "react-router-dom";

const RegistrationPage = () => {
  return (
    <div className="registration-container">
      <div className="registration-box">
        <h2>Register</h2>

        <form>

          <InputWithLabel
            type="text"
            id="fullName"
            name="fullName"
            label="Full Name"
            required
          />

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
          
          <InputWithLabel
            type="password"
            id="confirmPassword"
            name="confirmPassword"
            label="Confirm Password"
            required
          />

          <button className="submitbutton">Register</button>
          <p className="message">
            Already registered? <Link to="/">Login</Link>
          </p>
        </form>
      </div>
    </div>
  );
};

export default RegistrationPage;
