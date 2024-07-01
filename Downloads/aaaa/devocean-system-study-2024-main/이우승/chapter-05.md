
# 안정 해시 설계


## 로드밸런서와 안정 해시의 차이는 뭘까?

### 로드밸런서 (Load Balancer)

- 로드밸런서는 네트워크 트래픽을 여러 서버에 분산시켜 서버의 과부하 방지
- 시스템의 효율성과 가용성을 높이는 장치 또는 소프트웨어

1. **트래픽 분산**: 로드밸런서는 들어오는 요청을 여러 서버에 분배, 특정 서버에 과부하가 걸리지 않도록 
2. **고가용성**: 서버 중 하나가 다운되더라도 다른 서버가 요청을 처리, 시스템의 가용성 유지
3. **다양한 알고리즘**: 라운드 로빈, 최소 연결, IP 해시, 가중치 기반 분산 등 다양한 분산 알고리즘 사용
4. **스케일링**: 서버를 추가하여 시스템 확장

### 안정 해시 (Consistent Hashing)

- 안정 해시는 분산 시스템에서 데이터를 균형 있게 분배하는 방법
- 노드의 추가나 제거 시 데이터의 재분배를 최소화하는 해싱 기술

1. **데이터 분산**: 데이터를 특정 노드(서버)에 할당하는 해싱 방법
2. **최소한의 재분배**: 노드가 추가되거나 제거될 때, 재배치되는 데이터의 양을 최소화
3. **해싱 링**: 노드와 데이터를 해싱하여 해시 링(서클)에 매핑, 데이터는 시계 방향으로 가장 가까운 노드에 할당
4. **동적 확장**: 노드를 동적으로 추가하거나 제거할 때 시스템의 균형\ 유지

**로드 밸런서 vs 안정해시**
1. **목적**:
	• 로드밸런서 : 네트워크 트래픽을 여러 서버에 분산시켜 서버 과부하를 방지하고 가용성을 높이는 데 사용
	• 안정 해시 : 분산 시스템에서 데이터를 균등하게 분배하고 노드의 추가 및 제거 시 재분배를 최소화

2. **분산 대상**:
	• 로드밸런서 : 네트워크 요청이나 트래픽을 분산
	• 안정 해시 : 데이터 분산

3. **알고리즘의 복잡성**:
	• 로드밸런서 : 주로 간단한 분산 알고리즘을 사용하여 실시간으로 트래픽을 분배
	• 안정 해시 : 해싱 기술을 사용하여 데이터를 분배하며, 노드의 추가/제거 시에도 최소한의 재분배를 보장하는 복잡한 알고리즘을 사용


## 해시 키 재배치(rehash) 문제

- N개의 '캐시 서버'에 부하를 균등하게 나누는 보편적 방법은 다음과 같은 해시 함수를 사용하는 것
```
serverIndex = hash(key) % N (N은 서버의 개수)
```

![](/이우승/assets/ch-05/ch05_01.png)

- hash(key0) % 4 = 1 -> 서버 1로 부터 데이터를 가져옴

![](/이우승/assets/ch-05/ch05_02.jpeg)

- 위 해시 함수를 사용하면 키가 위 그림과 같이 균등하게 분포됨
- 하지만, 서버 개수가 추가되거나 장애등으로 인해 감소하는 경우 위와 같이 균등하게 분포되지 못 하는 문제가 있음

![](/이우승/assets/ch-05/ch05_03.jpeg)

- 위에서 보는 것과 같이 Server1이 장애로 정상동작하지 못하는 경우 클라이언트가 엉뚱한 곳에서 데이터를 찾게 되어 대규모 캐시 미스가 발생하게 됨

## 안정 해시(Consistent hash)

- 안정 해시는 해시 테이블 크기가 조정될 때 평균적으로 k/n 개의 키만 재배치하는 해시 기술
- k는 키의 개수, n은 슬롯(slot)의 개수

### 해시 공간과 해시 링

- 해시 함수 f로 SHA-1을 사용한다고 했을 때 공간 범위는 0부터 2^160 -1
- 해시 공간을 양 끝을 맞닿게 만들면 해시 링이 만들어짐

![](/이우승/assets/ch-05/ch05_04.png)

### 해시 서버

- 해시 함수 f를 사용하면 '서버 IP'나 '이름'을 링 위의 어떤 위치에 대응 시킬 수 있음
- 그림 5-5는 4개의 서버를 해시 링 위에 배치한 결과

![](/이우승/assets/ch-05/ch05_05.jpeg)

### 해시 키

- 그림 5-6에서와 같이 Key 또한 해시 링 위의 어느 지점에 배치 할 수 있음

![](/이우승/assets/ch-05/ch05_06.jpeg)


### 서버 조회

- 키는 해시 링의 시계 방향으로 마주하는 첫번째 서버에 저장
- 그림 5-7은 키가 저장되는 서버를 나타냄

![](/이우승/assets/ch-05/ch05_07.jpeg)


### 서버 추가

- 서버를 추가하더라도 키 가운데 일부만 재배치 됨
- 그림 5-8을 보면 키 중 key0만 재배치 되는 걸 확인할 수 있음

![](/이우승/assets/ch-05/ch05_08.jpeg)

### 서버 제거

- 일부만 재배치 됨

![](/이우승/assets/ch-05/ch05_09.jpeg)

### 기본 구현법의 두가지 문제

- 안정 해시 알고리즘은 MIT에서 처음 제안 됨
- 기본 절차
	- 서버와 키를 균등 분포(uniform distribution) 해시 함수를 사용해 해시 링에 배치
	- 키의 위치에서 링을 시계 방향으로 탐색했을 때 가장 먼저 탐색된 서버에 키가 저장됨
- 문제점
	- 서버가 추가되거나 삭제되는 경우 파티션의 크기를 균등하게 유지하는 게 불가능
	- 키의 균등 분포를 달성하기 어려움

### 가상 노드

- 가상 노드는 실제 노드 또는 서버를 가리키는 노드
- 하나의 서버는 링 위에 여러 개의 가상 노드를 가질 수 있음
- 가상 노드 개수를 늘리켠 키의 분포는 점점 더 균등해짐
- 가상 노드를 많이 사용하는 경우 가상 노드 데이터를 저장할 공간이 더 많이 필요함

### 재배치할 키 결정

![](/이우승/assets/ch-05/ch05_10.jpeg)



## Python Example

```python
import hashlib  
  
class ConsistentHashing:  
def __init__(self, replicas=3):  
	self.replicas = replicas # Number of replicas per server  
	self.server_ring = {}  
	self.sorted_keys = []  
  
def _get_hashed_key(self, key):  
	hash_object = hashlib.sha1(key.encode())  
	hash_key = int(hash_object.hexdigest(), 16)  
	return hash_key  
  
def add_server(self, server):  
	for i in range(self.replicas):  
		replica_key = self._get_hashed_key(f"{server}-{i}")  
		self.server_ring[replica_key] = server  
		self.sorted_keys.append(replica_key)  
		self.sorted_keys.sort()  
	  
def remove_server(self, server):  
keys_to_remove = []  
for key, value in self.server_ring.items():  
if value == server:  
keys_to_remove.append(key)  
  
for key in keys_to_remove:  
self.sorted_keys.remove(key)  
del self.server_ring[key]  
  
def get_server(self, key):  
if not self.server_ring:  
return None  
  
hashed_key = self._get_hashed_key(key)  
for server_key in self.sorted_keys:  
if hashed_key <= server_key:  
return self.server_ring[server_key]  
return self.server_ring[self.sorted_keys[0]]  
  
# Example usage  
ch = ConsistentHashing(replicas=3)  
  
servers = ['Server1', 'Server2', 'Server3']  
for server in servers:  
ch.add_server(server)  
  
keys = ['Key1', 'Key2', 'Key3', 'Key4', 'Key5']  
for key in keys:  
server = ch.get_server(key)  
print(f"Key {key} is directed to {server}")  
  
ch.add_server('Server4')  
added_server = 'Server4'  
print(f"Server {added_server} has been added.")  
  
key = 'Key6'  
server = ch.get_server(key)  
print(f"Key {key} is directed to {server} after server addition.")  
  
ch.remove_server('Server2')  
removed_server = 'Server2'  
print(f"Server {removed_server} has been removed.")  
  
key = 'Key7'  
server = ch.get_server(key)  
print(f"Key {key} is directed to {server} after server removal.")
```

**실행결과**

```
Key Key1 is directed to Server3
Key Key2 is directed to Server1
Key Key3 is directed to Server2
Key Key4 is directed to Server2
Key Key5 is directed to Server2
Server Server4 has been added.
Key Key6 is directed to Server4 after server addition.
Key Key1 is directed to Server4
Key Key2 is directed to Server1
Key Key3 is directed to Server2
Key Key4 is directed to Server2
Key Key5 is directed to Server2
Server Server2 has been removed.
Key Key7 is directed to Server4 after server removal.
Key Key1 is directed to Server4
Key Key2 is directed to Server1
Key Key3 is directed to Server4
Key Key4 is directed to Server4
Key Key5 is directed to Server4
Key Key6 is directed to Server4
```

## 참고


- https://jiwondev.tistory.com/299
- https://medium.com/@souravdas08/consistent-hashing-implemenation-a00699f408df
- https://shanu95.medium.com/consistent-hashing-101-a9edbb623f1f