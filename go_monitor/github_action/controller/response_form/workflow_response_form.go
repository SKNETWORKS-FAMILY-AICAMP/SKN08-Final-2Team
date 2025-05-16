package response_form

type WorkflowRun struct {
	ID         int    `json:"id"`
	Name       string `json:"name"`
	Status     string `json:"status"`
	Conclusion string `json:"conclusion"`
	CreatedAt  string `json:"created_at"`
	URL        string `json:"url"`
	HTMLURL    string `json:"html_url"`
}
