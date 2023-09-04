import React from "react";
import "./DocumentViewer.css";
import { Document, Page } from "react-pdf";

const DocumentViewer = ({ pdfUrl }) => {
  return (
    <div className="document-container">
      <div className="document-frame">
        <iframe src={pdfUrl} title="Document Viewer" />
        {/* <Document className="pdf" file={pdfUrl}>
          <Page pageNumber={1} />
        </Document> */}
      </div>
    </div>
  );
};

export default DocumentViewer;
