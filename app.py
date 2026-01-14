from flask import Flask, request
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import traceback

app = Flask(__name__)

KEY_VAULT_URL = "https://kv-secretnotes.vault.azure.net/"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

@app.route("/")
def home():
    try:
        # 1. Check authentication header
        user = request.headers.get("X-MS-CLIENT-PRINCIPAL-NAME")
        if not user:
            return "Authenticated, but user header missing", 200

        # 2. Decide secret
        if "user1" in user:
            secret_name = "note-user1"
        elif "user2" in user:
            secret_name = "note-user2"
        else:
            secret_name = "admin-note"

        # 3. Fetch secret
        secret = client.get_secret(secret_name)

        return f"<h2>Welcome {user}</h2><p>{secret.value}</p>"

    except Exception as e:
        # PRINT FULL ERROR TO LOG STREAM
        print("❌ ERROR OCCURRED")
        print(traceback.format_exc())
        return "Internal error – check log stream", 500

if __name__ == "__main__":
    app.run()
