import time

def load_wordlist(file_path):
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print("Wordlist file not found.")
        return []

def brute_force(password, wordlist):
    print("\nStarting brute force simulation...\n")
    start_time = time.time()

    for i, guess in enumerate(wordlist, 1):
        print(f"Trying password {i}: {guess}")
        time.sleep(0.1)  # Simulate delay

        if guess == password:
            end_time = time.time()
            print(f"\nPassword cracked! The password is: '{guess}'")
            print(f"Attempts: {i}")
            print(f"Time taken: {round(end_time - start_time, 2)} seconds")
            return True

    print("\nPassword not found in wordlist.")
    return False

if __name__ == "__main__":
    # Simulate a target password (you can change this to test)
    target_password = input("Enter the password to brute-force (e.g., nishitha123): ").strip()

    wordlist = load_wordlist("custom_wordlist.txt")
    if wordlist:
        brute_force(target_password, wordlist)
