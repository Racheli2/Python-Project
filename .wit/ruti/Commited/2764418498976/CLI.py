from datetime import datetime
from typing import List
import click
import os
from Classes import File, Commit
import Function


@click.group()
def cli():
    """Wit CLI tool"""
    pass


@cli.command()
def init():
    """Initialize a new repository."""
    try:
        if not os.path.exists(".wit"):
            os.mkdir(".wit")
            # click.echo("Hello, the directory created successfully!")
            Function.create_repo()
        else:
            click.echo("The directory '.wit' already exists.")
    except Exception as e:
        click.echo(f"Error initializing wit: {e}")


@cli.command()
@click.argument('files', nargs=-1)
def add(files: List[str]):
    """Add files to staging."""
    try:
        repo = Function.load_repo()
        if repo is None:
            raise Exception("Error: Repository is not initialized. Please run 'wit init' first.")
        if not files or files[0] == "":
            raise Exception("Command not valid.")
        else:
            Function.copy_files(os.getcwd(), f'.wit/{str(repo.name_repo)}/Staging', files, repo.wit_ignore)
            if files[0] == '.':
                files = [file for file in os.listdir(os.getcwd()) if file not in repo.wit_ignore]
            for file in files:
                new_file = File(file, f'.wit/{str(repo.name_repo)}/Staging')
                repo.staging.append(new_file)
                print(new_file)
            for staged_file in repo.staging:
                print(staged_file)
            Function.save_repo(repo)
    except Exception as e:
        click.echo(f"5. Error adding files: {e}")




@cli.command()
@click.option('-m', '--message', required=True, help="The commit message.")
def commit(message):
    """Create a new commit."""
    try:
        repo = Function.load_repo()
        staged = f'.wit/{str(repo.name_repo)}/Staging/'
        if not os.listdir(staged):
            raise Exception('No changes in the project')

        # יצירת commit חדש
        list_files = os.listdir(staged)
        new_commit = Commit(message, list_files)
        repo.list_commits.append(new_commit)

        # יצירת תיקיית commit חדשה
        repo_path = f'.wit\\{str(repo.name_repo)}\\Commited'

        #date_dir = os.path.join(repo_path, f"{datetime.now().strftime('%d.%m.%Y')}")
        Function.create_directory(repo_path, "Directory date created successfully.")
        id_commit = os.path.join(repo_path, str(new_commit.commit_id))
        Function.create_directory(id_commit, f"Directory id {id_commit} created successfully.")

        # העתקת קבצים מ-Staging
        Function.move_files(staged, id_commit)
        click.echo(f"Directory staging moved successfully.")

        # קריאה של ה-commit הקודם מ-JSON
        prev_json_path = f'{os.getcwd()}/prev.json'
        prev_commit_id = Function.get_last_commit(prev_json_path)
        print(prev_commit_id)
        if prev_commit_id:
            print("there is somthing")
            prev_commit_path = os.path.join(repo_path, f"{prev_commit_id}")
            print(prev_commit_path)
            if os.path.exists(prev_commit_path):
                print("copy from last commit!!!!!!!!!!!!!!!!!!!!!!!")
                # העתקת קבצים מה-commit הקודם
                Function.copy_all_files(prev_commit_path, id_commit)
                click.echo(f"Copied files from previous commit: {prev_commit_id}")
            else:
                print("cant find dest !!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        # עדכון קובץ ה-JSON עם ה-commit הנוכחי
        Function.get_last_commit(prev_json_path, new_commit.commit_id)

        # ניקוי Staging
        repo.staging = []
        Function.save_repo(repo)
        click.echo(f"Commit {new_commit.commit_id} created successfully.")

    except Exception as e:
        click.echo(f"Error during commit: {e}")


@cli.command()
def log():
    """Display commit logs."""
    try:
        data = Function.load_repo()
        for commit1 in data.list_commits:
            print(Commit(commit1['message'], commit1['list_files']), '\n')
    except Exception as e:
        click.echo(f"4. Error: {e}")


@cli.command()
def status():
    """Show the staging area for files who hasn't commited yet."""
    repo = Function.load_repo()
    if not repo.staging:
        click.echo("No changes in the project.")
    else:
        for file in repo.staging:
            click.echo(f'{file}')


@cli.command()
@click.argument('id_repo')
def checkout(id_repo):
    """Return the project to the selected commit."""
    try:
        repo = Function.load_repo()
        for commit1 in repo.list_commits:
            # Commit(commit['message'], commit['list_files'])
            if str(commit1['id_commit']) == str(id_repo):
                print(commit1['id_commit'])
                date_obj = datetime.strptime(commit1['date'].split()[0], "%d/%m/%Y")
                source = f'.wit/{repo.name_repo}/Commited/{date_obj.strftime("%d.%m.%Y")}/{id_repo}'
                dest = '.'
                Function.checkout_files(source, dest)
            else:
                print('bla bla checkout id_commit')
    except Exception as e:
        click.echo(f'13. Error while checkout: {e}')


if __name__ == "__main__":
    # CLI.get_command()
    cli()
