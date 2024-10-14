# Indian Institute of Technology Kanpur (IITK) Fortinet Command-Line Authentication Tool

## Overview

This repository provides a command-line utility, auth.py, which allows users to log in to the IITK Fortinet firewall using their IITK credentials. This script is particularly useful for users who are working on a server or any environment where they don't have access to a graphical user interface (GUI). Additionally, it sends a keep-alive request every 10 minutes to maintain the session, and upon termination, it automatically logs the user out.

## Features

- Command-line Authentication: Log in to the IITK Fortinet firewall without needing a web browser.
- Keep-Alive Functionality: Sends keep-alive requests every 10 minutes to maintain the session.
- Automatic Logout: On termination, the script logs out automatically, ensuring session security.

## Requirements
- Network: You must be connected to the IITK network.
- DNS Configuration: Your DNS servers should be set to 172.31.1.130 and 172.31.1.1.
- No DNS-over-HTTPS: DNS-over-HTTPS should be disabled at the operating system level.

## Installation

1. Clone the repository:

    git clone https://github.com/ritajitk/iitk_fortinet_commandline.git
    cd iitk_fortinet_commandline

2. Install required dependencies:

        pip install requests

## Usage

1. Run the script:

        python auth.py

2. You will be prompted to enter your IITK username and password:

        Enter your IITK username: your_username
        Enter your IITK password: 

    > Note: The password input is hidden for security, thanks to the `getpass` module.

3. Once you’ve entered your credentials, the script will:
    - Fetch the necessary magic token for login.
    - Log in with the provided credentials.
    - Send keep-alive requests every 10 minutes to maintain the session.
    - Display the keep-alive and logout URLs.
    - To end the session, press Ctrl+C to log out and terminate the program.

## Example Output

You’ll see output similar to the following:

    Keepalive URL: https://gateway.iitk.ac.in:1003/keepalive?16_string_token
    Logout URL: https://gateway.iitk.ac.in:1003/logout?16_string_token
    Keepalive sent successfully.
    Keepalive sent successfully.
    ...

To terminate the program, press Ctrl+C, and it will log you out automatically:

    Interrupted by user. Logging out...
    Logged out successfully.

## Code Structure

- `fetch_magic_token(url)`: Retrieves a "magic token" from the specified URL, which is required for the authentication process.
- `login(magic_token,usename,password)`: Logs in to the IITK Fortinet firewall using the provided magic token and the user's credentials.
- `fetch_keepalive_token(response_text)`: Extracts the keep-alive token needed to maintain the session.
- `keep_alive(keepalive_token)`: Sends a keep-alive request every 10 minutes to keep the session active.
- `logout(keepalive_token)`: Logs out from the firewall, ending the session.
- `main()`: Orchestrates the overall workflow, including login, keep-alive, and logout functionalities.


## Security Considerations

- **Credentials**: The script prompts for the username and password at runtime, so they are not stored anywhere.

- **Network Security**: Since the credentials are sent to gateway.iitk.ac.in over HTTPS, they are encrypted during transmission. 

## Contributing

Feel free to submit issues or pull requests if you'd like to improve the code or add additional features. Please make sure to follow best practices and test your changes before submitting.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Disclaimer
This program is an independent project and is not affiliated with, endorsed by, or officially supported by IIT Kanpur. Use this tool at your own discretion. The author assumes no responsibility for any misuse or issues arising from the use of this script.
