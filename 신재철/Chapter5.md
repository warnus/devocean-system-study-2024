# 안정 해시 설계

## 해시 키 재배치(rehash) 문제
N개의 캐시 서버가 있을 때 서버들에 부하를 균등하게 나누는 보편적 방법은 아래 해시 함수를 사용.
serverIndex = hash(key) % N

저장할 때 어떤 서버에 저장할지와, 데이터를 읽을 떄 어디서 읽을지 찾을때 사용.

이 방법은 서버 풀의 크기가 고정되어 있을 때, 그리고 데이터 분포가 균등할 떄는 잘 동작한다.
하지만 서버풀의 서버 일부가 죽어서 제외되거나 새로운 서버가 서버풀에 추가되었을 떄 문제가 발생한다.

안정 해시는 이 문제를 해결하는 기술이다.

## 안정 해시
안정 해시는 해시 테이블 크기가 조정될 때 평균적으로 오직 k/n개의 키만 재배치하는 해시 기술이다. (k=키의 개수, n=슬롯의 개수)
대부분의 전통적 해시 테이블은 슬롯의 수가 바뀌면 거의 대부분 키를 재배치한다.

### 해시 공간과 해시 링
- 해시 함수 f로는 SHA-1을 사용
- 함수의 출력 값 범위는 x0, x1, x2, ... xn
- SHA-1의 해시 공간 범위는 0부터 2^160-1

해시 공간의 양쪽을 구부려 접으면 해시링이 만들어짐.
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FHBbtW%2FbtrNoJqgIdK%2FaLrCZfoCQ19K6sMRjivCCk%2Fimg.png)
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdSvitx%2FbtrNqYfLshO%2FvJSMVwuTk5fEx6KB1aDIMk%2Fimg.png)

### 해시 서버
해시 함수 f를 사용하면 서버 IP나 이름을 링 위의 어떤 위치에 대응시킬 수 있다.
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdpF7y6%2Fbtrocdpmjac%2FtEGwQEWfAKKgL4zvXBYKY1%2Fimg.png)

### 해시 키
여기서 해시 함수는 나머지 연산(%)은 사용하지 않고 있음에 유의하자. 
캐시할 키 또한 해시 링 위의 어느 지점에 배치할 수 있다.
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F48dSo%2Fbtrob7iGKbw%2FWzdIUzy6cGDwhPKxprZI9K%2Fimg.png)

### 서버 조회
어떤 키가 저장되는 서버는, 해당 키의 위치로부터 시계 방향으로 링을 탐색해 나가면서 만나는 첫 번째 서버다.
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbxM5ud%2FbtrNlSuZ8Nt%2FaoFKAGkLjW9ftiX9203k11%2Fimg.png)

### 서버 추가
서버를 추가하더라도 키 가운데 일부만 재배치하면 된다.
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbvZeDx%2FbtrNoKpaIMD%2F3sQI6NQdqbi3K34II5kipk%2Fimg.png)

4번 서버가 추가되고 key0만 재배치되게 된다.

### 서버 제거
하나의 서버가 제거되면 키 가운데 일부만 재배치하면 된다.
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FwpmNF%2FbtrNqYUnIZx%2F4nAgDv3xNYZ44mmC2LApZK%2Fimg.png)

1번 서버가 제거되었을 때 key1만이 서버 2로 재배치된다.

### 기본 구현법의 두 가지 문제
안정 해시 알고리즘의 기본 절차는 다음과 같다.
- 서버와 키를 균등 분포 해시 함수를 사용해 해시 링에 배치
- 키의 위치에서 링을 시계 방향으로 탐색하다 만나는 최초의 서버가 키가 저장될 서버

이 접근법에는 두 가지 문제가 있다.
1. 서버가 추가되거나 삭제되는 상황을 감안하면 파티션의 크기를 균등하게 유지하는 게 불가능하다
2. 키의 균등 분포를 달성하기 어렵다

이 문제를 해결하기 위해 제안된 기법이 가상 노드 또는 복제라 불리는 기법이다.

### 가상 노드
실제 노드 또는 서버를 가리키는 노드로서, 하나의 서버는 링 위에 여러 개의 가상 노드를 가질 수 있다. 

키가 저장될 서버는 키의 위치로부터 시계 방향으로 돌며 만나는 첫번째 가상 노드이다.
![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FciHfIK%2FbtrNoD4N0As%2F3spKHNLrBRC45sKB3btR1k%2Fimg.png)

가상 노드의 개수를 늘리면 키의 분포는 점점 더 균등해진다. 
그러나 가상 노드가 늘어날 수록 데이터를 저장할 공간은 더 많이 필요하게 되는 tradeoff가 있다. 적절한 개수로 가상 노드를 설정할 필요가 있다.

### 재배치할 키 결정
서버가 추가되거나 제거되면 데이터 일부는 재배치해야 한다. 

## 마치며
안정 해시의 이점은 다음과 같다.
- 서버가 추가되거나 삭제될 떄 재배치되는 키의 수가 최소화된다.
- 데이터가 보다 균등하게 분포하게 되므로 수평적 규모 확장성을 달성하기 쉽다.
- 핫스팟 키 문제를 줄인다. 특정한 샤드에 대한 접근이 지나치게 빈번하면 서버 과부하 문제가 생길 수 있다.