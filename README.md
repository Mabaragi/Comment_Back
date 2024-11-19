## 프로젝트 구조
```
your_fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── comments.py
│   │   │   │   ├── episodes.py
│   │   │   │   └── rag.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── comment.py
│   │   └── episode.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── comment.py
│   │   ├── episode.py
│   │   └── rag.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── crawler.py
│   │   ├── database.py
│   │   └── rag_service.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── client.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_comments.py
│   ├── test_episodes.py
│   └── test_rag.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
├── Dockerfile
└── docker-compose.yml
```


## poetry


## Docker
- `--build` 옵션은 Dockerfile의 변경사항을 반영하여 이미지를 다시 빌드합니다.
--build 옵션이란?
--build 옵션은 docker-compose up 명령어에 추가하여 서비스의 도커 이미지를 다시 빌드하도록 강제하는 역할을 합니다. 기본적으로 docker-compose up은 필요한 경우에만 이미지를 빌드하지만, --build 옵션을 사용하면 이미지를 항상 다시 빌드하게 됩니다.

Docker Compose의 up 명령어는 다양한 상황에 따라 유연하게 동작하며, 효율적으로 컨테이너를 관리할 수 있도록 도와줍니다. 처음 사용 시 이미지 빌드와 컨테이너 생성을 수행하고, 이후에는 변경 사항에 따라 이미지를 재빌드하거나 컨테이너를 재생성합니다. 이러한 동작 방식을 이해하고 활용하면, 개발 및 배포 과정에서 Docker Compose를 더욱 효과적으로 사용할 수 있습니다.

## MongoDB

### 몽고db 컨테이너에 연결
```
docker exec -it mongodb bash
mongosh # 셀 실행
```

### 몽고 db 인증
docker-compose의 환경변수에서 정의한 계정으로 로그인한다
```bash
mongosh "mongodb://admin:secret@localhost:27017"
```

### 몽고sh 명령어
```js
showdbs # 데이터베이스 조회
use my_project # 데이터베이스 선택
db # 현재 데이터베이스 확인
show collections # 콜렉션 조회
db.comments.createIndex({commentUid: 1}, {unique:true}) # 고유 인덱스 생성
```
```js
comments> db.comments.getIndexes()
[
  { v: 2, key: { _id: 1 }, name: '_id_' },
  { v: 2, key: { commentUid: 1 }, name: 'commentUid_1', unique: true }
]
```
_id와 commentUid 필드가 오름차순으로 설정된 인덱스.

### 몽고 초기화 스크립트
초기화 스크립트를 다음과 같이 지정 할 수 있다.
```docker-compose
volumes:
    - mongo_data:/data/db
    - ./init-mongo.js:/docker-entrypoint-initdb.d/init-mongo.j
```
- 초기화 스크립트의 권한은 환경변수의 계정과 비밀번호로 부여된다.
- 초기화 스크립트는 몽고db의 데이터베이스가 비어있을 경우에만 실행된다.

- 초기화 스크립트
```js
// 몽고db는 데이터베이스나 콜렉션, 필드가 없을 경우에도 아래와 같은 작업이 가능하다.
db = db.getSiblingDB("my_project"); // 데이터베이스 선택

// 고유 인덱스 생성
db.comments.createIndex({ commentUid: 1 }, { unique: true });
db.episodes.createIndex({ productId: 1 }, { unique: true });

print("Indexes created successfully!");

```

## fastAPI

### dependencies

dependencies.py에 의존성 객체를 정의하고 다른 라우터에서 불러올 수 있다.
``` python
from ...dependencies import get_database

mongo: dict[str, MongoDB] = Depends(get_database)
```
`lifespan`을 사용하기 위해서 `main.py`에서 dependencies.py 의 객체를 수정했다.
참조형 객체인 딕셔너리로 해야지 모듈 외부에서 변수를 수정할 수 있었다. 일반 변수는 None이 할당됨.



## TODO

1. 같은 댓글들 크롤링하여 db에 저장하는 것을 방지하는 로직 개발