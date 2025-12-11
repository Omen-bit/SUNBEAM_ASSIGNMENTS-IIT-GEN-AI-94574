sentence = input("Enter a sentence: ")

num_characters = len(sentence)


words = sentence.split()

num_words = len(words)

num_vowels = 0
for i in range(num_characters):
    if sentence[i] in ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']:
        num_vowels += 1

print("Number of characters:", num_characters)
print("Number of words:", num_words)
print("Number of vowels:", num_vowels)
