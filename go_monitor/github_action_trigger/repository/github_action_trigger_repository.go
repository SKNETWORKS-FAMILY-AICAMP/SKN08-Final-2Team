package repository

type GitHubActionTriggerRepository interface {
	TriggerWorkflow(repoUrl string, token string, workflowFileName string) error
}
