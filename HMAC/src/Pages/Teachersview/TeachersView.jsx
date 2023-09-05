import React from "react";
import "./TeachersView.css";
import documentUrl from "../../assets/lorem_pdf.pdf";

import Navbar from "../../Components/Navbar/Navbar";
import DocumentViewer from "../../Components/DocumentViewer/DocumentViewer";
import SlidingIndicator from "../../Components/AIGeneratedContent/AIGeneratedContent";
import DuplicateDetection from "../../Components/DuplicateDetection/DuplicateDetection"; // Import the DuplicateDetection component

const TeachersView = () => {
  return (
    <>
      <Navbar goTo="Student's View"/>

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
          <h4 className="name-title">PDF Name</h4>
          <div className="pdf-name-field">
            <span> pdfname.pdf</span>
          </div>

          <h4 className="desc-title">Desc</h4>
          <div className="pdf-desc-field">
            <p>
              {" "}
              Lorem Ipsum is simply dummy text of the printing and typesetting
              industry. Lorem Ipsum has been the industry's standard dummy text
              ever since the 1500s.{" "}
            </p>
          </div>

          <SlidingIndicator />

          <DuplicateDetection />
        </div>
      </div>
    </>
  );
};

export default TeachersView;
