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
        response = requests.get(url, headers=headers, timeout=3, allow_redirects=True)
        
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

def search_instagram(query: str, max_results: int = 3) -> list:
    """
    DuckDuckGo 검색을 이용해 site:instagram.com {query} 형태로
    인스타그램 게시물 링크와 제목을 스크래핑하는 함수.
    """
    if not query:
        return []
        
    search_query = f"site:instagram.com {query}"
    results = []
    
    try:
        ddgs = DDGS()
        # DDGS.text() returns a generator
        for r in ddgs.text(search_query, max_results=max_results):
            url = r.get("href", "")
            title = r.get("title", "")
            body = r.get("body", "")
            
            # 인스타그램 프로필이나 게시물 링크만 필터링 (가끔 이상한 링크가 섞일 수 있음)
            if "instagram.com" in url:
                # 비공개/삭제 계정 필터링
                if is_valid_instagram_url(url):
                    results.append({
                        "title": title.replace(" - Instagram", "").strip(),
                        "url": url,
                        "snippet": body[:100] + "..." if len(body) > 100 else body
                    })
        
        # DDG API 레이트 리밋(Too Many Requests) 방지를 위한 짧은 딜레이
        time.sleep(1)
        return results
    except Exception as e:
        print(f"Error searching DuckDuckGo for {search_query}: {e}")
        return []

def get_recommendations_for_keywords(keywords: list, max_per_keyword: int = 2) -> list:
    """
    주어진 키워드 리스트에 대해 각각 검색을 수행하고 결과를 병합하여 리턴.
    """
    all_recommendations = []
    seen_urls = set()
    
    for kw in keywords:
        search_res = search_instagram(kw, max_results=max_per_keyword)
        for res in search_res:
            if res["url"] not in seen_urls:
                seen_urls.add(res["url"])
                # 태그 정보 추가
                res["matched_keyword"] = kw
                all_recommendations.append(res)
                
    return all_recommendations
