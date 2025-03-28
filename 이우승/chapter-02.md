
# 개략적인 규모 추정

- (back-of-the-envelope estimation)
- 보편적 성능 수치상에서 사고 실험을 통해 추정치를 계산하는 행위

### 2의 제곱
- 2^10 : 1킬로바이트
- 2^20 : 1메가바이트
- 2^30 : 1기가바이트
- 2^40 : 1테라바이트
- 2^50 : 1페타바이트

### 모든 프로그래머가 알아야 하는 응답지연 값

![](/이우승/assets/ch-02/ch02_01.png)

- 메모리는 빠르지만 디스크는 느리다
- 디스크 탐색은 피하자
- 단순 압축은 빠르다
- 데이터 전송 시 압축하여 전송하자
- 센터간 데이터 전송은 느리다


## 가용성 수치들

- 고가용성은 오랜 시간 중단 없이 운영될 수 있는 능력
- 퍼센트로 표시, 100%는 무중단

![](/이우승/assets/ch-02/ch02_02.png)

![](/이우승/assets/ch-02/ch02_03.png)

## QPS 추정

- 일간 능동 사용자 : 1.5억
- 사용자당 쿼리 : 2
- 평균 미디어 사용량 : 전체의 10%
- QPS = 1.5억 x 2 / 24시간 /3600초 = 3500
- 최대 QPS = 2 x QPS = 7000

미디어 저장
- 쿼리 한 건 데이터 크기
	- tweet_id : 64Byte
	- text : 140Byte
	- media : 1MB
- 저장소 요구량 : 1.5억 x 2 x 10% x 1MB = 30TB/일간

## 참고

### 가용성 수치
- https://soufianebouchaa.medium.com/sla-and-slo-fundamentals-and-how-to-calculate-sla-7f3e75831f79