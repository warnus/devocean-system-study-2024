
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

DATABASE_URL = "mysql://root:qlalfqjsgh1!@database-1.ctuokcc0ymlc.ap-northeast-2.rds.amazonaws.com/employees"

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

![](/이우승/assets/aws/rds_14.png)