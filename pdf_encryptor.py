import sys
import pyfiglet
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.errors import PdfReadError
import os
from termcolor import colored

# Banner
ascii_banner = pyfiglet.figlet_format("PDF Protection Tool")
colored_banner = colored(ascii_banner, color="red", attrs=["bold"])
print(colored_banner)

# --- Argument Parsing ---
try:
    input_file = sys.argv[1]
    password = sys.argv[2]
except IndexError:
    print(colored(f"Missing arguments. Use:\npython3 encrypt_pdf.py <input_file.pdf> <password>", color="green"))
    sys.exit(1)
except Exception as e:
    print(colored(f"Unexpected error occurred: {e}", color="green"))
    sys.exit(1)

# --- Password Strength Check ---
has_upper = any(c.isupper() for c in password)
has_lower = any(c.islower() for c in password)
has_digit = any(c.isdigit() for c in password)
has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?/~`' for c in password)
security_level = sum([has_upper, has_lower, has_digit, has_special])

# --- Encryption ---
try:
    if security_level == 4:
        pdf_reader = PdfReader(input_file)
        pdf_writer = PdfWriter()

        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        pdf_writer.encrypt(password)

        with open("new_encrypt.pdf", "wb") as ne:
            pdf_writer.write(ne)
    else:
        print(colored(f" Password is weak. Use upper, lower, digits & special chars.", "green"))
        sys.exit(1)

except FileNotFoundError:
    print(colored(f" File not found: {input_file}", color="green"))
    sys.exit(1)
except PermissionError as pe:
    print(colored(f" Permission denied: {pe}", color="green"))
    sys.exit(1)
except PdfReadError as pre:
    print(colored(f" Not a valid PDF: {pre}", color="green"))
    sys.exit(1)
except OSError as e:
    print(colored(f" OS error: {e}", color="green"))
    sys.exit(1)
except Exception as e:
    print(colored(f"Unexpected error: {e}", color="green"))
    sys.exit(1)

# --- Replace Original File ---
try:
    if os.path.exists("new_encrypt.pdf"):
        os.replace("new_encrypt.pdf", input_file)
        print(colored(f"'{input_file}' encrypted and replaced successfully.", "green"))
    else:
        print(colored(" File not found: new_encrypt.pdf", "green"))

except OSError as ose:
    print(colored(f" OSError: {ose}", color="green"))
    sys.exit(1)
except Exception as e:
    print(colored(f" Unexpected error occurred: {e}", color="green"))
    sys.exit(1)