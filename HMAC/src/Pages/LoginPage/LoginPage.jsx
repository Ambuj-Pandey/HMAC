import React from "react";
import "./LoginPage.css";

const LoginPage = () => {
  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Login</h2>
        <form>
        <div class="inputBox">
            <input type="text" required="required"/>
            <span>Email</span>
          </div>
          
          <div class="inputBox">
            <input type="password" required="required"/>
            <span>Password</span>
          </div>

          <button class="submitbutton">login</button>
          <p class="message">Not registered? <a href="{% url 'SignUp' %}">Create an account</a></p>
          
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
