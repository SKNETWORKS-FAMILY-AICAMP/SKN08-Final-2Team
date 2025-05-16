package routes

import (
	"snack/post/controller"

	"github.com/gofiber/fiber/v2"
)

func SetupPostRoutes(app *fiber.App, postController *controller.PostController) {
	// 게시글 라우트 그룹 생성
	postGroup := app.Group("/posts")

	// 게시글 생성
	postGroup.Post("/", postController.CreatePost)

	// 특정 게시글 조회
	postGroup.Get("/:id", postController.GetPostByID)

	// 모든 게시글 조회
	postGroup.Get("/", postController.GetAllPosts)

	// 게시글 수정
	postGroup.Put("/:id", postController.UpdatePost)

	// 게시글 삭제
	postGroup.Delete("/:id", postController.DeletePost)
}
