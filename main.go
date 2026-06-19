package main

import (
	"cis-083-api/database"

	"github.com/labstack/echo/v5"
	"github.com/labstack/echo/v5/middleware"
)

func main() {

	db := database.NewDatabase()

	// instantiates e as new instance of echo
	e := echo.New()

	// enables the request logger and panic recoverer
	e.Use(middleware.RequestLogger())
	e.Use(middleware.Recover())

	h := NewHandler(db)

	// The Echo method (POST, GET, PUT) determines what Postman must use
	e.GET("/requests", h.GetMaintenanceRequests)
	e.GET("/requests/:id", h.GetMaintenanceRequestByID)
	e.POST("/requests", h.CreateMaintenanceRequest)
	e.PUT("/requests/:id", h.UpdateMaintenanceRequestByID)

	if err := e.Start(":1323"); err != nil {
		e.Logger.Error("failed to start server", "error", err)
	}
}

/*
Why are main.go and handler.go both part of package main?

How does import cis-083-api/database find the right file to import?
*/
