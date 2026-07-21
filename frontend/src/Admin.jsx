import React, { useState, useEffect } from "react";
import axios from "axios";
import { local } from "./App"
export default function MaintenanceForm() {
  const [location, setLocation] = useState("");
  const [areaType, setAreaType] = useState("");
  const [category, setCategory] = useState("");
  const [categoryDesc, setCategoryDesc] = useState("");
  const [techDescription, setTechDescription] = useState("");
  const [urgency, setUrgency] = useState("3");
  const [photo, setPhoto] = useState(null);
  const [stage, setStage] = useState("Submitted");

  const handleCategoryChange = (e) => {
    const option = e.target.selectedOptions[0];
    setCategory(option.value);
    setCategoryDesc(option.title || "");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("tech_description", techDescription);
    formData.append("stage", stage);
    /*photos.forEach(p => {
    if (p instanceof File) formData.append("images", p);
});*/


    await local.put(`/requests/${requestId}`, formData, {
      headers: { "Content-Type": "multipart/form-data" }
    });
    alert("Request Altered");
  };
  const [activeRequests, setActiveRequests] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchRequests = async () => {
    setLoading(true);
    try {
      const response = await local.get("/requests", {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setActiveRequests(response.data);
    } catch (error) {
      console.error("Error fetching active requests:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRequests();
  }, []);
const [filters, setFilters] = useState({
  location: "",
  areaType: "",
  category: "",
  urgency: "",
  stage: ""
});

const handleFilterChange = (field, value) => {
  setFilters((prev) => ({ ...prev, [field]: value }));
  };

const filteredRequests = activeRequests.filter((request) => {
  return(
    (filters.location === "" || request.location === filters.location) &&
    (filters.areaType === "" || request.area_type === filters.areaType) &&
    (filters.category === "" || request.category === filters.category) &&
    (filters.urgency === "" || request.urgency === filters.urgency) &&
    (filters.stage === "" || request.stage === filters.stage)&&
    (filters.time === "" || request.time === filters.time)
  );
});
  return (
    <div className="form-container">
      <h1>Maintenance Request Form</h1>
         {/* Active Requests Scroll Box */}
        <div className="active-requests-container">
          <h2>Active Requests</h2>

       <div className="active-requests-scroll">
      {loading && <p>Loading...</p>}
      {!loading && filteredRequests.length === 0 && <p>No active requests found.</p>}

      {filteredRequests.map((request) => (
        <div key={request.id} className="active-request" data-category={request.category}>
          <p><strong>Location:</strong> {request.location}</p>
          <p><strong>Area Type:</strong> {request.area_type}</p>
          <p><strong>Category:</strong> {request.category}</p>
          <p><strong>Description:</strong> {request.description}</p>
          <p><strong>Urgency:</strong> {request.urgency}</p>
          <p><strong>Stage:</strong> {request.stage}</p>
          <p><strong>Time:</strong> {request.time}</p>
        </div>
      ))}
  </div>
 <form onSubmit={handleSubmit}>
        {/* Description */}
        <div className="form-group">
          <label htmlFor="description">Describe your work:</label>
          <input
            type="text"
            id="tech-description"
            name="tech-description"
            value={techDescription}
            onChange={(e) => setTechDescription(e.target.value)}
            required
          />
        </div>

        {/* Urgency */}
        <div className="form-group">
          <label>How urgent is this maintenance request?</label>

          <div className="urgency-container">
            {[1, 2, 3, 4, 5].map((num) => (
              <label key={num} className="urgency-option">
                <input
                  type="radio"
                  name="urgency"
                  value={num}
                  checked={urgency === String(num)}
                  onChange={(e) => setUrgency(e.target.value)}
                />
                <span className="scale-number">{num}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Photo Upload */}
        <div className="form-group">
          <label htmlFor="maintenance-photo">Upload a photo (Optional):</label>
          <input
            type="file"
            id="maintenance-photo"
            accept="image/*"
            onChange={(e) => setPhoto(e.target.files[0])}
          />
        </div>
        {/*Stage*/}
        <div className="form-group">
            <label>Stage of the Request:</label>
            <div className="stage-container">
                <label className="stage-option">
                    <input
                        type="radio"
                        name="stage"
                        value="Submitted"
                        checked={stage === "Submitted"}
                        onChange={(e) => setStage(e.target.value)}
                    />
                    Submitted
                </label>
                <label className="stage-option">
                    <input
                        type="radio"
                        name="stage"
                        value="In-Progress"
                        checked={stage === "In-Progress"}
                        onChange={(e) => setStage(e.target.value)}
                    />
                    In-Progress
                </label>
                <label className="stage-option">
                  <input
                    type="radio"
                    name="stage"
                    value="On-hold"
                    checked={stage === "On-hold"}
                    onChange={(e) => setStage(e.target.value)}
                 />
                </label>
                <label className="stage-option">
                    <input
                        type="radio"
                        name="stage"
                        value="Completed"
                        checked={stage === "Completed"}
                        onChange={(e) => setStage(e.target.value)}
                    />
                    Completed
                </label>
            </div>
        </div>

        {/* Submit */}
        <div className="form-group">
          <button type="submit" className="submit-btn">
            Alter Request
          </button>
        </div>
      </form>
    </div>
  </div>
  );
}
