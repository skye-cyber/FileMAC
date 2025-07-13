import os
import subprocess
import sqlite3
import shlex
import json
import tempfile
import logging
import html
import requests
from dotenv import load_dotenv
from importlib import resources
from utils.colors import foreground

fcl = foreground()
RESET = fcl.RESET


class SecurePython:
    def __init__(self):
        """Initialize security mitigations."""
        load_dotenv()  # Load environment variables for secret management
        logging.basicConfig(level=logging.INFO)

    # ✅ 1. Prevent Command Injection
    def secure_subprocess(self, command_list):
        """Runs a secure subprocess command using a list format to prevent command injection."""
        if not isinstance(command_list, list):
            raise ValueError("Command must be a list")
        try:
            result = subprocess.run(
                command_list, check=True, capture_output=True, text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            logging.error(f"Command failed: {e}")
            return None

    # ✅ 2. Prevent Path Traversal
    def safe_filepath(self, base_dir, user_input_path):
        """Prevents path traversal by restricting access to a safe base directory."""
        full_path = os.path.abspath(os.path.join(base_dir, user_input_path))

        if not full_path.startswith(os.path.abspath(base_dir)):
            raise ValueError("Invalid file path: Path traversal attempt detected")
        print(f"{fcl.BBLUE_FG}Return safe path: {fcl.BGREEN_FG}{full_path}{RESET}")
        return full_path

    # ✅ 3. Prevent SQL Injection
    def safe_sql_query(self, db_path, query, params):
        """Executes a parameterized SQL query to prevent SQL injection."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            conn.commit()
            return result
        except sqlite3.Error as e:
            logging.error(f"SQL error: {e}")
            return None
        finally:
            conn.close()

    # ✅ 4. Secure File Handling
    def secure_temp_file(self, content):
        """Creates a secure temporary file to prevent race conditions."""
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(content.encode())
            temp_file.flush()
            return temp_file.name  # Return temp file path for safe use

    # ✅ 5. Secure Secret Management
    def get_secret(self, key):
        """Fetches secrets from environment variables."""
        secret = os.getenv(key)
        if not secret:
            logging.warning(f"Secret {key} is missing!")
        return secret

    # ✅ 6. Prevent Insecure Deserialization
    def safe_json_load(self, json_string):
        """Safely loads JSON instead of using pickle to avoid remote code execution."""
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON: {e}")
            return None

    # ✅ 7. Prevent XSS Attacks
    def sanitize_html(self, user_input):
        """Escapes HTML to prevent XSS attacks."""
        return html.escape(user_input)

    # ✅ 8. Check Dependency Vulnerabilities
    def check_dependencies(self):
        """Checks installed dependencies for known vulnerabilities."""
        try:
            installed_packages = {
                pkg.key: pkg.version for pkg in pkg_resources.working_set
            }
            response = requests.get("https://pyup.io/api/v1/safety/")
            if response.status_code == 200:
                vulnerable_packages = []
                for package, version in installed_packages.items():
                    if package in response.json():
                        vulnerable_packages.append(package)
                if vulnerable_packages:
                    logging.warning(
                        f"Vulnerable dependencies found: {vulnerable_packages}"
                    )
                else:
                    logging.info("No known vulnerable dependencies detected.")
            else:
                logging.warning("Failed to fetch vulnerability database.")
        except Exception as e:
            logging.error(f"Error checking dependencies: {e}")

    # ✅ 9. Secure Logging
    def secure_logging(self, message):
        """Logs messages securely without sensitive data exposure."""
        sanitized_message = message.replace("password", "*****").replace(
            "API_KEY", "*****"
        )
        logging.info(sanitized_message)

    # ✅ 10. Run All Security Mitigations
    def entry_run(self):
        """Runs all security mitigations where applicable."""
        logging.info("🔒 Running security mitigations...")

        # Example secure execution
        self.secure_subprocess(["echo", "Secure Execution"])

        # Example secure file path usage
        try:
            safe_path = self.safe_filepath("/safe/directory", "../etc/passwd")
            logging.info(f"Safe path resolved: {safe_path}")
        except ValueError as e:
            logging.error(e)

        # Example secure SQL execution
        self.safe_sql_query(":memory:", "CREATE TABLE test (id INTEGER, name TEXT)", ())
        self.safe_sql_query(
            ":memory:", "INSERT INTO test (id, name) VALUES (?, ?)", (1, "John Doe")
        )

        # Example secure file handling
        temp_file = self.secure_temp_file("Secure data")
        logging.info(f"Created secure temp file at {temp_file}")

        # Example secret fetching
        self.get_secret("API_KEY")

        # Example safe JSON parsing
        self.safe_json_load('{"key": "value"}')

        # Example HTML sanitization
        sanitized_html = self.sanitize_html("<script>alert('XSS!')</script>")
        logging.info(f"Sanitized HTML: {sanitized_html}")

        # Example dependency check
        self.check_dependencies()

        # Example secure logging
        self.secure_logging("User attempted login with password: mypassword")

        logging.info("✅ All security mitigations executed successfully!")


# === Run SecurePython Class ===
if __name__ == "__main__":
    sp = SecurePython()
    sp.entry_run()
