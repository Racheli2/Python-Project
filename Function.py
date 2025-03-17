import click
import os
from Classes import Repository, File, Commit
import json
import shutil
from typing import List


def load_repo():
    try:
        if os.path.exists('repo.json') and os.path.getsize('repo.json') > 0:
            with open('repo.json', 'r') as f:
                data = json.load(f)
                repo = Repository(data['name_repo'])
                repo.list_commits = data['list_commits']
                repo.staging = data['staging']
                # repo.list_files = data['list_files']
                return repo
    except Exception as e:
        click.echo(click.style(f"1. Error loading repository: {e}", fg="red"))
    return None


def save_repo(repo: Repository):
    try:
        if repo is not None and isinstance(repo, Repository):
            existing_data = {}
            if os.path.exists('repo.json') and os.path.getsize('repo.json') > 0:
                with open('repo.json', 'r') as f:
                    existing_data = json.load(f)
            # print(click.style(type(repo), fg="magenta"))
            existing_data['name_repo'] = getattr(repo, 'name_repo', None)
            existing_data['list_commits'] = existing_data.get('list_commits', [])
            if not repo.staging:
                existing_data['staging'] = []
            existing_data['staging'] = existing_data.get('staging', [])
            if 'list_commits' not in existing_data:
                existing_data['list_commits'] = []
            existing_data['list_commits'].extend(
                [commit_to_dict(commit) for commit in repo.list_commits if isinstance(commit, Commit)])
            # print(click.style("after commits", fg="magenta"))
            # existing_data['staging'].extend([file_to_dict(stage) for stage in repo.staging])
            for stage in repo.staging:
                # print(click.style(stage, fg="magenta"))
                if repo.staging and not hasattr(stage, 'name'):
                    print(click.style("Error: 'name' attribute not found in stage.", fg="red"))
                    continue  # Skip if 'name' attribute doesn't exist
                if not any(existing_file['file_name'] == stage.name for existing_file in existing_data['staging']):
                    existing_data['staging'].append(file_to_dict(stage))
                    # print(click.style('success', fg="green"))
                else:
                    print()
                    # print(click.style("bla bla else staging", fg="green"))

            with open('repo.json', 'w') as f:
                json.dump(existing_data, f, indent=20)
            # print(click.style("bla bla dump", fg="green"))
        else:
            raise ValueError("Invalid repo object provided.")
    except Exception as e:
        click.echo(click.style(f"2. Error saving repository: {e}", fg="red"))


def file_to_dict(file: File):
    # print(click.style("bal bal file",fg="magenta"))
    return {
        'file_name': file.name,
        'path': file.path,
        'last_modified': file.last_modified
    }


def commit_to_dict(commit: Commit):
    return {
        'id_commit': commit.commit_id,
        'message': commit.message.split("wit commit -m", 1)[0].strip(),
        'date': commit.date,
        'list_files': commit.list_files
    }


def create_repo():
    try:
        name_repo = click.prompt("Enter the repository name", type=str)
        repo = Repository(str(name_repo))
        save_repo(repo)
        repo_path = os.path.join(".wit", name_repo)
        create_directory(repo_path, f"Repository '{name_repo}' created successfully!")

        stage = os.path.join(repo_path, "Staging")
        create_directory(stage, "Directory Staging created successfully.")

        commit = os.path.join(repo_path, "Commited")
        create_directory(commit, "Directory Commited created successfully.")
    except Exception as e:
        click.echo(click.style(f"6. Error creating repository: {e}", fg="red"))


def create_directory(path, success_message):
    if not os.path.exists(path):
        os.mkdir(path)
        click.echo(click.style(success_message,fg="green"))


def move_files(source_dir, dest_dir):
    check_path(source_dir, dest_dir)
    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)
        shutil.move(item_path, dest_dir)
        # click.echo(f"Directory '{item}' moved successfully.")


def get_last_commit(file_path: str, new_value=None):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        if new_value is not None:
            data['prev'] = new_value
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            return str(new_value)
        else:
            if data['prev'] == 0:
                raise Exception("No commit in the repository.")
            return str(data.get('prev', None))

    except FileNotFoundError:
        raise Exception(f"The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise Exception(f"The file {file_path} is not a valid JSON file.")


def checkout_files(source_dir, dest_dir):
    check_path(source_dir, dest_dir)
    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)
        shutil.copy(item_path, dest_dir)
        # click.echo(f"Directory '{item}' copied successfully.")


def check_path(source, dest=None):
    if not os.path.exists(source):
        raise Exception("Source directory does not exist.")
    if dest:
        if not os.path.exists(dest):
            raise Exception("Error: Repository is not initialized. Please run 'wit init' first.")


def copy_files(source_dir, dest_dir, files: List[str], ignore_list: List[str] = None):
    try:
        ignore_list = ignore_list or []

        check_path(source_dir, dest_dir)

        if files[0] == '.':
            files = os.listdir(source_dir)

        for filename in files:
            full_file_name = os.path.join(source_dir, filename)
            if any(ignore in full_file_name for ignore in ignore_list):
                # click.echo(f'{ignore_list}')
                # click.echo(f"Skipping ignored item: {full_file_name}")
                continue
            # click.echo('we reached to here')

            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, dest_dir)
                # click.echo(f"File '{filename}' copied successfully.")
            elif os.path.isdir(full_file_name):
                shutil.copytree(full_file_name, os.path.join(dest_dir, filename), dirs_exist_ok=True,
                                ignore=shutil.ignore_patterns(*ignore_list))
                # lick.echo(f"Directory '{filename}' copied successfully.")
            else:
                click.echo(f"Item '{filename}' does not exist in the source directory.")

    except Exception as e:
        click.echo(f"Error copying files: {e}")


def copy_all_files(source, dest):
    if not os.path.exists(source):
        raise Exception("Source directory does not exist.")

    if not os.path.exists(dest):
        raise Exception("Error: Repository is not initialized. Please run 'wit init' first.")

    for filename in os.listdir(source):
        source_file = os.path.join(source, filename)
        target_file = os.path.join(dest, filename)

        # אם הקובץ לא קיים בתיקיית היעד, העתק אותו
        if not os.path.exists(target_file):
            shutil.copy2(source_file, target_file)
            # print(f'Copied: {filename}')
        # else:
            # print(click.style(f'File already exists: {filename}',fg="yellow"))

# def has_file_changed(src_file, dest_file):
#     if not os.path.exists(dest_file):
#         return True
#     return os.path.getmtime(src_file) > os.path.getmtime(dest_file)


# def copy_changed_files(src_dir, dest_dir, files, ignore_list):
#     try:
#         for item in files:
#             src_path = os.path.join(src_dir, item)
#             dest_path = os.path.join(dest_dir, item)
#
#             if os.path.isdir(src_path):
#                 if not os.path.exists(dest_path):
#                     shutil.copytree(str(src_path), str(dest_path), ignore=shutil.ignore_patterns(*ignore_list))
#                     click.echo(f"Directory '{item}' copied successfully.")
#                 else:
#                     copy_changed_files(src_path, dest_path, files, ignore_list)
#             elif os.path.isfile(src_path):
#                 if has_file_changed(src_path, dest_path):
#                     shutil.copy2(str(src_path), str(dest_path))
#                     click.echo(f"File '{item}' copied successfully.")
#                 else:
#                     click.echo(f"File '{item}' not changed, skipping.")
#     except Exception as e:
#         print(f'9.{e}')
#


# def copy_files_if_not_exist(source_dir, target_dir):
#     # ודא שהתיקייה היעד קיימת
#     os.makedirs(target_dir, exist_ok=True)
#
#     # עבור על כל הקבצים בתיקיית המקור
#     for filename in os.listdir(source_dir):
#         source_file = os.path.join(source_dir, filename)
#         target_file = os.path.join(target_dir, filename)
#
#         # אם הקובץ לא קיים בתיקיית היעד, העתק אותו
#         if not os.path.exists(target_file):
#             shutil.copy2(source_file, target_file)
#             print(f'Copied: {filename}')
#         else:
#             print(f'File already exists: {filename}')
