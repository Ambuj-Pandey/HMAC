import { useEffect, useState } from "react";
import axios from "axios";
import "./StudentRecord.css";

import SlidingIndicator from "../AIGeneratedContent/AIGeneratedContent";

import { Link } from "react-router-dom";

const StudentRecord = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchStudentRecords = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8000/api/v1/teacher/files/"
        );

        console.log(response.data);

        if (response.status === 200) {
          setData(response.data.file_data);
        } else {
          console.error("Error fetching data:", response.statusText);
        }
      } catch (error) {
        console.error("Network error:", error);
      }
    };

    fetchStudentRecords();
  }, []);

  const cropFilename = (filename) => {
    const index = filename.indexOf('.');
    return index !== -1 ? filename.substring(0, index) : filename;
  };

  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Student Name</th>
            <th>File Name</th>
            <th>AI Detection </th>
            <th>Duplicate Content</th>
            <th>Max Similarity Found with</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr
              key={item.id}
              className={index % 2 === 0 ? "even-row" : "odd-row"}
            >
              <td> <Link to={`/OcrResult/${item.uploaded_by.user_id}`}>{item.uploaded_by.username}</Link></td>
              <td>{cropFilename(item.filename)}</td>
              <td>
                <SlidingIndicator className="ai-detection-indicator" 
                  value={item.user_aidetection_results[0].detection_results_AI.toFixed(
                    2
                  )}
                ></SlidingIndicator>
              </td>
              <td>
                <SlidingIndicator value={item.max_similarity} />
              </td>

              <td> {item.other_file_names.map((otherFileName) => (
                  <div key={otherFileName}>{cropFilename(otherFileName)}</div>
                ))}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StudentRecord;
