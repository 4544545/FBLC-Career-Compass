import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import customtkinter
import requests

# Define the scopes your application needs.
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile",  
    "https://www.googleapis.com/auth/userinfo.email",
    "openid"
]

TOKEN_PATH = "token.json"
CREDENTIALS_PATH = "credentials.json"


def authenticate():
    """Handles Google authentication and returns valid credentials."""
    creds = None

    # # Try to load existing credentials
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)


    #If no valid credentials, perform OAuth authentication
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the new credentials
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    return creds



def get_user_info():
    """Fetches the authenticated user's name and ID."""
    creds = authenticate()
    service = build('people', 'v1', credentials=creds)

    # Request name and ID
    profile = service.people().get(resourceName='people/me', personFields='names,metadata,emailAddresses').execute()

    # Extract name and email
    name = profile.get('names', [{}])[0].get('displayName', "Unknown User")

    email = profile.get('emailAddresses', [{}])[0].get('value', "Unknown Email")


    # Extract ID and email
    user_id = profile.get('metadata', {}).get('sources', [{}])[0].get('id', "Unknown ID")

    email = profile.get('emailAddresses', [{}])[0].get('value', "Unknown Email")

    return name, user_id, email


# def run_app(user_name, user_id, email):
#     """Displays the User Name and ID in a Tkinter window."""
#     root = customtkinter.ctk_tk()
#     root.title("User Info")
#     root.geometry("500x600")


#     label = customtkinter.CTkLabel(root, text=f"Welcome, {user_name}!", font=("Arial", 14))
#     label.pack(pady=10)

#     id_label = customtkinter.CTkLabel(root, text=f"User ID: {user_id}", font=("Arial", 12))
#     id_label.pack(pady=10)

#     email_label = customtkinter.CTkLabel(root, text=f"User Email: {email}", font=("Arial", 12))
#     email_label.pack(pady=10)

#     button = customtkinter.CTkButton(root, text="Exit", command=root.quit)
#     button.pack(pady=10)

    root.mainloop()


def log_in():
    """Authenticates and displays the user's name & ID."""
    user_name, user_id, email = get_user_info()

    print("Authentication successful!")
    # run_app(user_name, user_id, email)


if __name__ == "__main__":
    log_in()
