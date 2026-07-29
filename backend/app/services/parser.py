import os
import json
import re
import zipfile
from typing import Dict, List, Any
from app.utils.encoding import decode_insta_text, decode_obj

class InstaParser:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir

    def _read_json(self, relative_path: str) -> Any:
        full_path = os.path.join(self.root_dir, relative_path)
        if not os.path.exists(full_path):
            # Try case-insensitive or searching for file
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

    def parse_followers(self) -> List[Dict[str, Any]]:
        # connections/followers_and_following/followers_1.json
        data = self._read_json(os.path.join('connections', 'followers_and_following', 'followers_1.json'))
        followers = []
        if isinstance(data, list):
            for item in data:
                str_list = item.get('string_list_data', [])
                for entry in str_list:
                    followers.append({
                        'username': entry.get('value', ''),
                        'timestamp': entry.get('timestamp', 0),
                        'href': entry.get('href', '')
                    })
        return followers

    def parse_following(self) -> List[Dict[str, Any]]:
        # connections/followers_and_following/following.json
        data = self._read_json(os.path.join('connections', 'followers_and_following', 'following.json'))
        following = []
        if isinstance(data, dict):
            rel = data.get('relationships_following', [])
            for item in rel:
                username = item.get('title', '')
                str_list = item.get('string_list_data', [])
                ts = str_list[0].get('timestamp', 0) if str_list else 0
                href = str_list[0].get('href', '') if str_list else ''
                following.append({
                    'username': username,
                    'timestamp': ts,
                    'href': href
                })
        return following

    def parse_recently_unfollowed(self) -> List[Dict[str, Any]]:
        # connections/followers_and_following/recently_unfollowed_profiles.json
        data = self._read_json(os.path.join('connections', 'followers_and_following', 'recently_unfollowed_profiles.json'))
        unfollowed = []
        if isinstance(data, list):
            for item in data:
                ts = item.get('timestamp', 0)
                name = ""
                username = ""
                for lv in item.get('label_values', []):
                    lbl = lv.get('label', '')
                    val = lv.get('value', '')
                    if '이름' in lbl and '사용자' not in lbl:
                        name = val
                    elif '사용자' in lbl or 'username' in lbl.lower():
                        username = val
                unfollowed.append({
                    'username': username,
                    'name': name,
                    'timestamp': ts
                })
        return unfollowed

    def parse_close_friends(self) -> List[str]:
        # connections/followers_and_following/close_friends.json
        data = self._read_json(os.path.join('connections', 'followers_and_following', 'close_friends.json'))
        close = []
        if isinstance(data, list):
            for item in data:
                for lv in item.get('label_values', []):
                    if '사용자' in lv.get('label', ''):
                        close.append(lv.get('value', ''))
        return close

    def parse_favorited_profiles(self) -> List[str]:
        # connections/followers_and_following/profiles_you've_favorited.json
        data = self._read_json(os.path.join('connections', 'followers_and_following', "profiles_you've_favorited.json"))
        favs = []
        if isinstance(data, list):
            for item in data:
                for lv in item.get('label_values', []):
                    if '사용자' in lv.get('label', ''):
                        favs.append(lv.get('value', ''))
        return favs

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
                if lbl == 'URL':
                    url = val or lv.get('href', '')
                elif lbl == '캡션':
                    caption = val
                elif lbl == '해시태그':
                    for d1 in lv.get('dict', []):
                        for d2 in d1.get('dict', []):
                            if d2.get('label') == '이름':
                                hashtags.add(d2.get('value', '').strip('#'))
                elif '이름' in lbl or '소유자' in lbl or '작성자' in lbl:
                    for d1 in lv.get('dict', []):
                        for d2 in d1.get('dict', []):
                            if d2.get('label') == '이름':
                                owner = d2.get('value', '')

            # Extract hashtags from caption if any
            if caption:
                found_tags = re.findall(r'#(\w+)', caption)
                for tag in found_tags:
                    hashtags.add(tag)

            # Try extracting username from URL if owner not found
            if not owner and url:
                # e.g. https://www.instagram.com/p/CODE/ or https://www.instagram.com/reel/CODE/ or https://www.instagram.com/stories/USERNAME/123
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

    def parse_liked_posts(self) -> List[Dict[str, Any]]:
        return self._extract_posts_list(os.path.join('your_instagram_activity', 'likes', 'liked_posts.json'))

    def parse_saved_posts(self) -> List[Dict[str, Any]]:
        return self._extract_posts_list(os.path.join('your_instagram_activity', 'saved', 'saved_posts.json'))

    def parse_saved_collections(self) -> List[Dict[str, Any]]:
        data = self._read_json(os.path.join('your_instagram_activity', 'saved', 'saved_collections.json'))
        collections = []
        if not isinstance(data, list):
            return collections

        for item in data:
            name = ""
            c_type = ""
            privacy = ""
            updated_ts = 0
            posts = []

            for lv in item.get('label_values', []):
                lbl = lv.get('label', '')
                val = lv.get('value', '')
                if lbl == '이름':
                    name = val
                elif lbl == '유형':
                    c_type = val
                elif lbl == '공개 범위':
                    privacy = val
                elif lbl == '업데이트 시간':
                    updated_ts = lv.get('timestamp_value', 0)
                elif 'dict' in lv:
                    for post_d in lv.get('dict', []):
                        p_url = ""
                        p_cap = ""
                        p_owner = ""
                        p_tags = set()
                        for sub_d in post_d.get('dict', []):
                            s_lbl = sub_d.get('label', '')
                            s_val = sub_d.get('value', '')
                            if s_lbl == 'URL':
                                p_url = s_val
                            elif s_lbl == '캡션':
                                p_cap = s_val
                            elif s_lbl == '소유자':
                                for d1 in sub_d.get('dict', []):
                                    for d2 in d1.get('dict', []):
                                        if '이름' in d2.get('label', ''):
                                            p_owner = d2.get('value', '')
                        if p_cap:
                            for tag in re.findall(r'#(\w+)', p_cap):
                                p_tags.add(tag)
                        posts.append({
                            'url': p_url,
                            'caption': p_cap,
                            'owner': p_owner,
                            'hashtags': list(p_tags)
                        })

            collections.append({
                'name': name or "기본 저장",
                'type': c_type,
                'privacy': privacy,
                'updated_timestamp': updated_ts,
                'posts_count': len(posts),
                'posts': posts
            })
        return collections

    def parse_videos_watched(self) -> List[Dict[str, Any]]:
        return self._extract_posts_list(os.path.join('ads_information', 'ads_and_topics', 'videos_watched.json'))

    def parse_posts_viewed(self) -> List[Dict[str, Any]]:
        return self._extract_posts_list(os.path.join('ads_information', 'ads_and_topics', 'posts_viewed.json'))

    def parse_stories_viewed(self) -> List[Dict[str, Any]]:
        return self._extract_posts_list(os.path.join('your_instagram_activity', 'story_interactions', 'stories_viewed.json'))

    def parse_story_likes(self) -> List[Dict[str, Any]]:
        return self._extract_posts_list(os.path.join('your_instagram_activity', 'story_interactions', 'story_likes.json'))

    def parse_ad_categories(self) -> List[str]:
        # ads_information/instagram_ads_and_businesses/other_categories_used_to_reach_you.json
        data = self._read_json(os.path.join('ads_information', 'instagram_ads_and_businesses', 'other_categories_used_to_reach_you.json'))
        cats = []
        if isinstance(data, dict):
            for lv in data.get('label_values', []):
                for v in lv.get('vec', []):
                    if isinstance(v, dict) and 'value' in v:
                        cats.append(v['value'])
        return cats

    def parse_advertisers(self) -> List[str]:
        # ads_information/instagram_ads_and_businesses/advertisers_using_your_activity_or_information.json
        data = self._read_json(os.path.join('ads_information', 'instagram_ads_and_businesses', 'advertisers_using_your_activity_or_information.json'))
        advertisers = []
        if isinstance(data, dict):
            for lv in data.get('label_values', []):
                for v in lv.get('vec', []):
                    if isinstance(v, dict) and 'value' in v:
                        advertisers.append(v['value'])
        return advertisers

    def parse_locations(self) -> List[str]:
        # personal_information/information_about_you/locations_of_interest.json
        data = self._read_json(os.path.join('personal_information', 'information_about_you', 'locations_of_interest.json'))
        locations = []
        if isinstance(data, dict):
            for lv in data.get('label_values', []):
                if '위치' in lv.get('label', ''):
                    for v in lv.get('vec', []):
                        if isinstance(v, dict) and 'value' in v:
                            locations.append(v['value'])
        return locations

    def parse_login_activity(self) -> List[Dict[str, Any]]:
        # security_and_login_information/login_and_profile_creation/login_activity.json
        data = self._read_json(os.path.join('security_and_login_information', 'login_and_profile_creation', 'login_activity.json'))
        logins = []
        if isinstance(data, dict):
            history = data.get('account_history_login_history', [])
            for item in history:
                ip = ""
                ua = ""
                ts = 0
                s_map = item.get('string_map_data', {})
                if 'IP 주소' in s_map:
                    ip = s_map['IP 주소'].get('value', '')
                if '사용자 에이전트' in s_map:
                    ua = s_map['사용자 에이전트'].get('value', '')
                if '시간' in s_map:
                    ts = s_map['시간'].get('timestamp', 0)
                logins.append({
                    'ip': ip,
                    'user_agent': ua,
                    'timestamp': ts
                })
        return logins
