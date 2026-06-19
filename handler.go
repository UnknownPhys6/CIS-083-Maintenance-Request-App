package main

import (
	"cis-083-api/database"
	"fmt"
	"net/http"

	"github.com/labstack/echo/v5"
)

type Handler struct {
	db *database.Database
}

func NewHandler(db *database.Database) *Handler {
	return &Handler{db: db}
}

func (h *Handler) GetMaintenanceRequests(c *echo.Context) error {
	maintenanceRequests, err := h.db.GetMaintenanceRequests()
	if err != nil {
		return err
	}
	return c.JSON(http.StatusOK, maintenanceRequests)
}

type CreateMaintenanceRequest struct {
	Type        string `json:"type"`
	Description string `json:"description"`
	Location    string `json:"location"`
	Active      bool   `json:"active"`
}

// Struct to capture the incoming toggle payload
type UpdateActiveInput struct {
	Active bool `json:"active"`
}

func (h *Handler) GetMaintenanceRequestByID(c *echo.Context) error {
	id := c.Param("id")
	// Call the database function using the ID from the URL
	req, err := h.db.MaintenanceRequestByID(id)
	if err != nil {
		return c.JSON(http.StatusNotFound, map[string]string{"error": "maintenance request not found"})
	}
	return c.JSON(http.StatusOK, req)
}

// TODO have the api return the id for the newly created maintenance request
func (h *Handler) UpdateMaintenanceRequestByID(c *echo.Context) error {
	id := c.Param("id")
	var input UpdateActiveInput
	// Bind the JSON body (e.g., {"active": false}) to our struct
	if err := c.Bind(&input); err != nil {
		return fmt.Errorf("issue mapping request body: %w", err)
	}
	// Pass the ID from the URL and the boolean from the body to the DB
	err := h.db.UpdateRequestActive(id, input.Active)
	if err != nil {
		return fmt.Errorf("could not update maintenance request status: %w", err)
	}
	return c.NoContent(http.StatusOK)
}

// CreateMaintenanceRequest creates a new maintenance request and returns its new ID
func (h *Handler) CreateMaintenanceRequest(c *echo.Context) error {
	var request CreateMaintenanceRequest

	// We take the request body and map it to our CreateMaintenanceRequest object
	err := c.Bind(&request)
	if err != nil {
		return fmt.Errorf("issue mapping request body: %w", err)
	}

	// Call the database function and capture the newly created ID
	newID, err := h.db.CreateMaintenanceRequest(request.Type, request.Description, request.Location, request.Active)
	if err != nil {
		return fmt.Errorf("could not create maintenance request: %w", err)
	}

	// Returns a 201 Created status along with the new ID in a JSON object
	return c.JSON(http.StatusCreated, map[string]int64{"id": newID})
}
