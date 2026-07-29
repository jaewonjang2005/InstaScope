from typing import Dict, List, Any

def analyze_ideal_type(parser) -> Dict[str, Any]:
    liked = parser.parse_liked_posts()
    saved = parser.parse_saved_posts()
    stories_viewed = parser.parse_stories_viewed()
    story_likes = parser.parse_story_likes()
    followers = {f['username'] for f in parser.parse_followers() if f.get('username')}
    following = {f['username'] for f in parser.parse_following() if f.get('username')}
    close_friends = set(parser.parse_close_friends())
    favorited = set(parser.parse_favorited_profiles())

    account_scores = {}
    account_details = {}

    def add_interaction(owner: str, points: int, interaction_type: str):
        if not owner or len(owner) < 2:
            return
        owner_clean = owner.strip('@').lower()
        account_scores[owner_clean] = account_scores.get(owner_clean, 0) + points
        if owner_clean not in account_details:
            account_details[owner_clean] = {
                'username': owner_clean,
                'likes_count': 0,
                'saves_count': 0,
                'story_views_count': 0,
                'story_likes_count': 0,
                'sample_caption': '',
                'sample_url': ''
            }
        
        det = account_details[owner_clean]
        if interaction_type == 'like':
            det['likes_count'] += 1
        elif interaction_type == 'save':
            det['saves_count'] += 1
        elif interaction_type == 'story_view':
            det['story_views_count'] += 1
        elif interaction_type == 'story_like':
            det['story_likes_count'] += 1

    # Weighting scheme
    for p in liked:
        if p.get('owner'):
            add_interaction(p['owner'], 2, 'like')
            if p.get('url') and not account_details[p['owner'].strip('@').lower()]['sample_url']:
                account_details[p['owner'].strip('@').lower()]['sample_url'] = p['url']
                account_details[p['owner'].strip('@').lower()]['sample_caption'] = (p.get('caption', '') or '')[:100]

    for p in saved:
        if p.get('owner'):
            add_interaction(p['owner'], 3, 'save')
            if p.get('url') and not account_details[p['owner'].strip('@').lower()]['sample_url']:
                account_details[p['owner'].strip('@').lower()]['sample_url'] = p['url']
                account_details[p['owner'].strip('@').lower()]['sample_caption'] = (p.get('caption', '') or '')[:100]

    for p in stories_viewed:
        if p.get('owner'):
            add_interaction(p['owner'], 1, 'story_view')

    for p in story_likes:
        if p.get('owner'):
            add_interaction(p['owner'], 4, 'story_like')

    # Sort accounts by score
    sorted_accounts = sorted(account_scores.items(), key=lambda x: x[1], reverse=True)

    ideal_candidates = []
    close_friend_rank = []
    favorite_creators = []

    for un, score in sorted_accounts:
        det = account_details[un]
        is_following = un in following
        is_follower = un in followers
        is_close = un in close_friends
        is_fav = un in favorited

        item_data = {
            "username": un,
            "score": score,
            "likes_count": det['likes_count'],
            "saves_count": det['saves_count'],
            "story_likes_count": det['story_likes_count'],
            "story_views_count": det['story_views_count'],
            "is_close_friend": is_close,
            "is_favorited": is_fav,
            "is_following": is_following,
            "is_mutual": (is_following and is_follower),
            "sample_url": det['sample_url'],
            "sample_caption": det['sample_caption']
        }

        if is_close or (is_following and is_follower):
            close_friend_rank.append(item_data)
        elif det['saves_count'] > det['likes_count']:
            favorite_creators.append(item_data)
        else:
            ideal_candidates.append(item_data)

    # Fallback if lists are small
    if not ideal_candidates:
        ideal_candidates = [item for un, score in sorted_accounts[:10] for item in [account_details[un]]]

    # Top Recommended Posts based on highest interaction / saved status
    top_recommended_posts = []
    for p in saved[:6] + liked[:6]:
        if p.get('url'):
            top_recommended_posts.append({
                "url": p['url'],
                "caption": (p.get('caption', '') or '')[:120],
                "owner": p.get('owner', 'instagram'),
                "hashtags": p.get('hashtags', [])[:5]
            })

    return {
        "top_ideal_type_candidates": ideal_candidates[:10],
        "top_close_friends": close_friend_rank[:10],
        "top_favorite_creators": favorite_creators[:10],
        "recommended_posts": top_recommended_posts[:8]
    }
