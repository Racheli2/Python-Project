import os
from datetime import datetime
from typing import List

import click


class File:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.last_modified = datetime.fromtimestamp(os.path.getmtime(self.path)).isoformat()

    def is_last_modified(self):
        new_time = datetime.fromtimestamp(os.path.getmtime(self.path)).isoformat()
        if new_time != self.last_modified:
            self.last_modified = new_time
        return new_time != self.last_modified

    def __str__(self):
        return f"{self.name}, {self.path}"


class Commit:
    def __init__(self, message, list_files):
        self.commit_id = id(self)
        self.message = message
        self.date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.list_files = list_files

    def __str__(self):
        return (f'commit id: {self.commit_id}\n'
                f'date: {self.date}\n'
                f'files: {[file for file in self.list_files]}')


class Repository:
    def __init__(self, name_repo: str):
        self.id_repo = id(self)
        self.name_repo: str = name_repo
        self.list_commits: List[Commit] = []
        self.list_files = self.get_directory_structure(".")
        self.staging: List[File] = []
        self.wit_ignore = [".wit", ".venv", ".venv1", ".idea", "__pycache__", "repo.json", "prev.json", "wit.bat"]

    def get_directory_structure(self, path):
        structure = {}
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir():
                    structure[entry.name] = self.get_directory_structure(entry.path)
                elif entry.is_file():
                    structure[entry.name] = File(name=entry.name, path=entry.path)
        return structure

    def add(self,files):
        if files[0] == '.':  # ממלאים את הרשימה FILES בקבצים של הפרויקט אם המשתמש שלח .
            files = [file for file in os.listdir(os.getcwd()) if file not in self.wit_ignore]
        for file in files:  # הכנסת הקבצים לרשימת ה-STAGING
            new_file = File(file, f'.wit/{str(self.name_repo)}/Staging')
            self.staging.append(new_file)
            print(click.style(new_file,fg="yellow"))
        for staged_file in self.staging:  # הדפסת הקבצים שנוספו ל-STAGING
            print(click.style(staged_file,fg="yellow"))

    #def commit(self):


    def check_out(self, commit_id):
        for commit in self.list_commits:
            if commit.commit_id == commit_id:
                self.list_files = commit.list_files
                return
        raise ValueError("Commit ID not found.")


def print_structure(structure, indent=0):
    for name, item in structure.items():
        if isinstance(item, File):
            print("  " * indent + f"File: {item.name}, Path: {item.path}, Last Modified: {item.last_modified}")
        else:
            print("  " * indent + f"Directory: {name}")
            print_structure(item, indent + 1)
