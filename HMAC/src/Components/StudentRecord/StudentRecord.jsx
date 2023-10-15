import  { useEffect, useState } from 'react';
import axios from 'axios';
import "./StudentRecord.css"

const StudentRecord = () => {
    const [data, setData] = useState([]);
    const [maxSimilarities, setMaxSimilarities] = useState({});

    useEffect(() => {
        const fetchStudentRecords = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/teacher/files/');

                console.log(response.data);

                if (response.status === 200) {
                    setData(response.data.file_data);
                    setMaxSimilarities(response.data.max_similarities);
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
                        <th>AI Detection %</th>
                        <th>Duplicate Content %</th>
                        <th>with</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((item, index) => (
                        <tr key={item.id} className={index % 2 === 0 ? "even-row" : "odd-row"}>
                            <td>{item.uploaded_by_info.full_name}</td>
                            <td>{item.filename}</td>
                            <td>-</td>
                            <td>{item.max_similarity}</td>
                            <td>{item.other_file_names}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default StudentRecord;
