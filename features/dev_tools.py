def _parse_git_status(output: str) -> str:
    lines = output.splitlines()

    branch = lines[0].split()[-1]

    if "nothing to commit" in output:
        return "Working tree clean. No uncommitted changes"
    
    else:
        untracked_section = False

        modified = 0
        untracked = 0

        for line in lines:
            if "modified" in line:
                modified += 1

            if line.startswith("Untracked"):
                untracked_section  = True

            if line.startswith("\t") and untracked_section:
                    untracked += 1
    
        return f"On branch {branch}. {modified} modified files and {untracked} untracked files."
        


def _parse_git_log(output: str) -> str:
    lines = output.splitlines()
    
    commits = []
    for line in lines:
        commit = line.split(" ", 1)
        commits.append(commit[1])

    if not commits:
        return "No commits found."

    recent_commits = ", ".join(commits)
    return f"Recent commits: {recent_commits}"