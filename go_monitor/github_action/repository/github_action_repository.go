package repository

import (
	"snack/github_action/controller/response_form"
	"snack/github_action/entity"
)

// GitHubActionRepository는 GitHub API와 상호작용하는 저장소 인터페이스입니다.
type GitHubActionRepository interface {
	// 워크플로우 실행 정보를 GitHub API를 통해 가져옵니다.
	GetWorkflowRuns(repoUrl string, token string) ([]response_form.WorkflowRun, error)

	// 워크플로우 실행 정보를 데이터베이스에 저장합니다.
	SaveWorkflowRuns(workflows []entity.WorkflowRun) error

	// 특정 워크플로우 실행 정보를 ID로 가져옵니다.
	GetWorkflowRunByID(id uint) (*entity.WorkflowRun, error)

	// 특정 워크플로우 실행 정보를 데이터베이스에서 삭제합니다.
	DeleteWorkflowRun(id uint) error
}
