numbers = input("Enter numbers :  ")


num_list = [int(x.strip()) for x in numbers.split(",")]

even_count = 0
odd_count = 0

for num in num_list:
    if num % 2 == 0:
        even_count += 1
    else:
        odd_count += 1

print("Even numbers count:", even_count)
print("Odd numbers count:", odd_count)
