
# 채팅 시스템 설계


## 개략적 설계안 제시 및 동의 구하기

- 채팅 시스템의 경우 클라이언트는 모바일 앱이거나 웹 애플리케이션
- 클라이언트는 서로 직접 통신하지 않는다

채팅 서비스 기능 제공
- 클라이언트들로 부터 메시지 수신
- 메시지 수신자(recipient) 결정 및 전달
- 수신자가 접속(online) 상태가 아닌 경우 접속할 때까지 해당 메시지 보관

![](/이우승/assets/ch-12/ch12_01.jpeg)

- 채팅을 시작하려는 클라이언트는 네트워크 통신 프로토콜을 사용하여 서비스 접속
- 채팅 서비스의 경우 어떤 통신 프로토콜을 사용할 것인지 결정해야함
- 송신 클라이언트는 수신 클라이언트에게 전달할 메시지를 채팅 서비스에 보낼 때 HTTP 프로토콜 사용
- 채팅 서비스오 접속에는 keep-alive 헤더 사용 시 효율적
	- TCP 접속 과정에 발생하는 핸드셰이크 횟수를 줄일 수 있음
- HTTP는 클라이언트가 연결을 만드는 프로토콜이며, 서버에서 클라이언트로 임의 시점에 메시지를 보내기는 어려움
- 서버가 연결을 만드는 것처럼 동작시키는 방법은 폴링(polling), 롱 폴링(long polling), 웹소켓(websocket) 등이 있음

폴링
- 클라이언트에서 주기적으로 서버에게 메시지가 있는 지 확인하는 방법
- 폴링 비용은 폴링을 자주하면 할수록 올라감
- 서버 자원이 불필요하게 낭비된다는 문제 있음

롱폴링
- 클라이언트는 새 메시지가 반환되거나 타임아웃 될 때까지 연결 유지
- 클라이언트는 새 메시지를 받으면 기존 연결을 종료하고 서버에 새로운 요청을 보내 모든 절차를 다시 시작
- 문제점
	- 메시지를 보내는 클라이언트와 수신 클라이언트가 같은 채팅 서버에 접속되지 않을 수 있음
	- 서버 입장에서는 클라이언트가 연결을 해제 했는지 알만한 좋은 방법이 없음
	- 여전히 비효율적

웹소켓
- 서버가 클라이언트에게 비동기(async) 메시지를 보낼 때 널리 사용하는 기술

![](/이우승/assets/ch-12/ch12_02.jpeg)

- 웹소켓 연결은 클라이언트가 시작
- 한번 맺어진 연결은 항구적, 양방향
- 처음에는 HTTP 연결이지만 특정 핸드셰이크 절차 후 웹소켓 연결로 업그레이드
- 웹소켓은 방화벽 환경에서도 잘 동작, 80, 443 HTTP 또는 HTTPS 프로토콜을 기본 포트로 사용
- 서버에서 연결을 효율적으로 해야함

## 개략적 설계안

- 회원가입, 로그인, 사용자 프로파일 등은 일반적인 HTTP 상에 구현해도 됨
- 채팅 시스템은 세 부분으로 정의 될 수 있음
	- 무상태 서비스
	- 상태유지 서비스
	- 제3자 연동

![](/이우승/assets/ch-12/ch12_03.jpeg)

무상태 서비스
- 로그인, 회원가입, 사용자 프로파일 표시 등을 처리하는 요청/응답 서비스
- 서비스 탐색 서비스는 클라이언트가 접속할 채팅 서버의 DNS 호스트명을 클라이언트에게 알려주는 역할

상태 유지 서비스
- 채팅 서비스는 각 클라이언트가 채팅 서버와 독립적인 네트워크 연결을 유지해야하기 때문에 상태 유지 필요
- 클라이언트는 보통 서버가 살아 있는 한 다른 서버로 연결을 변경하지 않음

제3자 서비스 연동
- 푸시 알림등을 위해 필요


### 규모 확장성

- 동시 접속자 1M이라고 가정하고 접속당 10K의 서버 메모리가 필요하다면 10GB 정도의 서버 메모리로 커버됨
- 하지만 단일 서버로 서비스 제공시 SPOF 등의 이슈가 있기 때문에 서버 한대로 서비스를 하는 것은 위험

![](/이우승/assets/ch-12/ch12_04.jpeg)

- 채팅 서버 : 클라이언트 사이에 메시지 중개
- 접속상태 서버 : 사용자의 접속 여부 관리
- API 서버 : 로그인, 회원가입, 프로파일 변경 등 처리
- 알림 서버 : 푸시 알림 전송
- 키-값 저장소 : 채팅 이력 보관

저장소
- 채팅 시스템 데이터
	- 사용자 프로파일, 설정, 친구 목록과 같은 데이터는 관계형 데이터베이스에 보관
	- 채팅 이력 데이터는 키-값 저장소 사용
		- 키-값 저장소는 규모확장에 용이함
		- 데이터 접근 시간이 낮다

### 데이터 모델

1:1 채팅을 위한 메시지 테이블
- 서로 다른 메시지가 동시에 만들어질 수 있기 때문에 created_at은 메시지 순서로 사용할 수 없음

| message_id   | bigint    |
| ------------ | --------- |
| message_from | bigint    |
| message_to   | bigint    |
| content      | text      |
| created_at   | timestamp |

그룹 채팅을 위한 메시지 테이블
- channel_id, message_id의 복합키를 기본키로 사용
- 채널은 채팅 그룹과 동일한 뜻

| channel_id | bigint    |
| ---------- | --------- |
| message_id | bigint    |
| message_to | bigint    |
| content    | text      |
| created_at | timestamp |

메시지 ID
- message_id는 메시지들의 순서도 표현할 수 있어야 함
- 다음 속성들을 만족해야함
	- message_id 값은 고유해야함
	- ID 값은 정렬 가능해야 하며 시간 순서와 일치해야함


## 상세 설계

### 서비스 탐색

- 클라이언트에게 적합한 채팅 서버 추천
- 클라이언트의 위치, 서버의 용량 등을 기준으로 결정
- 서비스 탐색 기능을 구현하는데 널리 쓰이는 오픈 소스는 아파치 주키퍼
- 클라이언트가 접속을 시도하면 사전에 정한 기준에 따라 최적의 채팅 서버를 골라줌

![](/이우승/assets/ch-12/ch12_05.jpeg)

1. 사용자 A가 시스템에 로그인 시도
2. 로드밸런서가 로그인 요청을 API 서버들 중 하나로 보냄
3. API 서버가 사용자 인증 처리 후 서비스 탐색 기능으로 채팅 서버를 찾음
4. 사용자 A는 채팅 서버와 웹소켓 연결

### 메시지 흐름

1:1 채팅 메시지 처리 흐름

![](/이우승/assets/ch-12/ch12_06.jpeg)

1. 사용자 A가 채팅 서버 1로 메시지 전송
2. 채팅 서버 1은 ID 생성기를 사용해 메시지 ID 결정
3. 채팅 서버 1은 해당 메시지를 메시지 동기화 큐로 전송
4. 메시지가 키-값 저장소에 보관
5. (a) 사용자 B가 접속 중인 메시지는 사용자 B가 접속 중인 채팅 서버 2로 전송됨 (b) 사용자 B가 접속 중이 아니라면 푸시 알림 메시지 보냄
6. 채팅 서버 2는 메시지를 사용자 B에게 전송

여러 단말 사이의 메시지 동기화

![](/이우승/assets/ch-12/ch12_07.jpeg)

- 사용자 A는 모바일과 랩톱 두 대 단말을 이용
- 사용자 A가 모바일 채팅앱에 로그인한 결고로 채팅 서버 1과 해당 단말 사이 웹소켓 연결이 만들어져 있고 랩톰에서 로그인한 결과로 역시 채팅 서버 1에 연결되어 있는 상황
- 각 단말은 cur_max_meesage_id라는 변수를 유지, 해당 단말에서 관측된 가장 최신 메시지 ID 추적용도

소규모 그룹 채팅에서의 메시지 흐름

![](/이우승/assets/ch-12/ch12_08.jpeg)

- 그룹 채팅방에 3명의 사용자가 있는 경우 (사용자 A,B,C)
- 사용자 A가 보낸 메시지가 사용자 B와 C의 메시지 동기화 큐에 복사됨
	- 이 큐는 사용자 각각에 할당된 메시지 수신함 같은 것으로 가정해도됨
- 이 설계는 소규모 그룹 채팅에 적합
	- 새로운 메시지가 왔는지 확인하려면 자기 큐만 보면 됨, 동기화 플로우 단순
	- 그룹이 크지 않으면 메시지를 수신자별로 복사해서 큐에 넣는 작업 비용이 문제 되지 않음
	- 위챗의 경우 그룹 크기가 최대 500으로 제한됨


### 접속상태 표시

사용자의 상태가 바뀌는 시나리오

사용자 로그인
- 웹소켓 연결이 맺어진 후 접속상태 서버는 사용자 A의 상태와 last_active_at 타임스탬프 값을 키-값 저장소에 보관
- 해당 절차 후 사용자는 접속중인 것으로 표시됨

로그아웃
- 사용자 A가 로그아웃 요청
- 접속상태 서버는 키-값 저장소에 보관된 사용자 상태가 online에서 offline으로 변경

접속 장애
- 짧은 시간 동안 인터넷 연결이 끊겼다 복구되는 경우가 있음(차를 타고 터널을 지나는 경우)
- 항상 접속 상태를 변경하는 건 지나친 리소스 낭비
- heartbeat 검사를 통해 주기적으로 접속상태 확인하여 리소스 낭비를 줄임

상태 정보의 전송
- 상태 정보 서버는 publish-subscribe model 사용
- 각각의 친구관계마다 채널을 하나씩 만들어둠

![](/이우승/assets/ch-12/ch12_09.jpeg)