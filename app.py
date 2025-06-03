import os
from flask import Flask, jsonify
import psycopg2
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

# Get secrets from Azure Key Vault
key_vault_name = os.environ.get("KEY_VAULT_NAME")
key_vault_url = f"https://{key_vault_name}.vault.azure.net/"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=key_vault_url, credential=credential)

db_host = client.get_secret("DB-HOST").value
db_name = client.get_secret("DB-NAME").value
db_user = client.get_secret("DB-USER").value
db_password = client.get_secret("DB-PASSWORD").value

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=db_host,
        dbname=db_name,
        user=db_user,
        password=db_password
    )
    return conn

@app.route('/hello')
def hello():
    return jsonify({"message": "Hello from Azure Python App!"})

@app.route('/db-test')
def db_test():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({"db_version": db_version[0]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
