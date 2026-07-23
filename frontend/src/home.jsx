import React, { useState } from "react";
import { local } from "./App";

export default function Home() {
  const [requestID, setRequestID] = useState("");
  const [activeRequests, setActiveRequests] = useState([]);
  const [loading, setLoading] = useState(false);

  async function getRequest(e) {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await local.get(`/get_maintenance_request_by_id/${requestID}`);
      setActiveRequests([response.data]); 
    } catch (error) {
      console.error("Error fetching request details:", error);
      setActiveRequests([]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <form onSubmit={getRequest}>
        <h2>Campus Maintenance System</h2>
        <div className="maint-tag">
          <div className="maint-header">
            <label htmlFor="requestID">Enter request ID:</label>
            <input
              type="text"
              id="requestID"
              name="requestID"
              value={requestID}
              onChange={(e) => setRequestID(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <button type="submit" className="submit-btn">
              Find Request
            </button>
          </div>
        </div>
      </form>

      <div className="active-requests-scroll">
        {loading && <p>Loading...</p>}
        {!loading && activeRequests.length === 0 && <p>No active requests found.</p>}

        {activeRequests.map((request) => (
          <div key={request.id} className="active-request">
            <p><strong>Location:</strong> {request.location}</p>
            <p><strong>Area Type:</strong> {request.area_type}</p>
            <p><strong>Category:</strong> {request.category}</p>
            <p><strong>Description:</strong> {request.description}</p>
            <p><strong>Urgency:</strong> {request.urgency}</p>
            <p><strong>Stage:</strong> {request.stage}</p>
            {request.images && (
          <div>
            <strong>Photos:</strong>
            {request.images.split(",").map((filename) => (
            <img
              key={filename}
              src={`http://localhost:8000/uploads/${filename.trim()}`}
               alt="Maintenance photo"
              style={{ maxWidth: "200px", margin: "5px", display: "block" }}
                            />
            ))}
          </div>
)}
          </div>
        ))}
      </div>
      <div className="logo-container"></div>
    </div>
  );
}
