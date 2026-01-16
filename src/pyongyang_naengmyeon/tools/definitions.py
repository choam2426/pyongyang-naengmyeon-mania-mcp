"""평양냉면 MCP 서버 도구 정의"""

from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field
from typing import Optional

from ..models import (
    Region, Lineage, ExperienceLevel, BrothPreference, 
    VisitSituation
)


# ============================================================
# 도구 입력 스키마
# ============================================================

class SearchRestaurantsInput(BaseModel):
    """맛집 검색 입력"""
    region: Optional[Region] = Field(default=None, description="지역 필터")
    lineage: Optional[Lineage] = Field(default=None, description="계보 필터")
    max_price: Optional[int] = Field(default=None, description="최대 가격 (원)")
    experience_level: Optional[ExperienceLevel] = Field(
        default=None, description="추천 대상 경험 수준"
    )
    michelin_only: bool = Field(default=False, description="미쉐린 선정 맛집만")
    has_slush_ice: Optional[bool] = Field(default=None, description="살얼음 육수 맛집만")
    tier: Optional[int] = Field(default=None, description="등급 필터 (1=최상위, 2=우수)")
    query: Optional[str] = Field(default=None, description="자연어 검색")


class GetRestaurantInput(BaseModel):
    """맛집 상세 조회 입력"""
    id: Optional[str] = Field(default=None, description="맛집 ID")
    name: Optional[str] = Field(default=None, description="맛집 이름")


class GetLineageInfoInput(BaseModel):
    """계보 정보 조회 입력"""
    lineage: str = Field(description="계보 ID 또는 'all'")


class RecommendInput(BaseModel):
    """추천 입력"""
    experience_level: ExperienceLevel = Field(description="평양냉면 경험 수준")
    broth_preference: BrothPreference = Field(
        default=BrothPreference.NO_PREFERENCE,
        description="육수 선호도"
    )
    situation: Optional[VisitSituation] = Field(default=None, description="방문 상황")
    region: Optional[Region] = Field(default=None, description="선호 지역")
    avoid_long_wait: bool = Field(default=False, description="긴 웨이팅 회피")


class CompareInput(BaseModel):
    """비교 입력"""
    restaurant1: str = Field(description="첫 번째 맛집 (ID 또는 이름)")
    restaurant2: str = Field(description="두 번째 맛집 (ID 또는 이름)")
    focus_on: Optional[str] = Field(
        default=None, 
        description="비교 초점: broth, noodle, overall, value"
    )


class GetEatingGuideInput(BaseModel):
    """먹는 법 가이드 입력"""
    restaurant_id: Optional[str] = Field(default=None, description="특정 맛집용 가이드")
    topic: Optional[str] = Field(
        default="basic",
        description="주제: basic, condiments, ordering, etiquette, seasonal"
    )


class GetSidePairingsInput(BaseModel):
    """사이드 메뉴 추천 입력"""
    restaurant_id: Optional[str] = Field(default=None, description="맛집 ID")
    budget: Optional[int] = Field(default=None, description="1인 예산 (원)")
    include_alcohol: bool = Field(default=False, description="주류 포함")


# ============================================================
# 도구 정의
# ============================================================

TOOLS: list[Tool] = [
    Tool(
        name="search_restaurants",
        description="""평양냉면 맛집을 다양한 조건으로 검색합니다.

사용 예시:
- 강남 지역 미쉐린 맛집: region="gangnam_seocho", michelin_only=true
- 입문자용 맛집: experience_level="beginner"
- 우래옥 계열 맛집: lineage="wooraeok"
- 살얼음 육수 맛집: has_slush_ice=true
- 최상위 등급만: tier=1
- 자연어 검색: query="진한 육수 슴슴한"

반환: 조건에 맞는 맛집 목록 (이름, 위치, 계보, 가격, 특징)""",
        inputSchema=SearchRestaurantsInput.model_json_schema(),
    ),
    
    Tool(
        name="get_restaurant",
        description="""특정 맛집의 상세 정보를 조회합니다.

포함 정보:
- 기본 정보: 주소, 영업시간, 가격
- 계보와 역사: 창업 연도, 창업자, 유래
- 맛 프로필: 육수/면/고명 상세 분석
- 매니아 평가: 6개 항목별 점수, 정통성 점수
- 인증 이력: 미쉐린, 블루리본, 방송 출연
- 사이드 메뉴: 추천 메뉴와 페어링 팁
- 방문 팁: 웨이팅, 주차, 특이사항""",
        inputSchema=GetRestaurantInput.model_json_schema(),
    ),
    
    Tool(
        name="get_lineage_info",
        description="""평양냉면 계보(파벌) 정보를 조회합니다.

4대 계보:
- wooraeok: 우래옥 계열 (진한 육향, 입문자 추천)
- uijeongbu: 의정부파 (고춧가루, 간간한 맛)
- jangchungdong: 장충동파 (가장 슴슴함, 매니아 선호)
- eulmildae: 을밀대식 (살얼음, 굵은 면)

'all' 입력 시 전체 계보 비교 정보 제공""",
        inputSchema=GetLineageInfoInput.model_json_schema(),
    ),
    
    Tool(
        name="recommend",
        description="""사용자 취향과 상황에 맞는 맛집을 추천합니다.

고려 요소:
- 경험 수준: 입문자는 진한 맛, 매니아는 슴슴한 맛
- 육수 선호: 진한 육향 / 맑고 담백 / 동치미 새큼
- 상황: 첫 경험, 데이트, 비즈니스, 혼밥, 해장
- 지역 및 웨이팅 허용 여부

추천 근거와 함께 2-3곳 제안""",
        inputSchema=RecommendInput.model_json_schema(),
    ),
    
    Tool(
        name="compare",
        description="""두 맛집을 매니아 관점에서 비교 분석합니다.

비교 항목:
- 계보와 역사적 배경
- 육수: 맑기, 깊이, 간, 육향
- 면: 메밀 함량, 굵기, 식감
- 가격 및 가성비
- 분위기 및 웨이팅

상황별 추천 (입문자 vs 매니아, 혼밥 vs 접대 등) 제공""",
        inputSchema=CompareInput.model_json_schema(),
    ),
    
    Tool(
        name="get_eating_guide",
        description="""평양냉면 제대로 즐기는 법을 안내합니다.

주제:
- basic: 기본 먹는 순서 (면수 → 육수 → 면)
- condiments: 식초/겨자 사용법과 논쟁
- ordering: 주문 용어 (거냉, 양마니, 사리 등)
- etiquette: 면 자르기, 숟가락 사용 등 예절
- seasonal: 계절별 즐기는 팁

특정 맛집 ID 입력 시 해당 맛집 특화 가이드 제공""",
        inputSchema=GetEatingGuideInput.model_json_schema(),
    ),
    
    Tool(
        name="get_side_pairings",
        description="""냉면과 어울리는 사이드 메뉴를 추천합니다.

추천 유형:
- 맛집별 시그니처 사이드 (을밀대 녹두전, 우래옥 불고기)
- 예산별 코스 구성
- 선육후면 / 어복쟁반 코스 안내
- 주류 페어링 (소주, 막걸리)

특정 맛집 ID 입력 시 해당 맛집 메뉴 기반 추천""",
        inputSchema=GetSidePairingsInput.model_json_schema(),
    ),
]


# ============================================================
# 도구 핸들러 등록 함수
# ============================================================

def register_tools(server: Server, data_provider):
    """MCP 서버에 도구 핸들러 등록"""
    
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return TOOLS
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        
        if name == "search_restaurants":
            params = SearchRestaurantsInput(**arguments)
            result = await data_provider.search_restaurants(params)
            return [TextContent(type="text", text=result)]
        
        elif name == "get_restaurant":
            params = GetRestaurantInput(**arguments)
            result = await data_provider.get_restaurant(params)
            return [TextContent(type="text", text=result)]
        
        elif name == "get_lineage_info":
            params = GetLineageInfoInput(**arguments)
            result = await data_provider.get_lineage_info(params)
            return [TextContent(type="text", text=result)]
        
        elif name == "recommend":
            params = RecommendInput(**arguments)
            result = await data_provider.recommend(params)
            return [TextContent(type="text", text=result)]
        
        elif name == "compare":
            params = CompareInput(**arguments)
            result = await data_provider.compare(params)
            return [TextContent(type="text", text=result)]
        
        elif name == "get_eating_guide":
            params = GetEatingGuideInput(**arguments)
            result = await data_provider.get_eating_guide(params)
            return [TextContent(type="text", text=result)]
        
        elif name == "get_side_pairings":
            params = GetSidePairingsInput(**arguments)
            result = await data_provider.get_side_pairings(params)
            return [TextContent(type="text", text=result)]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
