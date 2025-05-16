package router

import (
	"snack/post/controller"
	"snack/post/repository"
	"snack/post/service"

	githubActionController "snack/github_action/controller"
	githubActionRepository "snack/github_action/repository"
	githubActionService "snack/github_action/service"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

// RegisterPostRoutes는 게시글 관련 모든 라우트를 등록하는 함수입니다.
func RegisterPostRoutes(app *fiber.App, db *gorm.DB) {
	// DB를 기반으로 Repository 생성
	postRepo := repository.NewPostRepositoryImpl(db)
	// Repository를 기반으로 Service 생성
	postService := service.NewPostService(postRepo)

	// Controller 생성
	postController := controller.NewPostController(postService)

	// 라우트 등록
	app.Post("/posts", postController.CreatePost)
	app.Get("/posts/:id", postController.GetPostByID)
	app.Get("/posts", postController.GetAllPosts)
	app.Put("/posts/:id", postController.UpdatePost)
	app.Delete("/posts/:id", postController.DeletePost)
}

// RegisterGitHubActionRoutes는 GitHub Action 관련 모든 라우트를 등록하는 함수입니다.
func RegisterGitHubActionRoutes(app *fiber.App, db *gorm.DB) {
	// DB를 기반으로 Repository 생성
	gitHubActionRepo := githubActionRepository.NewGitHubActionRepositoryImpl(db)
	// Repository를 기반으로 Service 생성
	gitHubActionService := githubActionService.NewGitHubActionServiceImpl(gitHubActionRepo)

	// Controller 생성
	gitHubActionController := githubActionController.NewGitHubActionController(gitHubActionService)

	// 라우트 등록
	app.Post("/github-actions/workflow", gitHubActionController.GetWorkflowRuns)
	// app.Get("/github-actions/:id", gitHubActionController.GetWorkflowRunByID)
	// app.Post("/github-actions", gitHubActionController.SaveWorkflowRuns)
	// app.Delete("/github-actions/:id", gitHubActionController.DeleteWorkflowRun)
}

// RegisterRoutes는 모든 도메인(게시글 등)의 라우트를 등록합니다.
func RegisterRoutes(app *fiber.App, db *gorm.DB) {
	RegisterPostRoutes(app, db)
	RegisterGitHubActionRoutes(app, db)
}
