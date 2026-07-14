import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./Login";
import MaintenanceForm from "./MaintenanceForm";
import Admin from "./Admin";
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
    <nav className= "nav">
      <Link to="/">Submit Request</Link>
      <Link to="/login">Maintenance Login</Link>
    </nav>
  );
}
export default App;
