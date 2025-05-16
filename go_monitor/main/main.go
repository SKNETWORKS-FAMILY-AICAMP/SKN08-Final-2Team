package main

import (
	"snack/config"
	"snack/initializer"
	"snack/router"
	"fmt"
	"os"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/joho/godotenv"
)

func main() {
	if err := godotenv.Load(); err != nil {
		fmt.Println("Error loading .env file")
		return
	}

	// 포트 번호를 .env에서 가져오기
	port := os.Getenv("PORT")
	if port == "" {
		// 포트 번호가 없으면 에러 발생
		fmt.Println("Error: PORT is not set in .env file")
		return
	}

	// DB 초기화
	db, err := initializer.DomainInitializer()
	if err != nil {
		fmt.Println("Error initializing domain:", err)
		return
	}

	app := fiber.New()
	app.Use(cors.New(config.CorsConfig()))
	router.RegisterRoutes(app, db)

	if err := app.Listen(":" + port); err != nil {
		fmt.Println("Error starting server:", err)
	}
}
