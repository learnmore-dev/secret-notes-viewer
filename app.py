from flask import Flask
import os
from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

# --- SAFE: create clients only ---
credential = ManagedIdentityCredential(
    client_id=os.environ.get("AZURE_CLIENT_ID")
)

client = SecretClient(
    vault_url="https://kv-secretnotes.vault.azure.net/",
    credential=credential
)

# --- SAFE: call Key Vault ONLY inside routes ---
@app.route("/")
def home():
    secret = client.get_secret("your-secret-name")
    return f"Secret value is: {secret.value}"

if __name__ == "__main__":
    app.run()
