import json
import os

def split_tests_with_multiple_methods(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    new_tests = []
    for test in data['tests']:
        methods = test.get('methods_under_test', [])
        if len(methods) > 1:
            for method in methods:
                new_test = test.copy()
                new_test['methods_under_test'] = [method]
                new_tests.append(new_test)
        else:
            new_tests.append(test)

    # Overwrite the JSON file with the split tests
    with open(file_path, 'w') as f:
        json.dump({'tests': new_tests}, f, indent=4)

    print(f"Updated file saved to: {file_path}")

# Modify all the files in the folder containing methods_under_test
folder_path = './'  # Replace with the correct folder path
for filename in os.listdir(folder_path):
    if filename.startswith('collected_tests_explanation__') and filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        print(f"Processing file: {filename}")
        split_tests_with_multiple_methods(file_path)

print("All files have been updated.")
