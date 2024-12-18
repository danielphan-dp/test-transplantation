import os
import json

# Define the folder path containing the files
folder_path = "./"

# Iterate through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):  # Ensure it's a JSON file
        file_path = os.path.join(folder_path, filename)

        # Open and load the JSON data
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Process each test in the data
        if "tests" in data:
            for test in data["tests"]:
                if "methods_under_test" in test:
                    for method in test["methods_under_test"]:
                        if "code_explanation" in method:
                            # Rename "code_explanation" to "method_explanation"
                            method["method_explanation"] = method.pop("code_explanation")

        # Save the updated JSON data back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

print("All files processed successfully!")
