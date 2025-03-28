
# 키-값 저장소 설계

- 키-값 데이터베이스라고도 불리는 비 관계형 데이터베이스
- 고유 식별자를 키로 가져야함
- 키-값 쌍에서의 키는 유일해야하며 저장된 값은 키를 통해서만 접근 가능
- 키는 짧을 수록 성능이 좋다
- 값은 문자열, 리스트, 객체일 수 있다
- 대표적으로 DynamoDB, memcached, Redis 같은 것들이 존재

## 문제 이해 및 설계 범위 확정

- 키-값 쌍의 크기는 10KB 이하
- 큰 데이터를 저장할 수 있어야함
- 높은 가용성 제공 -> 시스템 장애가 있떠라도 빠른 응답
- 높은 규모 확장성 제공 -> 트래픽 양에 따라 자동으로 Scale Out/In 가능해야됨
- 데이터 일관성 수준은 조정 가능해야함
- 응답 지연시간이 짧아야 함

## 단일 서버 키-값 저장소

- 키-값 쌍 전부를 메모리 해시 테이블로 저장하면 구현이 쉬움
- 다만, 모든 데이터를 메모리에 둔다는 것은 불가능
- 데이터 압축, 자주 쓰는 데이터만 메모리에 두는 방법이 있으나 종국엔 한 대 서버로 커버가 안 됨
- 많은 데이터를 처리하려면 분산 키-값 저장소(distributed key-value store)를 만들어야함

## 분산 키-값 저장소

- 분산 해시 테이블이라고도 불림
- 키-값 쌍을 여러 서버에 분산

### CAP 정리

- Consistency, Availability, Partition Tolerance theorem
- CAP 정리는 일관성, 가용성, 파티션 감내라는 세 가지 요구사항을 동시에 만족할 수 없다는 정리

- 데이터 일관성 : 모든 클라이언트는 어떤 노드에 접속하든 언제나 동일한 데이터를 보게 됨
- 가용성 : 클라이언트는 일부 노드에 장애가 발생하더라도 항상 응답을 받음
- 파티션 감내 : 네트워크에 파티션이 생기더라도 시스템은 계속 동작
- 어떤 두 가지 조건을 충족하면 나머지 하나는 희생되는 구조

![](/이우승/assets/ch-06/ch06_01.jpeg)

- CP 시스템 : 일관성과 파티션 감내 지원, 가용성 희생
- AP 시스템 : 가용성과 파티션 감내 지원, 데이터 일관성 희생
- CA 시스템 : 일관성과 가용성 지원, 파티션 감내 희생
	- 네트워크 장애는 피할 수 없으므로 통상 실제로는 CA 시스템은 존재하지 않음


## 세 대의 복제(replica) 노드 n1, n2, n3 예시

### 이상적 상태

- 이상적 환경에서는 네트워크가 파티션 되는 상황이 없을 것이므로 일관성과 가용성이 만족됨

![|600](/이우승/assets/ch-06/ch06_02.jpeg)

### 실세계의 분산 시스템

- 분산 시스템은 파티션 문제를 피할 수 없음 -> 일관성과 가용성 사이에 하나를 선택해야함
- 그림 6-3은 n3에 장애 발생한 케이스
	- n1, n2와 통신 불가
	- n1, n2에 기록된 내용 -> n3에 전달 불가
	- n3 기록된 내용 -> n1, n2 전달 불가

![|600](/이우승/assets/ch-06/ch06_03.jpeg)

- 일관성을 우선시 하는 경우
	- n1, n2에 쓰기 연산 중단
	- 은행권 시스템은 보통 데이터 일관성을 양보하지 않는다
	- 상황이 해결될 때 까지 오류 반환
- 가용성을 우선시 하는 경우
	- 오래된 데이터를 반환할 위험이 있더라도 계속 읽기 연산 허용
	- n1, n2에 쓰기 연산도 허용
	- 파티션 문제 해결 후 신규 데이터를 n3에 전송

### 시스템 컴포넌트

- 키-값 저장소 핵심 컴포넌트 및 기술들
	- 데이터 파티션
	- 데이터 다중화(replication)
	- 일관성(consistency)
	- 일관성 불일치 해소(inconsistency resolution)
	- 장애 처리
	- 시스템 아키텍처 다이어그램
	- 쓰기 경로(write path)
	- 일기 경로(read path)

### 데이터 파티션

- 데이터를 작은 파티션들로 분할하여 여러 서버에 저장
- 안정 해시를 적용하면 적절하게 데이터 분산 가능
	- 규모 확장 자동화 : 시스템 부하에 따라 서버가 자동으로 추가 되거나 삭제될 수 있음
	- 다양성 : 각 서버 용량에 맞게 가상 노드의 수를 조정할 수 있음

### 데이터 다중화

- 가용성 확보를 위해 데이터를 N개 서버에 비동기적으로 다중화함
- 안정 해시를 사용하는 경우, N개 서버 선정은 링을 순회하면서 만나는 첫 N개 서버에 사본을 보관하는 것
- 그림 6-5에서 보면 Key0는 s1, s2, s3에 저장됨
- 가상 노드를 사용하는 경우 동일한 물리서버가 중복선택되지 않게 해야함

![](/이우승/assets/ch-06/ch06_04.jpeg)

### 데이터 일관성

- 다중화된 데이터는 적절히 동기화 되어야 함
- 정족수 합의(Quorum Consensus) 프로토콜을 사용하면 읽기/쓰기 연산 모두에 일관성 확보 가능

- N = 사본 개수
- W = 쓰기 연산 정족수 : 쓰기 연산이 성공된 것으로 간주하려면 W개의 서버로 부터 쓰기 연산 성공 응답 필요
- R = 읽기 연산 정족수 : 읽기 연산이 성공된 것으로 간주하려면 R개의 서버로 부터 읽기 연산 성공 응답 필요

![](/이우승/assets/ch-06/ch06_05.jpeg)

- 그림 6-6과 같은 경우, W=1은 중재자가 최소 한대의 서버로 부터 쓰기 성공 응답을 받아야 한다는 것
- 중재자는 클라이언트와 노드 사이에서 proxy 역할을 함
- R=1, W=N: 빠른 읽기 연산 최적화됨
- W=1, R=N: 빠른 쓰기 연산 최적화됨
- W+R>N: 강한 일관성 보장(보통 N=3, W=R=2)
- W+R<=N: 강한 일관성 보장되지 않음

#### 일관성 모델

- 강한 일관성: 모든 읽기 연산은 가장 최근에 갱신된 결과 반환
- 약한 일관성: 가장 최근 갱신된 결과를 반환하지 못할 수 있음
- 결과적 일관성(eventual consistency): 갱신 결과가 결국 모든 사본에 반영

#### 비일관성 해소 기법: 데이터 버저닝

- versioning, vector clock으로 일관성이 깨진 경우 해결 가능

versioning : 데이터를 변경할 때마다 해당 데이터의 새로운 버전을 만듦, 각 버전 데이터는 변경 불가능(immutable)


![](/이우승/assets/ch-06/ch06_06.jpeg)

- 그림 6-8은 서버1, 서버2에서 동시에 데이터를 변경하는 모습이다.
- 이런 경우 단순 버저닝만으로는 충돌을 해소할 수 없다.
- 백터 시계(voctor clock)으로 이런 문제를 해결할 수 있음

- 백터 시계는 [서버, 버전]의 순서쌍을 데이터에 매단 것
- D : 데이터
- vi : 버전 카운터
- Si : 서버 번호
- [Si, vi]가 있으면 vi를 증가
- 그렇지 않으면 새 항목 [Si, 1]를 만듦

![](/이우승/assets/ch-06/ch06_07.jpeg)

로직 순서
1. 클라이언트가 데이터 D1을 시스템에 기록 서버 Sx가 실행, 백터 시계는 D1[(Sx, 1)]
2. 다른 클라이언트가 데이터 D1을 읽고 D2로 업데이트, 서버 Sx가 실행하여 D2[(Sx, 2)]로 변경
3. 다른 클라이언트가 데이터 D2를 읽어 D3로 갱신, Sy 서버가 처리하여 D3[(Sx, 2), (Sy, 1)]
4. 또 다른 클라이언트가 D2를 읽고 D4로 갱신, Sz 서버가 처리하여 D4[(Sx, 2), (Sz,1)]
5. 어떤 클라이언트가 D3과 D4를 읽으면 데이터간 충돌을 발견-> 클라이언트가 해소한 후 서버에 기록

이 방법에는 두가지 문제점 존재
- 클라이언트에 충돌감지 및 해소 로직이 들어가야해서 클라이언트 구현이 복잡해짐
- [서버, 버전] 순서쌍 개수가 굉장히 빠르게 증가

#### 장애감지

- 보통 두 대 이상의 서버가 똑같이 서버 A의 장애를 보고해야 실제로 장애가 발생했다고 간주
- 모든 노드 사이에 멀티캐스팅 채널을 구축하는 것이 서버 장애를 감지하는 손쉬운 방법
	- 서버가 많을 땐 비효율적

가십 프로토콜(gossip protocol)
- 동작원리
	- 각 노드는 멤버십 목록 유지
	- 멤버십 목록은 각 멤버 ID와 heartbeat counter 쌍의 목록
	- 각 노드는 주기적으로 heartbeat counter를 증가 시킴
	- 각 노드는 무작위로 선정된 노드들에게 주기적으로 자기 heartbat counter 목록을 보냄
	- heartbeat counter 목록을 받은 노드는 멤버십 목록을 최신 값으로 갱신
	- 어떤 멤버의 heartbeat counter 값이 지정된 시간 동안 갱신되지 않으면 해당 멤버는 장애상태인 것으로 간주

![](/이우승/assets/ch-06/ch06_08.jpeg)

#### 일시적 장애처리


- 엄격한 정족수(strict quorum) 접근법 -> 일관성을 위해 읽기와 쓰기 연산 금지
- 느슨한 정족수(sloppy quorum) 접근법 -> 조건을 완화하여 가용성을 높임
- 장애 상태인 서버로 가는 요청은 다른 서버가 잠시 맡아 처리
- 그동안 발생한 변경사항은 장애 서버가 복구되었을 때 일괄 반영하여 일관성 보존
- 임시 쓰기 연산을 처리한 서버에는 hint를 남김 -> hinted handoff

#### 영구 장애처리

- 영구 장애의 경우 반-앤트로피(anti-entropy) 프로토콜을 구현하여 사본들을 동기화
- 반-앤트로피 프로토콜은 사본들을 비교하여 최신 버전으로 갱신
- 사본 간의 일관성이 망가진 상태를 탐지하고 전송 데이터의 양을 줄이기 위해서 머클(Merkle)트리 사용

![](/이우승/assets/ch-06/ch06_09.jpeg)

- 서버1, 서버2의 해시 값이 다른 것으로 다른 데이터를 찾음

### 데이터센터 장애처리

- 정전, 네트워크 장애, 자연재해 등 다양한 이유로 문제 발생 가능
- 여러 데이터센터에 걸쳐 다중화 하는 것이 해법

### 시스템 아키텍처 다이어그램

- 클라이언트는 키-값 저장소가 제공하는 두 가지 단순한 API, get, put 통신
- 중재자는 클라이언트에게 키-값 저장소에 대한 proxy 역할을 하는 노드
- 노드는 안정 해시의 해시링 위에 분포
- 노드를 자동으로 추가, 삭제 가능
- 데이터는 여러 노드에 다중화
- 모든 노드가 같은 책임 하에 SPOF는 존재하지 않음

![](/이우승/assets/ch-06/ch06_10.jpeg)

### 쓰기 경로

- 카산드라의 사례를 기준으로 쓰기 동작 예시

![](/이우승/assets/ch-06/ch06_11.jpeg)

1. 쓰기 요청이 커밋 로그 파일에 기록
2. 데이터가 메모리 캐시에 기록됨
3. 메모리 캐시가 가득차거나 정의된 임계치에 도달하면 디스크에 있는 SSTable(Sorted-String Table)에 기록

### 읽기 경로

- 읽기는 두 가지 케이스로 나뉜다
- 메모리에 데이터가 존재 했을 때, 존재하지 않았을 때
- 메모리에 존재할 경우 읽기 요청된 데이터가 바로 반환
- 메모리에 없는 경우 그림 6-21과 같은 절차로 반환됨

![](/이우승/assets/ch-06/ch06_12.jpeg)