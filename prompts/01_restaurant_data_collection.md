# 평양냉면 맛집 데이터 수집 프롬프트

## 목적
MCP 서버 구축을 위한 수도권 평양냉면 맛집 데이터 수집

## 출력 형식
**반드시 아래 JSON 스키마를 준수하여 출력해주세요.**

---

## 프롬프트 1: 개별 맛집 심층 조사

```
다음 평양냉면 맛집에 대해 심층 조사하여 JSON 형식으로 정리해주세요.

맛집명: {맛집_이름}

### 조사 항목

1. **기본 정보**
   - 정확한 주소 (도로명)
   - 전화번호
   - 영업시간 및 휴무일
   - 물냉면 가격 (2024-2025년 기준)
   - 예약 가능 여부
   - 주차 가능 여부

2. **역사와 계보**
   - 창업 연도
   - 창업자 및 현재 몇 대째 운영인지
   - 창업자의 출신 (평양 어느 지역/식당 출신인지)
   - 어떤 계보에 속하는지 (우래옥/의정부파/장충동파/을밀대식/독자)
   - 분점 여부 및 위치

3. **육수 분석** (1-5점 척도와 함께 서술)
   - 베이스: 순수 소고기 / 소고기+닭 / 소고기+동치미 / 동치미 중심 / 혼합
   - 맑기 (1=탁함, 5=매우 맑음)
   - 깊이/감칠맛 (1=밋밋, 5=깊음)
   - 간 정도 (1=매우 슴슴, 5=간간함)
   - 육향 강도 (1=약함, 5=진함)
   - 살얼음 여부
   - 간장 사용 여부 (정통은 소금만)
   - 매니아들의 육수 평가 코멘트

4. **면 분석**
   - 메밀 함량 (% 추정)
   - 굵기: 가늘다 / 중간 / 굵다
   - 식감 키워드: 툭툭 끊김 / 쫄깃 / 꼬들꼬들 / 부드러움
   - 스타일: 가늘고 쫄깃 / 가늘고 툭툭 / 굵고 꼬들 / 중간 균형
   - 매니아들의 면 평가 코멘트

5. **고명 구성**
   - 편육 유무 및 특징
   - 달걀 유무
   - 오이 유무
   - 배 유무
   - 동치미 무 유무
   - 고춧가루 유무 (의정부파 특징)
   - 기타 고명

6. **인증 및 수상**
   - 미쉐린 선정 여부 (연도, 몇 년 연속)
   - 블루리본 선정 여부
   - 방송 출연 이력 (수요미식회, 백종원 등)

7. **사이드 메뉴**
   - 대표 사이드 메뉴 3-5개
   - 각 메뉴 가격
   - 시그니처 메뉴 여부
   - 냉면과의 페어링 팁

8. **방문 정보**
   - 평균 웨이팅 시간 (피크/비피크)
   - 추천 방문 시간대
   - 특이한 주문 방식이나 규칙
   - 유명인 방문 이력

9. **매니아 평가 종합**
   - 입문자에게 추천 여부와 이유
   - 매니아에게 추천 여부와 이유
   - 정통성 점수 (0-100)
   - 한줄 평가

### 출력 JSON 형식

```json
{
  "id": "kebab-case-id",
  "name": "맛집명",
  "region": "jongno_euljiro | gangnam_seocho | mapo_yeouido | songpa_jamsil | gyeonggi_north | gyeonggi_south",
  "address": "도로명 주소",
  "phone": "02-XXX-XXXX",
  "hours": "11:00-21:00 (브레이크 15:00-17:00)",
  "closed_days": "월요일, 명절",
  "naengmyeon_price": 15000,
  "price_range": "13,000-20,000원",
  
  "lineage": "wooraeok | uijeongbu | jangchungdong | eulmildae | okryugwan | independent",
  "founded_year": 1946,
  "generation": 3,
  "founder": "창업자명",
  "origin_story": "평양 명월관 출신, ...",
  
  "broth": {
    "base": "beef_only | beef_chicken | beef_dongchimi | dongchimi_main | mixed",
    "clarity_level": 4,
    "depth_level": 5,
    "saltiness_level": 3,
    "beef_aroma_level": 5,
    "has_slush_ice": false,
    "uses_soy_sauce": false,
    "description": "매니아 코멘트..."
  },
  
  "noodle": {
    "style": "thin_chewy | thin_crumbly | thick_chewy | medium_balanced",
    "buckwheat_ratio": 70,
    "thickness": "thin | medium | thick",
    "texture_keywords": ["툭툭", "구수함"],
    "description": "매니아 코멘트..."
  },
  
  "toppings": {
    "has_pyeonyuk": true,
    "has_egg": true,
    "has_cucumber": true,
    "has_pear": false,
    "has_dongchimi_mu": true,
    "has_red_pepper_powder": false,
    "extras": ["잣", "실고추"]
  },
  
  "expert_rating": {
    "broth_clarity": 4,
    "broth_depth": 5,
    "noodle_aroma": 4,
    "noodle_texture": 4,
    "temperature": 4,
    "overall_balance": 5,
    "authenticity_score": 85,
    "reviewer_note": "종합 평가 코멘트..."
  },
  
  "certifications": [
    {"type": "michelin_bib", "year": 2024, "detail": "6년 연속"},
    {"type": "broadcast", "year": 2023, "detail": "수요미식회"}
  ],
  
  "side_menus": [
    {"name": "편육", "price": 35000, "is_signature": true, "pairing_note": "선육후면 코스로"},
    {"name": "녹두전", "price": 15000, "is_signature": false, "pairing_note": null}
  ],
  
  "signature_dish": "물냉면",
  "recommended_for": ["beginner", "intermediate", "expert"],
  "best_season": "all | summer | winter",
  "average_wait_minutes": 30,
  "reservation_available": false,
  "parking_available": true,
  
  "special_notes": ["숟가락 미제공 - 그릇째 마심", "거냉 주문 가능"],
  "famous_visitors": ["BTS RM", "성시경"],
  
  "tags": ["미쉐린", "노포", "진한육수", "입문자추천"]
}
```

### 주의사항
- 확인되지 않은 정보는 null로 표기
- 가격은 2024-2025년 기준, 확인 불가 시 명시
- 매니아 커뮤니티, 블로그, 기사 등 다양한 소스 교차 검증
- 주관적 평가는 여러 리뷰를 종합하여 객관화
```

---

## 프롬프트 2: 수도권 전체 맛집 리스트 수집

```
수도권(서울, 경기) 평양냉면 맛집을 조사하여 JSON 배열로 정리해주세요.

### 수집 대상 기준 (우선순위)
1. 미쉐린 가이드 선정 맛집 (빕구르망, 스타)
2. 블루리본 선정 맛집
3. 40년 이상 역사를 가진 노포
4. 평양냉면 매니아 커뮤니티에서 검증된 맛집
5. 방송(수요미식회, 백종원 등) 출연 맛집

### 지역별 최소 수집 목표
- 종로/을지로/중구: 10곳 이상
- 강남/서초: 5곳 이상  
- 마포/여의도: 5곳 이상
- 송파/잠실: 3곳 이상
- 경기 북부 (의정부 등): 3곳 이상
- 경기 남부 (판교, 분당, 수원 등): 3곳 이상

### 출력 형식

```json
{
  "collection_date": "2025-01-08",
  "total_count": 30,
  "restaurants": [
    {
      "name": "우래옥",
      "region": "jongno_euljiro",
      "address": "서울 중구 창경궁로 62-29",
      "lineage": "wooraeok",
      "founded_year": 1946,
      "naengmyeon_price": 16000,
      "certifications": ["michelin_bib"],
      "priority_reason": "서울 최고(最古) 평양냉면, 미쉐린 선정",
      "data_confidence": "high | medium | low"
    },
    ...
  ],
  "by_lineage": {
    "wooraeok": ["우래옥", "봉피양"],
    "uijeongbu": ["필동면옥", "을지면옥", "의정부평양면옥"],
    "jangchungdong": ["장충동평양면옥", "진미평양냉면"],
    "eulmildae": ["을밀대"],
    "independent": ["남포면옥", "능라도"]
  },
  "by_region": {
    "jongno_euljiro": ["우래옥", "필동면옥", "을지면옥", "남포면옥"],
    "gangnam_seocho": ["진미평양냉면", "봉밀가", "피양옥"],
    ...
  }
}
```

### 참고할 소스
- 미쉐린 가이드 서울 2024/2025
- 블루리본 서베이
- 네이버/카카오 맛집 리뷰
- 평양냉면 관련 기사 (조선일보, 중앙일보, 한겨레 등)
- 매니아 커뮤니티 (디시인사이드, 에펨코리아, 클리앙 등)
- 유튜브 맛집 리뷰
```

---

## 프롬프트 3: 계보별 상세 정보 수집

```
평양냉면 4대 계보에 대해 심층 조사하여 JSON으로 정리해주세요.

### 조사할 계보
1. 우래옥 계열 (wooraeok)
2. 의정부파 (uijeongbu)  
3. 장충동파 (jangchungdong)
4. 을밀대식 (eulmildae)
5. (추가) 북한 옥류관식 (okryugwan)

### 각 계보별 조사 항목

1. **기원과 역사**
   - 본산(원조) 맛집과 창업 연도
   - 창업자와 그의 배경 (북한 어디 출신, 어느 식당 출신)
   - 서울/남한에 정착한 경위
   - 분파된 맛집들과 그 계보도

2. **맛의 철학과 특징**
   - 육수: 재료, 조리법, 맛의 방향성
   - 면: 메밀 함량, 제면 방식, 식감
   - 고명: 특징적인 구성
   - 이 계보만의 차별화 포인트

3. **대표 맛집 목록**
   - 본점/원조
   - 주요 분점/계승 맛집
   - 영향을 받은 맛집

4. **추천 대상**
   - 입문자 적합 여부
   - 매니아 적합 여부
   - 어떤 취향의 사람에게 맞는지

5. **계보 내 논쟁/분화**
   - 본점과 분점의 맛 차이
   - 세대별 변화
   - 매니아들의 평가

### 출력 JSON 형식

```json
{
  "lineages": [
    {
      "id": "wooraeok",
      "name": "우래옥 계열",
      "name_ko": "우래옥 계열",
      "origin": "1946년 을지로 '서북관'으로 시작, 현재 위치로 1948년 이전",
      "founder": "장원일·나정일 부부 (평양 명월관 출신)",
      "philosophy": "순수 소고기 육수로 진한 육향 추구, 동치미 미사용",
      
      "broth_characteristics": "한우 아롱사태, 엉덩이살로 5시간 이상 추출. 맑지만 진한 육향과 기름기. 탈북자 이한영이 '옥류관과 가장 유사'라 평가",
      "noodle_characteristics": "중간 굵기, 적당한 메밀 함량으로 부드러운 식감",
      "distinctive_features": "입문자 친화적인 진한 맛, 동치미 미사용이 특징",
      
      "representative_restaurants": ["wooraeok", "bongpiyang"],
      
      "suitable_for": ["beginner", "intermediate"],
      
      "lineage_tree": {
        "origin": "우래옥 (1946)",
        "branches": [
          {"name": "봉피양", "year": 2005, "relation": "우래옥 60년 근무 김태원 장인 영입"}
        ]
      },
      
      "controversies": "봉피양이 진정한 계승자인지에 대한 논쟁 존재",
      
      "expert_consensus": "평양냉면 입문의 정석. 거부감 없는 진한 맛으로 시작하기 좋음"
    },
    ...
  ]
}
```
```
