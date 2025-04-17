import os
import json
import re
from collections import OrderedDict

def add_repo_name_field_first(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".json") and filename.startswith("collected_tests_explanation__"):
            # Extract the repo name from the filename
            match = re.match(r"collected_tests_explanation__(.+)\.json", filename)
            if not match:
                continue
            repo_name = match.group(1)
            
            # Full file path
            file_path = os.path.join(folder_path, filename)
            
            # Load JSON data
            with open(file_path, "r") as file:
                data = json.load(file)
            
            # Add 'repo_name' to each test as the first field
            for i, test in enumerate(data.get("tests", [])):
                # Create a new OrderedDict with repo_name first, followed by name, then other keys
                reordered_test = OrderedDict()
                reordered_test["repo_name"] = repo_name
                reordered_test["name"] = test.get("name", "")
                for key, value in test.items():
                    if key not in {"repo_name", "name"}:
                        reordered_test[key] = value
                data["tests"][i] = reordered_test
            
            # Save updated data back to the file
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)


folder_path = "./"
add_repo_name_field_first(folder_path)
