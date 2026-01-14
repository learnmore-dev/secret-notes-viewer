import os
from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

credential = ManagedIdentityCredential(
    client_id=os.environ["AZURE_CLIENT_ID"]
)

client = SecretClient(
    vault_url="https://kv-secretnotes.vault.azure.net/",
    credential=credential
)

secret = client.get_secret("your-secret-name")
print(secret.value)
