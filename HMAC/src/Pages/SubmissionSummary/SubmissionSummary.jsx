import "./SumbissionSummary.css";
import Navbar from "../../Components/Navbar/Navbar";
import StudentRecord from "../../Components/StudentRecord/StudentRecord";
const SubmissionSummary = () => {
  return (
    <div className="submission-container">
      <Navbar goTo="Student"></Navbar>
      <div className="submission-bg-container">
        <div className="submission-column-header">
          <li>Roll No.</li>
          <li>Student Name</li>
          <li>AI content %</li>
          <li>Duplicate content %</li>
        </div>
        <StudentRecord />
      </div>
    </div>
  );
};

export default SubmissionSummary;
