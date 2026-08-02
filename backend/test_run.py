import os
from app.services.parser import InstaParser
from app.services.keyword_extractor import extract_taste_keywords
from app.services.search_service import get_recommendations_for_keywords
import time
import sys
import io

# Force UTF-8 stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_full_dataset():
    base_dir = r"c:\Users\jjaew\OneDrive\바탕 화면\2026 2학기 부트캠프 스터디\7-8월 토이프로젝트(인스타 알고리즘 분석)\instagram-lex_xelop-서브데이터(7.28.2026 기준)"
    print(f"Testing with Dataset: {base_dir}")

    start_time = time.time()
    
    parser = InstaParser(base_dir)
    print("Parser initialized.")
    
    keywords_result = extract_taste_keywords(parser)
    
    print("\n--- Keyword Extraction Results ---")
    print(f"Total Tags Found: {keywords_result['total_tags_found']}")
    print(f"Top SFW Search Queries: {keywords_result['search_sfw_queries']}")
    print(f"Top NSFW Search Queries: {keywords_result['search_nsfw_queries']}")
    
    print("\n--- Fetching Recommendations (DuckDuckGo) ---")
    sfw_recs = get_recommendations_for_keywords(keywords_result['search_sfw_queries'][:2], max_per_keyword=2)
    nsfw_recs = get_recommendations_for_keywords(keywords_result['search_nsfw_queries'][:2], max_per_keyword=2)
    
    print("\n[SFW Recommendations]:")
    for r in sfw_recs:
        print(f"  - [{r['matched_keyword']}] {r['title']} ({r['url']})")
        
    print("\n[NSFW Recommendations]:")
    for r in nsfw_recs:
        print(f"  - [{r['matched_keyword']}] {r['title']} ({r['url']})")

    elapsed_time = time.time() - start_time
    print(f"\nExecution Time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    test_full_dataset()
