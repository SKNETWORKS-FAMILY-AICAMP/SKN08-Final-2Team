package config

import (
	"fmt"
	"os"

	"github.com/gofiber/fiber/v2/middleware/cors"
)

// CorsConfig : Fiber에서 사용할 CORS 설정 반환
func CorsConfig() cors.Config {
	allowOrigins := os.Getenv("CORS_ALLOWED_ORIGINS")
	if allowOrigins == "" {
		fmt.Println("CORS_ALLOWED_ORIGINS 값이 설정되지 않았습니다. .env 파일을 확인하세요.")
		os.Exit(1)
	}

	return cors.Config{
		AllowOrigins: allowOrigins,
		AllowMethods: "GET,POST,PUT,DELETE,OPTIONS",
		AllowHeaders: "Origin, Content-Type, Accept, Authorization",
	}
}
