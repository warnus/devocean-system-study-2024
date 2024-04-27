## 1장 사용자 수에 따른 규모 확장

### 단일 서버 
- 사용자 단말(웹브라우저, 모바일)
- DNS
- 웹서버(HTML, JSON응답)
![server1](assets/server1.png)
### 데이터 베이스 
- 첫번째 서버 분리 - 사용자 증가시 "DB용 서버" 분리 

#### 어떤 데이터 베이스를 사용할 것인가
##### Relational DB
- RDBMS
- MySQL, 오라클, PostgreSQL
- 자료를 테이블과 열, 칼럼으로 표현
- SQL사용해 여러 테이블 join
##### Non - Relational DB - NoSQL
- CouchDB, Neo4j, Cassandra, HBase, Amazon DynamoDB
- 일반적으로 Join 미지원
- 세부 분류
	- key-value store
	- graph store
	- column store
	- document store

#### NoSQL 추천하는 경우
- 아주 낮은 응답지연시간 요구
- 다루는 데이터가 비정형
	- 추가 - 블로그 글등 표로 표현하기 어려운 것들, 
- 데이터(JSON, YAML, XML등)을 serialize, deserialize할수 있기만 하면 됨.
- 아주 많은 양의 데이터를 저장해야 할때 

### 수직적 규모확장 vs 수평적 규모 확장 