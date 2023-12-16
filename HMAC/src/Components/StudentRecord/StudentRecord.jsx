import  { useEffect, useState } from 'react';
import axios from 'axios';
import "./StudentRecord.css"

import SlidingIndicator from "../AIGeneratedContent/AIGeneratedContent";

const StudentRecord = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchStudentRecords = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/v1/teacher/files/');

                console.log(response.data);

                if (response.status === 200) {
                    setData(response.data.file_data);
                   
                } else {
                    console.error('Error fetching data:', response.statusText);
                }
            } catch (error) {
                console.error('Network error:', error);
            }
        };

        fetchStudentRecords();
    }, []); 

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
                        <tr key={item.id} className={index % 2 === 0 ? "even-row" : "odd-row"}>
                            <td>{item.uploaded_by.email}</td>
                            <td>{item.filename}</td>
                            <td><SlidingIndicator value={item.user_aidetection_results[0].detection_results_AI.toFixed(2)}></SlidingIndicator></td>
                            <td>
                                <SlidingIndicator
                                    value={item.max_similarity} /></td>
                           
                            <td>{item.other_file_names}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default StudentRecord;
