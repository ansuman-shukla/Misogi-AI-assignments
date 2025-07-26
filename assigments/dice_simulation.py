import random

count_sum_7 = 0
count_sum_2 = 0
count_sum_greater_10 = 0

for _ in range(10000):
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    dice_sum = dice1 + dice2
    
    if dice_sum == 7:
        count_sum_7 += 1
    elif dice_sum == 2:
        count_sum_2 += 1
    elif dice_sum > 10:
        count_sum_greater_10 += 1

prob_sum_7 = count_sum_7 / 10000
prob_sum_2 = count_sum_2 / 10000
prob_sum_greater_10 = count_sum_greater_10 / 10000

print(f"P(Sum = 7): {prob_sum_7:.4f}")
print(f"P(Sum = 2): {prob_sum_2:.4f}")
print(f"P(Sum > 10): {prob_sum_greater_10:.4f}")
