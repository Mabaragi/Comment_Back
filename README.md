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

몽고db 컨테이너에 연결
```
docker exec -it mongodb bash
mongosh # 셀 실행
```