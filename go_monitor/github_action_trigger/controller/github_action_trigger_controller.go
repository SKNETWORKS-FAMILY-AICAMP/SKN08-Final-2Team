package controller

import (
	"first/github_action_trigger/controller/request_form"
	"first/github_action_trigger/service"
	"fmt"
	"github.com/gofiber/fiber/v2"
)

type GitHubActionTriggerController struct {
	GitHubActionTriggerService service.GitHubActionTriggerService
}

func NewGitHubActionTriggerController(service service.GitHubActionTriggerService) *GitHubActionTriggerController {
	return &GitHubActionTriggerController{GitHubActionTriggerService: service}
}

func (c *GitHubActionTriggerController) TriggerWorkflow(ctx *fiber.Ctx) error {
	fmt.Println("🔧 controller - TriggerWorkflow() 시작")

	var req request_form.WorkflowTriggerRequestForm
	if err := ctx.BodyParser(&req); err != nil {
		fmt.Println("❌ controller - BodyParser 오류:", err)
		return ctx.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid request"})
	}

	// 실제 값 찍어보기
	fmt.Println("📥 입력값 확인:")
	fmt.Println("  📦 RepoUrl      :", req.RepoUrl)
	fmt.Println("  🔑 Token        :", req.Token)
	fmt.Println("  📝 WorkflowName :", req.WorkflowName)

	if req.RepoUrl == "" || req.Token == "" || req.WorkflowName == "" {
		fmt.Println("❌ controller - 필수 입력값 없음")
		return ctx.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Missing required fields"})
	}

	fmt.Println("✅ controller - 입력값 확인 완료")

	err := c.GitHubActionTriggerService.RunWorkflow(req.RepoUrl, req.Token, req.WorkflowName)
	if err != nil {
		fmt.Println("❌ controller - RunWorkflow 오류:", err)
		return ctx.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	fmt.Println("🎉 controller - 워크플로우 트리거 성공")
	return ctx.JSON(fiber.Map{"success": true})
}

