
# 알림 시스템 설계

- 최신 뉴스, 제품 업데이트, 이벤트, 선물 등 고객에게 중요할 만한 정보를 비동기적으로 제공
- 알림 시스템은 모바일 푸시 알림 외에도 SMS 메시지, 이메일 등도 있음


### 알림 유형별 지원 방안

#### iOS 푸시 알림

![](/이우승/assets/ch-10/ch10_01.jpeg)

- 알림 제공자(provider)
	- 알림 요청을 만들어 애플 푸시 알림 서비스(APNS: apple push notification service)로 보내는 주체
		- 단말 토큰(device token) : 알림 요청을 보내는데 필요한 고유 식별자
		- 페이로드(payload) : 알림 내용을 담은 JSON 딕셔너리
- APNS : 애플이 제공하는 원격 서비스. 푸시 알림을 iOS 장치로 보내는 역할
- iOS 단말 : 푸시 알림을 수신하는 사용자 단말

#### 안드로이드 푸시 알림

![](/이우승/assets/ch-10/ch10_02.jpeg)

- 안드로이드도 iOS와 유사한 구조로 동작. APNS대신 FCM(Firebase Cloud Messaging) 사용

#### SMS 메시지

![](/이우승/assets/ch-10/ch10_03.jpeg)

- 트윌리오(Twilio), 넥스모(Nexmo) 같은 제3자 사업자의 서비스를 이용

#### 이메일

![](/이우승/assets/ch-10/ch10_04.jpeg)

- 샌드그리드(Sendgrid), 메일침프(Mailchimp) 와 같은 상용 서비스들이 있음


### 연락처 정보 수집 절차

- 알림을 보내려면 모바일 단말 토큰, 전화번호, 이메일 주소 등의 정보 필요
- 앱을 설치 하거나 처음으로 계정을 등록하면 API 서버는 해당 사용자 정보를 DB에 저장

### 알림 전송 및 수신 절차

#### 설계안

![](/이우승/assets/ch-10/ch10_05.jpeg)

- 1부터 N까지의 서비스
	- 이 서비스 각각은 마이크로서비스, 크론잡, 분산 시스템 컴포넌트 등일 수 있음
	- 사용자 납기일을 알리고자하는 과금 서비스, 배송 알림을 보내려는 쇼핑몰 웹사이트 등
- 알림 시스템
	- 알림 시스템은 알림 전송/수신 처리의 핵심
	- 알림 전송을 위한 API를 제공해야함
	- 제3자 서비스에 전달할 알림을 만들어 낼 수 있어야 함
- 제3자 서비스
	- 사용자에게 알림을 실제 전달하는 역할
	- 제3자 서비스와 통합 시 유의할 것은 확장성
	- 쉽게 새로운 서비스를 통합하거나 기존 서비스를 제거할 수 있어야 함
- iOS, 안드로이드, SMS, 이메일 단말
	- 사용자는 자기 단말에서 알림 수신

위 구조만으로는 다음과 같은 문제 존재

- SPOF : 알림 서비스가 하나 밖에 없어 서버에 장애가 생기면 전체 장애가 됨
- 규모 확장성 : DB나 캐시 등 중요 컴포넌트의 규모를 개별적으로 늘릴 방법이 없음

#### 개선된 설계안

![](/이우승/assets/ch-10/ch10_06.jpeg)

- DB와 캐시 알림 시스템이 주 서버에서 분리됨
- 알림 서버를 증설 하고 자동으로 수평적 규모 확장이 이루어짐
- 메시지 큐를 이용해 시스템 컴포넌트 사이의 강한 결합을 끊는다

알림 서버
- 알림 전송 API : 스팸 방지를 위해 보통 사내 서비스 또는 인증된 클라이언트만 이용 가능
- 알림 검증 : 이메일 주소, 전화 번호 등에 대한 기본적 검증 수행
- 데이터베이스 또는 캐시 질의 : 알림에 포함시킬 데이터를 가져오는 기능
- 알림 전송 : 알림 데이터를 메시지 큐에 넣는다

![](/이우승/assets/ch-10/ch10_07.jpeg)

캐시
- 사용자 정보, 단말 정보, 알림 켐플릿 등을 캐시

데이터베이스
- 사용자, 알림, 설정 등 다양한 정보 저장

메시지 큐
- 시스템 컴포넌트 간 의존성 제거
- 다량의 알림 전송 시 버퍼 역할

작업 서버
- 메시지 큐에서 전송할 알림을 꺼내 제3자 서비스로 전달

제3자 서비스
iOS, 안드로이드, SMS, 이메일 단말

## 상세 설계

### 안정성

#### 데이터 손실 방지

- 알림이 소실 되면 안된다
- 알림이 지연되거나 순서가 틀려도 괜찮지만 사라지면 문제
- -> 알림 시스템은 알림 데이터를 DB에 보관하고 재시도 매커니즘을 구현해야함
- -> 알림 로그 DB를 유지하는 것이 한 가지 방법

#### 알림 중복 전송 방지

- 이벤트 ID를 검사하여 이전에 본적이 있는 이벤트인지 확인

#### 알림 템플릿

- 알림 템플릿은 인자(parameter)나 스타일, 추적 링크를 조정하기만 하면 사전에 지정한 형식에 맞춰 알림을 만들어 내는 틀

#### 알림 설정

- 사용자가 알림 설정을 상세히 조정할 수 있도록 제공

#### 전송률 제한

- 너무 많은 알림이 보내지지 않도록 함
- 한 사용자가 받을 수 있는 알림의 빈도 제한

#### 재시도 방법

- 알림 전송에 실패하면 해당 알림을 재시도 전용 큐에 넣는다
- 문제 지속 발생 시 개발자에게 통지

#### 푸시 알림과 보안

- 인증되거나 승인된 클라이언트만 알림 전송 가능

#### 큐 모니터링

- 큐에 쌓인 알림이 제대로 해소 되고 있는지 모니터링 필요
- 적절한 속도로 해소 되지 않는 경우 작업 스레드를 증설할 필요가 있음

#### 이벤트 추적

- 알림 확인률, 클릭율, 실제 앱 사용으로 이어지는 메트릭은 사용자를 이해하는데 중요한 요소

## 수정된 설계안

![](/이우승/assets/ch-10/ch10_08.jpeg)

# 참고

- https://www.etoday.co.kr/news/view/2227030