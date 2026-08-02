import os
import json
import re
import zipfile
from typing import Dict, List, Any
from app.utils.encoding import decode_insta_text, decode_obj

class InstaParser:
    """Parser focused strictly on extracting data for 1-Pick analysis."""
    def __init__(self, root_dir: str):
        self.root_dir = root_dir

    def _read_json(self, relative_path: str) -> Any:
        if not self.root_dir or not os.path.exists(self.root_dir):
            return None
        full_path = os.path.join(self.root_dir, relative_path)
        if not os.path.exists(full_path):
            dir_name = os.path.dirname(full_path)
            base_name = os.path.basename(full_path)
            if os.path.exists(dir_name):
                for f in os.listdir(dir_name):
                    if f.lower() == base_name.lower():
                        full_path = os.path.join(dir_name, f)
                        break
            if not os.path.exists(full_path):
                return None
        try:
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                data = json.load(f)
                return decode_obj(data)
        except Exception as e:
            print(f"Error reading {relative_path}: {e}")
            return None

    def _extract_posts_list(self, relative_path: str) -> List[Dict[str, Any]]:
        data = self._read_json(relative_path)
        posts = []
        if not isinstance(data, list):
            return posts

        for item in data:
            ts = item.get('timestamp', 0)
            url = ""
            caption = ""
            hashtags = set()
            owner = ""

            label_values = item.get('label_values', [])
            for lv in label_values:
                lbl = lv.get('label', '')
                val = lv.get('value', '')
                title = lv.get('title', '')
                
                if lbl == 'URL':
                    url = val or lv.get('href', '')
                elif lbl == '캡션':
                    caption = val
                elif title == '해시태그':
                    for d1 in lv.get('dict', []):
                        for d2 in d1.get('dict', []):
                            if d2.get('label') == '이름':
                                hashtags.add(d2.get('value', '').strip('#'))
                
                # Check for owner in either title or label
                if '이름' in lbl or '소유자' in lbl or '작성자' in lbl or '소유자' in title or '작성자' in title:
                    for d1 in lv.get('dict', []):
                        for d2 in d1.get('dict', []):
                            if d2.get('label') == '이름' or d2.get('label') == '사용자 이름':
                                owner = d2.get('value', '')

            if caption:
                found_tags = re.findall(r'#(\w+)', caption)
                for tag in found_tags:
                    hashtags.add(tag)

            if not owner and url:
                story_match = re.search(r'instagram\.com/stories/([^/]+)/', url)
                if story_match:
                    owner = story_match.group(1)

            posts.append({
                'timestamp': ts,
                'url': url,
                'caption': caption,
                'hashtags': list(hashtags),
                'owner': owner
            })
        return posts

    # your_instagram_activity Core Parsers
    def parse_liked_posts(self) -> List[Dict[str, Any]]:
        return self._extract_posts_list(os.path.join('your_instagram_activity', 'likes', 'liked_posts.json'))

    def parse_saved_posts(self) -> List[Dict[str, Any]]:
        return self._extract_posts_list(os.path.join('your_instagram_activity', 'saved', 'saved_posts.json'))

    def parse_stories_viewed(self) -> List[Dict[str, Any]]:
        return self._extract_posts_list(os.path.join('your_instagram_activity', 'story_interactions', 'stories_viewed.json'))

    def parse_story_likes(self) -> List[Dict[str, Any]]:
        return self._extract_posts_list(os.path.join('your_instagram_activity', 'story_interactions', 'story_likes.json'))

class InstaMemoryParser(InstaParser):
    """Memory parser that reads strictly your_instagram_activity JSONs."""
    def __init__(self, files_dict: Dict[str, Any]):
        super().__init__(root_dir="")
        self.files_dict = files_dict or {}

    def _read_json(self, relative_path: str) -> Any:
        normalized_key = relative_path.replace('\\', '/').lower()
        for key, val in self.files_dict.items():
            if key.replace('\\', '/').lower().endswith(normalized_key):
                return decode_obj(val)
        return None
