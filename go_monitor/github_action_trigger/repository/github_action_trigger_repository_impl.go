package repository

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
)

type GitHubActionTriggerRepositoryImpl struct{}

// NewGitHubActionTriggerRepositoryImpl 생성자 함수
func NewGitHubActionTriggerRepositoryImpl() GitHubActionTriggerRepository {
	return &GitHubActionTriggerRepositoryImpl{}
}

func (r *GitHubActionTriggerRepositoryImpl) TriggerWorkflow(repoUrl, token, workflowFileName string) error {
	owner, repo, err := parseRepoURL(repoUrl)
	if err != nil {
		return fmt.Errorf("invalid repo URL: %w", err)
	}
	fmt.Printf("📦 Repository: %s/%s\n", owner, repo)

	apiURL := fmt.Sprintf("https://api.github.com/repos/%s/%s/actions/workflows/%s/dispatches", owner, repo, workflowFileName)
	fmt.Printf("🔗 GitHub API URL: %s\n", apiURL)

	payload := map[string]interface{}{
		"ref": "main",
		"inputs": map[string]string{
			"triggered_by": "Go Trigger",
		},
	}

	body, _ := json.Marshal(payload)
	fmt.Printf("📤 Payload: %s\n", string(body))

	req, err := http.NewRequest("POST", apiURL, bytes.NewBuffer(body))
	if err != nil {
		return fmt.Errorf("❌ Failed to create request: %w", err)
	}

	req.Header.Set("Authorization", "Bearer "+token)
	req.Header.Set("Accept", "application/vnd.github+json")
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return fmt.Errorf("❌ Request failed: %w", err)
	}
	defer resp.Body.Close()

	fmt.Printf("📡 Response Status: %d %s\n", resp.StatusCode, http.StatusText(resp.StatusCode))

	if resp.StatusCode != 204 {
		var resBody bytes.Buffer
		resBody.ReadFrom(resp.Body)
		return fmt.Errorf("❌ GitHub API returned status %d: %s", resp.StatusCode, resBody.String())
	}

	fmt.Println("✅ 워크플로우 트리거 성공")
	return nil
}

// parseRepoURL extracts owner and repo from full repo URL
func parseRepoURL(repoUrl string) (string, string, error) {
	// Example input: https://github.com/owner/repo
	trimmed := strings.TrimPrefix(repoUrl, "https://github.com/")
	parts := strings.Split(trimmed, "/")
	if len(parts) < 2 {
		return "", "", fmt.Errorf("invalid repo URL")
	}
	return parts[0], parts[1], nil
}
