# SSH Brute Force Simulator 🥷

A Python GUI utility built to simulate dictionary-based credential stuffing and brute-force attacks against SSH (Port 22). Designed for SOC portfolio demonstration to illustrate attack vectors and the necessity of rate-limiting and complex password policies.

**Features:**
* Iterates through simulated password wordlists dynamically.
* Employs Python `threading` to keep the UI fully responsive during the attack loop.
* Uses `time.sleep()` to simulate the realistic cryptographic latency of SSH authentication handshakes.
* Features a stylized SOC terminal output with real-time success/failure color coding.

*Built as Day 11 of a 30-Day Network Engineering & Security portfolio streak.*
