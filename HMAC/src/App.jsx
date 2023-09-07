// import { useState } from "react";
import "./App.css";

import Student from "./Components/Student/Student";
import TeachersView from "./Pages/Teachersview/TeachersView";
import LoginPage from "./Pages/LoginPage/LoginPage";
import RegistrationPage from "./Pages/RegistrationPage/RegistrationPage";
import SubmissionSummary from "./Pages/SubmissionSummary/SubmissionSummary";

import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<LoginPage />}></Route>
        <Route exact path="/register" element={<RegistrationPage />}></Route>
        <Route path="/Student" element={<Student />}></Route>
        <Route path="/Professor" element={<TeachersView />}></Route>
        <Route path="/Summary" element={<SubmissionSummary />}></Route>
      </Routes>
    </Router>
  );
}

export default App;
