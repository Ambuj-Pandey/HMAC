import React from "react";
import "./DocumentViewer.css";


const DocumentViewer = ({ pdfUrl }) => {
  return (
    <div className="document-container">
      <div className="document-frame">
        <iframe src={pdfUrl} title="Document Viewer" />
      </div>
    </div>
  );
};

export default DocumentViewer;
