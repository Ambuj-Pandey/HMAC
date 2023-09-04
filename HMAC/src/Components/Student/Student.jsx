import React from "react";
import { useState } from "react";
import Navbar from "../Navbar/Navbar";
import "./Student.css"
import PDF from "../../assets/PDF.png"

const Student = () =>{
    const [selectedFile, setSelectedFile] = useState(null);

    const handleFileChange = (e) => {
      const file = e.target.files[0];
      setSelectedFile(file.name);
    };

    return(
        <>
        <Navbar goTo={'Professor View'}/>
        <div className="container">
            <div className="file-upload">
                <label htmlFor="file-input" className="custom-file-upload">
                    <img src={PDF} alt="Upload Icon" />
                    Upload File
                </label>
                <input id="file-input" type="file" accept=".pdf" onChange={handleFileChange} />
            </div>
            {/* <div className="metaData">
                <label>Rename</label>
                <input value={selectedFile} onChange={ (e)=> setSelectedFile(e.target.value)}/>
                <label>Description</label>
                <textarea />
            </div> */}
        </div>

        </>
    )
}

export default Student;