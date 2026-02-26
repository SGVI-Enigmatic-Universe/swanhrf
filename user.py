import pandas as pd
import bcrypt
from pathlib import Path

BASE_DIR = Path(__file__).parent
USER_FILE = BASE_DIR / "user.xlsx"

df = pd.read_excel(USER_FILE)

def hash_pw(p):
    return bcrypt.hashpw(str(p).encode(), bcrypt.gensalt()).decode()

def is_hashed(p):
    return isinstance(p, str) and p.startswith("$2b$")

df["Password"] = df["Password"].apply(
    lambda p: p if is_hashed(p) else hash_pw(p)
)

df.to_excel(USER_FILE, index=False)
print("Passwords hashed ✅")
