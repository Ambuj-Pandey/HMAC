import React from "react";
import "./TeachersView.css";
import documentUrl from "../../assets/lorem_pdf.pdf";

import DocumentViewer from "../../Components/DocumentViewer/DocumentViewer";

const TeachersView = () => {
  return (
    <>
      <div className="teacher-view-Left-container">
        <div className="teacher-view">
          <DocumentViewer pdfUrl={documentUrl} />
        </div>
        <div className="button-container">
          <button className="custom-button">Result</button>
          <button className="custom-button">Explanation</button>
        </div>
      </div>
    
      <div className="teacher-view-Right-container">
        <div className="teacher-analysis">
            
        </div>
      </div>

    </>
  );
};

export default TeachersView;
