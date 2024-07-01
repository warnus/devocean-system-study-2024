# 사용자 수에 따른 규모 확장성

수백만 사용자를 지원하는 시스템을 설계하는 것은 도전적인 과제이며, 지속적인 계량과 끝없는 개선이 요구되는 여정.

## 데이터베이스

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fdu9S1t%2FbtrXURZMqon%2FPFQycAbDF34aGQKCol6Su1%2Fimg.png)

### 관계형 데이터베이스
RDBMS(Relational Database Management System)이라고 부르며, 자주 사용하는 시스템으로는 MySQL, 오라클, PostgreSQL 등이 있음. 
SQL을 사용하면 여러 테이블에 있는 데이터를 그 관계에 따라 Join하여 합칠 수 있음.

### 비 관계형 데이터베이스
NoSQL이라고 부르며, 대표적으로 CouchDB, Neo4j, Cassandra, HBase, Amazon DynamoDB 등이 있음.
키-값 저장소(KV Store), Graph Store, Column Store, Document Store 부류로 나눌 수 있음.
일반적으로 Join연산은 지원하지 않음.

대부분은 관계형 데이터베이스가 최선이나, 구축하려는 시스템에 적합하지 않은 경우 다른 비 관계형 데이터베이스를 고려해볼 수 있음.

### 비 관계형 데이터베이스를 고려해볼 경우
- 아주 낮은 응답 지연시간(latency)이 요구됨
- 다루는 데이터가 비정형(unstructured)이라 관계형 데이터가 아님
- 데이터(JSON, YAML, XML 등)를 직렬화하거나(serialize) 역직렬화(deserialize) 할 수 있기만 하면 도미
- 아주 많은 양의 데이터를 저장할 필요가 있음

## 수직적 규모 확장 vs 수평적 규모 확장
- Scale Up: 서버에 고사양 자원(더 좋은 CPU, 더 많은 RAM 등)을 추가하는 행위
- Scale Out: 더 많은 서버를 추가하여 성능을 개선하는 행위.

서버로 유입되는 트래픽의 양이 적을 때는 Scale Up이 좋은 선택이며, 가장 큰 장점은 단순함.
단점으로는 한계가 있으며, 한 서버에 고사양 자원을 무한대로 증설할 수 없음. 

서버 1대로는 장애에 대한 Failover 방안이나 다중화 방안을 제시하지 않아 서버 장애시 서비스가 중단되는 문제가 있음.

### 로드밸런서
웹 서버들에게 트래픽 부하를 고르게 분산하는 역할.
사용자가 웹 서버 IP를 직접 호출하면 요청이 모두 그 서버로 가지만, 로드밸런서의 IP를 호출하면 분산되어 웹서버로 요청이 전달됨.

로드밸런서에 속한 서버 일부에 장애가 발생할 경우 해당 서버를 제외하고 요청을 전달하게 됨. 이로서 특정 서버 장애가 발생해도 서비스 중단으로 이어지지 않게 함.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbovgHS%2FbtrXVSXUpk4%2FifgbZfPdbK01yNH3TtKr41%2Fimg.png)

### 데이터베이스 다중화
데이터베이스 서버 사이에 Master-Slave 관계를 설정하고 역할을 분리. Master에선 Write만 지원하고, Slave에선 Master로부터 사본을 전달 받으며 Read 만을 지원.
대부분의 애플리케이션은 Read 연산이 높아, 통상 Slave 데이터베이스의 수가 Master의 수보다 많음.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FoyTrl%2FbtrXVyrGTcL%2FIW395bugcElsbICUNsXD4K%2Fimg.png)


## 캐시
값비싼 연산 결과 또는 자주 참조되는 데이터를 메모리 안에 두어, 요청이 빨리 처리될 수 있도록 하는 저장소.
캐시 계층은 데이터베이스보다 훨씬 빠르며, 데이터베이스의 부하를 줄일 수 있음.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbAKIrp%2FbtrXRVn9z1t%2FGXAM6tpwMs1oSDCzGaFp41%2Fimg.png)

### 캐시 사용 시 유의할 점
- 데이터 갱신은 자주 일어나지 않지만 참조는 빈번하게 일어날 때 고려
- 캐시는 휘발성 메모리로 영속적으로 보관할 데이터를 두는 것은 바람직하지 않음
- 캐시에 보관하는 데이터에 만료 조건을 적절히 설정
- 데이터 저장소와 캐시 데이터의 일관성이 일치하지 않을 수 있음
- 캐시가 단일 장애 지점(SPOF)가 되지 않도록 설계
- 캐시 메모리 사이즈가 너무 작으면 데이터가 너무 자주 밀려나서 성능이 떨어질 수 있음
- 캐시가 꽉 차면 기존 데이터를 내보내는 정책이 필요하며, 상황에 맞는 정책을 고려

## CDN
정적 콘텐츠를 캐싱.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fmkmej%2FbtrXVqOaLPF%2FTaF7dfWx1Jtpor0a49LorK%2Fimg.png)

### CDN 사용 시 고려해야 할 사항
- 비용: CDN으로 들어가고 나가는 데이터 전송 양에 요금을 지불하므로 자주 사용하는 콘텐츠를 보관
- 적절한 만료 시한 설정: 시의성이 중요한 콘텐츠의 경우 만료 시점을 잘 설정. 너무 길면 콘텐츠의 신선도가 떨어지고, 너무 짧으면 원본 서버에 빈번히 접속하게 됨
- CDN 장애에 대한 대처 방안: CDN이 장애인 경우 어떻게 동작할지 고려
- 콘텐츠 무효화 방법: 아직 만료되지 않은 콘텐츠여도 API를 이용하거나 버저닝을 통해 새로운 콘텐츠로 변경

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FKNQFG%2FbtrXUXyIRck%2FfOmkPth3uc4rutUriNh4v1%2Fimg.png)

## 무상태(stateless) 웹 계층
웹 계층을 수평적으로 확장하기 위해 상태 정보(사용자 세션 데이터 등)을 DB에 보관하고, 필요할 때 가져오도록 함.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FpmdMv%2FbtrXTSq3RB3%2Fo2a4QVl4C2BVfSQd6H6ur1%2Fimg.png)

## 데이터 센터
데이터 센터가 여러개 인경우 사용자는 가장 가까운 데이터 센터로 안내되는데, 이를 지리적 라우팅(geoDNS-routing, geo-routing)이라고 부름. 사용자의 위치에 따라 도메인 이름을 어떤 IP로 변환할지 결정해주는 DNS. 만약 가까운 데이터 센터가 장애시 다른 데이터 센터로 라우팅을 지원.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FkBPYO%2FbtrXRU3MMsi%2FMhEJKhj0EADpdJk7O13vo1%2Fimg.png)

## 메시지 큐
메시지 큐는 메시지의 무손실(durability)을 보장하는, 비동기 통신을 지원하는 컴포넌트.
메시지의 버퍼 역할을 하며, 비동기적으로 전송함.

Producer -> Meesage Queue -> Consumer
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FlFrk0%2FbtrXWxsiqK0%2Fci2Y4OYIuKhlox8YKu4Aj0%2Fimg.png)

메시지 큐를 이용하면 서비스 또는 서버 간 결합이 느슨해져서, 규모 확장성이 보장되어야 하는 안정적 애플리케이션을 구성하기 좋음. Producer는 Consumer가 다운되어 있어도 메시지를 발행할 수 있고, Consumer는 Producer가 가용한 상태가 아니라도 메시지를 수신할 수 있음.

## 로그, 메트릭 그리고 자동화
- 로그: 시스템의 오류와 문제를 찾기 위해 에러 로그를 모니터링 하는 것은 중요. 각 서버에서 볼 수도 있지만, 단일 서비스로 모아주는 도구를 활용하면 더 편리하게 검색하고 조회할 수 있음
- 메트릭: 메트릭을 잘 수집하면 사업 현황에 관한 유용한 정보를 얻을 수 있고, 시스템의 현재 상태를 손쉽게 파악할 수 있음
  - 호스트 단위 메트릭: CPU, Memory, Disk I/O
  - 종합(aggregated) 메트릭: DB 계층의 성능, 캐시 계층의 성능
  - 핵심 비지니스 메트릭: DAU, Revenue, Retention
- 자동화: 시스템이 크고 복잡해지면 생산성을 높이기 위해 고민이 필요. CI를 활용하면 개발자가 만드는 코드를 자동으로 검증하고 문제를 쉽게 감지. 이 외에도 빌드, 테스트, 배포 등의 절차를 자동화 할 수 있음.

## 데이터베이스의 규모 확장
저장할 데이터가 많아지면 DB에 대한 부하도 증가하며, DB 증설이 필요하게 됨.

### 수직적 확장
고성능 자원(CPU, RAM, Disk 등)을 증설하는 방법이며, 서버 증설과 마찬가지로 한 서버의 자원을 무한히 늘릴 수 없고 SPOF, 고비용 문제가 있음.

### 수평적 확장
데이터베이스의 수평적 확장은 샤딩(sharding)이라고 부름. 샤딩은 데이터베이스를 샤드라는 단위로 분할. 모든 샤드는 같은 스키마를 쓰지만 샤드에 보관되는 데이터는 중복이 없음.

(ex. 샤드가 4개 있고 어느 서버에 저장할지 계산한다면 user_id % 4 ...)

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FLyzdt%2FbtrXUXMhNZV%2FkCGwMwXsdlmLfcVvPGLYD0%2Fimg.png)

가장 중요한 것은 샤딩 키(sharding key)를 정하는 것. 파티션 키라고도 부르며, 데이터를 고르게 분할하여 효율을 높이는 것. 샤딩은 확장을 실현하는 훌륭한 기술이지만 도입하며 새로운 문제도 생김.

- 데이터의 재 샤딩(resharding): 데이터가 너무 많아져서 하나의 샤드로는 감당하기 어렵거나, 샤드 간 데이터 분포가 균등하지 못해 어떤 샤드 소진이 빠르게 진행될 때 샤드 키를 계산하는 함수를 변경하고 재배치
- 유명인사(celebrity) 문제: 핫스팟 키(hotspot key) 문제라고도 부르는데, 호출이 많은 key가 특저정 샤드에 모이는 경우 과부하가 발생. 
- 조인과 비정규화: 여러 샤드 서버로 쪼개면 여러 샤드에 걸친 데이터를 조인하기가 힘들어짐. 이를 해결하기 위해선 비정규화하여 하나의 테이블에서 질의하도록 함.

## 백만 사용자, 그리고 그 이상 (정리)
시스템의 규모를 확장하는 것은 지속적이고 반복적인 과정
- 웹 계층은 무상태 계층으로
- 모든 계층에 다중화 도입
- 가능한 한 많은 데이터를 캐시할 것
- 여러 데이터 센터를 지원할 것
- 정적 콘텐츠는 CDN을 통해 서비스할 것
- 데이터 계층은 샤딩을 통해 그 규모를 확장할 것
- 각 계층은 독립적 서비스로 분할할 것
- 시스템을 지속적으로 모니터링하고, 자동화 도구들을 활용할 것

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F6jmUc%2FbtrXUq84GwF%2FokBHmOB9tQE2dvv9VKfMxK%2Fimg.png)
