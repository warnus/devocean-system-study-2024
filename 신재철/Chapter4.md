# 처리율 제한 장치의 설계
네트워크 시스템에서 처리율 제한 장치(rate limiter)는 클라이언트 또는 서비스가 보내는 트래픽의 처리율을 제어하기 위한 장치다. 

- 사용자는 초당 2회 이상 새 글을 올릴 수 없다.
- 같은 IP 주소로는 하루에 10개 이상의 계정을 생성할 수 없다.
- 같은 디바이스로는 주당 5회 이상 리워드를 요청할 수 없다.

API 처리율 제한 장치를 두면 좋은 점
- DoS(Denial of Service) 공격에 의한 자원 고갈(resource starvation)을 방지할 수 있다. 처리율 제한 장치는 추가 요청에 대해서는 처리를 중단함으로써 DoS 공격을 방지한다.
- 비용을 절감한다. 추가 요청에 대한 처리를 제한하면 서버를 많이 두지 않아도 되고, 우선순위가 높은 API에 더 많은 자원을 할당할 수 있다. 
- 서버 과부하를 막는다. 봇에서 오는 트래픽이나 사용자의 잘못된 이용 패턴으로 유발된 트래픽을 걸러내는데 처리율 제한 장치를 활용할 수 있다.

## 1단계: 문제 이해 및 설계 범위 확정
처리율 제한 장치를 구현하는 데는 여러 가지 알고리즘을 사용할 수 있는데, 그 각각은 고유한 장단점을 갖고 있다. 면접관과 소통하면 어떤 제한 장치를 구현해야 하는지 분명히 할 수 있다.

### 요구사항
- 설정된 처리율을 초과하는 요청은 정확하게 제한한다.
- 낮은 응답시간: 이 처리율 제한 장치는 HTTP 응답시간에 나쁜 영향을 주어서는 곤란하다.
- 가능한 한 적은 메모리를 써야 한다.
- 분산형 처리율 제한: 하나의 처리율 제한 장치를 여러 서버나 프로세스에서 공유할 수 있어야 한다.
- 예외 처리: 요청이 제한되었을 때는 그 사실을 사용자에게 분명하게 보여주어야 한다.
- 높은 결함 감내성: 제한 장치에 장애기 생기더라도 전체 시스템에 영향을 주어서는 안 된다.

## 2단계: 개략적 설계안 제시 및 동의 구하기
일을 너무 복잡하게 만드는 것은 피하고, 기본적인 클라이언트-서버 통신 모델을 사용하자.

### 처리율 제한 장치는 어디에 둘 것인가?
직관적으로 보자면 이 장치는 클라이언트 측에 둘 수도 있고, 서버 측에 둘 수도 있다.
- 클라이언트: 위변조가 가능해지고, 모든 클라이언트의 구현을 통제하는 것은 어려울 수 있다.
- 서버: 서버에서 요청을 받은 후 장치를 동작 시킴.
- 미들웨어: 요청이 서버에 들어가기 전에 미들웨어에서 통제 (Too many requests, 429 code)

정답은 없지만 고려해봐야 할 점이 있음.
- 프로그래밍 언어, 캐시 서비스 등 현재 사용하고 있는 기술 스택을 점검. 현재 기술스택이 서버 측 구현을 지원하기에 충분히 효율이 높은지.
- 사업 필요에 맞는 처리율 제한 알고리즘을 찾기. 제 3 사업자가 제공하는 게이트웨이를 사용하기로 했다면 선택지는 제한될 수 있지만, 직접 구현한다면 자유롭게 선택 가능.
- MSA 구조를 이미 사용하고 있고 API 게이트웨이를 이미 설계에 포함시켰다면 처리율 제한 기능 또한 게이트웨이에 포함시켜야 할 수 있음.
- 처리율 제한 서비스를 직접 만드는 데는 시간이 들어 상용 서비스를 사용하는게 바람직할 수도 있음.

### 처리율 제한 알고리즘

#### 토큰 버킷 알고리즘
지정된 용량을 갖는 컨테이너이며, 이 버킷에는 사전 설정된 양의 토큰이 주기적으로 채워짐. 토큰이 꽉 찬 버킷에는 더 이상의 토큰은 추가되지 않음.
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcEaUA7%2FbtsBbLGNjgl%2Fo5qEQ3uSpyoL16GDjSnTb1%2Fimg.png)

각 요청은 처리될 때마다 하나의 토큰응 사용. 
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcIO7q7%2FbtsBgbjVugB%2Fz17op0f1Kiw4gKHUAVIEFk%2Fimg.png)

통상적으로 API 엔드포인트마다 별도의 버킷을 둔다. 예를 들어, 사용자마다 하루에 한 번만 포스팅을 할 수 있고, 친구는 150명까지 추가할 수 있고, 좋아요 버튼은 다섯 번까지만 누를 수 있다면, 사용자마다 3개의 버킷을 두어야 한다.

**파라미터**
- 버킷 크기: 버킷에 담을 수 있는 토큰의 최대 개수
- 토큰 공급률: 초당 몇 개의 토큰이 버킷에 공급되는가

**장점**
- 구현이 쉽다.
- 메모리 사용 측면에서도 효율적이다.
- 짧은 시간에 집중되는 트래픽도 처리 가능하다. 

**단점**
- 이 알고리즘은 버킷 크기와 토큰 공급률이라는 두 개 인자를 가지고 있는데, 이 두 값을 적절하게 튜닝하는 것은 까다로운 일이다.

#### 누출 버킷 알고리즘
토큰 버킷 알고리즘과 비슷하지만 요청 처리율이 고정되어 있다는 점이 다르다. 누출 버킷 알고리즘은 보통 FIFO 큐로 구현한다.

동작 원리는 다음과 같다.
- 요청이 도착하면 큐가 가득 차 있는지 본다. 빈자리가 있는 경우에는 큐에 요청을 추가한다.
- 큐가 가득 차 있는 경우에는 새 요청은 버린다.
- 지정된 시간마다 큐에서 요청을 꺼내어 처리한다.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fbj6CQ1%2FbtsBfw9FHb8%2FS9wnYBuAoWHIZGKqBfyGk0%2Fimg.png)

**파라미터**
- 버킷 크기: 큐 사이즈와 같은 값. 큐에는 처리될 항목들이 보관됨.
- 처리율: 지정된 시간당 몇 개의 항목을 처리할지 지정하는 값. 보통 초 단위로 표현.

**장점**
- 큐의 크기가 제한되어 있어 메모리 사용량 측면에서 효율적.
- 고정된 처리율을 갖고 있기 때문에 안정적 출력이 필요한 경우 적합.

**단점**
- 단시간에 많은 트래픽이 몰리;는 경우 큐에는 오래된 요청들이 쌓이게 되고, 그 요청들을 제때 처리 못하면 최신 요청들은 버려지게 된다.
- 두 개 인자를 갖고 있는데, 튜닝이 어렵다.

#### 고정 윈도 카운터 알고리즘
- 타임라인을 고정된 간격의 윈도로 나누고, 각 윈도마다 카운터를 붙인다.
- 요청이 접수될 때마다 이 카운터의 값은 1씩 증가한다.
- 이 카운터의 값이 사전에 설정된 임계치에 도달하면 새로운 요청은 새 윈도가 열릴 때까지 버려진다.
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FBTtvT%2FbtsBb6Rumc1%2FCyw1gaZXhzixjFrocGxC6K%2Fimg.png)

이 알고리즘의 가장 큰 문제는 윈도의 경계 부근에 순간적으로 많은 트래픽이 집중될 경우 윈도에 할당된 양보다 더 많은 요청이 처리될 수 있다.
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FMb2Ux%2FbtsBfxOjRFv%2FKl8AUNE3j0N7itvZbBKTk1%2Fimg.png)


**장점**
- 메모리 효율이 좋다.
- 이해하기 쉽다.
- 윈도가 닫히는 시점에 카운터를 초기화하는 방식은 특정한 트래픽 패턴을 처리하기에 적합하다.

**단점**
- 윈도 경계 부근에서 일시적으로 많은 트래픽이 몰려드는 경우, 기대했던 시스템의 처리 한도보다 많은 양의 요청을 처리하게 된다.

#### 이동 윈도 로깅 알고리즘
고정 윈도 카운터 알고리즘에는 경계 부분에서 트래픽이 집중될 수 있는 문제가 있다. 이 알고리즘은 해당 문제를 해결한다.

- 요청의 타임스탬프를 추적한다. 타임스탬프는 레디스의 정렬 집합 같은 캐시에 보관한다.
- 새 요청이 오면 만료된 타임스탬프는 제거한다.
- 새 요청의 타임스탬프를 로그에 추가한다.
- 로그의 크기가 허용치보다 같거나 작으면 요청을 시스템에 전달한다. 그렇지 않은 경우 처리를 거부한다.
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FXwDFG%2FbtsBeUwfApR%2FBdOjdehKPA7ikTJTZakkQK%2Fimg.png)

**장점**
- 이 알고리즘이 구현하는 처리율 제한 메커니즘은 아주 정교하다. 어느 순간의 윈도를 보더라도, 허용되는 요청의 개수는 시스템의 처리율 한도를 넘지 않는다.

**단점**
이 알고리즘은 다량으 메모리를 사용하는데, 거부된 요청의 타임스탬프도 보관하기 때문이다.

#### 이동 윈도 카운터 알고리즘
고정 윈도 카운터 알고리즘과 이동 윈도 로깅 알고리즘을 결합한 알고리즘이다.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FwP6Jz%2FbtsBcUjbipT%2FVbBlJmOhLkwnCkpQHlk3g1%2Fimg.png)

처리율 제한 장치의 한도가 분당 7개 요청을 설정되어 있다고 하고, 이전 1분 동안 5개의 요청이, 그리고 현재 1분 동안 3개의 요청이 왔다고 해 보자. 

- 현재 1분간의 요청 수 + 직전 1분간의 요청 수 * 이동 윈도와 직전 1분이 겹치는 비율
- 이 공식에 따르면 현재 윈도에 들어 있는 요청은 `3 + 5 * 0.7 = 6.5`개다. 

분당 7개 요청이라고 했으므로, 현재 1분의 30% 시점에 도착한 신규 요청은 시스템으로 전달될 것이다. 

**장점**
- 이전 시간대의 평균 처리율에 따라 현재 윈도의 상태를 계산하므로 짧은 시간에 몰리는 트래픽에도 잘 대응한다.
- 메모리 효율이 좋다.

**단점**
- 직전 시간대에 도착한 요청이 균등하게 분포되어 있다고 가정한 상태에서 추정치를 계산하기 때문에 다소 느슨하다. 하지만 심각하진 않다.

### 개략적인 아키텍처

처리율 제한 알고리즘의 기본 아이디어는 단순하다. 
얼마나 많은 요청이 접수되었는지를 추적할 수 있는 카운터를 대상별로 두고(사용자, IP, API, 서비스, ... 등) 카운팅을 하여 한도가 넘어가는 요청을 거부하는 것이다.

데이터베이스는 디스크 접근 때문에 느리기 때문에 메모리 기반인 레디스를 많이 사용한다.

아래 레디스 명령어를 활용할 수 있다.
- INCR: 메모리에 저장된 카운터의 값을 1만큼 증가시킨다.
- EXPIRE: 카운터에 타임아웃 값을 설정한다. 설정된 시간이 지나면 카운터는 자동으로 삭제된다.

동작 원리
1. 클라이언트가 처리율 제한 미들웨어에게 요청을 보냄
2. 처리율 제한 미들웨어는 레디스의 지정 버킷에서 카운터를 가져와 한도 체크
   1. 한도에 도달했다면 요청은 거부
3. 한도에 도달하지 않았다면 요청은 API 서버로 전달. 미들웨어는 카운터의 값을 증가시켜 레디스에 저장.

## 3단계: 상세 설계
- 처리율 제한 규칙은 어떻게 만들어지고 어디에 저장되는가?
- 처리가 제한된 요청들은 어떻게 처리되는가?

### 처리율 제한 규칙
보통 설정 파일 형태로 디스크에 저장됨.

### 처리율 한도 초과 트래픽의 처리
요청이 한도 제한에 걸리면 429 응답(too many requeests)을 클라이언트에 보냄. 큐에 저장하여 나중에 처리할 수도 있음.

#### 처리율 제한 장치가 사용하는 HTTP 헤더
- X-Ratelimit-Remaining: 윈도 내 남은 처리 가능 요청의 수
- X-Ratelimit-Limit: 매 윈도마다 클라이언트가 전송할 수 있는 요청의 수
- X-Ratelimit-Retry-After: 한도 제한에 걸리지 않으려면 몇 초 뒤에 요청을 다시 보내야 하는지 알림

### 상세 설계
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FHqE5u%2FbtsBcSeBmvG%2FV9YO6sYME1MZX67UKRWAO1%2Fimg.png)

### 분산 환경에서의 처리율 제한 장치의 구현
한 대의 서버에서 구현은 쉽지만 여러 대의 서버와 병렬 스레드를 지원하도록 시스템을 확장하는 것은 또 다른 문제다. 다음 문제가 있다.
- 경쟁 조건 (race condition)
- 동기화(synchronization)

#### 경쟁 조건
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FOjTNs%2FbtsBaYGHrRi%2F1brvCLf3DzAki1ZE7KW1pK%2Fimg.png)

- 두 개 요청을 처리하는 스레드가 병렬로 카운터 값을 읽었으며 아직 변경한 값을 저장하지 않은 상태라고 가정.
- 둘 다 카운터를 하나 증가시킨 값을 레디스에 기록할 것이며, 4로 저장되게 될 수 있음.
- 락으로 해결할 수 있으나, 시스템의 성능을 상당히 떨어뜨릴 수 있음.
  - 루아 스크립트나 정렬 집합(sorted set)이라 불리는 레디스 자료구조를 사용하여 해결할 수 있음

#### 동기화 이슈
수백만 사용자를 지원하려면 한 대의 처리율 제한 장치 서버로는 충분하지 않을 수 있음. 그래서 여러 처리율 제한 장치 서버를 두면 동기화가 필요해짐. 
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcPTZBY%2FbtsBfMR2zBG%2FOqhZwPZD2P4EeNbXL1DCMK%2Fimg.png)

해결방법
- 고정 세션(sticky session)을 활용해 같은 클라이언트로부터의 요청은 항상 같은 처리율 제한 장치로 보낼 수 있도록 해야함
  - 규모면에서 확장 가능하지도 않고 유연하지도 않아 추천하지는 않음
- 레디스와 같은 중앙 집중형 데이터 저장소를 사용하는 것

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbpYvkn%2FbtsBcRzZ5hL%2FUqsTKPGsVGPqSBOADzi0e0%2Fimg.png)

### 성능 최적화 
데이터 센터를 지원하는 문제는 처리율 제한 장치에서 매우 중요한 문제다. 데이터센터에서 멀리 떨어진 사용자를 지원하려면 지연시간(latency)이 증가할 수 밖에 없기 때문이다.

다음으로 고려해야 할 것은, 제한 장치 간에 데이터를 동기화할 때 최정 일관성 모델(eventual consistency model)을 사용하는 것이다.

### 모니터링
처리율 제한 장치를 설치한 이후에는 효과적으로 동작하고 있는지 보기 위해 데이터를 모아 볼 필요가 있다. 다음을 확인하고자 한다.
- 채택된 처리율 제한 알고리즘이 효과적이다.
- 정의한 처리율 제한 규칙이 횩과적이다.

규칙을 잘못 설정한다면 많은 요청이 버려지거나 너무 많은 요청을 받게 되버릴 수 있어 검토해볼 수 있다.

## 4단계: 마무리
시간이 허락한다면 다음과 같은 부분을 언급해보면 도움이 된다.

- 경성(hard) 또는 연성(soft) 처리율 제한
  - 경성 처리율 제한: 요청의 개수는 임계치를 절대 넘어설 수 없다.
  - 연성 처리율 제한: 요청 개수는 잠시 동안은 임계치를 넘어설 수 있다.
- 다양한 계층에서의 처리율 제한
  - 이번 장에서는 애플리케이션 계층에서만 살펴보았으나, 다른 계층에 처리율 제한도 가능하다. 예를 들면, Iptables를 사용하면 IP 주소(OSI 3번 계층)에 적용이 가능하다.
- 처리율 제한을 회피하는 방법. 클라리언트는 어떻게 설계하는게 최선인가?
  - 클라이언틑 측 캐시를 사용하여 API 호출 횟수를 줄인다.
  - 처리율 제한의 임계치를 이해하고, 짧은 시간 동안 너무 많은 요청을 보내지 않도록 한다.
  - 예외나 에러를 처리하는 코드를 도입하여 클라이언트가 예외적 상황으로부터 우아하게(gracefully) 복구될 수 있도록 한다.
  - 재시도(retry) 로직을 구현할 때는 충분한 백오프(back-off) 시간을 둔다.
