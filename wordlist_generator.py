import itertools

def get_user_input():
    print("Enter personal info to build a custom wordlist:")
    name = input("Name: ").strip().lower()
    birth_year = input("Birth Year: ").strip()
    pet_name = input("Pet Name: ").strip().lower()
    favorite_word = input("Favorite Word: ").strip().lower()
    common_numbers = ['123', '1234', '12345', '@123', '2020', '2023']

    base_words = [name, birth_year, pet_name, favorite_word]
    return base_words, common_numbers

def generate_wordlist(base_words, common_numbers):
    wordlist = set()

    for word in base_words:
        if word:
            wordlist.add(word)
            for num in common_numbers:
                wordlist.add(word + num)
                wordlist.add(num + word)
                wordlist.add(word.capitalize() + num)

    # Combine base words (like name + birth year)
    for combo in itertools.permutations(base_words, 2):
        joined = ''.join(combo)
        wordlist.add(joined)
        for num in common_numbers:
            wordlist.add(joined + num)

    return list(wordlist)

def save_wordlist(wordlist):
    with open("custom_wordlist.txt", "w") as file:
        for word in wordlist:
            file.write(word + "\n")
    print(f"\nWordlist saved as 'custom_wordlist.txt' with {len(wordlist)} entries.")

if __name__ == "__main__":
    base_words, common_numbers = get_user_input()
    wordlist = generate_wordlist(base_words, common_numbers)
    save_wordlist(wordlist)
