from git import Repo
import os

def clone_repo(repo_url, save_path="uploaded_repos"):

    repo_name = repo_url.split("/")[-1]   # take repo name from url

    repo_path = os.path.join(save_path, repo_name)   # take repo path

    if not os.path.exists(save_path):   # if not is not saved in local machine then save it
        os.makedirs(save_path)
    
    if not os.path.exists(repo_path):    # if path is not save then save it for future
        Repo.clone_from(repo_url, repo_path)

    return repo_path