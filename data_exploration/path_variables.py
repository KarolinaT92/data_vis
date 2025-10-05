from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv(filename=".env"), override=True)

PATH = os.getenv("CSV_PATH") 