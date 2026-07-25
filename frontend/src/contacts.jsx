import React, { useState, useEffect } from "react";

export default function Contacts() {
  const contacts = [
    {
      id: 1,
      building: "North Hall",
      phone: "217-254-7046",
      email: "maintenance@campus.edu"
    }
  ];

  return (
    <div className="contacts-page">
      <h1>Maintenance Contacts</h1>

      <div className="contacts-scroll">
        {contacts.map((c) => (
          <div key={c.id} className="contact-card">
            <p><strong>Building:</strong> {c.building}</p>
            <p><strong>Phone:</strong> {c.phone}</p>
            <p><strong>Email:</strong> {c.email}</p>
          </div>
        ))}
      </div>

      <div className="logo-container"></div>
    </div>
  );
}
