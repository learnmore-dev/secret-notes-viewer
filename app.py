from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from flask import Flask

app = Flask(__name__)

VAULT_URL = "https://kv-secretnotes-au.vault.azure.net/"
SECRET_NAME = "note-alice"

@app.route("/")
def get_secret():
    try:
        credential = DefaultAzureCredential()

        client = SecretClient(
            vault_url=VAULT_URL,
            credential=credential
        )

        secret = client.get_secret(SECRET_NAME)
        return f"Secret value: {secret.value}"

    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == "__main__":
    app.run()
