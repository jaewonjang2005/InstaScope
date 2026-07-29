import os
import json
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

from app.services.parser import InstaParser
from app.services.taste_dna import analyze_taste_dna
from app.services.secret_collection import analyze_secret_collection
from app.services.ideal_type import analyze_ideal_type
from app.services.algorithm_expose import analyze_algorithm_expose

if __name__ == "__main__":
    target_dir = r"c:\Users\jjaew\OneDrive\바탕 화면\2026 2학기 부트캠프 스터디\7-8월 토이프로젝트(인스타 알고리즘 분석)\instagram-lex_xelop-전체데이터(7.28.2026 기준)"
    print(f"Testing parser on: {target_dir}")
    parser = InstaParser(target_dir)

    print("\n--- 1. Taste DNA ---")
    dna = analyze_taste_dna(parser)
    print(json.dumps(dna, indent=2, ensure_ascii=False)[:600])

    print("\n--- 2. Secret Collection ---")
    secret = analyze_secret_collection(parser)
    print(json.dumps(secret, indent=2, ensure_ascii=False)[:600])

    print("\n--- 3. Ideal Type ---")
    ideal = analyze_ideal_type(parser)
    print(json.dumps(ideal, indent=2, ensure_ascii=False)[:600])

    print("\n--- 4. Algorithm Expose ---")
    expose = analyze_algorithm_expose(parser)
    print(json.dumps(expose, indent=2, ensure_ascii=False)[:600])

    print("\nSUCCESS: All 4 engines executed cleanly!")
