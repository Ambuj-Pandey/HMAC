import React, { useState } from "react";
import "./Navbar.css";
import collegeLogo from "../../assets/college_logo.png";
import { Link } from "react-router-dom";

const Navbar = ({ goTo }) => {
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  return (
    <div className={`header ${menuOpen ? "menu-open" : ""}`}>
      <div className="logoDiv">
        <img className="logo" src={collegeLogo} alt="College Logo" />
      </div>

      <div className="hamburger" onClick={toggleMenu}>
        <div className={`bar ${menuOpen ? "active" : ""}`}></div>
        <div className={`bar ${menuOpen ? "active" : ""}`}></div>
        <div className={`bar ${menuOpen ? "active" : ""}`}></div>
      </div>

      <nav className={`navbar ${menuOpen ? "open" : ""}`}>
        <div className="menu">
          <li className="listitem">
            <a href="#">Upload</a>
          </li>
          <li className="listitem">
            <a href="#">something/remove</a>
          </li>
          <li className="listitem">
            <a href="#">How to Use</a>
          </li>
          <li className="listitem">
            <a href="#">Contact</a>
          </li>
          <li className="listitem">
            {goTo === "Professor View" ? (
              <Link to="/teachersview">{goTo}</Link>
            ) : (
              <Link to="/student">{goTo}</Link>
            )}
          </li>
        </div>
      </nav>
      <div className="signUp">
        <div className="text">Sign Up</div>
      </div>
    </div>
  );
};

export default Navbar;
