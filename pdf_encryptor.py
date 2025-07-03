import sys
import pyfiglet
from PyPDF2 import PdfReader, PdfWriter
import os
from termcolor import colored
ascii_banner = pyfiglet.figlet_format("PDF Protection Tool")
colored_banner = colored(ascii_banner, color="red",attrs=["bold"])
print(colored_banner)
try:
    input_file=sys.argv[1]
    password=sys.argv[2]
except IndexError:
    print(colored(f"Missing arguments Use:python3 encrypt_pdf.py <input_file.pdf> <password>",color="green"))
    sys.exit(1)
except Exception as e:
    print(colored(f"Un-expected error occured:{e}",color="green"))
has_upper = any(c.isupper() for c in password)
has_lower = any(c.islower() for c in password)
has_digit = any(c.isdigit() for c in password)
has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?/~`' for c in password)
security_level=sum([has_upper,has_lower,has_digit,has_special])
try:
    if security_level==4:
        pdf_reader=PdfReader(input_file)
        pdf_writer=PdfWriter()
        pdf_writer.append(pdf_reader)
        pdf_writer.encrypt(password)
        pdf_writer.write('new_encrypt.pdf')
except FileNotFoundError as f:
    print(colored(f"No such file {input_file}  Found: {f}",color="green"))
    sys.exit(1)
except PermissionError as pe:
    print(colored(f" No permission to read the file or Permission denied while writing encrypted file: {pe}",color="green"))
    sys.exit(1)
except PdfReadError as p:
    print(colored(f"File is not a valid or supported PDF: {p}",color="green"))
    sys.exit(1)
except OsError as e:
    print(colored(f"OS error while writing file: {e}",color="green"))
    sys.exit(1)
except Exception as e:
    print(colored(f"Un-expected error occured:{e}",color="green"))
    sys.exit(1)
try:
    os.replace('new_encrypt.pdf',input_file)
    print(colored(f"Protected {input_file} with password",color="green"))
except OSError as ose:
    print(colored(f"OsError: {ose}",color="green"))
    sys.exit(1)
except Exception as e:
    print(colored(f"Un-expected error occured:{e}",color="green"))
    sys.exit(1)