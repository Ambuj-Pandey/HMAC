import "./StudentRecord.css"

const StudentRecord = ()=>{
    const data = [
        { rollNo: 101, name: "John", aiDetectionPercent: 85, duplicatePercent: 10 },
        { rollNo: 102, name: "Alice", aiDetectionPercent: 92, duplicatePercent: 5 },
        { rollNo: 103, name: "Bob", aiDetectionPercent: 78, duplicatePercent: 15 },
        { rollNo: 104, name: "Eve", aiDetectionPercent: 89, duplicatePercent: 8 },
      ];
    
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
                  <td>{item.rollNo}</td>
                  <td>{item.name}</td>
                  <td>{item.aiDetectionPercent}%</td>
                  <td>{item.duplicatePercent}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
}

export default StudentRecord;



