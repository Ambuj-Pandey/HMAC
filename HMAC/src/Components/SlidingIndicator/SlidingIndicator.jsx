import React, { useState, useEffect } from "react";
import "./SlidingIndicator.css"; // Create or import a CSS file for styling

const SlidingIndicator = () => {
  const [responseRate, setResponseRate] = useState(1); // Set an initial non-zero value

  // Function to generate a random initial value between 0 and 100
  const getRandomInitialValue = () => {
    return Math.floor(Math.random() * 101); // Generates a random number between 0 and 100
  };

  useEffect(() => {
    // Set the initial random value when the component mounts
    setResponseRate(getRandomInitialValue());
  }, []); // Empty dependency array to run this effect only once
  const animationWidth = `${Math.min(responseRate, 100)}%`;

  const progressBarColor = () => {
    if (responseRate >= 75) {
      return "#E76549";
    } else if (responseRate >= 50) {
      return "orange";
    }
    return "#43A047"; // Default color when responseRate < 50
  };

  return (
    <div className="sliding-indicator-container">
      <div className="text">AI Generated Content</div>
      <div className="progress-bar">
        <div
          className={`progress${responseRate > 0 ? " animate" : ""}`}
          style={{ width: animationWidth, backgroundColor: progressBarColor() }}
        >
          {responseRate > 0 && (
            <div className="percent-text">{responseRate}%</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SlidingIndicator;
