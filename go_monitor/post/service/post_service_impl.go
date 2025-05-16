package service

import (
	"snack/post/entity"
	"snack/post/repository"
)

// PostService는 비즈니스 로직을 처리
type PostServiceImpl struct {
	PostRepository repository.PostRepository
}

// NewPostService 생성자 함수
func NewPostService(postRepo repository.PostRepository) *PostServiceImpl {
	return &PostServiceImpl{PostRepository: postRepo}
}

// Create 게시글 생성
func (service *PostServiceImpl) Create(post *entity.Post) error {
	return service.PostRepository.Create(post)
}

// Read 특정 게시글 조회
func (service *PostServiceImpl) Read(id uint) (*entity.Post, error) {
	return service.PostRepository.GetByID(id)
}

// List 모든 게시글 조회
func (service *PostServiceImpl) List() ([]*entity.Post, error) {
	return service.PostRepository.GetAll()
}

// Update 게시글 수정
func (service *PostServiceImpl) Update(post *entity.Post) error {
	return service.PostRepository.Update(post)
}

// Delete 게시글 삭제
func (service *PostServiceImpl) Delete(id uint) error {
	return service.PostRepository.Delete(id)
}
