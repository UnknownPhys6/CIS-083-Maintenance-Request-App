import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./Login";
import MaintenanceForm from "./MaintenanceForm";
import Admin from "./Admin";
import {Link} from "react-router-dom";
import Home from "./home"
import axios from "axios"
function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/MaintenanceForm" element={<MaintenanceForm />} />
        <Route path="/login" element={<Login />} /> 
        <Route path="/maintenance" element={<Admin />} /> 
      </Routes>
    </Router>
  );
}
export function Navbar() {
  return (
    <nav className= "nav">
      <Link to="/MaintenanceForm">Submit Request</Link>
      <Link to="/login">Maintenance Login</Link>
      <Link to="/">Home</Link>
    </nav>
  );
}

export const local = axios.create({
  baseURL: "http://localhost:8000"
});


export default App;
