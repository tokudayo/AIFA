import "bootstrap/dist/css/bootstrap.min.css";
import { useEffect } from "react";
import "./App.css";
import Layout from "./components/Layout/Layout";
import WebcamStreamCapture from "./components/Webcam/Webcam";
import CameraStreamCapture from "./components/Camera/Camera";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import HomePage from "./components/Home/HomePage";
import { BaseSocket } from "./socket/BaseSocket";
import store from "./store/configureStore";
import { Provider } from "react-redux";
import SignUpPage from "./components/Home/SignUpPage";
import Analytics from "./components/Analytics/Analytics";

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
      {
        path: "/index/analytics",
        element: <Analytics />,
      },
    ],
  },
  {
    path: "/sign_up",
    element: <SignUpPage />,
  },
]);

function App() {
  useEffect(() => {
    BaseSocket.getInstance().disconnectSocket();
    BaseSocket.getInstance().connect();
  }, []);

  return (
    <Provider store={store}>
      <RouterProvider router={router} />
    </Provider>
  );
}

export default App;
