
## EC2 생성 및 접속

![](/이우승/assets/aws/ec2_01.png)

![](/이우승/assets/aws/ec2_02.png)


![](/이우승/assets/aws/ec2_03.png)

![](/이우승/assets/aws/ec2_04.png)


![](/이우승/assets/aws/ec2_05.png)

### ec2 접속
```bash
chmod 400 ec2_server1.pem 
ssh -i ec2_server1.pem ubuntu@43.201.20.15
```

## Backend 개발 환경 설정

### pyenv 설치
```bash
sudo apt update 
sudo apt install git curl build-essential libssl-dev zlib1g-dev libbz2-dev \ libreadline-dev libsqlite3-dev wget llvm libncurses5-dev libncursesw5-dev \ xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git 
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

### .bashrc 설정
```bash
export PYENV_ROOT="$HOME/.pyenv" [[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH" eval "$(pyenv init -)"
```

### python 설치
```bash
pyenv install --list 
pyenv install 3.10.14
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv 
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc 
pyenv virtualenv 3.10.14 dev310
```


### poetry 설치

```bash
curl -sSL https://install.python-poetry.org | python3 - 
poetry init 
poetry add fastapi databases aiomysql
```

## ec2 추가 생성
scale out 테스트를 위해 앞서 생성한 ec2와 동일한 ec2를 생성한다.

### ami 생성

![](/이우승/assets/aws/ec2_06.png)

![](/이우승/assets/aws/ec2_07.png)

![](/이우승/assets/aws/ec2_08.png)

![](/이우승/assets/aws/ec2_09.png)

![](/이우승/assets/aws/ec2_10.png)

![](/이우승/assets/aws/ec2_11.png)

![](/이우승/assets/aws/ec2_12.png)

![](/이우승/assets/aws/ec2_13.png)



## load balancer

![](/이우승/assets/aws/lb_01.png)
 ![](/이우승/assets/aws/lb_02.png) ![](/이우승/assets/aws/lb_03.png)mapping 설정 시 주의할 점은 Availability Zone 설정 때 EC2가 존재하는 AZ를 반드시 설정해야한다
 아래와 같이 생성된 EC2의 AZ를 확인해보자

![](/이우승/assets/aws/lb_14.png)

 ![](/이우승/assets/aws/lb_04.png) ![](/이우승/assets/aws/lb_05.png) ![](/이우승/assets/aws/lb_06.png) ![](/이우승/assets/aws/lb_07.png) ![](/이우승/assets/aws/lb_08.png)
 Health Check 정보는 본인이 생성한 백엔드 프레임워크 동작 port와 path에 맞게 설정한다.
 ![](/이우승/assets/aws/lb_09.png) ![](/이우승/assets/aws/lb_10.png) ![](/이우승/assets/aws/lb_11.png) ![](/이우승/assets/aws/lb_12.png)
설정 주의 사항

target group의 health check가 안 될 때
- ec2에서 서비스가 잘 동작하는지 확인
- 해당 서비스 Port로 inbound가 잘 설정되었는지 확인
- LB IP에서 ec2로 접속 가능하도록 inbound 설정 필요

인터넷에서 LB로 접속 안 될 때
- security group 설정에서 inbound 설정이 잘 되었는지 확인


## RDS 설정

![](/이우승/assets/aws/rds_01.png)

![](/이우승/assets/aws/rds_02.png)

![](/이우승/assets/aws/rds_03.png)

![](/이우승/assets/aws/rds_04.png)

![](/이우승/assets/aws/rds_05.png)

![](/이우승/assets/aws/rds_06.png)


![](/이우승/assets/aws/rds_07.png)

![](/이우승/assets/aws/rds_08.png)






### RDS 접속
```bash
 mysql -h database-1.ctuokcc0ymlc.ap-northeast-2.rds.amazonaws.com -u root -p
```


### mysql에 데이터 적재하기
테스트용 데이터 적재를 위해 아래 git repo 사용
https://github.com/datacharmer/test_db


```
mysql -h database-1.ctuokcc0ymlc.ap-northeast-2.rds.amazonaws.com -u root -p < employees.sql
```


## DB 조회 Backend 코드
```
from fastapi import FastAPI
from databases import Database

DATABASE_URL = "mysql://root:[비밀번호]@database-1.ctuokcc0ymlc.ap-northeast-2.rds.amazonaws.com/employees"

app = FastAPI()

database = Database(DATABASE_URL)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/employees/")
async def read_users():
    query = "SELECT * FROM employees limit 1000"
    return await database.fetch_all(query)


@app.get("/users/{user_id}")
async def read_user(user_id: int):
    query = "SELECT * FROM users WHERE id = :id"
    return await database.fetch_one(query=query, values={"id": user_id})

```


## RDS master-slave

![](/이우승/assets/aws/rds_09.png)

![](/이우승/assets/aws/rds_10.png)

![](/이우승/assets/aws/rds_11.png)

![](/이우승/assets/aws/rds_12.png)

![](/이우승/assets/aws/rds_13.png)

slave를 생성하고 이후 master에 쓰기 작업을 실행하면 slave에도 동일한 데이터가 sync 된다. 아래 캡처는 master에 데이터를 추가(좌측)하고 slave에서 데이터를 확인한 결과다(우측).
![](/이우승/assets/aws/rds_14.png)



## Locust

- https://locust.io/
- 오픈 소스로 제공되는 부하 테스트 도구
- 웹 애플리케이션의 성능을 측정하고 모니터링하는 데 사용

```
pip install locust
```


locustfile.py

```
from locust import HttpUser, between, task

  

class MyUser(HttpUser):

wait_time = between(1, 2)

  

@task

def calculate_fibonacci(self):

self.client.get("/fibonacci/random")
```


```
locust --users 10 --spawn-rate 5 -t 1m --autostart -H http://43.200.169.188:8000
```


apache ab

```
ab -n 100 -c 10 http://devo-lb-1082798530.ap-northeast-2.elb.amazonaws.com/fibonacci/random
```