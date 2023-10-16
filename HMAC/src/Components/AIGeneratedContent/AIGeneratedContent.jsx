import React, { useState, useEffect } from "react";
import "./AIGeneratedContent.css"; 

const SlidingIndicator = ({value}) => {
  const [responseRate, setResponseRate] = useState(1); // Set an initial non-zero value

  useEffect(() => {
    // Set the initial random value when the component mounts
    setResponseRate(value);
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
      {/* <div className="text">AI Generated Content</div> */}
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
