# Phased Migration Plan: miniver → setuptools-scm

## Phase 0: Pre-Migration Audit
1. Check `octoprint_octorelay/__init__.py` for version import patterns
2. Confirm a `v5.3.0` git tag exists (matches current version)
3. Confirm no `setup.py`/`setup.cfg` remains

---

## Phase 1: Update `pyproject.toml`
1. Add `setuptools-scm>=8` to `[build-system].requires`:
   ```toml
   [build-system]
   requires = ["setuptools>=77", "setuptools-scm>=8"]
   build-backend = "setuptools.build_meta"
   ```
2. Switch to dynamic version (remove static `version`, add `dynamic`):
   ```toml
   [project]
   name = "OctoRelay"
   dynamic = ["version"]
   # ... rest unchanged
   ```
3. Add setuptools-scm config (no `version_file` needed):
   ```toml
   [tool.setuptools_scm]
   ```

---

## Phase 2: Update `__init__.py` & Remove Miniver
1. In `octoprint_octorelay/__init__.py`, replace:
   ```python
   from ._version import __version__
   ```
   with:
   ```python
   from importlib.metadata import version
   __version__ = version("OctoRelay")
   ```
2. Delete miniver artifacts:
   - `octoprint_octorelay/_version.py`
   - `octoprint_octorelay/_static_version.py`

---

## Phase 3: Fix Release Workflow
Update `.github/workflows/release.yaml` to use `python -m build` instead of deprecated `python setup.py sdist`:
1. Replace install step: `pip install --upgrade wheel setuptools pip` → `pip install build`
2. Replace build step: `python setup.py sdist --formats=zip` → `python -m build --sdist`
3. Update artifact path: `dist/octorelay-*.zip` (build outputs `.tar.gz` by default, or add `--formats=zip` to build command)

---

## Phase 4: Validate & Test
1. `python -m build --sdist --wheel` — confirm version from git tag
2. `pip install -e . && python -c "import octoprint_octorelay; print(octoprint_octorelay.__version__)"`
3. Commit only after tests pass
