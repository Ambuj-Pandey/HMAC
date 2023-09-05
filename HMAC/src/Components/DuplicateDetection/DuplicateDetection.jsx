import React, { useState, useEffect } from "react";
import "./DuplicateDetection.css"; // Create or import a CSS file for styling

const DuplicateDetection = () => {
  const [duplicateRate, setDuplicateRate] = useState(1); // Set an initial non-zero value

  // Function to generate a random initial value between 0 and 100
  const getRandomInitialValue = () => {
    return Math.floor(Math.random() * 101); // Generates a random number between 0 and 100
  };

  useEffect(() => {
    // Set the initial random value when the component mounts
    setDuplicateRate(getRandomInitialValue());
  }, []); // Empty dependency array to run this effect only once

  // Define a CSS variable to set the keyframes width
  const animationWidth = `${Math.min(duplicateRate, 100)}%`;

  // Dynamically calculate the progress bar color based on duplicateRate
  const progressBarColor = () => {
    if (duplicateRate >= 75) {
      return "red";
    } else if (duplicateRate >= 50) {
      return "orange";
    }
    return "#43A047"; // Default color when duplicateRate < 50
  };

  return (
    <div className="duplicate-detection-container">
      <div className="text">Duplicate Detection</div>
      <div className="progress-bar">
        <div
          className={`progress${duplicateRate > 0 ? " animate" : ""}`}
          style={{ width: animationWidth, backgroundColor: progressBarColor() }}
        >
          {duplicateRate > 0 && (
            <div className="percent-text">{duplicateRate}%</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DuplicateDetection;
