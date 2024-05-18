
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

## 처리율 제한장치 요구사항 예시

- 설정된 처리율을 초과화는 요청은 정확하게 제한
- 낮은 응답시간: HTTP 응답시간에 나쁜 영향을 주면 안된다
- 적은 메모리 사용
- 분산형 처리율 제한: 하나의 처리율 제한 장치를 여러 서버나 프로세스에서 공유
- 예외처리 : 요청이 제한되었을 때 사용자에게 분명하게 알려야함
- Fault Tolerance: 제한 장치에 장애가 생기더라도 전체 시스템에 영향을 주면 안됨

## 처리율 제한 장치는 어디에 둘까?

- 클라이언트 사이드 : 클라이언트는 쉽게 위변조 가능, 적합하지 않다.
- 서버 사이드: API 서버에 두거나 미들웨어로 만들어서 요청을 통제

APi 서버에)
![](/이우승/assets/ch-04/ch04_02.jpeg)

미들웨어로)
![](/이우승/assets/ch-04/ch04_03.jpeg)

## API Gateway
- 클라우드 서비스의 경우 처리율 제한 장치는 일반적으로 API Gateway라 불리는 컴포넌트에 구현됨
- 처리율 제한, SSL termination, 사용자 인증, IP 허용 목록 관리 등을 담당

API Gateway
- kong : https://konghq.com/products/kong-gateway
- tyk : https://tyk.io/
- krakenD : https://www.krakend.io/



처리율 제한 HTTP 헤더
postman이나 insomnia로 확인하는 거 적기

## 처리율 제한 알고리즘


### 토큰 버킷 알고리즘(Token Bucket)

- 간단하고, 보편적으로 사용됨

동작 원리
- 토큰 버킷은 지정된 용량을 갖는 컨테이너
- 사전 설정된 양의 토큰이 주기적으로 채워짐
- 꽉 찬 버킷에는 더 이상의 토큰이 추가 되지 않음
- 각 요청은 처리될 때마다 하나의 토큰 사용
- 충분한 토큰이 없으면 요청은 버려짐

![](/이우승/assets/ch-04/ch04_04.jpeg)

토큰 버킷 알고리즘 인자
- 버킷 크기 : 버킷에 담을 수 있는 토큰의 최대 개수
- 토큰 공급률 : 초당 몇 개의 토큰이 버킷에 공급되는가

버킷 사용 개수
- 통상적으로, API endpoint마다 별도의 버킷 사용
- IP 주소별로 처리율 제한을 사용하는 경우 IP 주소마다
- 시스템 전체에 적용하려는 경우 버킷을 하나 사용하여 적용

장점
- 구현이 쉬움
- 메모리 사용 측면에서 효율적
- 짧은 시간에 집중되는 트래픽 처리 가능

단점
- 버킷 크기와 공급률 조정이 까다로움


### 누출 버킷 알고리즘(Leaky Bucket)

- 요청 처리율이 고정되어 있음
	- 요청 처리율이 고정되었다는 건 시스템 부하를 방지하기 위해 일정한 처리량을 설정하는 건가?
- 일반적으로 FIFO 큐로 구현

동작원리
- 큐에 빈자리가 있으면 요청을 추가
- 큐가 가득 차 있는 경우 요청을 버림
- 지정된 시간마다 큐에서 요청을 꺼내서 처리

![](/이우승/assets/ch-04/ch04_05.jpeg)

인자값
- 버킷 크기 : 큐 사이즈와 같은 값
- 처리율 : 지정된 시간당 몇 개의 항목을 처리할지 지정

장점
- 큐의 크기가 제한되어 있어 메모리 사용량 측면에 효율적
- 고정된 처리율로 안정적 출력이 필요한 경우 적합

단점
- 단시간에 많은 트래픽이 몰리는 경우 요청들을 제때 처리 못하여 신규 요청이 버려지게 됨
- 인자값을 올바르게 튜닝하기 까다로움


### 고정 윈도 카운터 알고리즘(Fixed Window Counter)

동작원리
- 타임라인(timeline)을 고정된 간격의 윈도(window)로 나누고, 각 윈도마다 카운터를 붙임
- 요청이 접수될 때마다 카운터의 값을 1 증가
- 카운터 값이 사전에 설정된 임계치(threshold)에 도달하면 새로운 요청은 새 윈도가 열릴 때까지 버려짐

문제점
- 트래픽이 집중될 경우 의도한 것과 달리 더 많은 요청을 처리할 수 있음

![](/이우승/assets/ch-04/ch04_06.jpeg)

장점
- 메모리 효율이 좋다
- 이해하기 쉽다
- 윈도가 닫히는 시점에 카운터를 초기화하는 방식은 특정한 트래픽 패턴을 처리하기에 적합

단점
- 문제점에서 지적한 것과 같이 의도와 달리 많은 요청을 처리할 수 있음

### 이동 윈도 로깅 알고리즘(Sliding Window Log)

- 고정 윈도 카운터 알고리즘의 특정 구건 더 많은 트래픽 처리 문제를 해결함

동작원리
- 요청의 타임스탬프를 추적
- 타임스탬프 데이터는 보통 Redis의 sorted set 같은 캐시에 보관
- 신규 요청이 오면 만료된 타임 스탬프는 제거
	- 만료 타임스탬프는 그 값이 현재 윈도 시작 시점보다 오래된 타임스탬프
- 신규 요청의 타임스탬프를 로그에 추가
- 로그 크기가 허용치 보다 같거나 작으면 요청 처리, 그렇지 않으면 거부

![](/이우승/assets/ch-04/ch04_07.jpeg)

장점
- 처리율 제한 메커니즘 정교하다(?)

단점
- 다량의 메모리 사용


### 이동 윈도 카운터 알고리즘(Sliding Window Counter)

- 고정 윈도 + 윈도 로깅의 결합


![](/이우승/assets/ch-04/ch04_08.jpeg)

동작원리
- 현재 1분간의 요청 수 + 직전 1분 간의 요청 수 X 이동 윈도와 직전 1분이 겹치는 비율

장점
- 이전 시간대의 평균 처리율에 따라 현재 윈도의 상태를 계산하므로 짧은 시간에 몰리는 트래픽 대응에 좋음
- 메모리 효율이 좋다

단점
- 추정치 계산으로 적용되기 때문에 완벽하진 않음


## 개략적인 아키텍처

- 카운터를 추적 대상 별로 만든다 : 사용자별, IP 주소별, API 엔드포인트, 서비스 단위
	- -> 한도를 벗어나면 요청을 거부
- 카운터 보관은 어디에? -> 데이터베이스는 느리니 캐시이용
	- Redis는 이를 구현하기에 적합한 구조를 가짐
		- INCR : 메모리에 저장된 카운터 값을 1만큼 증가
		- EXPIRE : 카운터에 타임아웃 값 설정

## 상세설계

### 처리율 제한 규칙

- 처리율 제한 규칙은 보통 설정 파일 형태로 디스크에 저장

### 처리율 한도 초과 트래픽 처리

- 한도 제한에 걸리면 HTTP 429 (too many requests)를 반환
- 제한된 메시지 처리는 원하는 방법으로 -> 큐 보관하여 나중에 처리

처리율 제한 장치가 사용하는 HTTP 헤더
- X-Ratelimit-Remaining: 윈도 내에 남은 처리 가능 요청 수
- X-Ratelimit-Limit: 매 윈도마다 클라이언트가 전송할 수 있는 요청 수
- X-Ratelimit-Retry-After: 몇 초 뒤에 재요청 해야하는지 알림

상세 설계안

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*h70PQKa_ehiZAoUHFXhJkg.png)

- 처리율 제한 규칙은 디스크에서 workers가 가져와 캐시로 저장
- 클라이언트가 서버에 요청을 보내면 rate limiter 미들웨어에 도달
- 미들웨어는 제한 규칙을 캐시에서 가져옴
- redis에서는 카운터와 마지막 요청의 타임스탬프를 가져옴
- 제한에 걸리지 않으면 API 서버로 보냄
- 제한에 걸리면 429 반환

## 분산 환경에서의 처리율 제한 장치의 구현

- 경쟁 조건(Race Condition)과 동기화(synchronization)을 고려해야함

### 경쟁조건

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*all1QUICSpltt0PCRAxxAQ.png)

- 락을 거는 방식은 성능을 상당히 떨어뜨리기 때문에 지양
- 루아 스크립트를 사용하거나 Sorted Set이라는 레디스 자료구조를 사용

### Lua Script를 이용해서 경쟁조건 피하기

- Redis에서 Lua script는 atomic하게 처리함
- 카운터를 증가 시킬 때 Lua script로 증가하게 해서 경쟁 조건 피함


### Redis Sorted Set

- 데이터가 자동으로 정렬되는 자료구조
```
zadd user_score 2 user:4
```


![](/이우승/assets/ch-04/ch04_10.png)

Sorted Set으로 Limiter 구현

```
ZADD rate_limiter:123.456.789.0 1679251200 1679251200
```

```python
import time
import redis

# Initialize Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)


def is_rate_limited(client_id, window_seconds, max_requests):
	current_time = int(time.time()) # Get the current Unix timestamp
	key = f'rate_limiter:{client_id}' # Create a unique Redis key for the client
	# Remove timestamps that are outside the time window

	r.zremrangebyscore(key, '-inf', current_time - window_seconds)

	# Get the current request count for the client within the time window
	request_count = r.zcard(key)

	# Check if the request limit has been reached
	if request_count < max_requests:
		# Add the new request timestamp to the Sorted Set and set the expiration time
		r.zadd(key, {current_time: current_time})
		r.expire(key, window_seconds)
		return False # Not rate-limited
	else:
		return True # Rate-limited

# Example usage

client_id = '123.456.789.0'
window_seconds = 60
max_requests = 10

if is_rate_limited(client_id, window_seconds, max_requests):
	print('You have reached the maximum number of requests. Please try again later.')
else:
	print('Request allowed.')
```
근데 이 방식이 왜 race condition에 안전한건지 모르겠네...

### 동기화 이슈

- 레디스 같은 중앙 집중형 데이터 저장소를 써서 동기화 처리하는 게 좋음

### 성능 최적화

- 에지 서버를 이용해서 최적화 함

### 모니터링

다음을 위해 모니터링이 필요함
- 채택된 처리율 제한 알고리즘이 효과적인지
- 정의한 처리율 제한 규칙이 효과적인지


# 참고

API Gateway
- https://velog.io/@holicme7/Kong-API-Gateway-%EA%B8%B0%ED%83%80-Gateway-%EC%86%94%EB%A3%A8%EC%85%98-%EB%B9%84%EA%B5%90

Rate Limiter
- https://engineering.linecorp.com/ko/blog/high-throughput-distributed-rate-limiter
- https://medium.com/geekculture/system-design-design-a-rate-limiter-81d200c9d392

Lua Script
- https://dev.gmarket.com/69
- https://redis.io/learn/develop/java/spring/rate-limiting/fixed-window/reactive-lua