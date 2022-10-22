import React from "react";
import "./App.css";
import Layout from "./components/Layout/Layout";
import WebcamStreamCapture from "./components/Webcam/Webcam";
import CameraStreamCapture from "./components/Camera/Camera";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import HomePage from "./components/Home/HomePage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
  },
  {
    path: "/index",
    element: <Layout />,
    children: [
      {
        path: "/index",
        element: <WebcamStreamCapture />,
      },
      {
        path: "/index/camera",
        element: <CameraStreamCapture />,
      },
    ],
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
