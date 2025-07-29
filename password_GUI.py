import tkinter as tk
from tkinter import messagebox, filedialog
import string
import random

# Global variable to keep current generated wordlist
current_wordlist = []

# === Password Strength Checker with suggestions ===
def check_strength(password):
    suggestions = []
    length = len(password)
    strength_points = 0

    if length >= 8:
        strength_points += 1
    else:
        suggestions.append("Use at least 8 characters.")

    if any(c.islower() for c in password):
        strength_points += 1
    else:
        suggestions.append("Add lowercase letters.")

    if any(c.isupper() for c in password):
        strength_points += 1
    else:
        suggestions.append("Add uppercase letters.")

    if any(c.isdigit() for c in password):
        strength_points += 1
    else:
        suggestions.append("Add digits.")

    if any(c in string.punctuation for c in password):
        strength_points += 1
    else:
        suggestions.append("Add special characters.")

    if strength_points == 5:
        strength = "Strong"
    elif strength_points >= 3:
        strength = "Medium"
    else:
        strength = "Weak"

    return strength, suggestions

# === Wordlist Generator based on inputs ===
def generate_wordlist(name, dob, pet):
    base_words = []
    if name:
        base_words.append(name.lower())
    if dob:
        base_words.append(dob)
    if pet:
        base_words.append(pet.lower())

    wordlist = []

    # Simple combinations
    for w in base_words:
        wordlist.append(w)
        wordlist.append(w + "123")
        wordlist.append(w + "@2025")
        wordlist.append(w.capitalize())
        wordlist.append(w[::-1])  # reversed

    # Combine pairs
    for i in range(len(base_words)):
        for j in range(len(base_words)):
            if i != j:
                combo = base_words[i] + base_words[j]
                wordlist.append(combo)
                wordlist.append(combo + "!")
                wordlist.append(combo + "2025")

    # Add some leetspeak variants (simple example)
    leet_map = {'a':'@', 'e':'3', 'i':'1', 'o':'0', 's':'$'}
    def leetspeak(word):
        return ''.join(leet_map.get(c, c) for c in word)

    for w in base_words:
        wordlist.append(leetspeak(w))

    # Remove duplicates and empty strings
    wordlist = list(set(filter(None, wordlist)))
    wordlist.sort()
    return wordlist

# === Save Wordlist to fixed file ===
def save_wordlist():
    global current_wordlist
    if not current_wordlist:
        messagebox.showwarning("No Wordlist", "Generate a wordlist first!")
        return
    try:
        with open("wordlist.txt", "w") as f:
            for word in current_wordlist:
                f.write(word + "\n")
        messagebox.showinfo("Saved", "Wordlist saved as 'wordlist.txt'")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file: {e}")

# === GUI Functions ===
def analyze_password():
    password = entry_password.get()
    if not password:
        messagebox.showwarning("Input Required", "Please enter a password.")
        return
    strength, suggestions = check_strength(password)
    output = f"Password Strength: {strength}\n"
    if suggestions:
        output += "\nSuggestions:\n" + "\n".join(f"- {s}" for s in suggestions)
    label_feedback.config(text=output)

def generate_and_show_wordlist():
    global current_wordlist
    name = entry_name.get().strip()
    dob = entry_dob.get().strip()
    pet = entry_pet.get().strip()
    if not (name or dob or pet):
        messagebox.showwarning("Input Required", "Please enter at least one field (Name, DOB, or Pet).")
        return
    current_wordlist = generate_wordlist(name, dob, pet)
    text_wordlist.delete('1.0', tk.END)
    text_wordlist.insert(tk.END, "\n".join(current_wordlist))

# === GUI Setup ===
root = tk.Tk()
root.title("Password Analyzer & Wordlist Generator")
root.geometry("500x600")
root.resizable(False, False)

# Password Section
tk.Label(root, text="Enter Password:", font=("Segoe UI", 11)).pack(pady=8)
entry_password = tk.Entry(root, width=40, show="*", font=("Segoe UI", 11))
entry_password.pack()

btn_check = tk.Button(root, text="Analyze Password Strength", command=analyze_password, bg="#3498db", fg="white", font=("Segoe UI", 10))
btn_check.pack(pady=10)

label_feedback = tk.Label(root, text="", font=("Segoe UI", 10), justify="left", fg="white", bg="#2c3e50", wraplength=460)
label_feedback.pack(pady=5, fill='x', padx=10)

# Separator
tk.Label(root, text="Wordlist Generator (Fill at least one)", font=("Segoe UI", 12, "bold")).pack(pady=15)

# Wordlist Inputs
frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=5)

tk.Label(frame_inputs, text="Name:", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="e", padx=5, pady=4)
entry_name = tk.Entry(frame_inputs, width=30)
entry_name.grid(row=0, column=1, pady=4)

tk.Label(frame_inputs, text="Date of Birth (YYYYMMDD):", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="e", padx=5, pady=4)
entry_dob = tk.Entry(frame_inputs, width=30)
entry_dob.grid(row=1, column=1, pady=4)

tk.Label(frame_inputs, text="Pet Name:", font=("Segoe UI", 10)).grid(row=2, column=0, sticky="e", padx=5, pady=4)
entry_pet = tk.Entry(frame_inputs, width=30)
entry_pet.grid(row=2, column=1, pady=4)

btn_generate = tk.Button(root, text="Generate Wordlist", command=generate_and_show_wordlist, bg="#2ecc71", fg="white", font=("Segoe UI", 10))
btn_generate.pack(pady=10)

btn_save = tk.Button(root, text="Save Wordlist to wordlist.txt", command=save_wordlist, bg="#27ae60", fg="white", font=("Segoe UI", 10))
btn_save.pack(pady=5)

# Wordlist Output Area
text_wordlist = tk.Text(root, height=15, width=58, wrap="word", font=("Consolas", 10))
text_wordlist.pack(pady=10, padx=10)

root.mainloop()
