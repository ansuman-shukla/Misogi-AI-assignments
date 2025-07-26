from collections import Counter, defaultdict

posts = [
    {"id": 1, "user": "alice", "content": "Love Python programming!", "likes": 15, "tags": ["python", "coding"]},
    {"id": 2, "user": "bob", "content": "Great weather today", "likes": 8, "tags": ["weather", "life"]},
    {"id": 3, "user": "alice", "content": "Data structures are fun", "likes": 22, "tags": ["python", "learning"]},
]

users = {
    "alice": {"followers": 150, "following": 75},
    "bob": {"followers": 89, "following": 120},
}

def most_popular_tags(posts):
    tag_counter = Counter()
    for post in posts:
        tag_counter.update(post["tags"])
    return tag_counter.most_common()

def user_engagement_analysis(posts):
    user_likes = defaultdict(int)
    for post in posts:
        user_likes[post["user"]] += post["likes"]
    return dict(user_likes)

def top_posts_by_likes(posts):
    return sorted(posts, key=lambda x: x["likes"], reverse=True)

def user_activity_summary(posts, users):
    user_summary = {}
    user_likes = user_engagement_analysis(posts)
    user_posts = defaultdict(int)
    
    for post in posts:
        user_posts[post["user"]] += 1
    
    for user in users:
        summary = {
            "posts_count": user_posts.get(user, 0),
            "total_likes": user_likes.get(user, 0),
            "followers": users[user]["followers"],
            "following": users[user]["following"]
        }
        user_summary[user] = summary
    
    return user_summary

print("Most Popular Tags:")
popular_tags = most_popular_tags(posts)
for tag, count in popular_tags:
    print(f"{tag}: {count}")

print("\nUser Engagement Analysis:")
engagement = user_engagement_analysis(posts)
for user, likes in engagement.items():
    print(f"{user}: {likes} total likes")

print("\nTop Posts by Likes:")
top_posts = top_posts_by_likes(posts)
for post in top_posts:
    print(f"Post {post['id']} by {post['user']}: {post['likes']} likes")

print("\nUser Activity Summary:")
activity_summary = user_activity_summary(posts, users)
for user, summary in activity_summary.items():
    print(f"{user}: {summary}")
