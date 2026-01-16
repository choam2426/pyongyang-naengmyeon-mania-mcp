"""평양냉면 MCP 서버 열거형 정의"""

from enum import Enum


class Lineage(str, Enum):
    """평양냉면 4대 계보 + α"""
    WOORAEOK = "wooraeok"           # 우래옥 계열: 진한 육향
    UIJEONGBU = "uijeongbu"         # 의정부파: 고춧가루, 간간한 맛
    JANGCHUNGDONG = "jangchungdong" # 장충동파: 가장 슴슴함
    EULMILDAE = "eulmildae"         # 을밀대식: 살얼음, 굵은 면
    OKRYUGWAN = "okryugwan"         # 북한 옥류관식
    INDEPENDENT = "independent"     # 독자 노선


class BrothBase(str, Enum):
    """육수 베이스 타입"""
    BEEF_ONLY = "beef_only"             # 순수 소고기 (우래옥식)
    BEEF_CHICKEN = "beef_chicken"       # 소고기 + 닭
    BEEF_DONGCHIMI = "beef_dongchimi"   # 소고기 + 동치미
    DONGCHIMI_MAIN = "dongchimi_main"   # 동치미 중심
    MIXED = "mixed"                     # 혼합 (꿩, 돼지 등 포함)


class NoodleStyle(str, Enum):
    """면 스타일"""
    THIN_CHEWY = "thin_chewy"           # 가늘고 쫄깃 (의정부식)
    THIN_CRUMBLY = "thin_crumbly"       # 가늘고 툭툭 끊김
    THICK_CHEWY = "thick_chewy"         # 굵고 꼬들 (을밀대식)
    MEDIUM_BALANCED = "medium_balanced" # 중간 굵기


class NoodleThickness(str, Enum):
    """면 굵기"""
    THIN = "thin"
    MEDIUM = "medium"
    THICK = "thick"


class ExperienceLevel(str, Enum):
    """경험 수준"""
    BEGINNER = "beginner"         # 입문자
    INTERMEDIATE = "intermediate" # 중급
    EXPERT = "expert"             # 매니아


class Region(str, Enum):
    """지역 구분"""
    JONGNO_EULJIRO = "jongno_euljiro"   # 종로/을지로/중구
    GANGNAM_SEOCHO = "gangnam_seocho"   # 강남/서초
    MAPO_YEOUIDO = "mapo_yeouido"       # 마포/여의도
    SONGPA_JAMSIL = "songpa_jamsil"     # 송파/잠실
    GYEONGGI_NORTH = "gyeonggi_north"   # 경기 북부 (의정부 등)
    GYEONGGI_SOUTH = "gyeonggi_south"   # 경기 남부 (판교, 분당 등)


class CertificationType(str, Enum):
    """인증/수상 타입"""
    MICHELIN_BIB = "michelin_bib"       # 미쉐린 빕구르망
    MICHELIN_STAR = "michelin_star"     # 미쉐린 스타
    MICHELIN_GUIDE = "michelin_guide"   # 미쉐린 가이드 등재
    MICHELIN_PLATE = "미쉐린 Plate"     # 미쉐린 플레이트
    BLUE_RIBBON = "blue_ribbon"         # 블루리본
    BROADCAST = "broadcast"             # 방송 출연


class BrothPreference(str, Enum):
    """육수 선호도 (추천용)"""
    RICH_BEEFY = "rich_beefy"           # 진한 육향
    LIGHT_CLEAN = "light_clean"         # 맑고 슴슴
    DONGCHIMI_SOUR = "dongchimi_sour"   # 동치미 새큼
    NO_PREFERENCE = "no_preference"


class VisitSituation(str, Enum):
    """방문 상황 (추천용)"""
    FIRST_TIMER = "first_timer"     # 첫 경험
    DATE = "date"                   # 데이트
    BUSINESS = "business"           # 비즈니스/접대
    SOLO = "solo"                   # 혼밥
    WITH_MANIA = "with_mania"       # 매니아와 함께
    HANGOVER = "hangover"           # 해장


class Season(str, Enum):
    """계절"""
    SUMMER = "summer"
    WINTER = "winter"
    ALL = "all"
