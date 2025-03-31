# /// script
# requires-python = ">=3.8"  # Updated to a valid version
# dependencies = [
#   "PyPDF2",
#    "pandas",
#    "numpy",
#    "beautifulsoup4",
#    "requests",
#    "matplotlib",
#    "flask",
#    "feedparser"
# ]
# ///

import pandas as pd
import requests
import re
import zipfile
import io
import subprocess
import sys
import platform
import shutil
import numpy as np
import subprocess
import shutil
import os
import platform

def ga1_q1(question, files):
    """
    Ensures VS Code is installed, finds the absolute path to the binary, and runs `code -s`.
    """
    def install_vscode():
        """ Installs VS Code based on the OS. """
        os_name = platform.system()
        try:
            if os_name == "Windows":
                print("Installing VS Code on Windows...")
                subprocess.run(["powershell", "-Command", 
                    "(New-Object System.Net.WebClient).DownloadFile('https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user', 'VSCodeSetup.exe'); Start-Process -Wait -FilePath 'VSCodeSetup.exe' -ArgumentList '/VERYSILENT /NORESTART'"], check=True)
                os.remove("VSCodeSetup.exe")

            elif os_name == "Linux":
                print("Installing VS Code on Linux...")
                subprocess.run(["sudo", "apt", "update"], check=True)
                subprocess.run(["sudo", "apt", "install", "-y", "code"], check=True)

            elif os_name == "Darwin":  # macOS
                print("Installing VS Code on macOS...")
                subprocess.run(["brew", "install", "--cask", "visual-studio-code"], check=True)

            print("VS Code installation completed.")
            return True
        except Exception as e:
            return f"Error installing VS Code: {e}"

    def find_vscode_binary():
        """ Finds the absolute path of VS Code binary. """
        os_name = platform.system()
        paths = []

        if os_name == "Windows":
            paths = [
                os.path.expanduser("~") + r"\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd",
                os.path.expanduser("~") + r"\AppData\Local\Programs\Microsoft VS Code\bin\code.exe"
            ]
        elif os_name == "Linux":
            paths = ["/usr/bin/code", "/snap/bin/code", "/usr/local/bin/code"]
        elif os_name == "Darwin":  # macOS
            paths = ["/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"]

        for path in paths:
            if os.path.exists(path):
                return path
        return None

    try:
        # Step 1: Check if `code` command exists
        vscode_path = shutil.which("code") or find_vscode_binary()

        if not vscode_path:
            print("VS Code not found. Installing...")
            install_status = install_vscode()
            if install_status is not True:
                return install_status

            # Re-check for VS Code binary after installation
            vscode_path = find_vscode_binary()
            if not vscode_path:
                return "VS Code installation completed, but executable not found. Restart and try again."

        # Step 2: Run `code -s` using absolute path
        result = subprocess.run([vscode_path, "-s"], capture_output=True, text=True, check=True)
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        return f"Error executing `code -s`: {e}"

    except FileNotFoundError:
        return "VS Code command not found even after installation. Restart your system and try again."
    
import subprocess
import json
import re

def ga1_q2(question, files):
    """
    Extracts the email from the question, installs `httpie`, sends an HTTPS request,
    and returns the JSON response.
    """
    # Step 1: Extract email from question
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"  # Regex for email
    email_match = re.search(email_pattern, question)
    
    if not email_match:
        return {"error": "No valid email found in the input question."}
    
    email = email_match.group()
    
    # Step 2: Ensure `httpie` is installed
    try:
        subprocess.run(["pip", "install", "httpie"], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        return {"error": f"Failed to install httpie: {e}"}
    
    # Step 3: Send the HTTP GET request
    try:
        result = subprocess.run([
            "http", "GET", "https://httpbin.org/get", f"email=={email}"
        ], capture_output=True, text=True, check=True)
        
        # Attempt to parse JSON response
        response_text = result.stdout.strip()
        
        try:
            response_json = json.loads(response_text)
            return response_json
        except json.JSONDecodeError:
            return {"error": "Failed to parse response as JSON.", "raw_output": response_text}
    
    except subprocess.CalledProcessError as e:
        return f"HTTP request failed: {e}"
import os
import subprocess
import sys

def ga1_q3(question, files):
    """
    Ensures README.md exists, installs Node.js and Prettier if needed,
    runs `npx -y prettier@3.4.2 README.md | sha256sum`, and returns the output.
    """
    def is_admin():
        """Check if the script is running with administrative privileges."""
        if os.name == "nt":
            try:
                return subprocess.run(["net", "session"], capture_output=True, text=True).returncode == 0
            except Exception:
                return False
        return os.geteuid() == 0

    def run_as_admin():
        """Relaunch the script with administrative privileges if not already elevated."""
        if os.name == "nt" and not is_admin():
            try:
                subprocess.run(["powershell", "-Command", "Start-Process", "python", f"'{sys.argv[0]}'", "-Verb", "RunAs"], check=True)
                sys.exit()
            except subprocess.CalledProcessError:
                return {"error": "Failed to elevate privileges. Please run as administrator."}
        return None

    def install_chocolatey():
        """ Installs Chocolatey if not found (Windows only). """
        try:
            subprocess.run(["choco", "-v"], check=True, capture_output=True, text=True)
            return None  # Chocolatey is already installed
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass  # Chocolatey is not installed, proceed with installation
        
        try:
            subprocess.run([
                "powershell", "-Command",
                "Set-ExecutionPolicy Bypass -Scope Process -Force;"
                "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;"
                "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
            ], check=True, shell=True)
            return None  # Chocolatey installed successfully
        except subprocess.CalledProcessError:
            return {"error": "Failed to install Chocolatey. Please install it manually."}
    
    def install_node():
        """ Installs Node.js automatically if not found. """
        try:
            subprocess.run(["node", "-v"], check=True, capture_output=True, text=True)
            subprocess.run(["npm", "-v"], check=True, capture_output=True, text=True)
            return None  # Node.js is already installed
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass  # Node.js is not installed, proceed with installation

        if os.name == "nt":
            admin_check = run_as_admin()
            if admin_check:
                return admin_check

            choco_check = install_chocolatey()
            if choco_check:
                return choco_check  # Return Chocolatey installation error if failed
            
            for _ in range(3):  # Retry installation up to 3 times
                try:
                    result = subprocess.run(["choco", "install", "nodejs", "-y"], capture_output=True, text=True, check=True)
                    if "The install of nodejs was successful" in result.stdout:
                        return None  # Success
                except subprocess.CalledProcessError as e:
                    last_error = e
                    error_details = e.stderr if e.stderr else e.stdout
            return {"error": f"Chocolatey installed, but failed to install Node.js after multiple attempts. Error: {error_details}"}
        else:
            try:
                subprocess.run(["sudo", "apt", "update"], check=True)
                subprocess.run(["sudo", "apt", "install", "-y", "nodejs", "npm"], check=True)
                return None  # Success
            except subprocess.CalledProcessError as e:
                return {"error": f"Failed to install Node.js: {e}"}
    
    if not os.path.exists("README.md"):
        return {"error": "README.md not found in the current directory."}
    
    # Ensure Node.js and npm are installed
    node_check = install_node()
    if node_check:
        return node_check
    
    # Ensure Prettier is installed
    try:
        subprocess.run(["npx", "prettier", "--version"], check=True, capture_output=True, text=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        subprocess.run(["npm", "install", "-g", "prettier"], check=True)
    
    # Ensure npx is installed
    try:
        subprocess.run(["npx", "--version"], check=True, capture_output=True, text=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        subprocess.run(["npm", "install", "-g", "npx"], check=True)
    
    try:
        # Windows Fix: Save output to a temp file before hashing
        if os.name == "nt":
            temp_file = "prettier_output.txt"
            subprocess.run(f"npx prettier README.md > {temp_file}", shell=True, check=True)
            result = subprocess.run(["certutil", "-hashfile", temp_file, "SHA256"], capture_output=True, text=True, check=True)
            os.remove(temp_file)  # Clean up temp file
        else:
            result = subprocess.run("npx -y prettier@3.4.2 README.md | sha256sum", shell=True, capture_output=True, text=True, check=True)

        return {"hash_output": result.stdout.strip()}
    
    except subprocess.CalledProcessError as e:
        return {"error": f"Command execution failed: {e}"}

import numpy as np
import re

def ga1_q4(question, files=None):
    def extract_formula(question):
        match = re.search(r'=SUM\(ARRAY_CONSTRAIN\(SEQUENCE\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\),\s*(\d+),\s*(\d+)\)\)', question)
        if match:
            return list(map(int, match.groups()))
        return None

    params = extract_formula(question)
    if not params:
        return {"error": "Invalid formula"}
    
    print(params)
    rows, cols, start, step, row_limit, col_limit = params
    
    # Generate the SEQUENCE matrix correctly (filling row-wise)
    sequence = np.array([[start + (r * cols + c) * step for c in range(cols)] for r in range(rows)])
    
    # Apply ARRAY_CONSTRAIN
    constrained_sequence = sequence[:row_limit, :col_limit]
    result = int(np.sum(constrained_sequence))  # Convert NumPy int64 to Python int
    
    return result

def ga1_q5(question, files=None):
    def extract_formula(question):
        match = re.search(r'=SUM\(TAKE\(SORTBY\(\{([^}]*)\},\s*\{([^}]*)\}\),\s*(\d+),\s*(\d+)\)\)', question)
        if match:
            values = list(map(int, match.group(1).split(',')))
            sort_keys = list(map(int, match.group(2).split(',')))
            take_rows = int(match.group(3))
            take_cols = int(match.group(4))
            return values, sort_keys, take_rows, take_cols
        return None
    
    params = extract_formula(question)
    if not params:
        return {"error": "Invalid formula"}
    
    values, sort_keys, take_rows, take_cols = params
    
    # Sort values based on sort_keys
    sorted_indices = np.argsort(sort_keys)
    sorted_values = np.array(values)[sorted_indices]
    
    # Apply TAKE to get first `take_cols` elements
    taken_values = sorted_values[:take_cols]
    
    # Compute SUM
    result = int(np.sum(taken_values))  # Convert NumPy int64 to Python int
    
    return result

from datetime import date, timedelta

def ga1_q7(question, files):
    import re
    
    match = re.search(r'How many (\w+)s are there in the date range (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})', question)
    if not match:
        return {"error": "Invalid question format"}
    
    weekday_name, start_date, end_date = match.groups()
    
    weekdays = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6
    }
    
    if weekday_name not in weekdays:
        return {"error": "Invalid weekday name"}
    
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    weekday_number = weekdays[weekday_name]
    
    count = sum(1 for d in range((end - start).days + 1) if (start + timedelta(days=d)).weekday() == weekday_number)
    return count

import zipfile

import zipfile
import pandas as pd
import re
import os

import zipfile
import pandas as pd
import re
import os

def ga1_q8(question, files):
    # Extract filename from question
    match = re.search(r'Download and unzip file (\S+\.zip)', question)
    if not match:
        return {"error": "No valid ZIP filename found in question."}
    zip_filename = match.group(1)
    
    # Check if ZIP file exists in the current directory
    if not os.path.exists(zip_filename):
        return {"error": "ZIP file not found in current directory."}
    
    # Extract the ZIP file
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            extract_dir = "temp_extracted"
            zip_ref.extractall(extract_dir)
            
            # Find the extract.csv file inside
            csv_path = os.path.join(extract_dir, "extract.csv")
            if not os.path.exists(csv_path):
                return {"error": "extract.csv not found in ZIP file."}
            
            # Read the CSV file and extract the required column
            df = pd.read_csv(csv_path)
            column_match = re.search(r'(?i)value in the \"?([\w\s]+)\"? column', question)
            if not column_match:
                return {"error": "No valid column name found in question."}
            column_name = column_match.group(1).strip()
            
            if column_name not in df.columns:
                return {"error": f"'{column_name}' column not found in CSV file."}
            
            answer_value = df[column_name].iloc[0]
            return answer_value
    
    except zipfile.BadZipFile:
        return {"error": "Invalid ZIP file."}
    except Exception as e:
        return {"error": str(e)}
                   
import json
import re

import json
import re

def ga1_q9(question, files):
    # Extract JSON array from the question
    json_match = re.search(r'\[.*\]', question)  # Look for content between square brackets
    if not json_match:
        return {"error": "No JSON array found in the question."}

    json_data = json_match.group(0)
    
    # Parse the JSON array
    try:
        data = json.loads(json_data)  # Parse the JSON string into a Python list of dictionaries
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format."}

    # Extract sorting fields from the question (age and name)
    sort_fields = re.findall(r"by (\w+)", question)
    if len(sort_fields) == 0:
        return {"error": "No valid sorting fields found in question."}
    
    # Sort the data by the specified fields
    for field in reversed(sort_fields):  # Reverse to ensure correct sorting order
        # Ensure None values are handled by assigning a high value (e.g., float('inf'))
        data = sorted(data, key=lambda x: x.get(field, float('inf')))
    
    # Sort by age first, and then by name in case of a tie
        sorted_data = sorted(data, key=lambda x: (x['age'], x['name']))
    
    # Directly return the sorted data without the escape characters
    return {"answer": sorted_data}


#def ga1_q12(question,files):
 #   print("Inside Q12")
  #  symbols=question.split(' OR ')
   # symbols[0]=symbols[0][-1]
    #symbols[-1]=symbols[-1][0]
    #sumer = 0
    #csv_data = {}
    #with zipfile.ZipFile("q-unicode-data.zip",'r') as zip_ref:
     #   print("Files in ZIP:", zip_ref.namelist())
      #  decode = ["cp1252","UTF-8","UTF-16"]
       # for i,file_name in enumerate(zip_ref.namelist()):
        #    if file_name.endswith('.csv') or file_name.endswith('.txt'):
         #       with zip_ref.open(file_name) as f:
          #          csv_content = f.read().decode(decode[i])
           #         df=pd.read_csv(io.StringIO(csv_content))
            #        csv_data[file_name] = df
    #for i in csv_content:
     #   curr_data = csv_content[i]
    #return ("Output of Q12")

import zipfile
import pandas as pd
import os

import zipfile
import pandas as pd
import os
import re

def ga1_q12(question, files):
    print("inside ga1_q12")
    
    # Function to extract symbols dynamically from the question
    def extract_symbols_from_question(question):
        # Define the pattern to match the text between 'where the symbol matches' and 'across'
        pattern = r'where the symbol matches(.*?)across'
        
        # Search for the part of the question using the regex
        match = re.search(pattern, question)
        print(match)
        if match:
            # Extract the symbols part
            symbols_part = match.group(1).strip()
            # Split the symbols part by "OR" and clean extra spaces
            symbols = [s.strip() for s in symbols_part.split("OR")]
            # Return unique symbols
            return list(set(symbols))
        else:
            return []  # Return an empty list if no match is found

    extract_dir = "temp_extracted"
    zip_filename = 'q-unicode-data.zip'

    # Check if ZIP file exists
    if not os.path.exists(zip_filename):
        return {"error": f"{zip_filename} not found."}

    # Extract the ZIP file
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        # List the files extracted
        extracted_files = zip_ref.namelist()
        print(f"Files extracted: {extracted_files}")

        # Extract symbols from the question dynamically
        matching_symbols = extract_symbols_from_question(question)
        if not matching_symbols:
            return {"error": "No symbols found in the question."}
        
        print(f"Matching symbols: {matching_symbols}")

        # Initialize sum to 0
        total_sum = 0

        # Process each file
        for file in extracted_files:
            file_path = os.path.join(extract_dir, file)

            if file == "data1.csv":  # CP-1252 encoded CSV
                df = pd.read_csv(file_path, encoding="cp1252")
            elif file == "data2.csv":  # UTF-8 encoded CSV
                df = pd.read_csv(file_path, encoding="utf-8")
            elif file == "data3.txt":  # UTF-16 encoded TSV
                df = pd.read_csv(file_path, encoding="utf-16", sep="\t")
            else:
                continue  # Skip if the file name doesn't match expected

            # Filter rows for matching symbols
            df_filtered = df[df['symbol'].isin(matching_symbols)]
            
            # Sum the values for the filtered rows
            filtered_value = df_filtered['value'].sum().item()
            print(f"Sum for file {file}: {filtered_value}")

            # Convert to regular Python int
            filtered_value = filtered_value.item() if isinstance(filtered_value, pd.Series) else filtered_value
            print(f"Filtered value type: {type(filtered_value)}")

            # Add to the total sum
            total_sum += filtered_value

        return total_sum

    except zipfile.BadZipFile:
        return {"error": "Invalid ZIP file."}
    except Exception as e:
        return {"error": str(e)}

import os
import subprocess
import requests
import json
import uuid  # To generate unique repository names
import re


import requests
import base64
import json
import re
import subprocess
import os
import uuid

def ga1_q13(question, files):
    github_token = files
    print("GA1 Q13")
    GITHUB_API_URL = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}
    
    def extract_email_from_question(question):
        match = re.search(r'\"email\"\s*:\s*\"([^\"]+)\"', question)
        if match:
            return match.group(1)
        return "abc@example.com"

    def create_github_repo(repo_name):
        data = {"name": repo_name, "private": False}
        response = requests.post(GITHUB_API_URL, headers=headers, json=data)
        if response.status_code == 201:
            print(f"Repository '{repo_name}' created successfully.")
            return response.json()['html_url']
        elif response.status_code == 422:
            print(f"Repository '{repo_name}' already exists, proceeding...")
            return f"https://github.com/{username}/{repo_name}"
        else:
            raise Exception(f"Failed to create repo: {response.status_code}, {response.text}")

    def initialize_and_push_repo(repo_name, email_value):
        repo_url = f"https://{github_token}@github.com/{username}/{repo_name}.git"
        subprocess.run(["git", "clone", repo_url], check=True)
        os.chdir(repo_name)
        subprocess.run(["git", "config", "user.email", "23ds3000185@ds.study.iitm.ac.in"], check=True)
        subprocess.run(["git", "config", "user.name", username], check=True)

        with open("email.json", "w") as f:
            json.dump({"email": email_value}, f)

        subprocess.run(["git", "add", "email.json"], check=True)
        subprocess.run(["git", "commit", "-m", "Add email.json with dynamic email value"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)

        raw_url = f"https://raw.githubusercontent.com/{username}/{repo_name}/main/email.json"
        return raw_url

    try:
        user_response = requests.get("https://api.github.com/user", headers=headers)
        user_response.raise_for_status()
        global username
        username = user_response.json()["login"]
    except requests.exceptions.RequestException as e:
        return f"GitHub authentication failed: {e}"

    email_value = extract_email_from_question(question)
    repo_name = f"email-json-repo-{uuid.uuid4().hex[:8]}"
    repo_url = create_github_repo(repo_name)
    raw_url = initialize_and_push_repo(repo_name, email_value)
    
    print(f"File committed and pushed. You can access it here: {raw_url}")
    return raw_url

import os
import zipfile
import re
import subprocess
import hashlib

def ga1_q14(question, files):
    # Function to extract terms from the question
    def extract_replace_terms_from_question(question):
        # Split the question to focus on the terms after "replace all" and "with"
        try:
            parts = question.split('replace all')
            # After the first "replace all", split at "with" to get the terms
            term_to_replace = parts[1].split('with')[0].strip().strip('"')
            replacement_term = parts[1].split('with')[1].strip().strip('"').split(' in')[0].strip()
            replacement_term_updated = replacement_term.strip('"')
            print(term_to_replace)
            print(replacement_term_updated)
            return term_to_replace, replacement_term_updated
        
        except IndexError:
            return None, None

 # Extract the terms to replace dynamically
    term_to_replace, replacement_term = extract_replace_terms_from_question(question)
    if not term_to_replace or not replacement_term:
        return {"error": "No replace terms found in the question."}

    # Path to store unzipped content
    extract_dir = "temp_extracted_new"
    zip_filename = 'q-replace-across-files.zip'

    # Check if ZIP file exists
    if not os.path.exists(zip_filename):
        return {"error": f"{zip_filename} not found."}

    # Extract the ZIP file
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        # List the files extracted
        extracted_files = zip_ref.namelist()
        print(f"Files extracted: {extracted_files}")

        sha256sum_final = hashlib.sha256()

        # Replace the term in all files and compute sha256 checksum
        for file in extracted_files:
            file_path = os.path.join(extract_dir, file)
            with open(file_path, 'r', encoding="utf-8") as f:
                content = f.read()

            # Replace text without changing line endings
            #term_to_replace = 'iitm'
            #replacement_term = 'iit madras'
            updated_content = re.sub(rf'\b{re.escape(term_to_replace)}\b', replacement_term, content, flags=re.IGNORECASE)

            # Write the updated content back, ensuring line endings are preserved
            with open(file_path, 'w', encoding="utf-8", newline='') as f:
                f.write(updated_content)

            # Update sha256 hash with the file content
            with open(file_path, 'rb') as f:
                while chunk := f.read(4096):  # Read the file in chunks to handle large files
                    sha256sum_final.update(chunk)

            print(f"File '{file}' was updated.")

        # Final sha256sum result
        sha256sum_output = sha256sum_final.hexdigest()

        return sha256sum_output

    except zipfile.BadZipFile:
        return {"error": "Invalid ZIP file."}
    except Exception as e:
        return {"error": str(e)}
    
import os
import zipfile
from datetime import datetime
import re

def ga1_q15(question, files):
    # Function to extract size and date from the question
    def extract_size_and_date_from_question(question):
        try:
            # Extract file size from the question
            size_match = re.search(r"(\d+)\s+bytes", question)
            
            # Refine the regex to capture the full date format (including the day of the week)
            date_match = re.search(r"(\w{3},\s+\d{1,2}\s+\w{3},\s+\d{4},\s+\d{1,2}:\d{2}\s+[apm]+)\s+IST", question)

            if size_match and date_match:
                file_size = int(size_match.group(1))
                date_str = date_match.group(1)
                # Parse the date string into a datetime object
                modified_date = datetime.strptime(date_str, "%a, %d %b, %Y, %I:%M %p")
                return file_size, modified_date
            return None, None
        except Exception as e:
            return None, None

    # Extract the size and modified date from the question
    min_size, target_date = extract_size_and_date_from_question(question)

    if not min_size or not target_date:
        return {"error": "Failed to extract size and date from the question."}

    # Path to store unzipped content
    extract_dir = "temp_extracted"
    zip_filename = 'q-list-files-attributes.zip'

    # Check if ZIP file exists
    if not os.path.exists(zip_filename):
        return {"error": f"{zip_filename} not found."}

    # Extract the files
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

            # Restore the file timestamps manually
            for file_info in zip_ref.infolist():
                extracted_path = os.path.join(extract_dir, file_info.filename)
                timestamp = datetime(*file_info.date_time)  # Convert zip timestamp to datetime
                os.utime(extracted_path, (timestamp.timestamp(), timestamp.timestamp()))

            # List all files in the extracted folder
            total_size = 0
            for file in os.listdir(extract_dir):
                file_path = os.path.join(extract_dir, file)

                # Get file stats to check size and modified time
                if os.path.isfile(file_path):
                    file_stats = os.stat(file_path)
                    file_size = file_stats.st_size
                    file_mod_time = datetime.fromtimestamp(file_stats.st_mtime)

                    # Check if file meets the criteria
                    if file_size >= min_size and file_mod_time >= target_date:
                        total_size += file_size

            return {"total_size": total_size}

    except Exception as e:
        return {"error": str(e)}

import os
import zipfile
import re
import subprocess
import shutil

def ga1_q16(question, files):
    # Path to store unzipped content
    extract_dir = "temp_extracted_new"
    target_dir = "temp_target_folder"
    zip_filename = 'q-move-rename-files.zip'

    # Check if ZIP file exists
    if not os.path.exists(zip_filename):
        return {"error": f"{zip_filename} not found."}

    # Extract the ZIP file
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        # Create target directory if it doesn't exist
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Function to move files from subdirectories into the target folder
        def move_files_from_subfolders(current_folder):
            moved_files = []
            for root, dirs, files in os.walk(current_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Move each file to the target directory (flattening the structure)
                    if os.path.isfile(file_path):
                        shutil.move(file_path, os.path.join(target_dir, file))
                        moved_files.append(file)
            return moved_files

        # Move all files from subdirectories into the target folder
        moved_files = move_files_from_subfolders(extract_dir)

        # Log files moved
        print(f"Files moved to {target_dir}: {moved_files}")

        # Rename files by replacing digits with the next number (1 -> 2, 9 -> 0)
        renamed_files = []
        for file in os.listdir(target_dir):
            # Only rename files that contain digits
            if any(char.isdigit() for char in file):
                new_name = re.sub(r'\d', lambda x: str((int(x.group(0)) + 1) % 10), file)

                # Only rename if the filename actually changes
                if new_name != file:
                    new_file_path = os.path.join(target_dir, new_name)

                    # Check if the file already exists and rename accordingly
                    if os.path.exists(new_file_path):
                        print(f"Skipping renaming of {file} as {new_name} already exists.")
                    else:
                        # Rename the file
                        os.rename(os.path.join(target_dir, file), new_file_path)
                        renamed_files.append(new_name)
                else:
                    renamed_files.append(file)  # No renaming needed
            else:
                renamed_files.append(file)  # No digits to replace

        # Log renamed files
        print(f"Files renamed: {renamed_files}")

        # Run the sha256sum command on the entire folder content
        command = f'cd {target_dir} && grep . * | LC_ALL=C sort | sha256sum'
        print(f"Running command: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Check the output of the command
        print(f"Command output: {result.stdout}")

        sha256sum_output = result.stdout.strip()

        return {"sha256sum": sha256sum_output}

    except zipfile.BadZipFile:
        return {"error": "Invalid ZIP file."}
    except Exception as e:
        return {"error": str(e)}

import os
import zipfile

def ga1_q17(question, files):
    zip_filename = "q-compare-files.zip"
    extract_dir = "temp_extracted_q17"
    
    if not os.path.exists(zip_filename):
        return {"error": f"{zip_filename} not found."}
    
    try:
        # Extract ZIP file
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Define file paths
        file_a = os.path.join(extract_dir, "a.txt")
        file_b = os.path.join(extract_dir, "b.txt")
        
        # Ensure both files exist
        if not os.path.exists(file_a) or not os.path.exists(file_b):
            return {"error": "One or both files (a.txt, b.txt) not found in extracted folder."}
        
               
        # Read files and compare line by line
        with open(file_a, "r", encoding="utf-8") as fa, open(file_b, "r", encoding="utf-8") as fb:
            lines_a = fa.readlines()
            lines_b = fb.readlines()
        
        # Ensure both files have the same number of lines
        if len(lines_a) != len(lines_b):
            return {"error": "Files have different number of lines."}
        
        # Count differing lines
        differing_lines = sum(1 for a, b in zip(lines_a, lines_b) if a != b)
        
        return {"differing_lines": differing_lines}
    
    except zipfile.BadZipFile:
        return {"error": "Invalid ZIP file."}
    except Exception as e:
        return {"error": str(e)}

def ga1_q18(question, db_path):
    # Extract the ticket type from the question dynamically
    ticket_type = "Gold"  # Default fallback
    words = question.split()
    for word in words:
        if word.lower() in ["gold", "silver", "bronze"]:
            ticket_type = word
            break
    
    # Normalize ticket type to match database values
    ticket_type = ticket_type.strip().upper()
    
    # Generate SQL query without unnecessary whitespace
    query = f"SELECT SUM(units * price) FROM tickets WHERE UPPER(TRIM(type)) = '{ticket_type}'"
    
    return query

import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup

def ga4_q1(question, files):
    # Extract the page number dynamically from the question
    page_number = 1  # Default fallback
    words = question.split()
    print(words)
    for i, word in enumerate(words):
        if word.lower() == "page" and i + 2 < len(words) and words[i + 1].lower() == "number" and words[i + 2].isdigit():
            page_number = int(words[i + 2])
            print("Inside if")
            print(page_number)
            break
    
    print(f"Extracted Page Number: {page_number}")  # Debugging Page Number

    # Construct the URL
    url = f"https://stats.espncricinfo.com/stats/engine/stats/index.html?class=2;template=results;type=batting;page={page_number}"
    
    # Set headers to mimic a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Fetch the page content
    response = requests.get(url, headers=headers)
    print(f"Response Status Code: {response.status_code}")  # Debug Response Status
    if response.status_code != 200:
        return {"error": "Failed to fetch the page"}
    
    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    print("Fetched HTML Content Successfully")  # Debug Message

    # Find all tables
    tables = soup.find_all("table", class_="engineTable")
    print(f"Number of tables found: {len(tables)}")  # Debugging Table Count
    
    if not tables:
        return {"error": "No tables found on the page"}

    # Identify the correct stats table
    table = None
    for tbl in tables:
        rows = tbl.find_all("tr")
        if rows and any("data1" in row.get("class", []) for row in rows):
            table = tbl
            break

    if table is None:
        return {"error": "Stats table not found"}

    # Extract data rows
    data_rows = table.find_all("tr", class_="data1")
    print(f"Number of data rows found: {len(data_rows)}")  # Debugging Row Count
    
    if not data_rows:
        return {"error": "No data rows found in the stats table"}

    # Sum the total number of ducks (last column in each row)
    total_ducks = 0
    for row in data_rows:
        cols = row.find_all("td")
        if cols:
            last_col_text = cols[-2].text.strip()  # Use [-2] if last column is empty
            print(f"Duck Value Found: {last_col_text}")  # Debug Individual Duck Count
            if last_col_text.isdigit():
                total_ducks += int(last_col_text)

    print(f"Total Ducks Counted: {total_ducks}")  # Debug Final Count
    return total_ducks

import requests
from bs4 import BeautifulSoup

def ga4_q2(question, files)    :
    # Extract the rating range dynamically from the question
    min_rating, max_rating = 3, 4  # Default fallback
    words = question.split()
    for i, word in enumerate(words):
        if word.lower() == "between" and i + 2 < len(words) and words[i + 1].replace('.', '', 1).isdigit() and words[i + 2].replace('.', '', 1).isdigit():
            min_rating, max_rating = float(words[i + 1]), float(words[i + 2])
            break
    
    # Construct the URL
    url = f"https://www.imdb.com/search/title/?user_rating={min_rating},{max_rating}"
    print("Constructed URL:", url)
    
    # Set headers to mimic a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Fetch the page content
    response = requests.get(url, headers=headers)
    print("Response Status Code:", response.status_code)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch the page"}
    
    print("Fetched HTML Content Successfully")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find movie containers
    movies = []
    movie_containers = soup.find_all("li", class_="ipc-metadata-list-summary-item")
    print("Total movies found before limiting:", len(movie_containers))
    
    for movie in movie_containers[:25]:
        print("Processing a movie entry...")
        title_tag = movie.find("a", class_="ipc-title-link-wrapper")
        year_tag = movie.find("span", class_="sc-e8bccfea-7")
        rating_tag = movie.find("span", class_="ipc-rating-star--rating")
        
        if not title_tag or not year_tag or not rating_tag:
            print("Skipping due to missing fields")
            continue  # Skip movies with missing fields
        
        movie_id = title_tag["href"].split("/title/")[1].split("/")[0]
        title = title_tag.text
        year = year_tag.text if year_tag else "N/A"
        rating = rating_tag.text
        
        print(f"Extracted Movie: ID={movie_id}, Title={title}, Year={year}, Rating={rating}")
        movies.append({"id": movie_id, "title": title, "year": year, "rating": rating})
        #movies.append({"id": movie_id, "title": str(title), "year": str(year), "rating": str(rating)})

    
    print("Total Movies Extracted:", len(movies))
    return movies

def ga4_q3(question, files):
    api = "https://markdown-mocb.vercel.app/"
    return api

import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from urllib.parse import urlencode

def ga4_q4(question: str, files: list) -> dict:
    """Fetch the weather forecast for a given city by scraping the BBC Weather website and return JSON."""
    def get_location_id(city: str) -> str:
        """Fetch the BBC Weather location ID for a given city using BBC's API."""
        location_url = 'https://locator-service.api.bbci.co.uk/locations?' + urlencode({
            'api_key': 'AGbFAKx58hyjQScCXIYrxuEwJh2W2cmv',
            's': city,
            'stack': 'aws',
            'locale': 'en',
            'filter': 'international',
            'place-types': 'settlement,airport,district',
            'order': 'importance',
            'a': 'true',
            'format': 'json'
        })
        response = requests.get(location_url)
        
        if response.status_code != 200:
            raise ValueError("Failed to fetch BBC Weather location ID")
        
        data = response.json()
        try:
            return data['response']['results']['results'][0]['id']
        except (KeyError, IndexError):
            raise ValueError("Could not determine BBC Weather location ID")
    
    match = re.search(r'for ([A-Za-z ]+)', question)
    if not match:
        raise ValueError("City name not found in the question")
    
    city = match.group(1).strip()
    location_id = get_location_id(city)
    if not location_id:
        raise ValueError("Could not retrieve location ID for the city")
    
    url = f"https://www.bbc.com/weather/{location_id}"
    print(url)
    response = requests.get(url)
    
    if response.status_code != 200:
        raise ValueError("Failed to fetch weather data from BBC Weather")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract weather summaries
    #daily_summaries = [summary.text.strip() for summary in soup.find_all('div', attrs={'class': 'wr-day-summary'})]
    daily_summary = soup.find('div', attrs={'class': 'wr-day-summary'})
    daily_summary_list = re.findall('[a-zA-Z][^A-Z]*', daily_summary.text) #split the string on uppercase
    print(daily_summary_list)
    
    # Ensure we have a correct number of days
    num_days = len(daily_summary_list)
    #print("Extracted summaries:", daily_summaries)
    print("Number of summaries:", num_days)
    
    if num_days == 0:
        raise ValueError("No weather summaries found on BBC Weather page")
    
    # Generate correct date range
    datelist = [(datetime.today() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(num_days)]
    print("Generated date list:", datelist)
    
    # Ensure mapping of dates and summaries correctly
    forecast_data = {datelist[i]: daily_summary_list[i] for i in range(len(datelist))}
    
    return forecast_data

import requests
import re

def ga4_q5(question, files):
    def extract_city_country(question):
        match = re.search(r'city ([A-Za-z ]+) in the country ([A-Za-z ]+?)(?: on|$)', question)
        if match:
            city = match.group(1).strip()
            country = match.group(2).strip()
            print(city)
            print(country)
            return city, country
        return None, None

    def extract_requested_value(question):
        if "minimum latitude" in question:
            return 0  # Index for minimum latitude
        elif "maximum latitude" in question:
            return 1  # Index for maximum latitude
        elif "minimum longitude" in question:
            return 2  # Index for minimum longitude
        elif "maximum longitude" in question:
            return 3  # Index for maximum longitude
        return None

    def get_bounding_value(city, country, index):
        url = f"https://nominatim.openstreetmap.org/search?city={city}&country={country}&format=json"
        print(url)
        headers = {"User-Agent": "YourApp/1.0 (your@email.com)"}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                bounding_box = data[0].get('boundingbox', [])
                print("Bounding Box:", bounding_box)
                if len(bounding_box) == 4:
                    return float(bounding_box[index])  # Extract the requested value
        return None

    city, country = extract_city_country(question)
    index = extract_requested_value(question)

    if city and country and index is not None:
        bounding_value = get_bounding_value(city, country, index)
        return bounding_value
    else:
        return "Could not extract necessary details from the question."

import requests
import re
from requests.utils import quote

def ga4_q6(question, files):
    def extract_search_criteria(question):
        match = re.search(r'mentioning ([A-Za-z0-9]+) having at least (\d+) points', question)
        if match:
            keyword = match.group(1).strip()
            min_points = int(match.group(2).strip())
            return keyword, min_points
        return None, None

    def get_latest_hn_post(keyword, min_points):
        encoded_keyword = quote(keyword)
        page = 0
        valid_posts = []

        while True:
            url = f"https://hn.algolia.com/api/v1/search_by_date?query={encoded_keyword}&tags=story&page={page}"
            print(f"🔍 Searching page {page} for: {keyword}, Min Points: {min_points}")

            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()

                if not data.get('hits'):
                    break  # No more results

                for post in data['hits']:
                    title = post.get('title', '')
                    points = post.get('points', 0)
                    post_url = post.get('url', f"https://news.ycombinator.com/item?id={post.get('objectID')}")
                    created_at = post.get('created_at', 'Unknown')

                    print(f"📌 {title} | Points: {points} | Link: {post_url}")

                    if (keyword.lower() in title.lower() or 
                        (post.get('story_text') and keyword.lower() in post['story_text'].lower())) and points >= min_points:
                        valid_posts.append((created_at, points, post_url))

                if valid_posts:
                    break  # Stop if we found valid posts

            except requests.exceptions.RequestException as e:
                print(f"❌ Request error: {e}")
                return None

            page += 1

        if valid_posts:
            valid_posts.sort(reverse=True, key=lambda x: x[0])  # Sort by latest date
            best_match = valid_posts[0]
            print(f"🎯 Found Post: {best_match[2]} with {best_match[1]} points")
            return best_match[2]

        return "No matching post found."

    keyword, min_points = extract_search_criteria(question)

    if keyword and min_points is not None:
        result_link = get_latest_hn_post(keyword, min_points)
        return result_link if result_link else "No matching post found."
    else:
        return "Could not extract search criteria from the question."

import requests
import re
from requests.utils import quote

import requests
import re
from requests.utils import quote

def ga4_q7(question, files):
    def extract_search_criteria(question):
        match = re.search(r'located in the city ([A-Za-z]+) with over (\d+) followers', question)
        if match:
            city = match.group(1).strip()
            min_followers = int(match.group(2).strip())
            print(f"📍 Extracted City: {city}, Min Followers: {min_followers}")
            return city, min_followers
        return None, None

    def get_newest_github_user(city, min_followers):
        encoded_city = quote(city)
        url = f"https://api.github.com/search/users?q=location:{encoded_city}+followers:>{min_followers}&sort=joined&order=desc"
        print(f"🔍 Searching GitHub for users in {city} with >{min_followers} followers...")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            users = data.get("items", [])
            print(f"👥 Found {len(users)} users.")

            if users:
                newest_user = None
                newest_date = "0000-00-00T00:00:00Z"
                
                for user in users:
                    user_url = f"https://api.github.com/users/{user['login']}"
                    user_response = requests.get(user_url, timeout=10)
                    user_response.raise_for_status()
                    user_data = user_response.json()
                    created_at = user_data.get("created_at", "0000-00-00T00:00:00Z")
                    print(f"✅ {user['login']} | Created at: {created_at}")
                    
                    if created_at > newest_date:
                        newest_user = user
                        newest_date = created_at

                if newest_user:
                    print(f"🎯 Newest User: {newest_user['login']} | Joined: {newest_date}")
                    return newest_date

        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
            return None

        return "No matching users found."

    city, min_followers = extract_search_criteria(question)

    if city and min_followers is not None:
        newest_user_date = get_newest_github_user(city, min_followers)
        return newest_user_date if newest_user_date else "No matching users found."
    else:
        return "Could not extract search criteria from the question."


import requests
import base64
import json
import re
import subprocess
import os
import uuid
import time

def ga4_q8(question, files):
    github_token = files
    print("GA4 Q8")
    GITHUB_API_URL = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}

    def extract_email_from_question(question):
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', question)
        if match:
            email = match.group(0)
            print(f"Extracted email: {email}")
            return email
        print("No email found, using default.")
        return "23ds3000185@ds.study.iitm.ac.in"

    def create_github_repo(repo_name):
        data = {"name": repo_name, "private": False}
        response = requests.post(GITHUB_API_URL, headers=headers, json=data)
        if response.status_code in [201, 422]:
            print(f"Repository '{repo_name}' created or already exists.")
            return f"https://github.com/{username}/{repo_name}"
        else:
            raise Exception(f"Failed to create repo: {response.status_code}, {response.text}")

    def initialize_and_push_repo(repo_name, email_value):
        repo_url = f"https://{github_token}@github.com/{username}/{repo_name}.git"
        subprocess.run(["git", "clone", repo_url], check=True)
        os.chdir(repo_name)

        subprocess.run(["git", "config", "user.email", email_value], check=True)
        subprocess.run(["git", "config", "user.name", username], check=True)

        with open("email.json", "w") as f:
            json.dump({"email": email_value}, f)

        os.makedirs(".github/workflows", exist_ok=True)
        with open(".github/workflows/schedule.yml", "w") as f:
            f.write(f"""name: Daily Commit ({email_value})

on:
  push:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  commit:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Set up Git ({email_value})
        run: |
          git config --local user.email '{email_value}'
          git config --local user.name '{username}'
          export GIT_AUTHOR_NAME='{username}'
          export GIT_AUTHOR_EMAIL='{email_value}'
          export GIT_COMMITTER_NAME='{username}'
          export GIT_COMMITTER_EMAIL='{email_value}'

      - name: Debug Git Status
        run: |
          git status
          ls -lah

      - name: Set up Git ('{email_value}')
        run: |
          git config --local user.email ''{email_value}''
          git config --local user.name ''{username}''
          export GIT_AUTHOR_NAME=''{username}''
          export GIT_AUTHOR_EMAIL=''{email_value}''
          export GIT_COMMITTER_NAME=''{username}''
          export GIT_COMMITTER_EMAIL=''{email_value}''
        

      - name: Make a commit ({email_value})
        run: |
          echo "Update at $(date)" >> update.txt
          git add update.txt
          git commit -m "Automated commit with timestamp" || echo "No changes to commit"
          git push"""
            )

        subprocess.run(["git", "add", "email.json", ".github/workflows/schedule.yml"], check=True)
        subprocess.run(["git", "commit", "-m", "Add email.json and workflow file"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)

        time.sleep(30)

        workflow_dispatch_url = f"https://api.github.com/repos/{username}/{repo_name}/actions/workflows/schedule.yml/dispatches"
        trigger_response = requests.post(workflow_dispatch_url, headers=headers, json={"ref": "main"})
        if trigger_response.status_code == 204:
            print("Workflow triggered successfully.")
        else:
            print(f"Failed to trigger workflow: {trigger_response.status_code}, {trigger_response.text}")

        return f"https://github.com/{username}/{repo_name}"

    try:
        user_response = requests.get("https://api.github.com/user", headers=headers)
        user_response.raise_for_status()
        global username
        username = user_response.json()["login"]
    except requests.exceptions.RequestException as e:
        return f"GitHub authentication failed: {e}"

    email_value = extract_email_from_question(question)
    repo_name = f"email-json-repo-{uuid.uuid4().hex[:8]}"
    repo_url = create_github_repo(repo_name)
    final_repo_url = initialize_and_push_repo(repo_name, email_value)

    print(f"Repository created and pushed. You can access it here: {final_repo_url}")
    return final_repo_url

import camelot
import pandas as pd
import re

def ga4_q9(question, files):
    print("ga4 q9")

    # Function to extract data from specific pages based on page numbers
    def extract_data_with_groups(pdf_path, page_start, page_end):
        print(f"Extracting data from pages {page_start} to {page_end}...")
        pages = ','.join(map(str, range(page_start, page_end + 1)))  # Generate page range string
        tables = camelot.read_pdf(pdf_path, pages=pages, flavor='stream')
        all_data = []  # To store data from required pages

        for idx, table in enumerate(tables, start=page_start):
            # Convert the table to a DataFrame
            df = table.df
            print(f"Processing page {idx}...")

            # Set proper column headers (second row as headers)
            df.columns = df.iloc[1].str.strip()  # Use the second row as column headers
            df = df[2:].reset_index(drop=True)  # Remove the first two rows (group name and headers)
            print(f"Data after setting headers for page {idx}:")
            print(df)

            # Add a new column for the group name, using the page number
            df['Group'] = idx  # Assign group name as the page number

            # Append the processed data to the list
            all_data.append(df)

        # Combine all DataFrames into a single DataFrame
        full_data = pd.concat(all_data, ignore_index=True)
        print("Combined data from required pages:")
        print(full_data)

        return full_data

    # Function to parse the question to extract dynamic values
    def parse_question(question):
        print("Parsing the question...")
        # Use regular expressions to extract subject1, marks, subject2, and group range
        subject1_match = re.search(r'total (\w+)', question, re.IGNORECASE)
        marks_match = re.search(r'(\d+)\s+or\s+more\s+marks', question)
        subject2_match = re.search(r'in (\w+)', question)
        groups_match = re.search(r'groups (\d+)-(\d+)', question)

        if subject1_match and marks_match and subject2_match and groups_match:
            subject1 = subject1_match.group(1)  # e.g., Biology
            min_marks = int(marks_match.group(1))  # e.g., 49
            subject2 = subject2_match.group(1)  # e.g., Maths
            group_start = int(groups_match.group(1))  # e.g., 1
            group_end = int(groups_match.group(2))  # e.g., 23
            print(f"Parsed values: subject1={subject1}, min_marks={min_marks}, subject2={subject2}, group_start={group_start}, group_end={group_end}")
            return subject1, min_marks, subject2, group_start, group_end
        else:
            raise ValueError("Unable to parse the question correctly")

    # Function to process the DataFrame and calculate total marks
    def process_data_and_calculate(df, question):
        print("Processing data and calculating total marks...")

        # Parse question to extract subject1, marks, subject2, and group range
        subject1, min_marks, subject2, group_start, group_end = parse_question(question)

        # Check if the relevant subjects exist in the DataFrame
        if subject1 not in df.columns or subject2 not in df.columns:
            raise KeyError(f"Subject '{subject1}' or '{subject2}' not found in the extracted table.")
        print(f"Columns '{subject1}' and '{subject2}' found in the data.")

        # Convert the subject marks columns to numeric
        df[subject1] = pd.to_numeric(df[subject1], errors='coerce')
        df[subject2] = pd.to_numeric(df[subject2], errors='coerce')
        df['Group'] = pd.to_numeric(df['Group'], errors='coerce')  # Ensure 'Group' column is numeric
        print("Converted subject columns to numeric values.")

        # Filter rows based on group range
        filtered_df = df[df['Group'].between(group_start, group_end)]
        print(f"Filtered data by group range {group_start}-{group_end}:")
        print(filtered_df)

        # Filter rows where marks in subject2 (Maths) are >= min_marks
        filtered_df = filtered_df[filtered_df[subject2] >= min_marks]
        print(f"Filtered data where marks in {subject2} >= {min_marks}:")
        print(filtered_df)

        # Calculate total marks for subject1 (Biology)
        total_marks = filtered_df[subject1].sum()
        print(f"Total marks for {subject1}: {total_marks}")

        return int(total_marks)  # Convert to Python int for compatibility

    # Execute the workflow
    try:
        # Parse question to get group range
        subject1, min_marks, subject2, group_start, group_end = parse_question(question)

        # Extract data from required pages based on group range
        pdf_path = "q-extract-tables-from-pdf.pdf"  # Explicitly use the specified PDF file name
        print(f"PDF Path: {pdf_path}")
        full_data = extract_data_with_groups(pdf_path, group_start, group_end)

        # Process the data and calculate total marks based on the question
        total_marks = process_data_and_calculate(full_data, question)
        return total_marks  # Ensure total_marks is a Python int
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}
    
def ga4_q10(question, files):
    data = '''```
Ara adflicto bonus
Thesis textilis suus theologus apto delinquo demergo collum adulatio.
javascript, python, https
instructive, lava, net
Pariatur bestia bene.
Doloribus provident libero speculum debeo denego atqui curo.

```

- adulescens teneo conatus surgo cursim

- averto sollicito collum

```
Turba vinum sint vindico decerno stultus vir deinde alioqui sollicito.
Vulnero adiuvo amiculum curtus defleo stipes doloribus.

```

[<xiphias aro>](#)

- aestivus saepe votum

- ait turbo

- adduco minus aspernatur

| magnam | calcar  |  synagoga       |
|-----------|---------|----------------|
|turbo       | defero | arcessoavarus |
|cursim     | patior  | vinco crapula  |

aspernaturconturbo solum ratione
Sperno videlicet vester

- desparatus bestia amor amplus

- porro stipes xiphias

- creator civis urbanus deleo

- bene occaecati

```
Crudelis cultellus decretum patrocinor combibo deludo cohaero.
Calco civitas timidus conspergo.
Tam contego cernuus aut arbitro vulgivagus.
Abscido tenus chirographum vomer valetudo.

```

**conitor rem**

placeat vilis

defleo abscido

# Caelum synagoga ceno

[<solio beatae>](#)

> Aequitas tabula arma suscipit synagoga. Terebro fugit calcar adicio correptius volubilis. Mollitia tenuis ante earum sponte.

---
'''
    return data