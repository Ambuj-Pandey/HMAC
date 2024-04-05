// import { useState } from "react";
import "./App.css";

import Student from "./Components/Student/Student";
import TeachersView from "./Pages/Teachersview/TeachersView";
import LoginPage from "./Pages/LoginPage/LoginPage";
import RegistrationPage from "./Pages/RegistrationPage/RegistrationPage";
import SubmissionSummary from "./Pages/SubmissionSummary/SubmissionSummary";
import OcrResultPage from "./Pages/OcrResultPage/OcrResultPage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<LoginPage />}></Route>
        <Route exact path="/register" element={<RegistrationPage />}></Route>
        <Route path="/Student" element={<Student />}></Route>
        <Route path="/Professor" element={<TeachersView />}></Route>
        <Route path="/Summary" element={<SubmissionSummary />}></Route>
        <Route path="/OcrResult/:id" element={<OcrResultPage/> }></Route>
      </Routes>
    </Router>
  );
}

export default App;
