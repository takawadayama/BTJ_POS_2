# uname() error回避
import platform

print(platform.uname())

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# 環境変数のロード
load_dotenv()
AZURE_MY_SERVER = os.getenv("AZURE_MY_SERVER")
AZURE_MY_ADMIN = os.getenv("AZURE_MY_ADMIN")
AZURE_MY_PASSWORD = os.getenv("AZURE_MY_PASSWORD")
AZURE_MY_DATABASE = os.getenv("AZURE_MY_DATABASE")

# SSL証明書のパスを設定(connect.pyと同じ場所におく)
base_path = os.path.dirname(os.path.abspath(__file__))
ssl_cert_path = os.path.join(base_path, 'DigiCertGlobalRootCA.crt.pem')

# SQLAlchemyの接続URLを作成
connection_url = f"mysql+pymysql://{AZURE_MY_ADMIN}:{AZURE_MY_PASSWORD}@{AZURE_MY_SERVER}.mysql.database.azure.com/{AZURE_MY_DATABASE}"

# SQLAlchemyエンジンを作成
engine = create_engine(connection_url, connect_args={"ssl": {"CA": ssl_cert_path}}, echo=True)

# 接続テスト
try:
    # withステートメントを使用して接続を確立
    # 手動で閉じるときにはconnection.close()
    with engine.connect() as connection:
        print("Connection established")
except Exception as e:
    print(f"Connection failed: {e}")
