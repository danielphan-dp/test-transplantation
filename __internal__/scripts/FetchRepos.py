import os
import json
from github import Github, auth

def fetch_repos(username, target_folder, access_token=None):
    # Create a Github instance
    g = Github(access_token) if access_token else Github()
    
    try:
        # Get the user
        user = g.get_user(username)
        
        # Fetch repositories
        repos = list(user.get_repos())
        
        # Create target folder if it doesn't exist
        os.makedirs(target_folder, exist_ok=True)
        
        # Prepare repo data for JSON serialization
        repo_data = [
            {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "url": repo.html_url,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "language": repo.language
            }
            for repo in repos
        ]
        
        # Write repo information to a JSON file
        output_file = os.path.join(target_folder, f"{username}_repos.json")
        with open(output_file, 'w') as f:
            json.dump(repo_data, f, indent=2)
        
        print(f"Fetched {len(repos)} repositories for {username}")
        print(f"Repo list saved to {output_file}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
if __name__ == "__main__":
    username = "octocat"  # Replace with the GitHub username you want to fetch repos for
    target_folder = "repo_lists"  # Replace with your desired target folder
    access_token = None  # Replace with your GitHub access token if you have one
    fetch_repos(username, target_folder, access_token)
    