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

def get_recommendations_for_keywords(keywords: list, tag_to_urls: dict = None, max_per_keyword: int = 2, used_urls: set = None) -> list:
    """
    키워드를 기반으로 추천 콘텐츠 링크를 생성합니다.
    (사용자의 실제 좋아요 데이터 기반 URL만 제공하며, 중복된 URL은 차단합니다.)
    """
    if used_urls is None:
        used_urls = set()
        
    all_recommendations = []
    
    if not keywords:
        return []
        
    import random
    
    for kw in keywords:
        safe_kw = kw.replace(" ", "")
        
        # 1. 실제 사용자가 반응했던 포스트 URL이 있다면 무작위로 추출
        if tag_to_urls and kw.lower() in tag_to_urls and tag_to_urls[kw.lower()]:
            urls = list(tag_to_urls[kw.lower()])
            random.shuffle(urls)
            
            added_count = 0
            for url in urls:
                if url not in used_urls:
                    used_urls.add(url)
                    all_recommendations.append({
                        "title": f"#{safe_kw} 관련 내 취향 게시물",
                        "url": url,
                        "snippet": f"과거에 반응을 남겼던 #{safe_kw} 태그의 게시물입니다.",
                        "matched_keyword": kw
                    })
                    added_count += 1
                    if added_count >= max_per_keyword:
                        break
                        
    return all_recommendations
