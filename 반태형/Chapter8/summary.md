# URL 단축기 설계

## 문제 이해 및 설계범위 확정
* 매일 1억개 생성
* 단축 URL에는 숫자 + 영문자만 사용
* 축약된 URL 을 원래 URL 로 리다이렉트
* 높은 가용성, 규모 확장성, 장애 감내
* 초당 쓰기 : 1160
* 읽기: 10:1이라 가정하고 11600
* 1억 * 10년 = 3650억개의 레코드, 약 36.5TB

## 개략적 설계
* 클라이언트는 단축 URL 방문
* 301 + location 원래 url
* 원래 url 방문
* 301: 이전됨, 브라우저 캐시 가능
* 302: 일시적으로 Location 의 url 로 처리
*  301 / 302 는 요청을 get 으로 변경한다.
* 307 /308을 고려해야할 수도 있다.
* https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/301
* https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/301
* https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/307
* https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/308
* URL 단축은 도메인/{hashValue} 라고 하면 해시함수를 정의하는 것이다.
* 입력이 다르면 해시값도 다르고 해시값을 원래 url 로 바꿀수 있어야 한다.

## 상세 설계
* 우리는 62개의 문자를 사용할 수 있고 62^7이 약 3.5조개의 url 을 만든다.
* 긴 url 을 줄이려면 해시함수 / base-62 변환이다.
* 해시함수
    * long url -> 해시 -> short url -> 디비에 없으면 저장, 있으면 특정 문자열 추가후 다시 해시함수
    * 고정된 결과값
    * 유일성보장 ID는 필요하지 않음
    * 충돌 해소필요
    * 다음에 사용할 url 을 알아내기 어렵다.
* base62
    * 62 진수로 값을 표현한다.
    * 단점은 유일성 보장 ID 생성기가 필요하다.
    * ID가 길어지면 같이 길어진다.
    * 다음 사용될 url을 쉽게 알아낸다.
