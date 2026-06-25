import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/Login";
import MaintenanceForm from "./components/MaintenanceForm";
import Admin from "./components/Admin";
import {Link} from "react-router-dom";


function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<MaintenanceForm />} />
        <Route path="/login" element={<Login />} />
        <Route path="/maintenance" element={<Admin />} />
      </Routes>
    </Router>
  );
}
export function Navbar() {
  return (
    <nav style={{ padding: "10px", background: "#eee" }}>
      <Link to="/" style={{ marginRight: "20px" }}>Submit Request</Link>
      <Link to="/login">Maintenance Login</Link>
    </nav>
  );
}
export default App;
