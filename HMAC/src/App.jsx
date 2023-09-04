import { useState } from "react";
import "./App.css";

import Student from "./Components/Student/Student";
import TeachersView from "./Pages/Teachersview/TeachersView";
import LoginPage from "./Pages/LoginPage/LoginPage";

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<LoginPage/>} >
         
        </Route>
        <Route path="/student" element={<Student/>}>
         
        </Route>
        <Route path="/teachersview" element={<TeachersView/>}>
          {/* <TeachersView /> */}
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
