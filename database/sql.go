package database

import (
	"database/sql"

	_ "github.com/go-sql-driver/mysql"
)

type Database struct {
	db *sql.DB
}

// NewDatabase creates a connection to database via the go-sql-driver.
// IP is hardcoded into the function definition. Change later.
func NewDatabase() *Database {
	db, err := sql.Open("mysql", "developer:Group2pass@tcp(localhost:3306)/maintenance_requests")
	if err != nil {
		panic(err)
	}

	return &Database{
		db: db,
	}
}

type MaintenanceRequest struct {
	RequestID          string `json:"request_id"`
	RequestType        string `json:"request_type"`
	RequestDescription string `json:"request_description"`
	RequestLocation    string `json:"request_location"`
	RequestActive      bool   `json:"request_active"`
}

// GetMaintenanceRequests returns all requests (it's a "SELECT *" statement)
func (d *Database) GetMaintenanceRequests() ([]MaintenanceRequest, error) {
	// 1. Define the SQL query
	query := `SELECT requestID, requestType, requestDesc, requestLocation, active FROM requests`
	rows, err := d.db.Query(query)
	if err != nil {
		return nil, err
	} // Error handling
	defer rows.Close() // Ensure rows are closed when the function returns
	var maintenanceRequests []MaintenanceRequest
	for rows.Next() {
		var req MaintenanceRequest
		// More error handling
		err := rows.Scan(&req.RequestID, &req.RequestType, &req.RequestDescription, &req.RequestLocation, &req.RequestActive)
		if err != nil {
			return nil, err
		} // more error handling
		maintenanceRequests = append(maintenanceRequests, req)
	}
	err = rows.Err() // more error handling
	if err != nil {
		return nil, err
	}
	return maintenanceRequests, nil
}

// MaintenanceRequestByID returns only the one request that matches the ID passed into it.
func (d *Database) MaintenanceRequestByID(requestID string) (*MaintenanceRequest, error) {
	statement := "SELECT requestID, requestType, requestDesc, requestLocation, active FROM requests WHERE requestID = ?"
	row := d.db.QueryRow(statement, requestID)
	var req MaintenanceRequest
	err := row.Scan(&req.RequestID, &req.RequestType, &req.RequestDescription, &req.RequestLocation, &req.RequestActive)
	if err != nil {
		return nil, err
	}
	return &req, nil
}

// CreateMaintenanceRequest inserts a maintenance request into the database.
// It returns the newly generated auto-increment ID.
func (d *Database) CreateMaintenanceRequest(requestType string, description string, location string, active bool) (int64, error) {
	statement := "INSERT INTO requests (requestType, requestDesc, requestLocation, active) VALUES (?, ?, ?, ?)"
	result, err := d.db.Exec(statement, requestType, description, location, active)
	if err != nil {
		return 0, err
	}
	// Grab the ID of the row we just inserted
	id, err := result.LastInsertId()
	if err != nil {
		return 0, err
	}
	return id, nil
}

// UpdateRequestActive updates the active status of a specific maintenance request by its ID.
func (d *Database) UpdateRequestActive(requestID string, active bool) error {
	statement := "UPDATE requests SET active = ? WHERE requestID = ?"
	_, err := d.db.Exec(statement, active, requestID)
	if err != nil {
		return err
	}
	return nil
}
