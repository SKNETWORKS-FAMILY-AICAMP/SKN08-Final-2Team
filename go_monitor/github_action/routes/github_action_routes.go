package routes

import (
	"snack/github_action/controller" // GitHub Action 컨트롤러 import

	"github.com/gofiber/fiber/v2"
)

// SetupGitHubActionRoutes는 GitHub Action에 관련된 라우트를 설정하는 함수입니다.
func SetupGitHubActionRoutes(app *fiber.App, githubActionController *controller.GitHubActionController) {
	// GitHub Action 라우트 그룹 생성
	githubActionGroup := app.Group("/github-actions")

	// 모든 워크플로우 실행 정보 조회
	githubActionGroup.Post("/workflow", githubActionController.GetWorkflowRuns)

	// // 특정 워크플로우 실행 정보 조회
	// githubActionGroup.Get("/:id", githubActionController.GetWorkflowRunByID)

	// // 워크플로우 실행 정보 저장
	// githubActionGroup.Post("/", githubActionController.SaveWorkflowRuns)

	// // 워크플로우 실행 정보 삭제
	// githubActionGroup.Delete("/:id", githubActionController.DeleteWorkflowRun)
}
