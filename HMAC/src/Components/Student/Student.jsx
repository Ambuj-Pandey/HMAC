import React, { useState } from "react";
import Navbar from "../Navbar/Navbar";
import "./Student.css";
import PDF from "../../assets/PDF.png";

const Student = () => {
  const [selectedFile, setSelectedFile] = useState("");
  const [desc, setDesc] = useState("");

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file.name);
  };

  return (
    <>
      <Navbar goTo={'Professor View'} />
      <div className="container">
        <div className="file-upload">
          <label htmlFor="file-input" className="custom-file-upload">
            <img src={PDF} alt="Upload Icon" />
            Upload File
          </label>
          <input
            id="file-input"
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
          />
            <button type="submit" className="submit-button">
                <span>Submit</span>
            </button>
        </div>
        <div className="metaData">
          <label htmlFor="rename">Rename</label>
          <input
            type="text"
            id="rename"
            value={selectedFile} 
            onChange={(e) => setSelectedFile(e.target.value)}
          />
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            value={desc}
            onChange={(e) => setDesc(e.target.value)}
          />
          <label htmlFor="pdf-name" id="pdf-name">PDF Name</label>
          <input value={selectedFile} disabled/>
        </div>
      </div>
    </>
  );
};

export default Student;