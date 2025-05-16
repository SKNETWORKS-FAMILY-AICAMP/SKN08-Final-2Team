package request_form

type WorkflowTriggerRequestForm struct {
	Token       string `json:"token"`
	RepoUrl     string `json:"repo_url"`
	WorkflowName string `json:"workflow_name"`
}
