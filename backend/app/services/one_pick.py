from typing import Dict, Any

def analyze_one_pick(parser) -> Dict[str, Any]:
    liked = parser.parse_liked_posts()
    saved = parser.parse_saved_posts()
    stories_viewed = parser.parse_stories_viewed()
    story_likes = parser.parse_story_likes()

    account_scores = {}
    account_details = {}

    def add_interaction(owner: str, points: int, interaction_type: str, post_data: dict = None):
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
                'sample_url': '',
                'score': 0
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
            
        if post_data and post_data.get('url') and not det['sample_url']:
            det['sample_url'] = post_data['url']
            det['sample_caption'] = (post_data.get('caption', '') or '')[:100]

    # Weights: Story View (1), Like (2), Save (3), Story Like (4)
    for p in stories_viewed:
        add_interaction(p.get('owner'), 1, 'story_view', p)
    for p in liked:
        add_interaction(p.get('owner'), 2, 'like', p)
    for p in saved:
        add_interaction(p.get('owner'), 3, 'save', p)
    for p in story_likes:
        add_interaction(p.get('owner'), 4, 'story_like', p)

    # Sort accounts by score
    sorted_accounts = sorted(account_scores.items(), key=lambda x: x[1], reverse=True)
    
    ranking = []
    for un, score in sorted_accounts:
        det = account_details[un]
        det['score'] = score
        ranking.append(det)

    return {
        "top_pick": ranking[0] if ranking else None,
        "runner_ups": ranking[1:6] if len(ranking) > 1 else [],
        "total_accounts_interacted": len(ranking)
    }
