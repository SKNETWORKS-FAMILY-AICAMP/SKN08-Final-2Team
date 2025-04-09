import uuid

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.response import Response

from account.service.account_service_impl import AccountServiceImpl
from account_profile.service.account_profile_service_impl import AccountProfileServiceImpl
from github_action_monitor.service.github_action_monitor_service_impl import GithubActionMonitorServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl


class GithubActionMonitorController(viewsets.ViewSet):
    githubActionMonitorService = GithubActionMonitorServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()

    accountService = AccountServiceImpl.getInstance()
    accountProfileService = AccountProfileServiceImpl.getInstance()

    def requestGithubActionWorkflow(self, request):  # 비동기 POST 요청 처리
        try:
            # 요청 데이터에서 userToken과 repoUrl 가져오기
            postRequest = request.data
            userToken = postRequest.get("userToken")
            repoUrl = postRequest.get("repoUrl")

            # 로그로 확인
            print(f"Request received: userToken={userToken}, repoUrl={repoUrl}")

            if not userToken or not repoUrl:
                return Response(
                    {"message": "userToken과 repoUrl이 제공되지 않았습니다."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            accountId = self.redisCacheService.getValueByKey(userToken)
            token = self.redisCacheService.getValueByKey(accountId)

            # GitHub Workflow 데이터 가져오기
            workflowData = self.githubActionMonitorService.requestGithubActionWorkflow(token, repoUrl)

            if workflowData is None:
                return Response(
                    {"message": "워크플로우 데이터를 가져오는 데 실패했습니다."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            print(f"workflowData: {workflowData}")

            # 성공적으로 데이터를 가져왔다면
            return Response({"workflowInfo": workflowData}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error in requestGithubActionWorkflow: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
