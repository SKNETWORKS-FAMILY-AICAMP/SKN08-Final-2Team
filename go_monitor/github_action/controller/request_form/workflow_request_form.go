package request_form

type WorkflowRequest struct {
	RepoUrl string `json:"repo_url"`
	Token   string `json:"token"`
}
