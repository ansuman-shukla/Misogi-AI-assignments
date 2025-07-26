def analyze_friendships():
    facebook_friends = {"alice", "bob", "charlie", "diana", "eve", "frank"}
    instagram_friends = {"bob", "charlie", "grace", "henry", "alice", "ivan"}
    twitter_friends = {"alice", "diana", "grace", "jack", "bob", "karen"}
    linkedin_friends = {"charlie", "diana", "frank", "grace", "luke", "mary"}
    
    all_platforms = facebook_friends & instagram_friends & twitter_friends & linkedin_friends
    
    facebook_only = facebook_friends - instagram_friends - twitter_friends - linkedin_friends
    
    instagram_xor_twitter = (instagram_friends | twitter_friends) - (instagram_friends & twitter_friends)
    
    total_unique = facebook_friends | instagram_friends | twitter_friends | linkedin_friends
    
    exactly_two_platforms = set()
    for friend in total_unique:
        count = 0
        if friend in facebook_friends:
            count += 1
        if friend in instagram_friends:
            count += 1
        if friend in twitter_friends:
            count += 1
        if friend in linkedin_friends:
            count += 1
        if count == 2:
            exactly_two_platforms.add(friend)
    
    return {
        'all_platforms': all_platforms,
        'facebook_only': facebook_only,
        'instagram_xor_twitter': instagram_xor_twitter,
        'total_unique': total_unique,
        'exactly_two_platforms': exactly_two_platforms
    }

result = analyze_friendships()
print("All platforms:", result.get('all_platforms'))
print("Facebook only:", result.get('facebook_only'))
print("Instagram XOR Twitter:", result.get('instagram_xor_twitter'))
print("Total unique friends:", result.get('total_unique'))
print("Exactly 2 platforms:", result.get('exactly_two_platforms'))
