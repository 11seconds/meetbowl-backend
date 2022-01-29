# meetbowl-backend


## 주요 개발 스택

* Python 3.6
* Fast API
* PostgreSQL


## Backend Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/) for Python package and environment management.


## 아키택쳐

- api: API 엔드포인트 라우팅
- core: 보안 관련 모듈, 환경변수 세팅
- crud: DB CRUD 관련 로직
- db: DB 세션 연결 관리
- models: DB 스키마 모델 정의
- schemas: Pydantic 이용한 객체 스키마 타입핑
- test: 테스트 코드 관련 (아직 Init 상태임)

## Backend local development 실행하기

* Start the stack with Docker Compose:

```bash
docker-compose up -d
```

* Now you can open your browser and interact with these URLs:


Backend, JSON based web API based on OpenAPI: http://localhost/api/

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost/docs

Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://localhost/redoc

PGAdmin, PostgreSQL web administration: http://localhost:5050


**Note**: 처음 배포시에는 시간이 10분 이상 길게 소요될 수 있습니다.

To check the logs, run:

```bash
docker-compose logs
```

To check the logs of a specific service, add the name of the service, e.g.:

```bash
docker-compose logs backend
```
