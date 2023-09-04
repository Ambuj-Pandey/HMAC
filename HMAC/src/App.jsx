import { useState } from "react";
import "./App.css";

import Student from "./Components/Student/Student";
import Navbar from "./Components/Navbar/Navbar";

import TeachersView from "./Pages/Teachersview/TeachersView";

function App() {
  return (
    <>
     {/* <Navbar /> */}
      <Student />
     
      {/* <TeachersView /> */}
    </>
  );
}

export default App;
