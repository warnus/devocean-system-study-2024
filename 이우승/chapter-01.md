
# 사용자 수에 따른 규모 확장성

## 단일 서버

- 모든 컴포넌트가 한 대의 서버에서 실행되는 시스템
	- 웹 앱, 데이터베이스, 캐시 등이 전부 서버 한 대에서 실행됨

![](/이우승/assets/ch-01/ch01_01.jpg)

- 단일 서버 사용자 요청 처리 흐름
	1. 도메인 이름(api.mystie.com)을 이용하여 웹사이트 접속
	2. DNS에서 IP 주소를 반환 받음
	3. 해당 IP주소로 HTTP 요청 전달
	4. 웹 서버로 부터 HTML 페이지 또는 JSON 형태의 응답 반환


### Web Server

- 웹 서버는 클라이언트(웹 브라우저)로부터 요청을 받아들이고, 정적인 콘텐츠(HTML, 이미지, CSS 등)를 제공하는 소프트웨어
- 예를 들어, 네트워크를 통해 웹사이트를 열거나 파일을 다운로드할 때 사용되는 소프트웨어가 웹 서버
- 웹 서버의 대표적인 예로는 Apache, Nginx 등
### Web Application Server

- 웹 애플리케이션 서버는 동적인 콘텐츠(사용자 인증, 데이터베이스 접근 등)를 생성하고 처리하는 소프트웨어
- 사용자의 요청에 따라 데이터베이스에 접근하여 정보를 가져오거나, 복잡한 비즈니스 로직을 처리
- 예를 들어, 온라인 쇼핑몰의 주문을 처리하거나, 소셜 미디어 애플리케이션의 친구 목록을 보여주는 것 등이 웹 애플리케이션 서버의 역할
- 웹 애플리케이션 서버의 대표적인 예로는 Tomcat, JBoss, WildFly 등

### WSGI(Web Server Gateway Interface)

- WSGI는 파이썬 웹 애플리케이션과 웹 서버 간의 표준 인터페이스
- 파이썬 웹 애플리케이션 프레임워크(예: Django, Flask)는 WSGI를 따르는데, 이를 통해 여러 웹 서버와 호환
- 쉽게 말해, WSGI는 파이썬 애플리케이션과 웹 서버 사이의 다리 역할
- WSGI를 사용하면 여러 가지 웹 서버(예: Apache, Nginx)에서 동일한 파이썬 애플리케이션을 실행할 수 있음

![](/이우승/assets/ch-01/ch01_03.png)
### ASGI(Asynchronous Server Gateway Interface)

- ASGI는 비동기적으로 작동하는 웹 애플리케이션을 다루기 위한 표준 인터페이스
- ASGI를 따르는 웹 애플리케이션은 비동기적으로 작동하며, 여러 요청을 동시에 처리
- I/O 작업을 기다리는 동안 다른 작업을 수행할 수 있어서 성능 향상
- ASGI는 WebSocket과 같은 실시간 통신 프로토콜도 지원
- FastAPI, Django Channels

![](/이우승/assets/ch-01/ch01_02.png)

### Backend & Frontend

#### Backend
- 백엔드는 웹 애플리케이션의 서버 측을 담당하는 부분
- 사용자의 요청을 받아들이고, 데이터를 처리하고, 비즈니스 로직을 구현하며, 데이터베이스와의 상호작용
- 백엔드는 서버 측에서 실행
#### Frontend
- 프론트엔드는 웹 애플리케이션의 사용자 측을 담당하는 부분
- 사용자가 직접적으로 보고 상호작용하는 부분을 구현하며, 사용자 경험을 개선하기 위한 디자인과 개발을 담당
- HTML, CSS, JavaScript 등을 사용하여 웹 페이지를 디자인하고, 사용자 입력을 처리하고, 서버로부터 데이터를 가져와 표시

#### Backend Framework 종류

1. **Django**(Python)
2. **Flask**(Python)
3. **Express.js**(JavaScript(Node.js))
4. **Ruby on Rails**(Ruby)
5. **Spring Boot**(Java)
6. **ASP.NET Core**(C#)
7. **Laravel**(PHP)
8. **FastAPI**(Python)
9. **Gin**(Go)
10. **NestJS**(TypeScript(Node.js))

### FastAPI

- FastAPI는 Python으로 작성된 빠르고 현대적인 웹 프레임워크
- **빠름**: (Starlette과 Pydantic 덕분에) **NodeJS** 및 **Go**와 대등할 정도로 매우 높은 성능
- **빠른 코드 작성**: 약 200%에서 300%까지 기능 개발 속도 증가. *
- **적은 버그**: 사람(개발자)에 의한 에러 약 40% 감소. *
- **직관적**: 훌륭한 편집기 지원. 모든 곳에서 자동완성. 적은 디버깅 시간.
- **쉬움**: 쉽게 사용하고 배우도록 설계. 적은 문서 읽기 시간.
- **짧음**: 코드 중복 최소화. 각 매개변수 선언의 여러 기능. 적은 버그.
- **견고함**: 준비된 프로덕션 용 코드를 얻으십시오. 자동 대화형 문서와 함께.
- **표준 기반**: API에 대한 (완전히 호환되는) 개방형 표준 기반


## 데이터베이스

- 사용자가 증가하는 경우 웹/모바일 트래픽 처리용 서버, 데이터베이스용 서버로 분리
![](/이우승/assets/ch-01/ch01_04.jpg)

### 관계형 데이터베이스(RDBMS)
- RDBMS(Relational Database Management System)
- 관계형 데이터베이스는 데이터를 테이블 형식으로 저장
- 테이블 간의 관계를 통해 데이터를 구성
- 장점
	- 데이터의 일관성을 유지 용이
	- ACID(원자성, 일관성, 고립성, 지속성) 속성을 지원하여 데이터 무결성 보장
	- 복잡한 쿼리를 수행하기에 적합
- 단점
	- 대량의 데이터를 다루기에는 확장성 한계
	- 스키마 변경이 어렵고 비용이 많이 들 수 있음
- Mysql, Oracle DB, PostgreSQL
### 비 관계형 데이터베이스(NoSQL)
- 비관계형 데이터베이스는 스키마가 없거나 유연한 스키마를 가지고 있음
- 키-값 저장소(key-value store), 문서 저장소(document store), 컬럼 저장소(column store), 그래프 저장소(graph store) 등 다양한 형태로 데이터를 저장
- 장점
	- 대량의 분산된 데이터를 효율적으로 처리
	- 확장성 용이
	- 분산형 아키텍처를 활용하여 성능을 최적화
	- 유연한 스키마를 통해 데이터 모델을 쉽게 변경하고 적응 가능
- 단점
	- 데이터의 일관성을 보장하기 어려움
	- 복잡한 쿼리나 데이터 조인이 어렵거나 비효율적일 수 있음
	- 특정 작업에 따라 적합한 NoSQL 데이터베이스 유형을 선택해야함
- Neo4j, HBase, AWS DynamoDB, Cassandra, MongoDB

#### key-value store(ex: redis)
- 예시 데이터: 사용자 세션 관리
```
Key: user_session:1 Value: {"user_id": 1, "username": "example_user", "login_time": "2024-05-06T10:00:00", "expiry_time": "2024-05-06T11:00:00"}
```

#### document store(ex: mongodb)
- 예시 데이터: 블로그 포스트
```
{ 
	"_id": ObjectId("6092d8572121c275c90e146a"), 
	"title": "Introduction to NoSQL databases", 
	"author": "John Doe", 
	"content": "NoSQL databases provide a flexible way to store and manage data...", 
	"tags": ["NoSQL", "Database", "MongoDB"], 
	"comments": [ {"user": "Alice", "comment": "Great article!"}, {"user": "Bob", "comment": "Very informative."}, {"user": "Charlie", "comment": "Thanks for sharing!"} ], 
	"created_at": ISODate("2021-05-06T08:00:00"), 
	"updated_at": ISODate("2021-05-06T10:30:00") }
```

#### graph store(ex: neo4j)
- 예시 데이터: 소셜 네트워크 친구 관계
```
(Alice)-[:FRIENDS_WITH]->(Bob) 
(Bob)-[:FRIENDS_WITH]->(Charlie) 
(Charlie)-[:FRIENDS_WITH]->(David)
```

#### column store(ex: apache cassandra)
- 예시 데이터: 사용자 활동 로그
```
| user_id | activity_date | page_visited | duration_seconds | 
|---------|---------------|-----------------|------------------| 
| 1 | 2024-05-06 | /home | 30 | 
| 2 | 2024-05-06 | /profile | 45 | 
| 1 | 2024-05-06 | /products | 60 |
```


## 수직적 규모 확장 vs 수평적 규모 확장

- 수직적 규모 확장
	- 스케일업(scale up), 서버에 고사양 자원을 추가하는 행위
	- 트래픽 양이 적은 경우 수직적 확장이 좋음
	- 단점
		- 한 대의 서버에 CPU나 메모리를 무한대로 증설할 방법이 없음
		- 장애에 대한 failover나 다중화가 안 됨
		- -> 따라서 대규모 애플리케이션 지원은 수평적 규모 확장이 일반적
- 수평적 규모 확장
	- 스케일 아웃(scale out), 더 많은 서버를 추가

![](/이우승/assets/ch-01/ch01_06.png)

### 로드밸런서
- 웹 서버들에게 트래픽 부하를 고르게 분산하는 역할
- 장점
	- 부하 분산
		- 여러 서버로 트래픽을 분산
	- 고가용성
		- 한 대의 서버가 다운되더라도 다른 서버가 요청 처리
	- 확장성
		- 트래픽 분산을 위한 서버 추가 쉬움
	- 성능 향상
		- 최적의 서버를 선택하여 라우팅 하여 성능을 최적화 할 수 있음
- 단점
	- 단일 장애점
		- 로드 밸런서 자체가 단일 장애점이 될 수 있음
	- 성능 오버헤드
		- 로드 밸런서 자체에서 트래픽을 처리하는 오버헤드가 있을 수 있음
	- 관리 비용 증가

![](/이우승/assets/ch-01/ch01_05.jpg)
#### 로드밸런싱 알고리즘
- Round Robin
	- 각 서버를 번갈아가며 분배
	- 서버 성능이 다를 때는 적합하지 않음
- Least Connection(최소 연결)
	- 연결된 클라이언트 수가 가장 적은 서버에 요청을 전달
	- 각 서버의 성능이 다를 때 효과적
- Least Response Time (최소 응답 시간)
	- 각 서버의 응답 시간을 기준으로 가장 빠른 서버에 전달
	- 서버 간 응답 시간 차이가 큰 경우 효과적
- IP Hash
	- 클라이언트 IP 주소를 해시하여 특정 서버로 고정된 방식으로 트래픽 전달
	- 같은 클라이언트가 같은 서버에 요청이 전달되어 세션 유지가 필요한 경우 용이

#### AWS 로드밸런서 유형
- Application Load Balancer(ALB)
	- OSI 7계층(L7)에서 동작하는 로드 밸런서로, HTTP 및 HTTPS 트래픽 지원
- Network Load Balancer (NLB)
	- OSI 4계층(L4)에서 동작하는 로드 밸런서로, TCP 및 UDP 트래픽 지원
- Gateway Load Balancer (GWLB)
	- OSI 7계층(L7)에서 동작하는 로드 밸런서로, 다양한 프로토콜을 지원하며 VPN 및 NAT 기능도 제공

![](/이우승/assets/ch-01/ch01_07.png)


### 데이터베이스 다중화

- 일반적으로 주(master)-부(slave) 관계로 설정
- 데이터 원본은 master 서버, 사본은 slave 서버에 저장
- 쓰기 연산은 마스터에서만 지원
- slave db는 master db로 부터 사본 전달 받음, 읽기만 지원
- 장점
	- 더 나은 성능 : 읽기 연산이 분산되어 병렬로 처리될 수 있는 query 수가 늘어나 성능이 좋아짐
	- 안정성(reliability) : 서버 일부가 망가져도 데이터가 보존됨
	- 가용성(availability) : 서버에 장애가 발생해도 다른 곳에서 데이터를 제공

#### 로드밸런서와 데이터베이스 다중화 설계안

![](/이우승/assets/ch-01/ch01_08.jpg)

동작 시나리오
1. 사용자는 DNS로 부터 로드밸런서 Public IP 획득
2. 사용자는 해당 IP 주소로 로드밸런서 접속
3. HTTP 요청은 서버 1 또는 서버 2로 전달
4. 웹 서버는 사용자 데이터를 slave db에서 읽음
5. 데이터 업데이트 연산은 master db로 전달



## 캐시
- 연산이 오래 걸리거나 자주 참조 되는 데이터를 메모리에 적재
- 이 후 메모리에서 참조하도록 하는 것
- 애플리케이션 성능은 데이터베이스를 얼마나 자주 호출하냐에 크게 좌우

### 캐시 계층
- 웹서버 - 데이터베이스 사이에 별도의 캐시를 위치
- 캐시를 독립적 확장하는 것도 가능

![](/이우승/assets/ch-01/ch01_09.jpg)

## 캐시전략

![](/이우승/assets/ch-01/ch01_10.jpeg)
- Cache Aside
	- 장점
		- 업데이트 로직은 응용 프로그램 수준에서 이루어지며, 구현이 쉬움
		- 캐시에는 응용 프로그램이 요청한 것만 포함
	- 단점
		- 각 캐시 미스는 3trip 전송 필요
		- 데이터베이스가 직접 업데이트되면 데이터가 오래되어 있을 수 있음
- Read Through
	- 장점
		- 응용 프로그램 로직 심플
		- 읽기를 쉽게 확장할 수 있으며, 하나의 쿼리만 데이터베이스에 접근
	- 단점
		- 데이터 액세스 로직은 캐시에 있으며, 데이터베이스에 접근하기 위해 플러그인을 작성해야 함
- Write Around 
	- 장점
		- 일관된 공급원
		- 낮은 응답 지연
	- 단점
		- 쓰기 지연 시간이 높음
		- 캐시 내의 데이터가 오래될 수 있습니다
- Write Back
	- 장점
		- 쓰기 지연 시간이 낮음
		- 읽기 지연 시간이 낮음
		- 캐시와 데이터베이스는 최종 일관성을 가집
	- 단점
		- 캐시가 다운되면 데이터 손실 발생
		- 드물게 액세스되는 데이터도 캐시에 저장됨
- Write Through
	- 장점
		- 읽기 지연 시간이 낮음
		- 캐시와 데이터베이스가 동기화됨
	- 단점
		- 쓰기가 완료될 때까지 기다려야 하기 때문에 더 높은 지연 시간 발생
		- 드물게 액세스되는 데이터도 캐시에 저장됨

### 캐시 사용 시 유의사항

- 데이터 갱신은 드물지만 참조는 빈번한 경우 유리함
- 영속적인 데이터는 비추
- 만료정책에 대한 고민 필요
- 일관성 유지에 대한 고민 필요
- 캐시 자체가 단일 장애 지점(Single Point of Failure, SPOF)이 될 가능성이 있음
- 캐시 메모리는 과할당이 유리
- 데이터 방출 정책 고려해야됨(어떤 놈을 내보낼 것인가)


## 콘텐츠 전송 네트워크(CDN)

- 정적 콘텐츠 전송에 쓰이며 지리적으로 분산된 네트워크
- 이미지, 비디오, CSS, Javascript 파일 등을 캐시

![](/이우승/assets/ch-01/ch01_11.jpg)

### CDN 사용 시 고려사항

- 비용
- 만료 시한 설정
- CDN 장애 대응 방안
- 콘텐츠 무효화 방법


### CDN과 캐시가 추가된 설계안

- ![](/이우승/assets/ch-01/ch01_12.jpg)

## 무상태(stateless) 웹 계층

- 수평 확장을 위해서는 상태 정보(Ex. 사용자 세션)를 웹 계층에서 제거해야함
- 상태 정보는 데이터베이스에 보관
- 해당 구조는 단순하고, 안정적이며 규모 확장이 용이함

![](/이우승/assets/ch-01/ch01_13.jpg)


### Stateless 구조 설계안

- 트래픽 양에 따라 웹 서버를 늘리거나 줄이기 용이함

![](/이우승/assets/ch-01/ch01_14.jpg)

## 데이터센터

- 가용성을 높이고 세계 어느 지역에서나 쾌적한 환경 제공
- 기술적 난제
	- 트래픽 우회 : 올바른 데이터 센터로 트래픽을 보내야함 -> GeoDNS 사용 가능
	- 데이터 동기화
	- 테스트와 배포

## 메시지 큐

- 무손실 보장하는 비동기 통신 컴포넌트
- 생산자 또는 발행자(producer/publisher) 입력 서비스가 메시지를 생성해서 큐에 발행
- 큐에는 소비자 또는 구독자(consumer/subscriber)가 메시지를 받아 동작 수행
- 사용예시
	- 전자상거래플랫폼 (ex: https://d2.naver.com/helloworld/9581727)
		- 사용자가 주문을 생성하면 해당 주문 정보를 큐에 전송
		- 주문 처리 서비스는 메시지 큐에서 주문 정보를 비동기적으로 가져와 처리

![](/이우승/assets/ch-01/ch01_15.jpg)

- 메시지큐 서비스 : Apache Kafka, RabbitMQ, Amazon SQS

## 로그, 메트릭 그리고 자동화

- 사업 규모가 커지면 로그나 메트릭, 자동화 같은 작업이 필수적
- 로그
	- 에러 로그 모니터링
- 메트릭
	- CPU, 메모리, 디스크 I/O 정보
	- DB 성능, 캐시 성능
	- 비즈니스 메트릭, DAU, revenue, retention
- 서비스 예시
	- Elasticsearch와 Logstash를 활용한 ELK 스택
	- Fluentd와 Elasticsearch를 활용한 EFK 스택
	- Prometheus와 Grafana
	- Datadog
	- AWS CloudWatch

- 자동화
	- CI/CD
- 도구들
	- Jenkins, gitlab, github actions, travis ci


### 메시지큐, 로그, 메트릭, 자동화 적용 설계안

![](/이우승/assets/ch-01/ch01_16.jpg)


## 데이터베이스 규모 확장

- 데이터베이스도 수직, 수평 확장 방법이 있음
- 수직적 확장
	- 고성능 DB 사용
	- 약점
		- 무한히 CPU, RAM 등을 증설할 수 없음
		- SPOF 위험성
		- 비용이 많이 든다
- 수평적 확장
	- 샤딩이라고도 부름
	- 대규모 데이터베이스를 샤드(shard) 단위로 분할
	- 모든 샤드는 같은 스키마, 샤드간 중복 데이터는 없음
	- 샤딩 키로 구분되어 저장

![](/이우승/assets/ch-01/ch01_17.jpg)

- 샤딩에 따르는 이슈
	- 데이터 resharding
		- 샤드가 가득 찼을 때 다시 분배해야됨
	- 유명인사(celebrity) 문제
		- 특정 샤드에만 쿼리가 집중 되는 문제
	- 조인과 비정규화
		- 샤드간 데이터 조인이 어려움


### 샤딩을 적용한 설계안

![](/이우승/assets/ch-01/ch01_18.jpg)



## 참고
### Web Server & Web Application
- https://gmlwjd9405.github.io/2018/10/27/webserver-vs-was.html
- https://jay-ji.tistory.com/66
- https://derlin.github.io/introduction-to-fastapi-and-celery/02-fastapi/

### 로드밸런서
- https://www.smileshark.kr/post/what-is-a-load-balancer-a-comprehensive-guide-to-aws-load-balancer

### 캐시
- https://yoongrammer.tistory.com/101
- https://twitter.com/sahnlam/status/1767053897028550763/photo/1
- https://velog.io/@psk84/Caching-%EC%A0%84%EB%9E%B5