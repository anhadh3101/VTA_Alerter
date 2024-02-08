import pandas as pd
import subprocess

def get_url(rNum, direction):
    try:
        # Execute the JavaScript file as a separate process
        process = subprocess.Popen(["node", "vta-nav.js", rNum, direction], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        # Check for any errors in stderr
        if stderr:
            print("Error:", stderr.decode().strip())
        # Decode the output and return the URL
        return stdout.decode().strip()
    except Exception as e:
        print("Exception:", str(e))

# Call the get_url function with arguments
rNum = input("VTA Number: ")
direction = input("What time of the week and in which direction are you going? ")
URL = get_url(rNum, direction)
print("Result:", URL)
tables = pd.read_html(URL)
print(tables)
