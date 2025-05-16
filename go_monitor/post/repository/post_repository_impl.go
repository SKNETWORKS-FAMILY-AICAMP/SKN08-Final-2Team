package repository

import (
	"snack/post/entity"

	"gorm.io/gorm"
)

// PostRepositoryImpl은 PostRepository 인터페이스를 구현하는 구조체
type PostRepositoryImpl struct {
	DB *gorm.DB
}

// NewPostRepositoryImpl은 PostRepositoryImpl을 초기화하는 함수
func NewPostRepositoryImpl(db *gorm.DB) PostRepository {
	return &PostRepositoryImpl{DB: db}
}

// Create는 게시글을 생성합니다.
func (r *PostRepositoryImpl) Create(post *entity.Post) error {
	return r.DB.Create(post).Error
}

// GetByID는 특정 ID의 게시글을 반환합니다.
func (r *PostRepositoryImpl) GetByID(id uint) (*entity.Post, error) {
	var post entity.Post
	if err := r.DB.First(&post, id).Error; err != nil {
		return nil, err
	}
	return &post, nil
}

// GetAll은 모든 게시글을 반환합니다.
func (r *PostRepositoryImpl) GetAll() ([]*entity.Post, error) {
	var posts []*entity.Post
	if err := r.DB.Find(&posts).Error; err != nil {
		return nil, err
	}
	return posts, nil
}

// Update는 게시글을 수정합니다.
func (r *PostRepositoryImpl) Update(post *entity.Post) error {
	return r.DB.Save(post).Error
}

// Delete는 게시글을 삭제합니다.
func (r *PostRepositoryImpl) Delete(id uint) error {
	return r.DB.Delete(&entity.Post{}, id).Error
}
