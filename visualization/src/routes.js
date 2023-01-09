import React from "react";
import { Routes, Route } from "react-router-dom";
import ForceGraphPageMonth from "./pages/GraphvisPage/ForceGraphPageMonth";

export default function AppRoutes() {
  return (
    <>
        <Routes>
            <Route path="/" element={<ForceGraphPageMonth />} />
        </Routes>
    </>
  );
}
