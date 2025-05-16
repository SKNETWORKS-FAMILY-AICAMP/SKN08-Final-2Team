package controller

import (
	"snack/github_action/controller/request_form"
	"snack/github_action/entity"
	"snack/github_action/service"
	"strconv"

	"github.com/gofiber/fiber/v2"
)

// GitHubActionController 구조체
type GitHubActionController struct {
	GitHubActionService service.GitHubActionService
}

// NewGitHubActionController 생성자 함수
func NewGitHubActionController(service service.GitHubActionService) *GitHubActionController {
	return &GitHubActionController{GitHubActionService: service}
}

// GetWorkflowRuns 워크플로우 실행 정보 가져오기
func (c *GitHubActionController) GetWorkflowRuns(ctx *fiber.Ctx) error {
	println("controller - GetWorkflowRuns()")

	// 요청 바디 파싱
	var req request_form.WorkflowRequest
	if err := ctx.BodyParser(&req); err != nil {
		return ctx.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}
	println("controller - pass request_form")

	// 요청 파라미터 검증
	if req.RepoUrl == "" || req.Token == "" {
		return ctx.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "repo_url and token are required",
		})
	}
	println("controller - non-null request_form")

	workflowRuns, err := c.GitHubActionService.GetWorkflowRuns(req.RepoUrl, req.Token)
	if err != nil {
		return ctx.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return ctx.JSON(workflowRuns)
}

// SaveWorkflowRuns 워크플로우 실행 정보 저장하기
func (c *GitHubActionController) SaveWorkflowRuns(ctx *fiber.Ctx) error {
	var workflowRuns []entity.WorkflowRun
	if err := ctx.BodyParser(&workflowRuns); err != nil {
		return ctx.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid request"})
	}

	if err := c.GitHubActionService.SaveWorkflowRuns(workflowRuns); err != nil {
		return ctx.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return ctx.Status(fiber.StatusCreated).JSON(workflowRuns)
}

// GetWorkflowRunByID 특정 워크플로우 실행 정보 조회
func (c *GitHubActionController) GetWorkflowRunByID(ctx *fiber.Ctx) error {
	id, err := strconv.Atoi(ctx.Params("id"))
	if err != nil {
		return ctx.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid ID"})
	}

	workflowRun, err := c.GitHubActionService.GetWorkflowRunByID(uint(id))
	if err != nil {
		return ctx.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "WorkflowRun not found"})
	}

	return ctx.JSON(workflowRun)
}

// DeleteWorkflowRun 워크플로우 실행 정보 삭제
func (c *GitHubActionController) DeleteWorkflowRun(ctx *fiber.Ctx) error {
	id, err := strconv.Atoi(ctx.Params("id"))
	if err != nil {
		return ctx.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid ID"})
	}

	if err := c.GitHubActionService.DeleteWorkflowRun(uint(id)); err != nil {
		return ctx.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return ctx.SendStatus(fiber.StatusNoContent)
}
