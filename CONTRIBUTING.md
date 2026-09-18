# Contributing to AI Agent 01

Thank you for your interest in contributing! This document outlines the workflow, coding conventions, and expectations for the repository. By participating, you agree to abide by its terms.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
   - [Reporting Bugs](#reporting-bugs)
   - [Suggesting Enhancements](#suggesting-enhancements)
   - [Your First Code Contribution](#your-first-code-contribution)
3. [Development Setup](#development-setup)
4. [Coding Guidelines](#coding-guidelines)
5. [Testing](#testing)
6. [Commit & Pull Request Workflow](#commit--pull-request-workflow)
7. [Style Checklist](#style-checklist)

---

## Code of Conduct

Be respectful, constructive, and inclusive. Harassment, offensive language, and trolling of any kind will not be tolerated. Focus discussions on the code and the problem at hand.

## How to Contribute

### Reporting Bugs

Before opening an issue:

- Search the [issue tracker](https://github.com/bilalhaider-ux/ai_agent_01/issues) for existing reports.
- Provide a **minimal, reproducible example** — include the dataset (or a small sample), the exact `--query`, the LLM provider/model used, and the full error output.
- Mention your OS, Python version, and the versions of the packages in `requirements.txt`.

Please use the issue template fields (if available) and mark checkboxes clearly.

### Suggesting Enhancements

Clearly describe the problem you want to solve and the proposed solution. If it changes the agent workflow, consider updating `AI_AGENT_DEVELOPMENT_GUIDE.md` alongside your code.

### Your First Code Contribution

Unsure where to start? Great entry points:

- Areas with missing error handling or edge cases in `src/nodes.py` / `src/executor.py`.
- Expanding the mock LLM in `src/mock_llm.py` (taking `src/contracts.py` into account).
- Adding more integration tests in `tests/test_agent_pipeline.py`.
- Improving the report HTML styling in `src/main.py`.

## Development Setup

1. **Fork** the repository and **clone** your fork:

   ```bash
   git clone https://github.com/<your-username>/ai_agent_01.git
   cd ai_agent_01
   ```

2. **Create a virtual environment** and install dependencies:

   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS / Linux:
   source .venv/bin/activate

   pip install -r requirements.txt
   ```

3. **Add the upstream remote** (for syncing):

   ```bash
   git remote add upstream https://github.com/bilalhaider-ux/ai_agent_01.git
   ```

4. **Create a feature branch** from the latest `main`:

   ```bash
   git checkout main
   git pull upstream main
   git checkout -b feature/<your-feature-name>
   ```

> 🔑 Never modify or commit `.env` — it lives under local development only.

## Coding Guidelines

- **Language**: Python 3.10+.
- **Style**: Follow [PEP 8](https://peps.python.org/pep-0008/). Keep lines readable (≤ ~100 characters).
- **Docstrings**: New modules, functions, and classes should use Google-style/practical docstrings explaining the *what* and *why*.
- **Types**: Prefer clear typing (`Optional`, `Literal`, Pydantic models) matching the existing code in `src/contracts.py` and `src/config.py`.
- **No secrets**: Never commit API keys, tokens, or any real credential — including in tests, sample files, or commit messages.
- **Stay in the workflow**: New logic should fit the existing LangGraph stage structure unless you are intentionally redesigning it (and updating the guide accordingly).
- **Do not commit generated artifacts**: `decision_ready_artifact.md` / `.html` files generated during local runs are usually not intended for PRs unless explicitly required by the change.

## Testing

All changes must keep the test suite green. Tests use the standard `unittest` module and run **without** any LLM server (the mock engine is used for full-pipeline invocation):

```bash
python -m unittest discover -s tests -v
```

When adding a feature:

1. Add or update tests in `tests/test_agent_pipeline.py` (or a new test module).
2. Prefer isolated unit tests for pure functions and integration tests through `build_data_agent_graph()` with `LLM_PROVIDER=mock`.
3. Run the full suite locally and ensure existing tests still pass.

## Commit & Pull Request Workflow

1. **Commit with a clear message**, using a short imperative summary line:

   ```
   Add --minimize-context CLI flag to limit minifier rollout
   ```

   Bullet points may follow the summary line to explain the rationale.

2. **Push your branch** to your fork:

   ```bash
   git push -u origin feature/<your-feature-name>
   ```

3. **Open a pull request** against the `main` branch. In the PR description, include:
   - What the change does and why.
   - How it was tested (commands + observed results).
   - Any trade-offs or follow-ups.

4. **Keep the PR focused** — one logical change per PR. Smaller PRs are reviewed and merged faster.

5. **Respond to review feedback** in the same branch; the PR updates automatically.

> If a merge conflict arises, rebase your branch onto the latest `main` (`git pull --rebase upstream main`) and force-push your follow-up commits. That's also the right time to confirm you are helping rather than just curious once review is finished.

## Style Checklist

Before submitting your PR, confirm:

- [ ] Tests added/updated and the full suite passes locally.
- [ ] No `print` debugging left in `src/` unless intentional diagnostics.
- [ ] No `.env`, credentials, or generated artifacts staged.
- [ ] Docstrings present for new public functions/classes.
- [ ] Guide documentation (`AI_AGENT_DEVELOPMENT_GUIDE.md`) updated if the workflow changed.
- [ ] Lint-clean (PEP 8); imports organized and unused ones removed.

Thanks again for contributing! 🙌