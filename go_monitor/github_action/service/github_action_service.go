package service

import (
	"snack/github_action/controller/response_form"
	"snack/github_action/entity"
)

// GitHubActionService는 GitHub API와 상호작용하는 비즈니스 로직을 처리합니다.
type GitHubActionService interface {
	// 워크플로우 실행 정보를 가져옵니다.
	GetWorkflowRuns(repoUrl string, token string) ([]response_form.WorkflowRun, error)

	// 워크플로우 실행 정보를 데이터베이스에 저장합니다.
	SaveWorkflowRuns(workflows []entity.WorkflowRun) error

	// 특정 워크플로우 실행 정보를 가져옵니다.
	GetWorkflowRunByID(id uint) (*entity.WorkflowRun, error)

	// 특정 워크플로우 실행 정보를 삭제합니다.
	DeleteWorkflowRun(id uint) error
}
