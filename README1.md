# 🔐 Secret Notes Viewer – Azure Secure Web Application

A secure web application built on Microsoft Azure that allows authenticated users to view secret notes stored in **Azure Key Vault**, using **Azure Active Directory (Microsoft Entra ID)** for authentication and **Managed Identity** for secure access.

This project demonstrates **enterprise-grade Azure security best practices** with zero secrets in code.

---

## 📌 Project Objective

To build a secure web application where:
- Users authenticate using Azure Active Directory
- Each user can access **only their assigned secrets**
- Secrets are securely stored in Azure Key Vault
- The application uses **Managed Identity** instead of credentials
- CI/CD is implemented using GitHub Actions
- Monitoring is enabled using Azure Application Insights

---

## 🏗️ Architecture Overview


## 🏗️ Architecture Overview

User
↓ Login
Azure Active Directory (Microsoft Entra ID)
↓ Token
Azure App Service (Flask Application)
↓ Managed Identity
Azure Key Vault (Secrets)


---

## ☁️ Azure Services Used

| Service | Purpose |
|------|-------|
| Microsoft Entra ID (Azure AD) | User authentication |
| Azure App Service | Hosting Flask web application |
| Azure Key Vault | Secure storage of secrets |
| Managed Identity | Secure access without credentials |
| GitHub Actions | CI/CD pipeline |
| Azure Application Insights | Monitoring & logging |

---

## 🔐 Security Design

- **No secrets stored in code or environment files**
- **Managed Identity** is used to authenticate the App Service to Azure Key Vault
- **Azure RBAC** controls access to Key Vault secrets
- Users authenticate using **OAuth 2.0 via Azure AD**
- Principle of **least privilege** is enforced

---

## 📁 Project Structure

SecretNotesApp/
├── app.py
├── requirements.txt
├── README.md


---

## ⚙️ Application Flow

1. User accesses the web app
2. User is redirected to Azure AD login
3. After authentication, Azure AD issues a token
4. App Service uses Managed Identity
5. Key Vault validates RBAC permissions
6. Secret is retrieved and displayed to the user

---

## 🧪 Sample Secrets Setup

| Secret Name | Description |
|-----------|------------|
| note-alice | Secret note for Alice |
| note-bob | Secret note for Bob |

Each user can only access their own secret.

---

## 🧑‍💻 Application Code (`app.py`)

```python
from flask import Flask, redirect, url_for, session
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)
app.secret_key = "demo-secret-key"

VAULT_URL = "https://kv-secretnotes-au.vault.azure.net/"

@app.route("/")
def index():
    if "user" not in session:
        return redirect("/.auth/login/aad")
    return redirect(url_for("notes"))

@app.route("/notes")
def notes():
    try:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=VAULT_URL, credential=credential)

        username = session.get("user", "alice")
        secret_name = f"note-{username}"

        secret = client.get_secret(secret_name)
        return f"<h2>Welcome {username}</h2><p>{secret.value}</p>"

    except Exception as e:
        return f"Error fetching secret: {str(e)}", 500

if __name__ == "__main__":
    app.run()
📦 Dependencies (requirements.txt)
Flask==2.3.3
azure-identity==1.15.0
azure-keyvault-secrets==4.9.0
gunicorn==20.1.0
🚀 Deployment Steps
1️⃣ Create Azure Resources
Azure App Service (Python 3.10, Linux)

Azure Key Vault (RBAC enabled)

Azure AD App Registration

2️⃣ Enable Managed Identity
App Service → Identity → System Assigned → ON

3️⃣ Assign RBAC Role
Assign Key Vault Secrets User role to App Service on Key Vault scope.

4️⃣ Configure Authentication
App Service → Authentication → Enable

Identity provider → Microsoft

Use existing App Registration

5️⃣ Startup Command
gunicorn app:app
🔄 CI/CD Pipeline
Source control: GitHub

Deployment: GitHub Actions

Authentication: Managed Identity

Auto-deploy on every push to main branch

📊 Monitoring & Logging
Azure Application Insights enabled
