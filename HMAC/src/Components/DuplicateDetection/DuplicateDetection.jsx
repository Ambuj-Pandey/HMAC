import { useState, useEffect } from "react";
import "./DuplicateDetection.css";

const DuplicateDetection = () => {
  const [duplicateRate, setDuplicateRate] = useState(1); 

  const getRandomInitialValue = () => {
    return Math.floor(Math.random() * 101); 
  };

  useEffect(() => {
    setDuplicateRate(getRandomInitialValue());
  }, []); 

  
  const animationWidth = `${Math.min(duplicateRate, 100)}%`;

 
  const progressBarColor = () => {
    if (duplicateRate >= 75) {
      return "#E76549";
    } else if (duplicateRate >= 50) {
      return "orange";
    }
    return "#43A047"; 
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
