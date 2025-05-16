package routes

import (
	"first/github_action_trigger/controller"

	"github.com/gofiber/fiber/v2"
)

func SetupGitHubActionTriggerRoutes(app *fiber.App, githubActionTrigerController *controller.GitHubActionTriggerController) {
	githubActionGroup := app.Group("/github-actions-trigger")

	// Github Actions Trigger 구동
	githubActionGroup.Post("/run", githubActionTrigerController.GetTriggers)
}
