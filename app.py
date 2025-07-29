import os
import zipfile
import tempfile
from flask import Flask, request, redirect, render_template
from github import Github

app = Flask(__name__)

# Replace with your own GitHub token and repo
GITHUB_TOKEN = 'ghp_BmQM6S7H6s200qhXRb7z4PxggbuVLN1gx9'
REPO_NAME = 'MANOJKANNAN04/github-uploaded'  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_zip():
    if 'zip_file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['zip_file']
    if file.filename == '':
        return 'No selected file', 400

    if file and file.filename.endswith('.zip'):
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, file.filename)
        file.save(zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        github = Github(GITHUB_TOKEN)
        repo = github.get_repo(REPO_NAME)

        for root, dirs, files in os.walk(temp_dir):
            for filename in files:
                if filename.endswith('.zip'):
                    continue

                local_path = os.path.join(root, filename)
                with open(local_path, 'rb') as f:
                    content = f.read()

                relative_path = os.path.relpath(local_path, temp_dir)
                try:
                    repo.create_file(relative_path, f"Add {relative_path}", content)
                except Exception as e:
                    print(f"Error: {e}")
                    continue

        return 'Files uploaded and pushed to GitHub successfully!'

    return 'Invalid file format. Upload a .zip file.', 400

if __name__ == '__main__':
    app.run(debug=True)
