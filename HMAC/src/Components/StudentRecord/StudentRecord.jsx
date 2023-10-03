import  { useEffect, useState } from 'react';
import axios from 'axios';
import "./StudentRecord.css"

const StudentRecord = ()=>{
    const [data, setData] = useState([]);

    useEffect(() => {

      const fetchStudentRecords = async () => {
        try {
          
          const response = await axios.get('http://127.0.0.1:8000/teacher/files/');
  
          if (response.status === 200) {
            setData(response.data);
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
                <th>Roll No</th>
                <th>Student Name</th>
                <th>AI Detection %</th>
                <th>Duplicate Content %</th>
              </tr>
            </thead>
            <tbody>
              {data.map((item, index) => (
                <tr key={item.rollNo} className={index % 2 === 0 ? "even-row" : "odd-row"}>
                  <td>{item.filename}</td>
                  <td>{item.filename}</td>
                  <td>{item.filename}%</td>
                  <td>{item.filename}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
}

export default StudentRecord;



