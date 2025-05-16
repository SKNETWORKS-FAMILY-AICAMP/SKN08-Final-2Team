package service

type GitHubActionTriggerService interface {
	RunWorkflow(repoUrl string, token string, workflowFileName string) error
}
