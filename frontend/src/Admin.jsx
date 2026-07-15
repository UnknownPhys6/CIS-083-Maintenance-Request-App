import React, { useState } from "react";
import axios from "axios";

export default function MaintenanceForm() {
  const [location, setLocation] = useState("");
  const [areaType, setAreaType] = useState("");
  const [category, setCategory] = useState("");
  const [categoryDesc, setCategoryDesc] = useState("");
  const [description, setDescription] = useState("");
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
    formData.append("location", location);
    formData.append("area_type", areaType);
    formData.append("category", category);
    formData.append("description", description);
    formData.append("urgency", urgency);
    photos.forEach(p => {
    if (p instanceof File) formData.append("images", p);
});


    await axios.post("http://localhost:8000/submit", formData, {
      headers: { "Content-Type": "multipart/form-data" }
    });

    alert("Request submitted");
  };

  return (
    <div className="form-container">
      <h1>Maintenance Request Form</h1>

      <form onSubmit={handleSubmit}>
         {/* Active Requests Scroll Box */}
        <div className="active-requests-container">
          <h2>Active Requests</h2>

          <div className="active-requests-scroll">
            {}
            <p>Loading active requests...</p>
          </div>
        </div>
        
        {/* Location */}
        <div className="form-group">
          <label htmlFor="location-select">Choose or type a campus location:</label>
          <input
            list="locations"
            id="location-select"
            name="location"
            placeholder="Type to search..."
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            required
          />

          <datalist id="locations">
            <option value="Agriculture Land Lab" />
            <option value="Ag-Tech Building" />
            <option value="Board and Administration Center" />
            <option value="Foundation and Alumni Center" />
            <option value="Field House" />
            <option value="Judge Learning Resource Center" />
            <option value="Lensink Hall" />
            <option value="Luther Student Center" />
            <option value="Northeast Classroom Building" />
            <option value="Neal Hall" />
            <option value="Northwest Classroom Building" />
            <option value="Power House" />
            <option value="Physical Plant" />
            <option value="Recycling Center" />
            <option value="Storage Building 1" />
            <option value="Vo-Tech Building" />
            <option value="West Classroom Building" />
            <option value="Workforce Development Center" />
            <option value="Webb Hall" />
            <option value="Other/Unsure" />
          </datalist>
        </div>

        {/* Inside / Outside */}
        <div className="form-group">
          <label htmlFor="area-type-select">Is the maintenance inside or outside?</label>
          <input
            list="area-types"
            id="area-type-select"
            name="area_type"
            placeholder="Type or select..."
            value={areaType}
            onChange={(e) => setAreaType(e.target.value)}
            required
          />

          <datalist id="area-types">
            <option value="Inside" />
            <option value="Outside" />
          </datalist>
        </div>

        {/* Category */}
        <div className="form-group">
          <label htmlFor="category-select">Select Maintenance Category:</label>

          <select
            id="category-select"
            name="category"
            value={category}
            onChange={handleCategoryChange}
            required
          >
            <option value="" disabled hidden>
              -- Choose a Category --
            </option>

            <option value="HVAC/Climate Control" title="Heating, air conditioning, ventilation, thermostats, and air quality.">
              HVAC/Climate Control
            </option>
            <option value="Plumbing" title="Leaks, clogged drains, toilets, sinks, and water fountains.">
              Plumbing
            </option>
            <option value="Electrical" title="Outlets, light switches, breaker panels, and flickering lights.">
              Electrical
            </option>
            <option value="Structural & Carpentry" title="Broken doors, windows, drywall damage, flooring, and ceiling tiles.">
              Structural & Carpentry
            </option>
            <option value="Lock & Security" title="Keys, smart locks, badges, security cameras, and alarms.">
              Lock & Security
            </option>
            <option value="Technical" title="IT hardware, internet connection, network ports, and smart classroom tech.">
              Technical
            </option>
            <option value="Landscaping & Grounds" title="Lawn mowing, tree trimming, courtyard upkeep, and sprinklers.">
              Landscaping & Grounds
            </option>
            <option value="Snow & Ice Removal" title="Salting sidewalks, shoveling pathways, and plowing parking areas.">
              Snow & Ice Removal
            </option>
            <option value="Pest Control" title="Insects, rodents, wasps, or any unwanted wildlife sightings.">
              Pest Control
            </option>
            <option value="Waste & Recycling" title="Overflowing trash bins, dumpster issues, and recycling pickup.">
              Waste & Recycling
            </option>
            <option value="Safety & Fire Protection" title="Fire extinguishers, smoke alarms, emergency exits, and hazards.">
              Safety & Fire Protection
            </option>
            <option value="Custodial / Janitorial" title="Spills, messy areas, and restocking soap or paper towels.">
              Custodial / Janitorial
            </option>
            <option value="Other / Unsure" title="Select if your issue doesn't fit neatly into the choices above.">
              Other / Unsure
            </option>
          </select>

          {categoryDesc && (
            <div className="description-box">{categoryDesc}</div>
          )}
        </div>

        {/* Description */}
        <div className="form-group">
          <label htmlFor="description">Describe the issue:</label>
          <input
            type="text"
            id="description"
            name="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
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
            Submit Request
          </button>
        </div>
      </form>
    </div>
  );
}
