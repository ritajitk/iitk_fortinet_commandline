import re
import requests
import time
from getpass import getpass

# Constants
BASE_URL = 'http://www.example.com' #any arbitrary website for getting the magic_token
LOGIN_URL_TEMPLATE = "https://gateway.iitk.ac.in:1003/fgtauth?{}"
KEEPALIVE_URL_TEMPLATE = "https://gateway.iitk.ac.in:1003/keepalive?{}"
LOGOUT_URL_TEMPLATE = "https://gateway.iitk.ac.in:1003/logout?{}"

# Initialize a session
session = requests.Session()

def fetch_magic_token(url):
    """Fetches the magic token from the specified URL."""
    response = session.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    match = re.search(r'window\.location="https://gateway\.iitk\.ac\.in:1003/fgtauth\?(\w+)"', response.text)
    if match:
        return match.group(1)
    raise ValueError("Magic token not found.")

def login(magic_token,USERNAME,PASSWORD):
    """Logs in using the provided magic token."""
    login_url = LOGIN_URL_TEMPLATE.format(magic_token)
    data = {
            'magic': magic_token,
            'username': USERNAME,
            'password': PASSWORD
            }
    session.get(login_url)
    response = session.post(login_url, data=data)
    response.raise_for_status()  # Raise an error for bad responses
    return response.text

def fetch_keepalive_token(response_text):
    """Fetches the keepalive token from the response text."""
    match = re.search(r'window\.location="https://gateway\.iitk\.ac\.in:1003/keepalive\?(\w+)"', response_text)
    if match:
        return match.group(1)
    raise ValueError("Keepalive token not found.")

def keep_alive(keepalive_token):
    keepalive_url = KEEPALIVE_URL_TEMPLATE.format(keepalive_token)
    while True:
        try:
            session.get(keepalive_url)
            print("Keepalive sent successfully.")
        except Exception as e:
            print(f"Error during keepalive: {e}")
        time.sleep(600)  # Sleep for 10 minutes

def logout(keepalive_token):
    logout_url = LOGOUT_URL_TEMPLATE.format(keepalive_token)
    try:
        session.get(logout_url)
        print("Logged out successfully.")
    except Exception as e:
        print(f"Error during logout: {e}")

def main():
    try:
        username = input("Enter your IITK username: ")
        password = getpass("Enter your IITK password: ")
        # Step 1: Get the magic token
        magic_token = fetch_magic_token(BASE_URL)

        # Step 2: Log in with the magic token
        response_text = login(magic_token,username,password)

        # Step 3: Fetch the keepalive token
        keepalive_token = fetch_keepalive_token(response_text)

        # Step 4: Construct the keepalive and logout URLs
        keepalive_url = KEEPALIVE_URL_TEMPLATE.format(keepalive_token)
        logout_url = LOGOUT_URL_TEMPLATE.format(keepalive_token)

        print("Keepalive URL:", keepalive_url)
        print("Logout URL:", logout_url)

        # Start the keepalive loop
        keep_alive(keepalive_token)

    except KeyboardInterrupt:
        print("Interrupted by user. Logging out...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if keepalive_token:
            logout(keepalive_token)

if __name__ == "__main__":
    main()
