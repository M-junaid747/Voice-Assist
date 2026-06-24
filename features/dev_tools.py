import subprocess
import platform
import config

from core.registry import register_intent

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


@register_intent(intent = "open_vscode", keywords = ["vscode", "code", "editor", "coding", "project"])
def handle_open_vscode(text: str) ->str:
    system = platform.system()
    if system == "Windows":
        subprocess.Popen(["code", "."], shell=True)
    elif system == "Linux":
        subprocess.Popen(["code", "."])
    elif system == "Darwin":
        subprocess.Popen(["code", "."])
    else:
        return "Opening VSCode isn't supported on this system yet"
    return "Opening VSCode"


@register_intent(intent= "open_terminal", keywords = ["terminal", "shell", "console", "command", "powershell"])
def handle_open_terminal(text: str) ->str:
    system = platform.system()
    if system == "Windows":
        subprocess.Popen(["powershell"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        return "Opening terminal"
    elif system == "Linux":
        subprocess.Popen(["gnome-terminal"])
        return "Opening terminal"
    elif system == "Darwin":
        subprocess.Popen(["open", "-a", "Terminal"])
        return "Opening terminal"
    return "Opening terminal not supported yet"
    

@register_intent(intent= "open_python_shell", keywords = ["python", "shell", "interpreter", "repl", "interactive"])
def handle_python_shell(text: str) ->str:
    system = platform.system()
    if system == "Windows":
        subprocess.Popen(["python"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        return "Opening Python Shell"
    elif system == "Linux":
        subprocess.Popen(["gnome-terminal", "--", "python3"])
        return "Opening Python Shell"
    elif system == "Darwin":
        subprocess.Popen(["open", "-a", "Terminal"])
        return "Opening Terminal. Type python3 to start the shell"
    else:
        return "Shell no supported yet"
    

@register_intent(intent= "git_status", keywords = ["git", "status", "changes", "modified", "staged"])
def handle_git_status(text: str) ->str:
    result = subprocess.run(["git", "status"], capture_output=True, text=True)
    if result.returncode !=0:
        return f"Something went wrong: {result.stderr}"
    return _parse_git_status(result.stdout)

@register_intent(intent= "git_log", keywords = ["log", "commits", "history", "recent", "previous"])
def handle_git_log(text: str) ->str:
    result = subprocess.run(["git", "log", "--oneline", "-5"], capture_output=True, text=True)
    if result.returncode !=0:
        return f"Something went wrong: {result.stderr}"
    return _parse_git_log(result.stdout)   


@register_intent(intent= "run_script", keywords = ["run", "execute", "script", "launch", "start"])
def handle_run_script(text: str) ->str:
    result = subprocess.run(["python",config.DEFAULT_SCRIPT], capture_output=True, text=True)
    if result.returncode !=0:
        return f"Something went wrong: {result.stderr}"
    if result.stdout:
        return f"Script ran successfully. Output: {result.stdout[:100]}"
    return "Script ran with no output."   
