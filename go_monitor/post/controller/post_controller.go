package controller

import (
	"snack/post/entity"
	"snack/post/service"
	"strconv"

	"github.com/gofiber/fiber/v2"
)

// PostController 구조체
type PostController struct {
	PostService service.PostService
}

// NewPostController 생성자 함수
func NewPostController(service service.PostService) *PostController {
	return &PostController{PostService: service}
}

// CreatePost 게시글 생성 핸들러
func (c *PostController) CreatePost(ctx *fiber.Ctx) error {
	var post entity.Post
	if err := ctx.BodyParser(&post); err != nil {
		return ctx.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid request"})
	}

	if err := c.PostService.Create(&post); err != nil {
		return ctx.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return ctx.Status(fiber.StatusCreated).JSON(post)
}

// GetPostByID 특정 게시글 조회 핸들러
func (c *PostController) GetPostByID(ctx *fiber.Ctx) error {
	id, err := strconv.Atoi(ctx.Params("id"))
	if err != nil {
		return ctx.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid ID"})
	}

	post, err := c.PostService.Read(uint(id))
	if err != nil {
		return ctx.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "Post not found"})
	}

	return ctx.JSON(post)
}

// GetAllPosts 모든 게시글 조회 핸들러
func (c *PostController) GetAllPosts(ctx *fiber.Ctx) error {
	posts, err := c.PostService.List()
	if err != nil {
		return ctx.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return ctx.JSON(posts)
}

// UpdatePost 게시글 수정 핸들러
func (c *PostController) UpdatePost(ctx *fiber.Ctx) error {
	id, err := strconv.Atoi(ctx.Params("id"))
	if err != nil {
		return ctx.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid ID"})
	}

	var post entity.Post
	if err := ctx.BodyParser(&post); err != nil {
		return ctx.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid request"})
	}

	post.ID = uint(id)
	if err := c.PostService.Update(&post); err != nil {
		return ctx.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return ctx.JSON(post)
}

// DeletePost 게시글 삭제 핸들러
func (c *PostController) DeletePost(ctx *fiber.Ctx) error {
	id, err := strconv.Atoi(ctx.Params("id"))
	if err != nil {
		return ctx.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid ID"})
	}

	if err := c.PostService.Delete(uint(id)); err != nil {
		return ctx.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return ctx.SendStatus(fiber.StatusNoContent)
}
