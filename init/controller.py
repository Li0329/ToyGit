import os 
import sys
import configparser






class GitRepository(object):
    """
        This is a git repository.
    """

    worktree = None 
    gitdir = None
    conf = None

    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception(f"这不是个git仓库{path}")


        # Read configuration file in .git/config
        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")

        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("配置文件丢失")

        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception(f"不支持当前{vers}的仓库版本")


    def repo_path(repo, *path):
        """
            Compute path under repo's gitdir.
        """
        return os.path.join(repo.gitdir, *path)


     def repo_dir(repo, *path, mkdir=False):
         """
            Same as repo_path, but mkdir *path if absent if mkdir.
         """
         path = repo_path(repo, *path)

         if os.path.exists(path):
             if (os.path.isdir(path)):
                 return path
             else:
                 raise Exception(f"{path}?,这不是目录")


         if mkdir:
             os.makedirs(path)
             return path
         else:
             return None

    
    def repo_file(repo, *path):
        """
            Same as repo_path, but create dirname(*path) if absent.
            For example, repo_file(r, \"refs\", \"remotes\", \"origin\", \"HEAD"\)
            will create .git/refs/remotes/origin.
        """

        if repo_dir(repo, *path[:-1], mkdir=mkdir):
            return repo_path(repo, *path)



