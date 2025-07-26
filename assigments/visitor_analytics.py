monday_visitors = {"user1", "user2", "user3", "user4", "user5"}
tuesday_visitors = {"user2", "user4", "user6", "user7", "user8"}
wednesday_visitors = {"user1", "user3", "user6", "user9", "user10"}

unique_visitors = monday_visitors | tuesday_visitors | wednesday_visitors
print(f"Total unique visitors across all days: {len(unique_visitors)}")

returning_tuesday = monday_visitors & tuesday_visitors
print(f"Returning visitors on Tuesday: {returning_tuesday}")

new_monday = monday_visitors
new_tuesday = tuesday_visitors - monday_visitors
new_wednesday = wednesday_visitors - (monday_visitors | tuesday_visitors)
print(f"New visitors Monday: {new_monday}")
print(f"New visitors Tuesday: {new_tuesday}")
print(f"New visitors Wednesday: {new_wednesday}")

loyal_visitors = monday_visitors & tuesday_visitors & wednesday_visitors
print(f"Loyal visitors (all three days): {loyal_visitors}")

monday_tuesday_overlap = monday_visitors & tuesday_visitors
tuesday_wednesday_overlap = tuesday_visitors & wednesday_visitors
monday_wednesday_overlap = monday_visitors & wednesday_visitors
print(f"Monday-Tuesday overlap: {monday_tuesday_overlap}")
print(f"Tuesday-Wednesday overlap: {tuesday_wednesday_overlap}")
print(f"Monday-Wednesday overlap: {monday_wednesday_overlap}")
