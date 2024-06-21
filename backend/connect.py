import platform
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Print platform information
print(platform.uname())

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

AZURE_MY_SERVER = os.getenv("AZURE_MY_SERVER")
AZURE_MY_ADMIN = os.getenv("AZURE_MY_ADMIN")
AZURE_MY_PASSWORD = os.getenv("AZURE_MY_PASSWORD")
AZURE_MY_DATABASE = os.getenv("AZURE_MY_DATABASE")

if AZURE_MY_SERVER is None or AZURE_MY_ADMIN is None or AZURE_MY_PASSWORD is None or AZURE_MY_DATABASE is None:
    raise ValueError("All database credentials must be set")

# Get the path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
ssl_cert_path = os.path.join(current_dir, 'DigiCertGlobalRootCA.crt.pem')

# SQLAlchemyの接続URLを作成
connection_url = f"mysql+pymysql://{AZURE_MY_ADMIN}:{AZURE_MY_PASSWORD}@{AZURE_MY_SERVER}.mysql.database.azure.com/{AZURE_MY_DATABASE}"

# SQLAlchemyエンジンを作成
engine = create_engine(connection_url, connect_args={"ssl": {"ca": ssl_cert_path}}, echo=True)

# 接続テスト
try:
    # withステートメントを使用して接続を確立
    with engine.connect() as connection:
        print("Connection established")
except Exception as e:
    print(f"Connection failed: {e}")
