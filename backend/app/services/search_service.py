from ddgs import DDGS
import time
import requests

def is_valid_instagram_url(url: str) -> bool:
    """
    HTTP HEAD/GET 요청을 보내 인스타그램 계정/게시물이 비공개이거나 삭제되었는지(로그인 리다이렉트/404) 확인합니다.
    """
    try:
        # User-Agent를 짧고 간결하게 설정 (긴 문자열은 봇 차단에 걸릴 확률이 높음)
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        # 인스타그램은 HEAD 요청에 대해 405 Method Not Allowed를 반환하는 경우가 있으므로 GET을 사용하되 타임아웃을 짧게 둡니다.
        # Vercel 환경에서 timeout 방지를 위해 최대 1.5초로 제한
        response = requests.get(url, headers=headers, timeout=1.5, allow_redirects=True)
        
        # 404면 삭제됨
        if response.status_code == 404:
            return False
            
        if "/accounts/login/" in response.url:
            return False
            
        import re
        match = re.search(r'<title>(.*?)</title>', response.text)
        if match and match.group(1).strip() == "Instagram":
            # 정상 페이지는 "이름(@아이디) • Instagram..." 형식의 타이틀을 가짐
            # 타이틀이 정확히 "Instagram" 뿐이라면 404 혹은 비공개 계정 화면임
            return False
            
        return True
    except Exception as e:
        # 타임아웃 등 에러가 나면 일단 안전하게 제외
        print(f"URL validation error for {url}: {e}")
        return False

def get_recommendations_for_keywords(keywords: list, max_per_keyword: int = 2) -> list:
    """
    키워드를 기반으로 인스타그램 해시태그 검색 링크를 생성하여 반환합니다.
    (Vercel 서버리스 환경에서 C-Extension 충돌 및 타임아웃을 방지하기 위해 크롤링 대신 직접 링크 생성)
    """
    all_recommendations = []
    
    if not keywords:
        return []
        
    for kw in keywords:
        # 안전한 키워드로 해시태그 생성
        safe_kw = kw.replace(" ", "")
        
        all_recommendations.append({
            "title": f"#{safe_kw} 관련 인기 게시물 둘러보기",
            "url": f"https://www.instagram.com/explore/tags/{safe_kw}/",
            "snippet": f"인스타그램에서 #{safe_kw} 태그가 포함된 최신 트렌드와 릴스를 확인해보세요.",
            "matched_keyword": kw
        })
                
    return all_recommendations
