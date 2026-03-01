IP-grb is a Flask-based educational utility designed to demonstrate how web servers interact with client-side metadata and network headers. This project illustrates the concept of Browser Fingerprinting and HTTP Header Analysis—the process of collecting non-cookie data points to identify or analyze a unique network connection.

This tool is designed for developers and security researchers to learn about:

HTTP Request Headers: How servers parse information like User-Agent, X-Forwarded-For, and Accept-Language.

Metadata Synthesis: Combining JavaScript-based hardware detection with backend network logs.

Network Integrity: Using third-party APIs to verify IP reputation and detect VPNs, Proxies, or Tor nodes.

⚠️ Legal & Ethical Disclaimer

This software is for EDUCATIONAL AND RESEARCH PURPOSES ONLY.
The author does not condone the use of this tool for unauthorized tracking or malicious activities.
Gathering data on users without their explicit, informed consent is a violation of privacy and may be illegal under regulations like GDPR or CCPA.
The developer assumes no liability and is not responsible for any misuse or damage caused by this program.

🛠️ Features
 Adaptive OS Detection: Custom logic to identify Windows, macOS, Linux, and Termux environments.
Hardware Fingerprinting: JavaScript-driven collection of screen resolution, touch support, and device orientation.
Network Intelligence: Integration with ip-api.com to detect Hosting/DataCenter IPs and VPN status.
Cross-Platform CLI: A beautiful, emoji-supported terminal output for real-time monitoring of incoming requests.
Persistent Logging: All sessions are recorded locally in creds.txt for post-analysis.





🚀 Installation & Setup

Follow these steps to set up the environment and run the IP-grb server on your local machine or a VPS.
1. Clone the Repository

Open your terminal and run the following command to download the source code:
Bash

    git clone https://github.com/eRdI3435/IP-Grabber.git
    cd IP-grb

2. Create a Virtual Environment

It is best practice to use a virtual environment to avoid conflicts with other Python packages:
Bash

     python3 -m venv venv

3. Activate the Environment

You must activate the virtual environment before installing the requirements:
On Linux / macOS / Termux:

     source venv/bin/activate
     

4. Install Required Dependencies

This project requires Flask and requests. Install them using the provided requirements file:
Bash

    pip3 install -r requirements.txt

5. Run the Application

Start the Flask server by running the main script:
Bash

     python3 ip.py

🌐 Making it Public

By default, the server runs on http://127.0.0.1:5000 (your local machine). To test this with external devices, you can use a service like Cloudflare Tunnel:

    cloudflared tunnel --url http://localhost:5000

Copy the .trycloudflare.com link provided and visit it to see the tool in action.
