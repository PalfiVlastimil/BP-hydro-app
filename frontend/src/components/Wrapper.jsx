import { BrowserRouter, Routes, Route, useRoutes } from "react-router-dom";
import LoginPage from "./LoginPage";
import Dashboard from "./Dashboard";
import PrivateRoute from "./PrivateRoute";
import { ToastContainer } from 'react-toastify';
import SigningForms from "./SigningForms";

function App() {
  return (
    <>
      <ToastContainer/>
      <Routes>
        <Route exact path="/" element={<SigningForms />} />
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />
      </Routes>
    </>
  );
}

export default App;