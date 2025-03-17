from datetime import datetime
from typing import List
import click
import os
from Classes import Commit
import Function


# black, red, green, yellow, blue, magenta, cyan, white
# bold: טקסט מודגש (ברירת מחדל: False).
# dim: טקסט עמום (חלש יותר).
# reverse: הופך את צבעי הטקסט והרקע.
@click.group()
def cli():
    """Wit CLI tool"""
    pass


@cli.command()
def init():
    """Initialize a new repository."""
    try:
        Function.create_directory(".wit", "Hello, the directory created successfully!")
        Function.create_repo()
    except Exception as e:
        click.echo(click.style(f"Error initializing wit: {e}", fg="red"))


@cli.command()
@click.argument('files', nargs=-1)
def add(files: List[str]):
    """Add files to staging."""
    try:
        repo = Function.load_repo()
        if repo is None:
            raise Exception("Error: Repository is not initialized. Please run 'wit init' first.")
        if not files or files[0] == "":
            raise Exception(click.style("Command not valid.",fg="red"))
        else:
            Function.copy_files(os.getcwd(), f'.wit/{str(repo.name_repo)}/Staging', files, repo.wit_ignore)
            repo.add(files)
            Function.save_repo(repo)
    except Exception as e:
        click.echo(click.style(f"5. Error adding files: {e}", fg="red"))


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
        # click.echo(click.style("reached to here",fg="magenta"))

        # יצירת תיקיית commit חדשה
        repo_path = f'.wit\\{str(repo.name_repo)}\\Commited'

        # date_dir = os.path.join(repo_path, f"{datetime.now().strftime('%d.%m.%Y')}")
        Function.create_directory(repo_path, "Directory date created successfully.")
        id_commit = os.path.join(repo_path, str(new_commit.commit_id))
        Function.create_directory(id_commit, f"Directory id {id_commit} created successfully.")

        # העברת הקבצים מ-Staging
        Function.move_files(staged, id_commit)
        click.echo(click.style(f"Directory staging moved successfully.", fg="green"))

        # קריאה של ה-commit הקודם מ-JSON
        prev_json_path = f'{os.getcwd()}/prev.json'
        prev_commit_id = Function.get_last_commit(prev_json_path)
        # click.echo(click.style(prev_commit_id, fg="magenta"))
        if prev_commit_id:
            # click.echo(click.style("there is somthing", fg="magenta"))
            prev_commit_path = os.path.join(repo_path, f"{prev_commit_id}")
            # click.echo(click.style(prev_commit_path, fg="magenta"))
            if os.path.exists(prev_commit_path):
                # click.echo(click.style("copy from last commit!!!!!!!!!!!!!!!!!!!!!!!", fg="magenta"))
                # העתקת קבצים מה-commit הקודם
                Function.copy_all_files(prev_commit_path, id_commit)
                click.echo(click.style(f"Copied files from previous commit: {prev_commit_id}", fg="green"))
            else:
                click.echo(click.style("cant find dest !!!!!!!!!!!!!!!!!!!!!!!!!!!!!",fg="yellow"))

        # עדכון קובץ ה-JSON עם ה-commit הנוכחי
        Function.get_last_commit(prev_json_path, new_commit.commit_id)

        # ניקוי ה Staging
        repo.staging = []
        Function.save_repo(repo)
        click.echo(click.style(f"Commit {new_commit.commit_id} created successfully.",fg="green"))

    except Exception as e:
        click.echo(click.style(f"Error during commit: {e}",fg="red"))


@cli.command()
def log():
    """Display commit logs."""
    try:
        data = Function.load_repo()
        for commit1 in data.list_commits:
            click.echo(click.style(f"{Commit(commit1['message'], commit1['list_files'])} \n",fg="yellow"))
    except Exception as e:
        click.echo(click.style(f"4. Error: {e}",fg="red"))


@cli.command()
def status():
    """Show the staging area for files who hasn't commited yet."""
    repo = Function.load_repo()
    if not repo.staging:
        click.echo(click.style("No changes in the project.",fg="yellow"))
    else:
        for file in repo.staging:
            click.echo(click.style(f'{file}',fg="cyan"))


@cli.command()
@click.argument('id_repo')
def checkout(id_repo):
    """Return the project to the selected commit."""
    try:
        repo = Function.load_repo()
        for commit1 in repo.list_commits:
            # Commit(commit['message'], commit['list_files'])
            if str(commit1['id_commit']) == str(id_repo):
                click.echo(click.style(commit1['id_commit'],fg="magenta"))
                date_obj = datetime.strptime(commit1['date'].split()[0], "%d/%m/%Y")
                source = f'.wit/{repo.name_repo}/Commited/{date_obj.strftime("%d.%m.%Y")}/{id_repo}'
                dest = '.'
                Function.checkout_files(source, dest)
            else:
                click.echo(click.style('bla bla checkout id_commit',fg="magenta"))
    except Exception as e:
        click.echo(click.style(f'13. Error while checkout: {e}',fg="red"))


if __name__ == "__main__":
    cli()
