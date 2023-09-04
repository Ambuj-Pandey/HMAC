import React from "react";
import "./RegistrationPage.css";
import { Link } from "react-router-dom";

const RegistrationPage = () => {
  return (
    <div className="registration-container">
      <div className="registration-box">
        <h2>Register</h2>
        <form>
          <div className="inputBox">
            <input type="text" required="required" />
            <span>Full Name</span>
          </div>

          <div className="inputBox">
            <input type="text" required="required" />
            <span>Email</span>
          </div>

          <div className="inputBox">
            <input type="password" required="required" />
            <span>Password</span>
          </div>

          <div className="inputBox">
            <input type="password" required="required" />
            <span>Confirm Password</span>
          </div>

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
