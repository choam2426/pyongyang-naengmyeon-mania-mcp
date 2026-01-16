"""평양냉면 MCP 서버 데이터 스키마"""

from typing import Optional, Union
from pydantic import BaseModel, Field

from .enums import (
    Lineage, BrothBase, NoodleStyle, NoodleThickness,
    ExperienceLevel, Region, CertificationType, Season
)


# ============================================================
# 프로필 스키마
# ============================================================

class Hours(BaseModel):
    """영업시간"""
    weekday: Optional[str] = None
    weekend: Optional[str] = None


class History(BaseModel):
    """역사/유래"""
    founded_year: Optional[int] = None
    founder: Optional[str] = None
    origin: Optional[str] = None
    lineage: Optional[str] = None
    story: Optional[str] = None


class Menu(BaseModel):
    """메뉴 정보"""
    signature: Optional[str] = None
    naengmyeon_price: int = Field(description="물냉면 가격 (원)")
    bibim_naengmyeon: bool = Field(default=False)
    onmyeon: bool = Field(default=False)
    mandu: bool = Field(default=False)
    pyeonyuk: bool = Field(default=False)
    other_menus: list[str] = Field(default_factory=list)


class BrothProfile(BaseModel):
    """육수 프로필"""
    base: BrothBase = Field(description="육수 베이스 타입")
    clarity_level: int = Field(ge=1, le=5, description="맑기 (5=매우 맑음)")
    depth_level: int = Field(ge=1, le=5, description="깊이/감칠맛")
    saltiness_level: int = Field(ge=1, le=5, description="간 (1=슴슴, 5=간간)")
    beef_aroma_level: int = Field(ge=1, le=5, description="육향 강도")
    has_slush_ice: bool = Field(default=False, description="살얼음 여부")
    uses_soy_sauce: bool = Field(default=False, description="간장 사용 여부 (정통은 소금만)")
    description: str = Field(default="", description="매니아 코멘트")
    # 추가 필드
    dongchimi: bool = Field(default=False, description="동치미 사용 여부")
    characteristics: Optional[str] = Field(default=None, description="육수 특징")
    taste_profile: Optional[str] = Field(default=None, description="맛 프로필")
    saltiness: Optional[str] = Field(default=None, description="간 정도 설명")


class NoodleProfile(BaseModel):
    """면 프로필"""
    style: NoodleStyle = Field(description="면 스타일")
    buckwheat_ratio: int = Field(ge=0, le=100, description="메밀 함량 (%)")
    thickness: NoodleThickness = Field(description="면 굵기")
    texture_keywords: list[str] = Field(default_factory=list, description="식감 키워드")
    description: str = Field(default="", description="매니아 코멘트")
    # 추가 필드
    homemade: bool = Field(default=False, description="자가제면 여부")
    texture: Optional[str] = Field(default=None, description="식감 설명")


class ToppingsProfile(BaseModel):
    """고명 구성"""
    has_pyeonyuk: bool = Field(default=True, description="편육")
    has_egg: bool = Field(default=True, description="달걀")
    has_cucumber: bool = Field(default=True, description="오이")
    has_pear: bool = Field(default=False, description="배")
    has_dongchimi_mu: bool = Field(default=False, description="동치미 무")
    has_red_pepper_powder: bool = Field(default=False, description="고춧가루 (의정부파 특징)")
    extras: list[str] = Field(default_factory=list, description="기타: ['잣', '실고추']")


class ExpertRating(BaseModel):
    """매니아 평가"""
    broth_clarity: int = Field(ge=1, le=5, description="육수 맑기")
    broth_depth: int = Field(ge=1, le=5, description="육수 깊이")
    noodle_aroma: int = Field(ge=1, le=5, description="면 메밀향")
    noodle_texture: int = Field(ge=1, le=5, description="면 식감")
    temperature: int = Field(ge=1, le=5, description="온도 적절성")
    overall_balance: int = Field(ge=1, le=5, description="전체 밸런스")
    authenticity_score: int = Field(ge=0, le=100, description="정통성 점수")
    reviewer_note: str = Field(default="", description="매니아 코멘트")


# ============================================================
# 인증 및 메뉴 스키마
# ============================================================

class Certification(BaseModel):
    """인증/수상 이력"""
    type: CertificationType
    year: int
    detail: Optional[str] = Field(default=None, description="'빕구르망 6년 연속' 등")


class SideMenu(BaseModel):
    """사이드 메뉴"""
    name: str = Field(description="메뉴명: '편육', '녹두전'")
    price: int = Field(description="가격 (원)")
    is_signature: bool = Field(default=False, description="시그니처 여부")
    pairing_note: Optional[str] = Field(default=None, description="페어링 팁")


# ============================================================
# 메인 엔티티
# ============================================================

class Restaurant(BaseModel):
    """맛집 메인 엔티티"""
    id: int = Field(description="고유 ID")
    slug: Optional[str] = Field(default=None, description="URL용 슬러그")
    tier: int = Field(default=2, ge=1, le=3, description="등급 (1=최상위, 2=우수)")
    name: str = Field(description="맛집명")
    name_hanja: Optional[str] = Field(default=None, description="한자명")
    name_english: Optional[str] = Field(default=None, description="영문명")
    
    # 기본 정보
    region: Region
    region_code: Optional[str] = Field(default=None)
    address: str
    address_detail: Optional[str] = Field(default=None, description="상세주소")
    phone: Optional[str] = None
    hours: Optional[Hours] = Field(default=None, description="영업시간")
    hours_string: Optional[str] = Field(default=None, description="영업시간 문자열")
    closed_days: list[str] = Field(default_factory=list, description="휴무일")
    closed_days_string: Optional[str] = Field(default=None, description="휴무일 문자열")
    
    # 역사
    history: Optional[History] = Field(default=None, description="역사/유래")
    
    # 계보와 역사 (레거시 호환)
    lineage: Lineage
    generation: Optional[int] = Field(default=None, description="몇 대째 운영")
    origin_story: Optional[str] = Field(default=None, description="유래")
    
    # 메뉴 및 가격
    menu: Optional[Menu] = Field(default=None, description="메뉴 정보")
    price_range: Optional[str] = Field(default=None, description="가격대")
    
    # 맛 프로필
    broth: BrothProfile
    noodle: NoodleProfile
    toppings: ToppingsProfile
    
    # 평가
    expert_rating: ExpertRating
    certifications: list[Certification] = Field(default_factory=list)
    awards: list[str] = Field(default_factory=list, description="수상 이력")
    rating_score: Optional[float] = Field(default=None, description="평점")
    
    # 메뉴
    side_menus: list[SideMenu] = Field(default_factory=list)
    
    # 편의시설
    features: list[str] = Field(default_factory=list, description="특징")
    parking: Optional[str] = Field(default=None, description="주차 정보")
    parking_available: Optional[bool] = Field(default=False)
    reservation: Optional[bool] = Field(default=None, description="예약 가능 여부")
    reservation_available: Optional[bool] = Field(default=False)
    accessibility: Optional[str] = Field(default=None, description="접근성 정보")
    
    # 메타 정보
    recommended_for: list[ExperienceLevel] = Field(default_factory=list)
    best_season: Optional[Season] = Field(default=Season.ALL)
    average_wait_minutes: Optional[int] = Field(default=None, description="평균 대기 시간 (분)")
    
    # 특이사항
    special_notes: list[str] = Field(default_factory=list, description="['숟가락 미제공'] 등")
    famous_visitors: list[str] = Field(default_factory=list, description="['BTS RM'] 등")
    
    # 검색용
    tags: list[str] = Field(default_factory=list)
    order_options: Optional[str] = Field(default=None)
    
    @property
    def naengmyeon_price(self) -> int:
        """물냉면 가격 (menu에서 추출)"""
        if self.menu:
            return self.menu.naengmyeon_price
        return 0
    
    @property
    def founded_year(self) -> Optional[int]:
        """창업년도 (history에서 추출)"""
        if self.history:
            return self.history.founded_year
        return None
    
    @property
    def founder(self) -> Optional[str]:
        """창업자 (history에서 추출)"""
        if self.history:
            return self.history.founder
        return None


class LineageInfo(BaseModel):
    """계보 정보"""
    name: str = Field(description="계보 이름")
    origin_history: str = Field(description="계보 역사")
    philosophy_of_taste: str = Field(description="맛 철학")
    distinctive_features: str = Field(description="차별화 포인트")
    representative_restaurants: list[str] = Field(description="대표 맛집 목록")
    suitability: str = Field(description="적합 대상")
    internal_branches: list[dict] = Field(default_factory=list, description="분파 연혁")


class EatingGuide(BaseModel):
    """먹는 법 가이드"""
    topic: str = Field(description="주제: basic, condiments, ordering, etiquette, seasonal")
    title: str
    description: Optional[str] = Field(default=None)
    steps: list[str] = Field(description="단계별 가이드")
    tips: list[str] = Field(description="팁")
    common_mistakes: list[str] = Field(description="흔한 실수")
    expert_opinions: list[str] = Field(default_factory=list, description="전문가 의견")
    restaurant_notes: list[str] = Field(default_factory=list, description="맛집별 참고사항")


# ============================================================
# 검색/추천 스키마
# ============================================================

class SearchFilters(BaseModel):
    """검색 필터"""
    region: Optional[Region] = None
    lineage: Optional[Lineage] = None
    max_price: Optional[int] = None
    experience_level: Optional[ExperienceLevel] = None
    michelin_only: bool = False
    has_slush_ice: Optional[bool] = None
    tier: Optional[int] = Field(default=None, description="등급 필터 (1=최상위)")
    query: Optional[str] = Field(default=None, description="자연어 검색")


class TastePreference(BaseModel):
    """취향 프로필 (추천용)"""
    broth_preference: str = Field(description="육수 선호")
    noodle_preference: Optional[str] = Field(default=None, description="면 선호")
    experience_level: ExperienceLevel
    situation: Optional[str] = None
    avoid_long_wait: bool = False
    region: Optional[Region] = None


class ComparisonResult(BaseModel):
    """비교 결과"""
    restaurant1: Restaurant
    restaurant2: Restaurant
    differences: list[dict] = Field(description="카테고리별 차이점")
    recommendation: dict = Field(description="상황별 추천")


class SearchResult(BaseModel):
    """검색 결과"""
    restaurants: list[Restaurant]
    total_count: int
    filters_applied: SearchFilters
