## pytest 사용법

### 기본 명령어 
``` bash
# 기본 명령
pytest tests/test_episode_crawler.py

# 출력 보여주는 명령어
pytest -s tests/test_episode_crawler.py
```

### 결과
- `passed`: 예상대로 성공한 테스트
- `xpassed`: 예상과 달리 성공한 테스트
- `xfailed`: 예상대로 실패한 테스트


## test_episode_crawler.py

series id로 부터 모든 episode를 가져오는 크롤러

