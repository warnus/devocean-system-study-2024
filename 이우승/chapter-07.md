
# 분산 시스템을 위한 유일 ID 생성기 설계

- 분산 환경에서 유일성이 보장되는 ID 생성 시스템을 설계하는 것이 목표

## 문제 이해 및 설계 범위 확정

유일 ID 생성 시스템은 아래의 조건 범위를 만족시킨다

- ID는 유일해야 한다
- ID는 숫자로만 구성되어야 한다
- ID는 64비트로 표현할 수 있는 값
- ID는 발급 날짜에 따라 절렬 하능해야한다
- 초등 10000개이의 ID


## 유일 ID 생성 방법

아래와 같은 유일 ID 생성 방법에 대해 살펴볼 것

- 다중 마스터 복제(multi-master replication)
- UUID(Universally Unique Identifier)
- 티켓 서버(ticket server)
- 트위터 스노프레이크(twitter snowflake) 접근법

### 다중 마스터 복제

![|600](/이우승/assets/ch-07/ch07_01.jpeg)

