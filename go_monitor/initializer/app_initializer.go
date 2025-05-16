package initializer

import (
	"first/post/controller"
	"first/post/routes"

	"github.com/gofiber/fiber/v2"
)

// AppInitializer는 Fiber 앱을 초기화하고 라우팅을 설정하는 함수입니다.
func AppInitializer(postController *controller.PostController) *fiber.App {
	// Fiber 앱 초기화
	app := fiber.New()

	// 라우트 설정
	routes.SetupPostRoutes(app, postController)

	return app
}
