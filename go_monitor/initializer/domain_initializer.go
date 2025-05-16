package initializer

import (
	"first/post/entity" // entity 패키지 import
	"first/post/repository"
	"first/post/service"

	"github.com/google/wire"
	"github.com/joho/godotenv"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"

	// alias
	githubActionEntity "first/github_action/entity"
	githubActionRepo "first/github_action/repository"
	githubActionService "first/github_action/service"

	githubActionTriggerRepo "first/github_action_trigger/repository"
	githubActionTriggerService "first/github_action_trigger/service"

	"fmt"
	"os"
)

var PostSet = wire.NewSet(
	NewPostService,
	NewPostRepository,
)

// NewPostService 생성자 함수
func NewPostService(postRepo repository.PostRepository) service.PostService {
	return service.NewPostService(postRepo)
}

// NewPostRepository 생성자 함수
func NewPostRepository(db *gorm.DB) repository.PostRepository {
	return repository.NewPostRepositoryImpl(db)
}

var GitHubActionSet = wire.NewSet(
	NewGitHubActionService,
	NewGitHubActionRepository,
)

// NewGitHubActionService 생성자 함수
func NewGitHubActionService(gitHubActionRepo githubActionRepo.GitHubActionRepository) githubActionService.GitHubActionService {
	return githubActionService.NewGitHubActionServiceImpl(gitHubActionRepo)
}

// NewGitHubActionRepository 생성자 함수
func NewGitHubActionRepository(db *gorm.DB) githubActionRepo.GitHubActionRepository {
	return githubActionRepo.NewGitHubActionRepositoryImpl(db)
}

var GitHubActionTriggerSet = wire.NewSet(
	NewGitHubActionTriggerService,
	NewGitHubActionTriggerRepository,
)

// GitHubActionTrigger
func NewGitHubActionTriggerService(githubActionTriggerRepo githubActionTriggerRepo.GitHubActionTriggerRepository) githubActionTriggerService.GitHubActionTriggerService {
	return githubActionTriggerService.NewGitHubActionTriggerServiceImpl(githubActionTriggerRepo)
}

func NewGitHubActionTriggerRepository() githubActionTriggerRepo.GitHubActionTriggerRepository {
	return githubActionTriggerRepo.NewGitHubActionTriggerRepositoryImpl()
}

// DB를 초기화하고, wire를 통해 의존성을 주입하는 함수
func DomainInitializer() (*gorm.DB, error) {
	// .env 파일 로딩
	if err := godotenv.Load(); err != nil {
		return nil, fmt.Errorf("error loading .env file")
	}

	// MySQL 연결 설정
	dbUser := os.Getenv("DB_USER")
	dbPassword := os.Getenv("DB_PASSWORD")
	dbHost := os.Getenv("DB_HOST")
	dbPort := os.Getenv("DB_PORT")
	dbName := os.Getenv("DB_NAME")
	dbCharset := os.Getenv("DB_CHARSET")
	dbLoc := os.Getenv("DB_LOC")

	dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s?charset=%s&parseTime=True&loc=%s", dbUser, dbPassword, dbHost, dbPort, dbName, dbCharset, dbLoc)
	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		return nil, fmt.Errorf("error connecting to the database: %v", err)
	}

	// 테이블 마이그레이션
	if err := db.AutoMigrate(&entity.Post{}, &githubActionEntity.WorkflowRun{}); err != nil {
		return nil, fmt.Errorf("failed to auto-migrate: %v", err)
	}

	return db, nil
}
