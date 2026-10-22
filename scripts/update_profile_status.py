from datetime import datetime, timedelta
import subprocess
from pathlib import Path

README_PATH = Path(__file__).resolve().parents[1] / "README.md"
START = "<!-- PROFILE STATUS:START -->"
END = "<!-- PROFILE STATUS:END -->"


def run_git(args):
    result = subprocess.run(["git", *args], capture_output=True, text=True)
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def count_commits(days):
    since = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    output = run_git(["log", f"--since={since}", "--pretty=format:%H"])
    if not output:
        return 0
    return len(output.splitlines())


def level_from_commits(commits_7d):
    if commits_7d >= 20:
        return "HIGH PULSE", "Deep focus and strong momentum", "7CFFB2"
    if commits_7d >= 10:
        return "ACTIVE", "Consistent progress and solid rhythm", "5EEAD4"
    if commits_7d >= 4:
        return "STEADY", "Building momentum, one commit at a time", "60A5FA"
    if commits_7d >= 1:
        return "GROWING", "Small steps, steady improvement", "F59E0B"
    return "RESTING", "Recharge and plan the next move", "A78BFA"


weekly = count_commits(7)
monthly = count_commits(30)
status, note, color = level_from_commits(weekly)
updated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

block = f'''{START}
## ⚡ System Pulse

<p align="center">
  <img src="https://img.shields.io/badge/GIT+PULSE-{status}-{color}?style=for-the-badge&labelColor=101826&logo=git" alt="Git pulse" />
</p>

> {note}

- 7-day commits: {weekly}
- 30-day commits: {monthly}
- Last update: {updated_at}
{END}
'''

readme = README_PATH.read_text(encoding="utf-8")
if START in readme and END in readme:
    before, _ = readme.split(START, 1)
    _, after = readme.split(END, 1)
    readme = before + block + after
else:
    readme += "\n" + block

README_PATH.write_text(readme.strip() + "\n", encoding="utf-8")
