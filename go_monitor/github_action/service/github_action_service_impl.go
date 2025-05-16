package service

import (
	"errors"
	"snack/github_action/controller/response_form"
	"snack/github_action/entity"
	"snack/github_action/repository"
)

// GitHubActionServiceImpl은 GitHubActionService 인터페이스를 구현하는 구조체입니다.
type GitHubActionServiceImpl struct {
	GitHubActionRepo repository.GitHubActionRepository
}

// NewGitHubActionServiceImpl 생성자 함수
func NewGitHubActionServiceImpl(gitHubActionRepo repository.GitHubActionRepository) GitHubActionService {
	return &GitHubActionServiceImpl{GitHubActionRepo: gitHubActionRepo}
}

// GetWorkflowRuns 구현
func (s *GitHubActionServiceImpl) GetWorkflowRuns(repoUrl string, token string) ([]response_form.WorkflowRun, error) {
	// GitHub API와 상호작용하여 워크플로우 실행 정보 가져오기 (실제 API 호출 로직은 여기서 구현)
	return s.GitHubActionRepo.GetWorkflowRuns(repoUrl, token)
}

// SaveWorkflowRuns 구현
func (s *GitHubActionServiceImpl) SaveWorkflowRuns(workflows []entity.WorkflowRun) error {
	return s.GitHubActionRepo.SaveWorkflowRuns(workflows)
}

// GetWorkflowRunByID 구현
func (s *GitHubActionServiceImpl) GetWorkflowRunByID(id uint) (*entity.WorkflowRun, error) {
	workflowRun, err := s.GitHubActionRepo.GetWorkflowRunByID(id)
	if err != nil {
		return nil, err
	}
	if workflowRun == nil {
		return nil, errors.New("workflow run not found")
	}
	return workflowRun, nil
}

// DeleteWorkflowRun 구현
func (s *GitHubActionServiceImpl) DeleteWorkflowRun(id uint) error {
	workflowRun, err := s.GitHubActionRepo.GetWorkflowRunByID(id)
	if err != nil {
		return err
	}
	if workflowRun == nil {
		return errors.New("workflow run not found")
	}
	return s.GitHubActionRepo.DeleteWorkflowRun(id)
}
