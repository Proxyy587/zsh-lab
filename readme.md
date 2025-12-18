# zsh-lab

A minimal custom commands for your terminal using python

as per now there are only two commands

- **`cf`**: opens random codeforces question in ur browser.
- **`gpt`**: tiny cli based gpt.

you can install, uninstall and check status everything using one script.

---

## Requirements

- **macOS or Linux** (zsh shell)
- **Python 3.8+**
- **git**
- **OpenAI API key** (for GPT command)

_All commands use a local virtual environment (venv), so your system Python is untouched._

---

## Installation

### 1. Fork and clone this repo

```bash
git clone https://github.com/<your-username>/zsh-lab.git
cd zsh-lab
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install requests
```
as per now its only using requests. I will update this if we use more packages

### 4. Install `cf` and `gpt` global commands

In your activated venv:
```bash
python devcli.py install
```
_Output will show you the launcher directory and PATH instructions._

### 5. Add `~/bin` to your Zsh `PATH` (if not already on PATH)

```bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

## Usage

Once installed, use the commands in **any terminal** (no need to activate the venv or be in the repo):

### Codeforces

```bash
cf          # open a random Codeforces problem
cf random   # (also works)
```

### GPT (OpenAI Chat)

1. **Store your OpenAI API key:**
   ```bash
   gpt --token sk-...YOUR_API_KEY...
   ```
   _(Key is safely saved at `~/.config/zsh-lab/config.json`.)_

2. **Ask a question:**
   ```bash
   gpt "What are Python decorators?"
   gpt "Explain quicksort."
   ```

---

## Uninstalling / Reinstalling

All command management uses `devcli.py`. For best results, reactivate the same venv:

```bash
cd zsh-lab
source .venv/bin/activate
```

_Check install status:_
```bash
python devcli.py status
```

_Uninstall (removes launchers from `~/bin`, keeps your config):_
```bash
python devcli.py uninstall
```

_Reinstall anytime:_
```bash
python devcli.py install
```

---

## How it Works

- **`commands/cf.py`** — Fetches and opens random Codeforces problems.
- **`commands/gpt.py`** — Manages API keys and talks to OpenAI.
- **`devcli.py`** — Installs, uninstalls, status checks, and dispatches calls to the other scripts.

When you install, small launcher scripts (`cf`, `gpt`) get created in `~/bin`. These always call into your current repo and Python venv (no global Python requirement). You almost never have to reinstall unless you move the directory or break launcher symlinks.

---

## Contributing

Contributions are welcome! To propose changes, fix bugs, or add features:

1. **Fork** the repo and create a branch.
2. Make your changes (please add/update [docstrings](https://www.python.org/dev/peps/pep-0257/) and [type hints](https://docs.python.org/3/library/typing.html) where possible).
3. Test your additions locally using a venv and the CLI.
4. Submit a pull request describing your changes.

**Ideas for contribution:**
- Add more commands or integrate other APIs/tools.
- Improve GPT prompt experience or allow model selection.
- Enhance config file management or add encryption for the API key.
- Write tests or better error messages.
- Update and improve documentation.

Please keep your code style simple and follow PEP-8 where practical. All contributions, big or small, are appreciated!

---

## License

MIT

---


