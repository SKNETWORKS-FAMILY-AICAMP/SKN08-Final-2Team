from django.shortcuts import render

from account_profile.entity.account_profile import AccountProfile

class MypageController(viewsets.ViewSet):
    __accountService = AccountServiceImpl.getInstance()
    __accountProfileService = AccountProfile.getInstance()
    __boardService = BoardServiceImpl.getInstance()
    __commentService = CommentServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()


    pass