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