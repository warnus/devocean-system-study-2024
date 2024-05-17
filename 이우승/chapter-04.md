
# 처리율 제한 장치의 설계

- 처리율 제한 장치(rate limiter) : 클라이언트 또는 서비스가 보내는 트래픽의 처리율을 제어하기 위한 장치
- ex) 특정 기간 요청되는 HTTP 횟수 제한
- 임계치를 넘는 요청은 중단 시킴

사례
- 사용자는 초당 2회 이상 새 글을 올릴 수 없음
- 같은 IP주소로 하루 10개 이상의 계정을 생성할 수 없음

제한 장치의 이점
- DoS 공격 방지
- 비용 절감 : 서버를 불필요하게 많이 둘 필요 없음
- 서버 과부하 방지 : 봇에서 오는 트래픽이나 사용자의 잘못된 이용 패턴 예벙
	- ex) 무분별한 크롤링

DoS(Denial of Service)란?
- 장치의 정상적인 작동을 방해
- 정상적인 트래픽을 처리 할 수 없을 때까지 대상 시스템에 요청을 폭주시킴

DDoS(Distributed DoS) vs DoS
![](/이우승/assets/ch-04/ch04_01.png)

DDoS 공격 유형 참고 : https://www.cloudflare.com/ko-kr/learning/ddos/what-is-a-ddos-attack/

API Gateway
- kong

윈도우 로깅
- 1분 내에 다른 요청이 오면 못하게 하는 걸로 잘 동작할 거 같은데..

처리율 제한 HTTP 헤더
postman이나 insomnia로 확인하는 거 적기