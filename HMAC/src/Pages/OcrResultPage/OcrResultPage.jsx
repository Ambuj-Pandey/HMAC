import React, { useEffect, useState } from "react";
import "./OcrResult.css";
import { useParams } from "react-router-dom";
import axios from "axios";

const OcrResultPage = () => {
  const { id } = useParams();
  const [ocrData, setOcrData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOcrResult = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/api/v1/results/${id}`
        );
        console.log(response.data);

        if (response.status === 200) {
          setOcrData(response.data);
          setLoading(false);
        } else {
          console.error("Error fetching data:", response.statusText);
        }
      } catch (error) {
        console.error("Network error:", error);
      }
    };

    fetchOcrResult();
  }, [id]);

  return (
    <div className="OcrContainer">
      {loading ? (
        <div className="loading">
          <div className="spinner"></div>
        </div>
      ) : (
        <>
          {ocrData && (
            <div>
              <h1 className="OcrHeader">Ocr Result for ID: {ocrData.id}</h1>
              <div>
                <h3 className="OcrSubheader">
                  Uploaded By: {ocrData.uploaded_by}
                </h3>
                <p className="OcrResults">OCR Results: {ocrData.ocr_results}</p>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default OcrResultPage;
