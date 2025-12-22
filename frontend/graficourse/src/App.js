import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";


import CoursePage from "./pages/CoursePage";
import LessonPage from "./pages/LessonPage";
import AboutPage from "./pages/AboutPage";


const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<CoursePage />} />

        <Route path="/course/:id" element={<CoursePage />} />
        <Route
          path="/course/:courseId/lesson/:lessonId"
          element={<LessonPage />}
        />
        <Route path="/lesson/:lessonId" element={<LessonPage />} />
        <Route path="/about" element={<AboutPage />} />
      </Routes>
    </Router>
  );
};

export default App;
