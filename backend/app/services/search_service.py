from duckduckgo_search import DDGS
import time

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
