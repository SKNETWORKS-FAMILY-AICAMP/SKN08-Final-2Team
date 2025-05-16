package entity

import "gorm.io/gorm"

type Post struct {
	gorm.Model   // 기본 필드: ID, CreatedAt, UpdatedAt, DeletedAt
	Title   string `gorm:"size:255"`
	Content string
}