import os
import sys
from dotenv import load_dotenv
import google.genai as genai
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

load_dotenv()
api_key = os.getenv("Enter your api key here")
security_prompt = """
Analyze this code for security vulnerabilities. Be concise.

For each issue use this exact format:

---
SEVERITY: [CRITICAL/HIGH/MEDIUM/LOW]
TYPE: [Vulnerability Name]
DESCRIPTION: [One sentence explaining the issue]
IMPACT: [One sentence on potential damage]
FIX: [Code snippet only]
---

Code:
{code}
"""

client = genai.Client(api_key=api_key)

def add_colors_to_output(text):
    """Add colors to severity levels in the output."""
    text = text.replace("SEVERITY: CRITICAL", f"SEVERITY: {Fore.RED}{Style.BRIGHT}CRITICAL{Style.RESET_ALL}")
    text = text.replace("SEVERITY: HIGH", f"SEVERITY: {Fore.YELLOW}{Style.BRIGHT}HIGH{Style.RESET_ALL}")
    text = text.replace("SEVERITY: MEDIUM", f"SEVERITY: {Fore.BLUE}MEDIUM{Style.RESET_ALL}")
    text = text.replace("SEVERITY: LOW", f"SEVERITY: {Fore.GREEN}LOW{Style.RESET_ALL}")
    return text

# File path from command line: python scanner.py <file_path>
if len(sys.argv) < 2:
    print("Usage: python scanner.py <file_path>")
    sys.exit(1)

code_path = sys.argv[1]
with open(code_path, "r") as f:
    code = f.read()

prompt = security_prompt.format(code=code)


try:
    response = client.models.generate_content(
        model='gemini-3.5-flash-lite', contents=prompt
    )
    print(add_colors_to_output(response.text))
except Exception as e:
    print(f"❌ Connection failed: {e}")