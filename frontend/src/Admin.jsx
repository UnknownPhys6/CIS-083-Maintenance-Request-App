import React, { useState, useEffect } from "react";
import { local } from "./App";

export default function MaintenanceForm() {
  const [techDescription, setTechDescription] = useState("");
  const [urgency, setUrgency] = useState("3");
  const [images, setImages] = useState(null);
  const [stage, setStage] = useState("Submitted");

  const [activeRequests, setActiveRequests] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedRequest, setSelectedRequest] = useState(null);
  const [successMessage, setSuccessMessage] = useState("");
  const fetchRequests = async () => {
    setLoading(true);
     try {
    const response = await local.get("/requests");
    setActiveRequests(response.data);
    } catch (error) {
      console.error("Error fetching active requests:", error);
    } finally {
      setLoading(false);
    }
  };

  

  const viewRequest = (request) => {
    setSelectedRequest(request);
    setTechDescription(request.tech_description || "");
    setStage(request.stage || "Submitted");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedRequest) return;

    const formData = new FormData();
    formData.append("tech_description", techDescription);
    formData.append("stage", stage);
    if (images && images.length > 0) {
      images.forEach((image) => {
        if (image instanceof File) formData.append("images", image);
      });
    }
    try {
      await local.put(`/request/${selectedRequest.id}`, formData, { 
        headers: { "Content-Type": "multipart/form-data" }});
        setSuccessMessage("Request updated successfully!");
        setTimeout(() => setSuccessMessage(""), 3000); // Clear message after 3 seconds
      setSelectedRequest(null);
      setFilters({ location: "", areaType: "", category: "", urgency: "", stage: "" }); // reset filters
      fetchRequests();
      } catch (error) {
         console.error("Error updating request:", error);
      }
    
  };
useEffect(() => {
    fetchRequests();
  }, []);
  // ------------------------------------------------------------
  // Filters
  // ------------------------------------------------------------
  const [filters, setFilters] = useState({
    location: "",
    areaType: "",
    category: "",
    urgency: "",
    stage: ""
  });

  const handleFilterChange = (field, value) => {
    console.log("FILTER CHANGED:", field, value);
    setFilters((prev) => ({ ...prev, [field]: value }));
  };

  const filteredRequests = activeRequests.filter((request) => {
    return (
      (filters.location === "" || request.location === filters.location) &&
      (filters.areaType === "" || request.area_type === filters.areaType) &&
      (filters.category === "" || request.category === filters.category) &&
      (filters.urgency === "" || request.urgency === filters.urgency) &&
      (filters.stage === "" ? request.stage !== "Completed" : request.stage === filters.stage)
    );
  });

  return (
    <div className="form-container">
      <h1>Maintenance Request Form</h1>

      <div className="active-requests-container">
        <h2>Active Requests</h2>
        {successMessage && <p style={{ color: "green" }}>{successMessage}</p>}
        {/* Filter controls */}
        <div className="filter-container">
          <select value={filters.location} onChange={(e) => handleFilterChange("location", e.target.value)}>
            <option value="">All Locations</option>
            {[...new Set(activeRequests.map((r) => r.location))].map((loc) => (
              <option key={loc} value={loc}>{loc}</option>
            ))}
          </select>

          <select value={filters.category} onChange={(e) => handleFilterChange("category", e.target.value)}>
            <option value="">All Categories</option>
            {[...new Set(activeRequests.map((r) => r.category))].map((cat) => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>

          <select value={filters.urgency} onChange={(e) => handleFilterChange("urgency", e.target.value)}>
            <option value="">All Urgency</option>
            {[1, 2, 3, 4, 5].map((n) => (
              <option key={n} value={n}>{n}</option>
            ))}
          </select>

          <select value={filters.stage} onChange={(e) => handleFilterChange("stage", e.target.value)}>
            <option value="">All Stages</option>
            <option value="Submitted">Submitted</option>
            <option value="In-Progress">In-Progress</option>
            <option value="On-hold">On-hold</option>
            <option value="Completed">Completed</option>
          </select>
        </div>

        {/* Request list — click to select */}
        <div className="active-requests-scroll">
          {loading && <p>Loading...</p>}
          {!loading && filteredRequests.length === 0 && <p>No active requests found.</p>}

          {filteredRequests.map((request) => (
            <div
              key={request.id}
              className="active-request"
              onClick={() => viewRequest(request)}
              style={{
                cursor: "pointer",
                border: selectedRequest?.id === request.id ? "2px solid blue" : "1px solid #ccc",
                padding: "8px",
                marginBottom: "6px"
              }}
            >
              <p><strong>ID:</strong> {request.id}</p>
              <p><strong>Location:</strong> {request.location}</p>
              <p><strong>Category:</strong> {request.category}</p>
              <p><strong>Description:</strong> {request.description}</p>
              <p><strong>Urgency:</strong> {request.urgency}</p>
              <p><strong>Stage:</strong> {request.stage}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Edit form — only shows once a request is selected */}
      {selectedRequest && (
        <form onSubmit={handleSubmit}>
          <h3>Editing Request #{selectedRequest.id}</h3>

          <div className="form-group">
            <label htmlFor="tech-description">Describe your work:</label>
            <input
              type="text"
              id="tech-description"
              value={techDescription}
              onChange={(e) => setTechDescription(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="maintenance-photo">Upload a photo (Optional):</label>
            <input
              type="file"
              id="maintenance-photo"
              accept="image/*"
              multiple
              onChange={(e) => setImages([...e.target.files])}
            />
          </div>

          <div className="form-group">
            <label>Stage of the Request:</label>
            <div className="stage-container">
              {["Submitted", "In-Progress", "On-hold", "Completed"].map((s) => (
                <label key={s} className="stage-option">
                  <input
                    type="radio"
                    name="stage"
                    value={s}
                    checked={stage === s}
                    onChange={(e) => setStage(e.target.value)}
                  />
                  {s}
                </label>
              ))}
            </div>
          </div>

          <div className="form-group">
            <button type="submit" className="submit-btn">Alter Request</button>
            <button type="button" onClick={() => setSelectedRequest(null)}>Cancel</button>
          </div>
        </form>
      )}
    </div>
  );
}