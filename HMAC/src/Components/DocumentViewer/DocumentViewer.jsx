import React from "react";
import "./DocumentViewer.css";

const DocumentViewer = ({ pdfUrl }) => {
  return (
    <div className="document-container">
      <div className="document-frame">
        <iframe src={pdfUrl+"#toolbar=0&navpanes=0"} title="Document Viewer" />
      </div>
    </div>
  );
};

export default DocumentViewer;
