import json
import os

def delete_tests_without_methods(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    filtered_tests = [test for test in data['tests'] if test.get('methods_under_test')]

    # Overwrite the JSON file with only the tests containing methods_under_test
    with open(file_path, 'w') as f:
        json.dump({'tests': filtered_tests}, f, indent=4)

    print(f"Updated file saved to: {file_path}")

# Modify all the files in the folder to delete tests without methods_under_test
folder_path = './'  # Replace with the correct folder path
for filename in os.listdir(folder_path):
    if filename.startswith('collected_tests_explanation__') and filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        print(f"Processing file: {filename}")
        delete_tests_without_methods(file_path)

print("All files have been updated.")
