import 'package:kakao_flutter_sdk/kakao_flutter_sdk.dart';
import 'package:snack/kakao_authentication/domain/usecase/login_usecase.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../../domain/usecase/fetch_user_info_usecase.dart';
import '../../domain/usecase/request_user_token_usecase.dart';


class KakaoAuthProvider with ChangeNotifier {
  final LoginUseCase loginUseCase;
  final FetchUserInfoUseCase fetchUserInfoUseCase;
  final RequestUserTokenUseCase requestUserTokenUseCase;

  // Nuxt localStorage와 같은 역할, 보안이 필요한 데이터 저장
  final FlutterSecureStorage secureStorage = FlutterSecureStorage();

  String? _accessToken;
  String? _userToken;
  bool _isLoggedIn = false;
  bool _isLoading = false;
  String _message = '';

  // 해당 변수 값을 즉시 가져올 수 있도록 구성
  bool get isLoggedIn => _isLoggedIn;
  bool get isLoading => _isLoading;
  String get message => _message;

  KakaoAuthProvider({
    required this.loginUseCase,
    required this.fetchUserInfoUseCase,
    required this.requestUserTokenUseCase,
  }); // 객체 의존성 주입 받아 초기화

  Future<void> login() async {
    _isLoading = true;
    _message = '';
    notifyListeners();

    try {
      print("Kakao loginUseCase.execute()");
      _accessToken = await loginUseCase.execute();
      print("AccessToken obtained: $_accessToken");

      final userInfo = await fetchUserInfoUseCase.execute();
      print("User Info fetched: $userInfo");

      final email = userInfo.kakaoAccount?.email;
      final nickname = userInfo.kakaoAccount?.profile?.nickname;

      final accountPath = "Kakao";  // ✅ 추가
      final roleType = "USER";  // ✅ 추가

      print("User email: $email, User nickname: $nickname, Account Path: $accountPath, Role Type: $roleType");

      _userToken = await requestUserTokenUseCase.execute(
          _accessToken!, email!, nickname!, accountPath, roleType);

      print("User Token obtained: $_userToken");

      await secureStorage.write(key: 'userToken', value: _userToken);

      _isLoggedIn = true;
      _message = '로그인 성공';
      print("Login successful");
    } catch (e) {
      _isLoggedIn = false;
      _message = "로그인 실패: $e";
    }

    _isLoading = false;
    notifyListeners();
  }

  Future<User> fetchUserInfo() async {
    try {
      final userInfo = await fetchUserInfoUseCase.execute();
      return userInfo;
    } catch (e) {
      print("Kakao 사용자 정보 불러오기 실패: $e");
      rethrow;
    }
  }


  Future<void> logout() async {
    try {
      await UserApi.instance.logout();
      await secureStorage.delete(key: 'userToken');
      _isLoggedIn = false;
      notifyListeners();
    } catch (e) {
      print("Kakao 로그아웃 실패: $e");
    }
  }
}