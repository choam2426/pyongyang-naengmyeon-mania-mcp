"""평양냉면 MCP 서버 엔트리포인트"""

import asyncio
import json
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server

from .tools.definitions import register_tools
from .models import Restaurant, SearchFilters, LineageInfo, EatingGuide


class DataProvider:
    """데이터 제공자 클래스"""
    
    def __init__(self, data_dir: Path | None = None):
        self.data_dir = data_dir or Path(__file__).parent / "data"
        self.restaurants: list[Restaurant] = []
        self.lineages: list[dict] = []
        self.eating_guides: list[dict] = []
        self.side_menus: dict = {}
        self._load_data()
    
    def _load_data(self):
        """JSON 데이터 로드"""
        # 레스토랑 데이터
        restaurants_file = self.data_dir / "restaurants.json"
        if restaurants_file.exists():
            with open(restaurants_file, encoding="utf-8") as f:
                data = json.load(f)
                self.restaurants = [
                    Restaurant(**r) for r in data.get("restaurants", [])
                ]
        
        # 계보 데이터
        lineages_file = self.data_dir / "lineages.json"
        if lineages_file.exists():
            with open(lineages_file, encoding="utf-8") as f:
                data = json.load(f)
                self.lineages = data.get("lineages", [])
        
        # 먹는 법 가이드
        guides_file = self.data_dir / "eating_guides.json"
        if guides_file.exists():
            with open(guides_file, encoding="utf-8") as f:
                data = json.load(f)
                self.eating_guides = data.get("eating_guides", [])
        
        # 사이드 메뉴
        side_file = self.data_dir / "side_menus.json"
        if side_file.exists():
            with open(side_file, encoding="utf-8") as f:
                self.side_menus = json.load(f)
    
    async def search_restaurants(self, params) -> str:
        """맛집 검색"""
        results = self.restaurants
        
        # 필터 적용
        if params.region:
            results = [r for r in results if r.region == params.region]
        
        if params.lineage:
            results = [r for r in results if r.lineage == params.lineage]
        
        if params.max_price:
            results = [r for r in results if r.naengmyeon_price <= params.max_price]
        
        if params.experience_level:
            results = [
                r for r in results 
                if params.experience_level in r.recommended_for
            ]
        
        if params.michelin_only:
            results = [
                r for r in results
                if any(c.type.value.startswith("michelin") for c in r.certifications)
            ]
        
        if params.has_slush_ice is not None:
            results = [r for r in results if r.broth.has_slush_ice == params.has_slush_ice]
        
        # tier 필터 추가
        if hasattr(params, 'tier') and params.tier is not None:
            results = [r for r in results if r.tier == params.tier]
        
        # rating_score로 정렬 (높은 순)
        results = sorted(results, key=lambda r: r.rating_score or 0, reverse=True)
        
        # 결과 포맷팅
        if not results:
            return "조건에 맞는 맛집을 찾지 못했습니다."
        
        output = f"## 검색 결과 ({len(results)}곳)\n\n"
        for r in results:
            tier_badge = "⭐" if r.tier == 1 else ""
            output += f"### {r.name} {tier_badge}\n"
            output += f"- 위치: {r.address}\n"
            output += f"- 계보: {r.lineage.value}\n"
            output += f"- 가격: {r.naengmyeon_price:,}원\n"
            if r.rating_score:
                output += f"- 평점: {r.rating_score}\n"
            if r.broth.description:
                desc = r.broth.description[:50]
                output += f"- 특징: {desc}{'...' if len(r.broth.description) > 50 else ''}\n"
            output += "\n"
        
        return output
    
    async def get_restaurant(self, params) -> str:
        """맛집 상세 조회"""
        restaurant = None
        
        if params.id:
            # id가 문자열로 올 수 있으므로 변환
            try:
                target_id = int(params.id)
            except ValueError:
                target_id = params.id
            restaurant = next((r for r in self.restaurants if r.id == target_id), None)
        elif params.name:
            restaurant = next(
                (r for r in self.restaurants if params.name in r.name), None
            )
        
        if not restaurant:
            return f"'{params.id or params.name}' 맛집을 찾을 수 없습니다."
        
        r = restaurant
        tier_badge = "⭐ Tier 1" if r.tier == 1 else "Tier 2"
        output = f"# {r.name} ({tier_badge})\n\n"
        
        output += f"## 기본 정보\n"
        output += f"- 주소: {r.address}\n"
        if r.address_detail:
            output += f"- 상세주소: {r.address_detail}\n"
        output += f"- 전화: {r.phone or '정보없음'}\n"
        output += f"- 영업시간: {r.hours_string or '정보없음'}\n"
        output += f"- 휴무: {r.closed_days_string or ', '.join(r.closed_days) or '정보없음'}\n"
        output += f"- 물냉면 가격: {r.naengmyeon_price:,}원\n"
        if r.accessibility:
            output += f"- 접근성: {r.accessibility}\n"
        if r.parking:
            output += f"- 주차: {r.parking}\n"
        if r.rating_score:
            output += f"- 평점: {r.rating_score}\n"
        output += "\n"
        
        output += f"## 계보와 역사\n"
        output += f"- 계보: {r.lineage.value}\n"
        if r.founded_year:
            output += f"- 창업: {r.founded_year}년\n"
        if r.generation:
            output += f"- 현재: {r.generation}대째 운영\n"
        if r.origin_story:
            output += f"- 유래: {r.origin_story}\n"
        if r.history and r.history.story:
            output += f"- 역사: {r.history.story}\n"
        output += "\n"
        
        output += f"## 맛 프로필\n"
        output += f"### 육수\n"
        if r.broth.description:
            output += f"{r.broth.description}\n"
        output += f"- 베이스: {r.broth.base.value}\n"
        output += f"- 맑기: {'★' * r.broth.clarity_level}{'☆' * (5 - r.broth.clarity_level)}\n"
        output += f"- 깊이: {'★' * r.broth.depth_level}{'☆' * (5 - r.broth.depth_level)}\n"
        output += f"- 육향: {'★' * r.broth.beef_aroma_level}{'☆' * (5 - r.broth.beef_aroma_level)}\n"
        output += f"- 간: {'★' * r.broth.saltiness_level}{'☆' * (5 - r.broth.saltiness_level)} ({r.broth.saltiness or '보통'})\n"
        output += f"- 살얼음: {'있음' if r.broth.has_slush_ice else '없음'}\n"
        if r.broth.dongchimi:
            output += f"- 동치미: 사용\n"
        output += "\n"
        
        output += f"### 면\n"
        if r.noodle.description:
            output += f"{r.noodle.description}\n"
        output += f"- 스타일: {r.noodle.style.value}\n"
        output += f"- 메밀 함량: {r.noodle.buckwheat_ratio}%\n"
        output += f"- 굵기: {r.noodle.thickness.value}\n"
        if r.noodle.texture_keywords:
            output += f"- 식감: {', '.join(r.noodle.texture_keywords)}\n"
        if r.noodle.homemade:
            output += f"- 자가제면: 예\n"
        output += "\n"
        
        output += f"## 매니아 평가\n"
        output += f"정통성 점수: {r.expert_rating.authenticity_score}/100\n"
        if r.expert_rating.reviewer_note:
            output += f"> {r.expert_rating.reviewer_note}\n"
        output += "\n"
        
        if r.certifications:
            output += f"## 인증/수상\n"
            for cert in r.certifications:
                output += f"- {cert.year}년 {cert.type.value}: {cert.detail or ''}\n"
            output += "\n"
        
        if r.side_menus:
            output += f"## 사이드 메뉴\n"
            for menu in r.side_menus:
                sig = "⭐" if menu.is_signature else ""
                output += f"- {menu.name} {sig}: {menu.price:,}원\n"
                if menu.pairing_note:
                    output += f"  └ {menu.pairing_note}\n"
            output += "\n"
        
        if r.features:
            output += f"## 특징\n"
            for f in r.features:
                output += f"- {f}\n"
            output += "\n"
        
        if r.special_notes:
            output += f"## 방문 팁\n"
            for note in r.special_notes:
                output += f"- {note}\n"
        
        return output
    
    async def get_lineage_info(self, params) -> str:
        """계보 정보 조회"""
        if not self.lineages:
            return "계보 데이터가 로드되지 않았습니다."
        
        lineage_id = params.lineage.lower() if isinstance(params.lineage, str) else params.lineage
        
        # 전체 조회
        if lineage_id == "all":
            output = "# 평양냉면 계보 총정리\n\n"
            for lin in self.lineages:
                output += f"## {lin['name']}\n"
                output += f"{lin.get('philosophy_of_taste', '')[:100]}...\n"
                output += f"- 대표 맛집: {', '.join(lin.get('representative_restaurants', [])[:3])}\n"
                output += f"- 적합: {lin.get('suitability', '')[:50]}...\n\n"
            return output
        
        # 계보명 매핑
        lineage_map = {
            "wooraeok": "우래옥",
            "uijeongbu": "의정부파",
            "jangchungdong": "장충동파",
            "eulmildae": "을밀대",
            "okryugwan": "옥류관"
        }
        
        search_name = lineage_map.get(lineage_id, lineage_id)
        
        # 검색
        lineage = None
        for lin in self.lineages:
            if search_name in lin.get("name", "") or lineage_id in lin.get("name", "").lower():
                lineage = lin
                break
        
        if not lineage:
            return f"'{lineage_id}' 계보 정보를 찾을 수 없습니다.\n\n사용 가능한 계보: wooraeok, uijeongbu, jangchungdong, eulmildae, okryugwan, all"
        
        output = f"# {lineage['name']}\n\n"
        output += f"## 역사\n{lineage.get('origin_history', '')}\n\n"
        output += f"## 맛 철학\n{lineage.get('philosophy_of_taste', '')}\n\n"
        output += f"## 특징\n{lineage.get('distinctive_features', '')}\n\n"
        output += f"## 대표 맛집\n"
        for rest in lineage.get("representative_restaurants", []):
            output += f"- {rest}\n"
        output += f"\n## 누구에게 추천?\n{lineage.get('suitability', '')}\n"
        
        if lineage.get("internal_branches"):
            output += f"\n## 연혁\n"
            for branch in lineage.get("internal_branches", []):
                output += f"- {branch.get('year', '')}년: {branch.get('event', '')}\n"
        
        return output
    
    async def recommend(self, params) -> str:
        """맛집 추천"""
        results = self.restaurants
        
        # 경험 수준 필터
        results = [
            r for r in results 
            if params.experience_level in r.recommended_for
        ]
        
        # 육수 선호도 필터
        if params.broth_preference.value == "rich_beefy":
            results = [r for r in results if r.broth.beef_aroma_level >= 4]
        elif params.broth_preference.value == "light_clean":
            results = [r for r in results if r.broth.saltiness_level <= 2]
        elif params.broth_preference.value == "dongchimi_sour":
            results = [r for r in results if r.broth.dongchimi]
        
        # 지역 필터
        if params.region:
            results = [r for r in results if r.region == params.region]
        
        # 웨이팅 회피
        if params.avoid_long_wait:
            results = [r for r in results if (r.average_wait_minutes or 0) <= 20]
        
        # tier와 rating_score로 정렬
        results = sorted(results, key=lambda r: (r.tier, -(r.rating_score or 0)))
        
        if not results:
            return "조건에 맞는 추천 맛집을 찾지 못했습니다."
        
        output = f"## {params.experience_level.value} 맞춤 추천\n\n"
        for r in results[:3]:
            tier_badge = "⭐" if r.tier == 1 else ""
            output += f"### {r.name} {tier_badge}\n"
            output += f"- 계보: {r.lineage.value}\n"
            output += f"- 가격: {r.naengmyeon_price:,}원\n"
            if r.expert_rating.reviewer_note:
                output += f"> {r.expert_rating.reviewer_note}\n"
            output += "\n"
        
        return output
    
    async def compare(self, params) -> str:
        """맛집 비교"""
        # 맛집 찾기
        def find_restaurant(query: str) -> Restaurant | None:
            # ID로 검색
            try:
                target_id = int(query)
                return next((r for r in self.restaurants if r.id == target_id), None)
            except ValueError:
                pass
            # 이름으로 검색
            return next((r for r in self.restaurants if query in r.name), None)
        
        r1 = find_restaurant(params.restaurant1)
        r2 = find_restaurant(params.restaurant2)
        
        if not r1:
            return f"'{params.restaurant1}' 맛집을 찾을 수 없습니다."
        if not r2:
            return f"'{params.restaurant2}' 맛집을 찾을 수 없습니다."
        
        output = f"# {r1.name} vs {r2.name} 비교\n\n"
        
        # 기본 정보
        output += "## 기본 정보\n"
        output += f"| 항목 | {r1.name} | {r2.name} |\n"
        output += "|------|--------|--------|\n"
        output += f"| 등급 | Tier {r1.tier} | Tier {r2.tier} |\n"
        output += f"| 계보 | {r1.lineage.value} | {r2.lineage.value} |\n"
        output += f"| 가격 | {r1.naengmyeon_price:,}원 | {r2.naengmyeon_price:,}원 |\n"
        output += f"| 창업 | {r1.founded_year or '정보없음'}년 | {r2.founded_year or '정보없음'}년 |\n"
        output += f"| 평점 | {r1.rating_score or '-'} | {r2.rating_score or '-'} |\n\n"
        
        # 육수 비교
        output += "## 육수 비교\n"
        output += f"| 항목 | {r1.name} | {r2.name} |\n"
        output += "|------|--------|--------|\n"
        output += f"| 베이스 | {r1.broth.base.value} | {r2.broth.base.value} |\n"
        output += f"| 맑기 | {'★' * r1.broth.clarity_level} | {'★' * r2.broth.clarity_level} |\n"
        output += f"| 깊이 | {'★' * r1.broth.depth_level} | {'★' * r2.broth.depth_level} |\n"
        output += f"| 육향 | {'★' * r1.broth.beef_aroma_level} | {'★' * r2.broth.beef_aroma_level} |\n"
        output += f"| 간 | {'★' * r1.broth.saltiness_level} | {'★' * r2.broth.saltiness_level} |\n"
        output += f"| 살얼음 | {'O' if r1.broth.has_slush_ice else 'X'} | {'O' if r2.broth.has_slush_ice else 'X'} |\n\n"
        
        # 면 비교
        output += "## 면 비교\n"
        output += f"| 항목 | {r1.name} | {r2.name} |\n"
        output += "|------|--------|--------|\n"
        output += f"| 스타일 | {r1.noodle.style.value} | {r2.noodle.style.value} |\n"
        output += f"| 메밀 함량 | {r1.noodle.buckwheat_ratio}% | {r2.noodle.buckwheat_ratio}% |\n"
        output += f"| 굵기 | {r1.noodle.thickness.value} | {r2.noodle.thickness.value} |\n\n"
        
        # 평가 비교
        output += "## 매니아 평가\n"
        output += f"| 항목 | {r1.name} | {r2.name} |\n"
        output += "|------|--------|--------|\n"
        output += f"| 정통성 점수 | {r1.expert_rating.authenticity_score}/100 | {r2.expert_rating.authenticity_score}/100 |\n"
        output += f"| 전체 밸런스 | {'★' * r1.expert_rating.overall_balance} | {'★' * r2.expert_rating.overall_balance} |\n\n"
        
        # 추천
        output += "## 상황별 추천\n"
        # 입문자
        beginner_scores = [
            (r1, r1.broth.beef_aroma_level + (5 - r1.broth.saltiness_level)),
            (r2, r2.broth.beef_aroma_level + (5 - r2.broth.saltiness_level))
        ]
        beginner_pick = max(beginner_scores, key=lambda x: x[1])[0]
        output += f"- **입문자**: {beginner_pick.name} (육향이 진하고 친숙한 맛)\n"
        
        # 매니아
        mania_scores = [
            (r1, r1.expert_rating.authenticity_score),
            (r2, r2.expert_rating.authenticity_score)
        ]
        mania_pick = max(mania_scores, key=lambda x: x[1])[0]
        output += f"- **매니아**: {mania_pick.name} (정통성 점수 높음)\n"
        
        # 가성비
        value_scores = [
            (r1, r1.expert_rating.overall_balance * 10000 / r1.naengmyeon_price if r1.naengmyeon_price else 0),
            (r2, r2.expert_rating.overall_balance * 10000 / r2.naengmyeon_price if r2.naengmyeon_price else 0)
        ]
        value_pick = max(value_scores, key=lambda x: x[1])[0]
        output += f"- **가성비**: {value_pick.name}\n"
        
        return output
    
    async def get_eating_guide(self, params) -> str:
        """먹는 법 가이드"""
        if not self.eating_guides:
            return "먹는 법 가이드 데이터가 로드되지 않았습니다."
        
        topic = params.topic or "basic"
        
        # 특정 맛집용 가이드
        restaurant_note = ""
        if params.restaurant_id:
            try:
                target_id = int(params.restaurant_id)
            except ValueError:
                target_id = params.restaurant_id
            restaurant = next((r for r in self.restaurants if r.id == target_id or params.restaurant_id in r.name), None)
            if restaurant:
                restaurant_note = f"\n\n## {restaurant.name} 특화 팁\n"
                if restaurant.special_notes:
                    for note in restaurant.special_notes:
                        restaurant_note += f"- {note}\n"
                if restaurant.broth.characteristics:
                    restaurant_note += f"- 육수 특징: {restaurant.broth.characteristics}\n"
        
        # 주제별 가이드 찾기
        guide = next((g for g in self.eating_guides if g.get("topic") == topic), None)
        
        if not guide:
            available = ", ".join(g.get("topic", "") for g in self.eating_guides)
            return f"'{topic}' 주제를 찾을 수 없습니다.\n\n사용 가능한 주제: {available}"
        
        output = f"# {guide['title']}\n\n"
        if guide.get("description"):
            output += f"{guide['description']}\n\n"
        
        output += "## 단계별 가이드\n"
        for i, step in enumerate(guide.get("steps", []), 1):
            output += f"{i}. {step}\n"
        output += "\n"
        
        output += "## 팁\n"
        for tip in guide.get("tips", []):
            output += f"- {tip}\n"
        output += "\n"
        
        output += "## 흔한 실수\n"
        for mistake in guide.get("common_mistakes", []):
            output += f"- ❌ {mistake}\n"
        
        if guide.get("expert_opinions"):
            output += "\n## 전문가 의견\n"
            for opinion in guide.get("expert_opinions", []):
                output += f"> {opinion}\n\n"
        
        if guide.get("restaurant_notes"):
            output += "\n## 맛집별 참고사항\n"
            for note in guide.get("restaurant_notes", []):
                output += f"- {note}\n"
        
        output += restaurant_note
        
        return output
    
    async def get_side_pairings(self, params) -> str:
        """사이드 메뉴 추천"""
        if not self.side_menus:
            return "사이드 메뉴 데이터가 로드되지 않았습니다."
        
        output = ""
        
        # 특정 맛집의 사이드 메뉴
        if params.restaurant_id:
            try:
                target_id = int(params.restaurant_id)
            except ValueError:
                target_id = params.restaurant_id
            restaurant = next((r for r in self.restaurants if r.id == target_id or params.restaurant_id in r.name), None)
            
            if restaurant and restaurant.side_menus:
                output += f"# {restaurant.name} 사이드 메뉴\n\n"
                for menu in restaurant.side_menus:
                    sig = "⭐ 시그니처" if menu.is_signature else ""
                    output += f"### {menu.name} {sig}\n"
                    output += f"- 가격: {menu.price:,}원\n"
                    if menu.pairing_note:
                        output += f"- 페어링 팁: {menu.pairing_note}\n"
                    output += "\n"
                return output
        
        # 일반 사이드 메뉴 가이드
        output += "# 평양냉면 사이드 메뉴 가이드\n\n"
        
        side_dishes = self.side_menus.get("side_dishes", [])
        for dish in side_dishes:
            output += f"## {dish['name']}\n"
            output += f"{dish['description']}\n\n"
            output += f"- 가격대: {dish['price_range']}\n"
            output += f"- 양: {dish['portion_size']}\n"
            output += f"- 페어링: {dish['pairing_notes']}\n"
            if dish.get("best_restaurants"):
                output += f"- 추천 맛집: {', '.join(dish['best_restaurants'])}\n"
            output += f"- 추천 상황: {dish['recommended_situations']}\n\n"
        
        # 예산에 맞는 코스 추천
        if params.budget:
            output += f"\n## 예산 {params.budget:,}원 추천 코스\n"
            courses = self.side_menus.get("course_examples", [])
            for course in courses:
                # 예산 파싱 (간단히)
                budget_str = course.get("budget", "")
                try:
                    max_budget = int("".join(filter(str.isdigit, budget_str.split("~")[-1])))
                except (ValueError, IndexError):
                    max_budget = 100000
                
                if max_budget <= params.budget:
                    output += f"\n### {course['name']}\n"
                    output += f"- 예산: {course['budget']}\n"
                    output += f"- 구성: {', '.join(course['dishes'])}\n"
                    output += f"- 순서: {course['serving_order']}\n"
                    output += f"- 팁: {course['tips']}\n"
        
        # 주류 포함 추천
        if params.include_alcohol:
            output += "\n## 술과 함께하는 페어링\n"
            output += "- 막걸리: 녹두전과 함께 전통 조합\n"
            output += "- 소주: 편육, 제육과 함께 선주후면 스타일\n"
            output += "- 문배주: 고급 접대 자리에서 어복쟁반과 함께\n"
        
        return output


def create_server() -> Server:
    """MCP 서버 생성"""
    server = Server("pyongyang-naengmyeon")
    data_provider = DataProvider()
    register_tools(server, data_provider)
    return server


async def main():
    """서버 실행"""
    server = create_server()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
