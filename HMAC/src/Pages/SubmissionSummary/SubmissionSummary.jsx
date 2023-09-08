import "./SubmissionSummary.css";
import Navbar from "../../Components/Navbar/Navbar";
import StudentRecord from "../../Components/StudentRecord/StudentRecord";
const SubmissionSummary = () => {
  return (
    <div className="submission-container">
      <Navbar goTo="Student"></Navbar>
      <div className="submission-bg-container">
        <StudentRecord />
      </div>
    </div>
  );
};

export default SubmissionSummary;
