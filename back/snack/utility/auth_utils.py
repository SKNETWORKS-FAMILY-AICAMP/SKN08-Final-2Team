from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl
from board.entity.board import Board
from comment.entity.comment import Comment
from account_profile.entity.account_profile import AccountProfile
from account.entity.role_type import RoleType


def is_authorized_user(board: Board, token: str) -> tuple[bool, int, str]:
    redisService = RedisCacheServiceImpl.getInstance()
    account_id = redisService.getValueByKey(token)

    if not account_id:
        return False, 401, "로그인 인증이 필요합니다."

    if not board or not board.author or not board.author.account:
        return False, 404, "게시글 또는 작성자 정보를 찾을 수 없습니다."

    try:
        user = AccountProfile.objects.get(account__id=account_id)
    except AccountProfile.DoesNotExist:
        return False, 404, "유저 정보를 찾을 수 없습니다."

    if user.get_role() == RoleType.ADMIN or str(account_id) == str(board.author.account.id):
        return True, 200, "인증 성공"

    return False, 403, "작성자 또는 관리자가 아닙니다."


def is_comment_authorized(comment: Comment, token: str) -> tuple[bool, int, str]:
    redisService = RedisCacheServiceImpl.getInstance()
    account_id = redisService.getValueByKey(token)

    if not account_id:
        return False, 401, "로그인 인증이 필요합니다."

    if not comment or not comment.author or not comment.author.account:
        return False, 404, "댓글 또는 작성자 정보를 찾을 수 없습니다."

    try:
        user = AccountProfile.objects.get(account__id=account_id)
    except AccountProfile.DoesNotExist:
        return False, 404, "사용자 정보를 찾을 수 없습니다."

    if user.get_role() == RoleType.ADMIN or str(account_id) == str(comment.author.account.id):
        return True, 200, "댓글 인증 성공"

    return False, 403, "댓글 작성자 또는 관리자가 아닙니다."

def get_user_info_from_token(request) -> tuple[int | None, bool]:
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    redis = RedisCacheServiceImpl.getInstance()
    account_id = redis.getValueByKey(token)

    if not account_id:
        return None, False

    try:
        user = AccountProfile.objects.get(account__id=account_id)
        is_admin = user.get_role() == RoleType.ADMIN
        return int(account_id), is_admin
    except AccountProfile.DoesNotExist:
        return None, False
