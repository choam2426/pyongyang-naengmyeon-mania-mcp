# 평양냉면 MCP 서버 🍜

평양냉면 매니아/입문자를 위한 MCP(Model Context Protocol) 서버입니다.

## 기능

### 도구 목록

| 도구 | 설명 | 입문자 | 매니아 |
|------|------|:------:|:------:|
| `search_restaurants` | 다중 조건 맛집 검색 | ✓ | ✓ |
| `get_restaurant` | 맛집 상세 정보 조회 | ✓ | ✓ |
| `get_lineage_info` | 계보(파벌) 정보 조회 | | ✓ |
| `recommend` | 취향 기반 맛집 추천 | ✓ | ✓ |
| `compare` | 두 맛집 비교 분석 | | ✓ |
| `get_eating_guide` | 먹는 법 가이드 | ✓ | |
| `get_side_pairings` | 사이드 메뉴 추천 | ✓ | ✓ |

### 평양냉면 4대 계보

- **우래옥 계열**: 진한 육향, 입문자 친화적
- **의정부파**: 고춧가루, 간간한 맛
- **장충동파**: 가장 슴슴함, 매니아 선호
- **을밀대식**: 살얼음, 굵은 면

## 설치

```bash
# 저장소 클론
git clone https://github.com/choam2426/pyongyang-naengmyeon-mania-mcp
cd pyongyang-naengmyeon-mcp

# uv로 의존성 설치 (권장)
uv sync

# 또는 pip으로 설치
pip install -e .
```

## 로컬 테스트 (배포 전)

### 1. MCP Inspector로 테스트

MCP Inspector를 사용하면 브라우저에서 도구를 직접 테스트할 수 있습니다.

```bash
# PYTHONPATH 설정 후 실행
$env:PYTHONPATH="src"  # PowerShell
# export PYTHONPATH=src  # Bash

npx @modelcontextprotocol/inspector python -m pyongyang_naengmyeon.server
```

브라우저에서 `http://localhost:5173` 접속 후 도구 테스트 가능

### 2. 직접 실행 테스트

```bash
# PYTHONPATH 설정 후 서버 실행 (stdio 모드)
$env:PYTHONPATH="src"  # PowerShell
python -m pyongyang_naengmyeon.server
```

### 3. 린트 & 타입 체크

```bash
# 린트
uv run ruff check src/

# 타입 체크
uv run mypy src/
```

## 사용법

### Claude Desktop 설정

`claude_desktop_config.json`에 추가:

```json
{
  "mcpServers": {
    "pyongyang-naengmyeon": {
      "command": "python",
      "args": ["-m", "pyongyang_naengmyeon.server"],
      "cwd": "/path/to/pyongyang-naengmyeon-mcp",
      "env": {
        "PYTHONPATH": "/path/to/pyongyang-naengmyeon-mcp/src"
      }
    }
  }
}
```

### Cursor 설정

`.cursor/mcp.json`에 추가:

```json
{
  "mcpServers": {
    "pyongyang-naengmyeon": {
      "command": "python",
      "args": ["-m", "pyongyang_naengmyeon.server"],
      "cwd": "/path/to/pyongyang-naengmyeon-mcp",
      "env": {
        "PYTHONPATH": "/path/to/pyongyang-naengmyeon-mcp/src"
      }
    }
  }
}
```

### 사용 예시

```
# 입문자 추천
"평양냉면 처음인데 어디 가면 좋을까?"
→ recommend(experience_level="beginner", situation="first_timer")

# 계보별 검색
"우래옥 계열 맛집 알려줘"
→ search_restaurants(lineage="wooraeok")

# 상세 정보
"을밀대 상세 정보 보여줘"
→ get_restaurant(name="을밀대")

# 비교
"우래옥이랑 장충동평양면옥 비교해줘"
→ compare(restaurant1="우래옥", restaurant2="장충동평양면옥")
```

## 데이터 구축

`prompts/` 폴더의 프롬프트를 사용하여 Deep Research로 데이터를 수집합니다.

```
prompts/
├── 01_restaurant_data_collection.md   # 맛집 데이터 수집
├── 02_terminology_and_guide_collection.md  # 용어/가이드 수집
└── 03_deep_research_execution.md      # 실행 가이드
```

### 실행 순서

1. `03_deep_research_execution.md`의 **프롬프트 A** 실행 → 맛집 데이터
2. **프롬프트 B** 실행 → 계보, 용어, 가이드 데이터
3. **프롬프트 C** 실행 → 데이터 검증
4. JSON 파일을 `src/pyongyang_naengmyeon/data/`에 저장

## 프로젝트 구조

```
pyongyang-naengmyeon-mcp/
├── src/pyongyang_naengmyeon/
│   ├── __init__.py
│   ├── server.py              # MCP 서버 엔트리포인트
│   ├── models/
│   │   ├── enums.py           # 열거형 정의
│   │   └── schemas.py         # Pydantic 스키마
│   ├── tools/
│   │   └── definitions.py     # MCP 도구 정의
│   └── data/
│       ├── restaurants.json   # 맛집 데이터
│       ├── lineages.json      # 계보 데이터
│       ├── eating_guides.json # 먹는 법 가이드
│       └── side_menus.json    # 사이드 메뉴 데이터
├── prompts/                   # Deep Research 프롬프트
├── pyproject.toml
└── README.md
```

## 데이터 스키마

### Restaurant (맛집)

```python
class Restaurant(BaseModel):
    id: int
    name: str
    region: Region
    lineage: Lineage
    
    # 맛 프로필
    broth: BrothProfile      # 육수
    noodle: NoodleProfile    # 면
    toppings: ToppingsProfile # 고명
    
    # 평가
    expert_rating: ExpertRating
    certifications: list[Certification]
    
    # 메타
    recommended_for: list[ExperienceLevel]
    special_notes: list[str]
```

## Fly.io 배포 (무료)

### 1. Fly CLI 설치 & 로그인

```bash
# Windows PowerShell
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# 로그인
fly auth login
```

### 2. 배포

```bash
# 첫 배포 (앱 생성)
fly launch --no-deploy

# 배포
fly deploy
```

### 3. 배포 후 사용

배포 완료 시 URL 출력됨: `https://pyongyang-naengmyeon-mcp.fly.dev`

```json
{
  "mcpServers": {
    "pyongyang-naengmyeon": {
      "url": "https://pyongyang-naengmyeon-mcp.fly.dev/sse"
    }
  }
}
```

### 무료 티어

- 3개 shared-cpu-1x VM 무료
- 월 160GB 아웃바운드 트래픽 무료
- `auto_stop_machines = true` 설정으로 비활성 시 자동 중지

### 로컬 SSE 서버 테스트

```bash
$env:PYTHONPATH="src"  # PowerShell
python -m pyongyang_naengmyeon.mcp_server

# http://localhost:8000/health 로 헬스체크
```

## 기여

1. 새로운 맛집 데이터 추가
2. 평가 정보 업데이트
3. 용어 사전 확장

## 라이선스

MIT License
