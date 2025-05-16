from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl


class AuthenticationController(viewsets.ViewSet):
    redisCacheService = RedisCacheServiceImpl.getInstance()

    def requestKakaoLogout(self, request):
        postRequest = request.data
        userToken = postRequest.get("userToken")
        
        if userToken:
            try:
                accountId = self.redisCacheService.getValueByKey(userToken)
                self.redisCacheService.deleteKey(userToken)
                self.redisCacheService.deleteKey(accountId)
                return JsonResponse({"message": "로그 아웃 성공"}, status=status.HTTP_200_OK)
            
            except Exception as e:
                print(f"redis key 삭제 중 에러 발생: {e}")        # AAA
                return JsonResponse({"error": "코드 내부 에러"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse({"error": "userToken이 필요합니다"}, status=status.HTTP_400_BAD_REQUEST)

    def requestNaverLogout(self, request):
        postRequest = request.data
        userToken = postRequest.get("userToken")

        if not userToken:
            return JsonResponse({"error": "userToken이 필요합니다"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Redis에서 userToken을 기반으로 accountId 가져오기
            accountId = self.redisCacheService.getValueByKey(userToken)

            if accountId is None:
                print("Redis에서 userToken에 해당하는 accountId를 찾을 수 없음")       # AAA
                return JsonResponse({"error": "유효하지 않은 userToken입니다"}, status=status.HTTP_400_BAD_REQUEST)

            # Redis에서 해당 키 삭제 (로그아웃 처리)
            delete_token = self.redisCacheService.deleteKey(userToken)
            delete_account = self.redisCacheService.deleteKey(accountId)

            print(f"✅ 유저 토큰 삭제 성공: {delete_token}")      # AAA
            print(f"✅ 유저 accountId 삭제 성공: {delete_account}")  # AAA

            return JsonResponse({"message": "네이버 로그아웃 성공"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"❌ redis key 삭제 중 에러 발생: {e}")
            return JsonResponse({"error": "코드 내부 에러"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def requestGoogleLogout(self, request):
        postRequest = request.data
        userToken = postRequest.get("userToken")

        if not userToken:
            return JsonResponse({"error": "userToken이 필요합니다"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Redis에서 userToken을 기반으로 accountId 가져오기
            accountId = self.redisCacheService.getValueByKey(userToken)
            print(f"Redis에서 조회된 accountId: {accountId}")  # AAA 디버깅 확인

            if accountId is None:
                print(" Redis에서 userToken에 해당하는 accountId를 찾을 수 없음")      #    AAA
                return JsonResponse({"error": "유효하지 않은 userToken입니다"}, status=status.HTTP_400_BAD_REQUEST)

            # Redis에서 해당 키 삭제 (로그아웃 처리)
            self.redisCacheService.deleteKey(userToken)
            self.redisCacheService.deleteKey(accountId)
            print("구글 로그아웃 성공")                             # AAA 디버깅 확인
            print(f"유저 토큰 삭제 성공: {userToken}")              # AAA
            print(f"유저 accountId 삭제 성공: {accountId}")        # AAA

            return JsonResponse({"message": "구글 로그아웃 성공"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f" 구글 로그아웃 중 에러 발생: {e}")           #    AAA
            return JsonResponse({"error": "코드 내부 에러"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def requestGithubLogout(self, request):
        postRequest = request.data
        userToken = postRequest.get("userToken")

        if not userToken:
            return JsonResponse({"error": "userToken이 필요합니다"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Redis에서 userToken을 기반으로 accountId 가져오기
            accountId = self.redisCacheService.getValueByKey(userToken)
            print(f" Redis에서 조회된 accountId: {accountId}")  # AAA 디버깅 확인

            if accountId is None:
                return JsonResponse({"error": "유효하지 않은 userToken입니다"}, status=status.HTTP_400_BAD_REQUEST)

            self.redisCacheService.deleteKey(userToken)
            self.redisCacheService.deleteKey(accountId)
            print("GitHub 로그아웃 성공")                    # AAA 디버깅 확인
            print(f"유저 토큰 삭제 성공: {userToken}")        # AAA
            print(f"유저 accountId 삭제 성공: {accountId}")  # AAA

            return JsonResponse({"message": "GitHub 로그아웃 성공"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"GitHub 로그아웃 중 에러 발생: {e}")  # AAA 디버깅 확인
            return JsonResponse({"error": "코드 내부 에러"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def requestUserTokenValidation(self, request):
        postRequest = request.data
        userToken = postRequest.get("userToken")

        if not userToken:
            return JsonResponse({"valid": False, "error": "userToken이 필요합니다"},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            accountId = self.redisCacheService.getValueByKey(userToken)
            if not accountId:
                return JsonResponse({"valid": False}, status=status.HTTP_200_OK)

            return JsonResponse({"valid": True}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"valid": False, "error": "코드 내부 에러"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)