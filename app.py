import base64
import json
from flask import Flask, request
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

KEY_VAULT_URL = "https://kv-secretnotes.vault.azure.net/"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

@app.route("/")
def home():
    principal = request.headers.get("X-MS-CLIENT-PRINCIPAL")
    if not principal:
        return "Authenticated, but no principal header found", 200

    # Decode Easy Auth principal
    user_info = json.loads(base64.b64decode(principal))
    user = user_info.get("userDetails") or user_info.get("user_id", "unknown")

    # Decide which secret to show
    if "user1" in user:
        secret_name = "note-user1"
    elif "user2" in user:
        secret_name = "note-user2"
    else:
        secret_name = "admin-note"

    secret = client.get_secret(secret_name)
    return f"<h2>Welcome {user}</h2><p>{secret.value}</p>"
