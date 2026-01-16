# Deep Research 실행용 종합 프롬프트

## 사용법
이 프롬프트를 Deep Research에 입력하여 전체 데이터를 한 번에 수집합니다.

---

## 프롬프트 A: 맛집 전체 데이터 수집 (1회차)

```
# 평양냉면 MCP 서버용 데이터 수집

수도권(서울, 경기) 평양냉면 맛집 데이터를 수집하여 JSON으로 출력해주세요.

## 수집 대상 맛집 (우선순위순)

### 필수 수집 (Tier 1) - 반드시 포함
1. 우래옥 (을지로)
2. 을밀대 (마포)
3. 필동면옥 (필동)
4. 장충동평양면옥 (장충동)
5. 의정부평양면옥 (의정부)
6. 진미평양냉면 (강남 논현)
7. 봉피양 (송파 방이동)
8. 남포면옥 (을지로)
9. 을지면옥 (종로 낙원동)
10. 능라도 (판교)

### 권장 수집 (Tier 2) - 가능하면 포함
11. 봉밀가 (강남)
12. 피양옥 (청담)
13. 강서면옥 (서소문)
14. 평래옥 (을지로)
15. 유진식당 (을지로)
16. 정인면옥 (여의도)
17. 본가평양면옥 (강남)
18. 서경도락 (중구)
19. 동무밥상 (합정) - 옥류관 스타일
20. 평안도상원냉면 (홍대)

등등 기타 맛집도 포함

## 각 맛집별 수집 항목

```json
{
  "id": "kebab-case-id",
  "name": "맛집명",
  "region": "jongno_euljiro | gangnam_seocho | mapo_yeouido | songpa_jamsil | gyeonggi_north | gyeonggi_south",
  "address": "도로명 주소",
  "phone": "02-XXX-XXXX 또는 null",
  "hours": "영업시간 또는 null",
  "closed_days": "휴무일 또는 null",
  "naengmyeon_price": 15000,
  "price_range": "가격대 문자열",
  
  "lineage": "wooraeok | uijeongbu | jangchungdong | eulmildae | okryugwan | independent",
  "founded_year": 1946,
  "generation": 3,
  "founder": "창업자명 또는 null",
  "origin_story": "유래 설명 또는 null",
  
  "broth": {
    "base": "beef_only | beef_chicken | beef_dongchimi | dongchimi_main | mixed",
    "clarity_level": 1-5,
    "depth_level": 1-5,
    "saltiness_level": 1-5,
    "beef_aroma_level": 1-5,
    "has_slush_ice": true/false,
    "uses_soy_sauce": true/false,
    "description": "육수 특징 설명"
  },
  
  "noodle": {
    "style": "thin_chewy | thin_crumbly | thick_chewy | medium_balanced",
    "buckwheat_ratio": 0-100,
    "thickness": "thin | medium | thick",
    "texture_keywords": ["키워드1", "키워드2"],
    "description": "면 특징 설명"
  },
  
  "toppings": {
    "has_pyeonyuk": true/false,
    "has_egg": true/false,
    "has_cucumber": true/false,
    "has_pear": true/false,
    "has_dongchimi_mu": true/false,
    "has_red_pepper_powder": true/false,
    "extras": ["추가 고명"]
  },
  
  "expert_rating": {
    "broth_clarity": 1-5,
    "broth_depth": 1-5,
    "noodle_aroma": 1-5,
    "noodle_texture": 1-5,
    "temperature": 1-5,
    "overall_balance": 1-5,
    "authenticity_score": 0-100,
    "reviewer_note": "종합 평가"
  },
  
  "certifications": [
    {"type": "michelin_bib | michelin_star | blue_ribbon | broadcast", "year": 2024, "detail": "상세"}
  ],
  
  "side_menus": [
    {"name": "메뉴명", "price": 가격, "is_signature": true/false, "pairing_note": "페어링 팁 또는 null"}
  ],
  
  "recommended_for": ["beginner", "intermediate", "expert"],
  "best_season": "all | summer | winter",
  "average_wait_minutes": 30,
  "reservation_available": true/false,
  "parking_available": true/false,
  
  "special_notes": ["특이사항"],
  "famous_visitors": ["유명인"],
  "tags": ["검색태그"]
}
```

## 출력 형식

```json
{
  "metadata": {
    "collection_date": "2025-01-08",
    "total_count": 20,
    "data_sources": ["미쉐린가이드", "블루리본", "네이버", "매니아블로그", "기사"]
  },
  "restaurants": [
    { /* 맛집1 */ },
    { /* 맛집2 */ },
    ...
  ]
}
```

## 주의사항
1. 확인되지 않은 정보는 null로 표기
2. 가격은 2025년 기준
3. 평가 점수는 여러 소스를 종합하여 객관화
4. 계보 분류가 모호한 경우 "independent"로 처리
5. 폐업/이전 확인 필수
```

---

## 프롬프트 B: 계보 및 용어/가이드 데이터 수집 (2회차)

```
# 평양냉면 계보, 용어, 가이드 데이터 수집

## Part 1: 계보 정보

평양냉면 5대 계보에 대해 상세 조사해주세요.

### 수집할 계보
1. wooraeok - 우래옥 계열
2. uijeongbu - 의정부파
3. jangchungdong - 장충동파
4. eulmildae - 을밀대식
5. okryugwan - 북한 옥류관식

### 각 계보별 필요 정보
- 기원과 역사 (본산, 창업자, 연도)
- 맛의 철학 (육수, 면, 고명 특징)
- 대표 맛집 목록
- 추천 대상 (입문자/매니아)
- 계보 내 분파와 논쟁

### 출력 형식
```json
{
  "lineages": [
    {
      "id": "wooraeok",
      "name": "우래옥 계열",
      "name_ko": "우래옥 계열",
      "origin": "기원 설명",
      "founder": "창업자",
      "philosophy": "맛의 철학",
      "broth_characteristics": "육수 특징",
      "noodle_characteristics": "면 특징",
      "distinctive_features": "차별점",
      "representative_restaurants": ["맛집ID1", "맛집ID2"],
      "suitable_for": ["beginner", "intermediate"],
      "lineage_tree": {
        "origin": "본점명 (연도)",
        "branches": [{"name": "분점명", "year": 2005, "relation": "관계설명"}]
      }
    }
  ]
}
```

---

## Part 2: 용어 사전

평양냉면 전문 용어 30개 이상 수집해주세요.

### 카테고리
- broth (육수): 슴슴하다, 깊다, 텁텁하다, 맑다, 진하다, 살얼음 등
- noodle (면): 툭툭, 뚝뚝, 쫄깃, 구수하다, 목넘김, 불다 등
- ordering (주문): 거냉, 양마니, 면수, 사리, 곱빼기 등
- culture (문화): 선육후면, 어복쟁반, 면스플레인 등
- evaluation (평가): 정통, 밸런스, 상업화 등

### 출력 형식
```json
{
  "terminology": [
    {
      "term": "용어",
      "category": "broth | noodle | ordering | culture | evaluation",
      "definition": "정의",
      "usage_example": "사용 예시",
      "related_terms": ["관련어1", "관련어2"],
      "is_positive": true | false | null,
      "etymology": "어원 (있으면)"
    }
  ]
}
```

---

## Part 3: 먹는 법 가이드

5개 주제의 가이드를 작성해주세요.

### 주제
1. basic - 기본 먹는 순서
2. condiments - 식초/겨자 사용법
3. ordering - 주문 요령
4. etiquette - 예절
5. seasonal - 계절별 팁

### 출력 형식
```json
{
  "eating_guides": [
    {
      "id": "basic",
      "title": "제목",
      "description": "설명",
      "steps": ["단계1", "단계2"],
      "tips": ["팁1", "팁2"],
      "common_mistakes": ["실수1", "실수2"],
      "expert_opinions": ["의견1"],
      "restaurant_specific": {
        "을밀대": {"terms": ["거냉"], "notes": "숟가락 미제공"}
      }
    }
  ]
}
```

---

## Part 4: 사이드 메뉴 가이드

```json
{
  "side_menus": [
    {
      "name": "메뉴명",
      "description": "설명",
      "price_range": "가격대",
      "portions": "인분",
      "pairing_note": "페어링 팁",
      "best_at": ["맛집1", "맛집2"],
      "recommended_for": ["상황1", "상황2"]
    }
  ],
  "course_examples": [
    {
      "name": "코스명",
      "for_people": 2,
      "budget": "예산",
      "menu": ["메뉴1", "메뉴2"],
      "order": "순서 설명",
      "tip": "팁"
    }
  ]
}
```

---

## 전체 출력을 하나의 JSON으로 통합

```json
{
  "metadata": {
    "collection_date": "2025-01-08",
    "version": "1.0"
  },
  "lineages": [...],
  "terminology": [...],
  "eating_guides": [...],
  "side_menus": [...],
  "course_examples": [...]
}
```
```

---

## 프롬프트 C: 데이터 검증 및 보완 (3회차)

```
# 평양냉면 데이터 검증 및 보완

수집 데이터를 검증하고 누락된 정보를 보완해주세요.

## 검증 항목

### 1. 맛집 정보 검증
- [ ] 주소가 현재 유효한지 (이전/폐업 확인)
- [ ] 가격이 2025년 기준인지
- [ ] 영업시간 변경 여부
- [ ] 미쉐린/블루리본 선정 연도 정확성

### 2. 누락 맛집 추가 조사
다음 맛집이 누락되었다면 추가 조사:
- 평래옥, 강서면옥, 서경도락, 냉면제면소 등

### 3. 최신 정보 업데이트
- 2025-2026 미쉐린 가이드, 블루리본 반영
- 최근 오픈/폐업 맛집
- 가격 인상 정보

### 4. 교차 검증
- 계보 분류가 여러 소스에서 일치하는지
- 평가 점수가 극단적이지 않은지
- 특이사항이 실제로 맞는지

```

---

## 실행 순서 권장

1. **프롬프트 A** 실행 → `restaurants.json` 저장
2. **프롬프트 B** 실행 → `lineages.json`, `terminology.json`, `guides.json` 저장
3. **프롬프트 C** 실행 → 데이터 검증 및 수정
4. 수동 검토 후 최종 데이터 확정

---

## 데이터 파일 구조

```
data/
├── restaurants.json      # 맛집 데이터
├── lineages.json         # 계보 데이터
├── terminology.json      # 용어 사전
├── eating_guides.json    # 먹는 법 가이드
├── side_menus.json       # 사이드 메뉴
└── metadata.json         # 메타 정보
```
