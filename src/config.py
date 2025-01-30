import os

from dotenv import load_dotenv

load_dotenv()

true_val = ("true", "yes", "y", 1, "1")


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRE_MINUTES = int(os.getenv("EXPIRE_MINUTES"))


DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT")

TEST_DB_NAME = os.getenv("TEST_DB_NAME")
TEST_DB_HOST = os.getenv("TEST_DB_HOST")
TEST_DB_USER = os.getenv("TEST_DB_USER")
TEST_DB_PASS = os.getenv("TEST_DB_PASS")
TEST_DB_PORT = os.getenv("TEST_DB_PORT")
TESTING = os.getenv("TESTING").lower() in true_val
