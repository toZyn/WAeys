# Contributing to WAeys

Thanks for your interest! Please read this before opening a PR.

## Development setup

```bash
git clone https://github.com/toZyn/WAeys.git
cd WAeys
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e . ".[dev]"
```

## Project layout

```
WAeys/
├── Defaults/   # default config & constants
├── Types/      # public types
├── Utils/      # crypto, messages, media, auth, noise, ...
├── WABinary/   # binary node codec
├── WAProto/    # generated pure-python protobuf classes
├── Signal/     # Signal protocol implementation
├── Socket/     # make_socket + message layers
├── WAM/        # WhatsApp Analytics Message
└── WAUSync/    # USync queries
```

## Rules

1. **No Node.js**. The whole point of the project is zero JS dependencies. Do not add `node_modules`-style code.
2. **Pure stdlib where possible**. The only runtime dependency is `websockets`.
3. **Match Baileys semantics**. This is a port; behavior, event names and payload shapes should mirror `WhiskeySockets/Baileys`.
4. **Don't add comments** unless they document non-obvious porting decisions (matching repo convention).
5. **Keep `__pycache__`, `dist/`, session files out** of commits (see `.gitignore`).
6. **Never commit session data** (`creds.json`, `keys.json`) or tokens.

## Checking your changes

```bash
python -c "import WAeys; print(WAeys.__version__)"          # imports
python -m build                                              # builds wheel + sdist
python -c "
import zipfile, glob
z = zipfile.ZipFile(glob.glob('dist/*.whl')[0])
assert any(n.endswith('WAeys/__init__.py') for n in z.namelist())
assert any(n.endswith('.proto') for n in z.namelist())
print('wheel OK')"
```

The CI workflow (`ci.yml`) runs the import checks and the wheel build on Python 3.10–3.13 across Linux, macOS and Windows.

## Releases

Creating a **GitHub Release** (not just a tag) triggers `publish-to-pypi.yml`, which builds and publishes `waeys` to PyPI using Trusted Publishing. Make sure the version in `pyproject.toml` is bumped before the release.

## License

By contributing you agree your changes are licensed under the MIT license of this project.
