import os
from app.services.parser import InstaParser
from app.services.one_pick import analyze_one_pick
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
    
    result = analyze_one_pick(parser)
    
    print("\n--- 1-Pick Analysis Results ---")
    if result.get("top_pick"):
        print(f"[Top 1 Pick]: {result['top_pick']['username']} (Score: {result['top_pick']['score']})")
        print(f"  - Likes: {result['top_pick']['likes_count']}")
        print(f"  - Saves: {result['top_pick']['saves_count']}")
        print(f"  - Story Views: {result['top_pick']['story_views_count']}")
        print(f"  - Story Likes: {result['top_pick']['story_likes_count']}")
    
    print("\n[Runner-Ups]:")
    for ru in result.get("runner_ups", []):
        print(f"  {ru['username']} (Score: {ru['score']})")
        
    print(f"\nTotal Accounts Interacted: {result['total_accounts_interacted']}")

    elapsed_time = time.time() - start_time
    print(f"\nExecution Time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    test_full_dataset()
