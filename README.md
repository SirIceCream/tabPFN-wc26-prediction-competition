# TabPFN World Cup 2026 Prediction Competition

Workspace for building a TabPFN-based prediction entry for the World Cup 2026 match outcome competition.

## Layout

```text
.
├── docs/
│   ├── data.md
│   └── rules.md
├── data/
│   └── raw/
│       └── international_results/
└── tabpfn-football-predictions/
```

## Upstream Inputs

- `tabpfn-football-predictions/`: Prior Labs starter repository with the baseline script, sample output pattern, and submission-oriented prediction format.
- `data/raw/international_results/`: raw clone of `martj42/international_results`, used for historical international results and fixture rows.

Both upstream repositories are registered as submodules in `.gitmodules` so this wrapper project can track exact source revisions.

## First Commands

```bash
cd tabpfn-football-predictions
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python predict.py
```

See [docs/rules.md](docs/rules.md) and [docs/data.md](docs/data.md) before changing modeling logic.

