from zxcvbn import zxcvbn
import csv
from datetime import datetime
import re

def simple_strength_check(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Add digits.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Add special characters.")

    return score, feedback


def analyze_password(password):
    # Run zxcvbn analysis
    result = zxcvbn(password)
    z_score = result['score']  # 0 to 4
    crack_time = result['crack_times_display']['offline_fast_hashing_1e10_per_second']

    # Run simple custom checks
    simple_score, simple_feedback = simple_strength_check(password)

    # Print results
    print("\nPassword Analysis (zxcvbn):")
    print(f"Strength Score (0-4): {z_score}")
    print(f"Estimated Crack Time (offline): {crack_time}")

    print("\nStrength Check (Custom Rules):")
    print(f"Score (0-4): {simple_score}")
    if simple_feedback:
        print("Suggestions to improve:")
        for tip in simple_feedback:
            print(f"  - {tip}")
    else:
        print("Password meets basic complexity requirements.")

    return {
        'password': password,
        'zxcvbn_score': z_score,
        'crack_time': crack_time,
        'simple_score': simple_score,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


def save_log(data, filename="password_logs.csv"):
    file_exists = False
    try:
        with open(filename, 'r'):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Password', 'Score', 'Crack Time', 'Timestamp'])
        writer.writerow([data['password'], data['simple_score'], data['crack_time'], data['timestamp']])


if __name__ == "__main__":
    print("Welcome to Password Strength Analyzer")
    user_password = input("Enter a password to analyze: ")
    result_data = analyze_password(user_password)

    choice = input("Do you want to save this analysis to a log file? (y/n): ").lower()
    if choice == 'y':
        save_log(result_data)
        print("Analysis saved to password_logs.csv")
