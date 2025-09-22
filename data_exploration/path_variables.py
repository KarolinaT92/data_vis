from dotenv import load_dotenv
import os

load_dotenv()

POSTINGS_PATH = os.getenv("POSTINGS_CSV_PATH")