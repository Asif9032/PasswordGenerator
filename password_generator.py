import argparse
import string
import random
import sys

def parse_args():
    parser = argparse.ArgumentParser(
        description="🔐 Strong Password Generator CLI Tool"
    )
    parser.add_argument(
        "-l", "--length",
        type=int,
        help="Length of the password (minimum 6)",
    )
    parser.add_argument(
        "-s", "--special",
        action="store_true",
        help="Include special characters (e.g., !@#$%)"
    )
    parser.add_argument(
        "-d", "--digits",
        action="store_true",
        help="Include digits (0-9)"
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Save password to a file (filename)"
    )
    parser.add_argument(
        "-c", "--clipboard",
        action="store_true",
        help="Copy password to clipboard (requires pyperclip)"
    )
    return parser.parse_args()

def get_user_input():
    print("=== Strong Password Generator ===")
    while True:
        try:
            length = int(input("Password length (min 6): "))
            if length < 6:
                print("Password should be at least 6 characters. Try again.")
            else:
                break
        except ValueError:
            print("Invalid integer! Try again.")
    special = input("Include special characters? (y/n): ").strip().lower().startswith('y')
    digits = input("Include digits? (y/n): ").strip().lower().startswith('y')
    save_file = input("Save to file? Enter filename or press Enter to skip: ").strip()
    to_clipboard = input("Copy to clipboard? (y/n): ").strip().lower().startswith('y')
    return {
        'length': length,
        'special': special,
        'digits': digits,
        'file': save_file if save_file else None,
        'clipboard': to_clipboard
    }

def generate_password(length, use_special, use_digits):
    chars = list(string.ascii_letters)
    if use_digits:
        chars += list(string.digits)
    if use_special:
        chars += list(string.punctuation)
    if not chars:
        raise ValueError("No valid character sets provided for password generation.")
    # Guarantee one from each selection for security
    password = []
    if use_digits:
        password.append(random.choice(string.digits))
    if use_special:
        password.append(random.choice(string.punctuation))
    password += [random.choice(chars) for _ in range(length - len(password))]
    random.shuffle(password)
    return ''.join(password)

def save_to_file(password, filename):
    try:
        with open(filename, "w") as f:
            f.write(password + "\n")
        print(f"✅ Password saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving to file: {e}")

def copy_to_clipboard(password):
    try:
        import pyperclip
        pyperclip.copy(password)
        print("✅ Password copied to clipboard!")
    except ImportError:
        print("❌ pyperclip module not found.\n"
              "To enable clipboard copying, install pyperclip by running:\n"
              "   pip install pyperclip\n"
              "Alternatively, re-run the script without the --clipboard/-c flag or respond 'n' to clipboard prompts.")
        print("Continuing without clipboard functionality.\n")
    except Exception as e:
        print("❌ Error copying to clipboard:", e)
        print("Continuing without clipboard functionality.\n")

def main():
    args = parse_args()
    if any([args.length, args.special, args.digits, args.file, args.clipboard]):
        params = {
            'length': args.length or 12,
            'special': args.special,
            'digits': args.digits,
            'file': args.file,
            'clipboard': args.clipboard
        }
    else:
        params = get_user_input()

    if params['length'] < 6:
        print("❌ Password length must be at least 6.")
        sys.exit(1)

    try:
        password = generate_password(
            params['length'],
            params['special'],
            params['digits']
        )
    except ValueError as e:
        print("❌", e)
        sys.exit(1)

    print("\nGenerated Password: 🔑", password)

    if params.get('file'):
        save_to_file(password, params['file'])
    if params.get('clipboard'):
        copy_to_clipboard(password)

if __name__ == "__main__":
    main()