# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`django-adminlte2-pdq` is a reusable Django app (package `adminlte2_pdq`, built with flit) that provides AdminLTE2 templates, a settings-driven sidebar menu, Django Admin restyling, and an authentication/authorization layer (middleware + decorators + mixins). It supports Python >= 3.7 and Django >= 3.2, so avoid syntax or Django APIs newer than those floors.

## Commands

Dependencies come from uv: `uv sync --all-extras` creates `.venv/` with the package and its `dev`, `doc`, and `test` extras. `uv run` always uses the project's `.venv/`, even when the shell has `VIRTUAL_ENV` set from another project (it prints a warning and ignores it).

```bash
# Run all tests (pytest; settings come from pyproject.toml)
uv run pytest -n auto

# Single file / class / test
uv run pytest tests/django_adminlte2_pdq/tests/test_middleware.py
uv run pytest "tests/django_adminlte2_pdq/tests/test_decorators/test_strict_mode.py::TestStrictAuthenticationDecorators::test__no_decorators"

# Tests with an HTML coverage report (written to .django_adminlte_pdq_coverage_html_report/)
uv run python runtests.py --with-coverage [--less-than-100]

# Full matrix (Python/Django versions, docs build, warnings-as-errors against Django main)
tox

# Format / lint with Ruff (line length 120; settings in pyproject.toml)
uv run ruff format .
uv run ruff check .

# Docs (Sphinx, reStructuredText in docs/source). CI builds them with -W, so warnings fail.
uv run sphinx-build -WE docs/source docs/build
./docs/generate_docs.sh   # regenerates docs/source/api_reference via sphinx-apidoc, then rebuilds
```

## Commits, changelog, and writing style

- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/): `type(scope): summary`, with the summary in lowercase imperative and no trailing period. Types used here: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `build`, `ci`, `chore`. `style` means code formatting only; CSS changes are `feat(css)` or `fix(css)`. Common scopes: `middleware`, `sidebar`, `menu`, `css`, `js`, `templates`, `views`, `docs`, `tests`. Mark breaking changes with `!` (e.g. `feat(css)!: ...`) and a `BREAKING CHANGE:` footer.
- Commits are GPG-signed (`commit.gpgsign` is set in this repo's local git config).
- Each user-facing change adds an entry to the "Unreleased" section at the top of `docs/source/version_history.rst` in the same commit. At release, that section is renamed to the version number.
- Docs, changelog entries, and commit messages are direct and neutral: state what changed and how to use it. No opinions or emotional wording ("it was bad", "really needed it").

## Architecture

### Settings are frozen into module constants at import time

`adminlte2_pdq/constants/` reads all `ADMINLTE2_*` settings with `getattr(settings, ...)` when the module is imported, and computes `STRICT_POLICY` / `LOGIN_REQUIRED` (strict implies login required; using a whitelist setting without its policy raises `ImproperlyConfigured`). Other modules import these constants by name, so `override_settings` has **no effect** on them in tests. Tests instead `unittest.mock.patch` the name in the module that uses it, e.g. `@patch("adminlte2_pdq.middleware.STRICT_POLICY", True)` and `@patch("adminlte2_pdq.templatetags.sidebar_menu.STRICT_POLICY", True)`. A behavior change usually needs both the middleware and the sidebar patched.

### Auth: three policy modes enforced in one middleware

The project runs in one of three modes: loose (default), login-required (`ADMINLTE2_USE_LOGIN_REQUIRED`), or strict (`ADMINLTE2_USE_STRICT_POLICY`, which means every view needs explicit permissions or a whitelist entry).

- **Decorators** (`decorators.py`) and **mixins** (`mixins.py`) come in matching sets: `allow_anonymous_access`, `login_required`, `allow_without_permissions`, `permission_required`, and `permission_required_one`. Each one attaches an `admin_pdq_data` dict to the view function or class. Decorators set it on the function. Mixins define it as a class attribute and record subclasses through `__init_subclass__`.
- **`middleware.AuthMiddleware`** resolves the request URL (`parse_request_data`), reads `admin_pdq_data` from the resolved view, and decides whether to allow, redirect to login, redirect home with a message (403), or raise `Http404`/`PermissionDenied`. It also raises `ImproperlyConfigured` for decorator/policy combinations that conflict (`check_main_error_states`, `check_post_login_check_error_states`). Whitelists come in exact form (route names/URLs) and "fuzzy" form (path prefixes, via `path_starts_with_whitelist_entry`), including the `SERVE_403`/`SERVE_404` fuzzy whitelists.
- **Sidebar** (`templatetags/sidebar_menu.py`) mirrors the same rules to decide which menu nodes to show (`is_allowed_node`). It resolves each node's route to its view and reads the permissions from that view's decorator or mixin. When auth behavior changes, the middleware and sidebar logic usually both need updating.

### Generated CSS

Some CSS under `adminlte2_pdq/static/adminlte2_pdq/css/` is generated and committed; never edit it by hand. Tests fail when the committed files differ from the generator output.

- `python -m adminlte2_pdq.color_css` writes `css/extra-colors/color-variables.css` (`--pdq-{color}-{part}` custom properties) and `css/extra-colors/extra-colors.css` (color classes for every component). It only emits classes that AdminLTE 2.3.11 / Bootstrap 3.3.7 don't already define, so stock components keep their look. `--custom NAME BASE` prints CSS for a project's own color.
- `python -m adminlte2_pdq.dark_css` writes `css/dark-mode/dark-skins.css` (AdminLTE skins renamed to `skin-{color}-dark`) and `css/dark-mode/dark-mode.css` from `adminlte2_pdq/css_source/dark_mode.css`, where the `.pdq-dark` prefix expands to `:is(.skin-blue-dark, ...)`. Every dark rule must stay scoped to a dark skin (tested), because the files are always loaded.
- To check rendering, compare screenshots of the demo pages (`/demo-css/`) in light and dark skins.

### Menu and templates

- The menu is built from `ADMINLTE2_MENU_FIRST`, `ADMINLTE2_MENU` (default in `menu.py`), the auto-generated admin menu (`admin_menu.py` / `templatetags/admin/`), and `ADMINLTE2_MENU_LAST`. If you change the default `menu.py` routes, also update `_default_routes_are_registered` in `sidebar_menu.py`.
- Templates live in `adminlte2_pdq/templates/` (`adminlte2/`, `admin/` overrides, `registration/`). The app must be listed before Django's apps in `INSTALLED_APPS` so its admin and registration templates take precedence.
- `adminlte_tags.py` / `adminlte_filters.py` provide form rendering and styling helpers used by the templates.

### Tests

- A test Django project lives at `tests/django_adminlte2_pdq/django_test_project/` (`DJANGO_SETTINGS_MODULE = tests.django_adminlte2_pdq.django_test_project.settings`). Its `views.py`/`urls*.py` define one test view for each decorator/mixin variant, under the `adminlte2_pdq_tests:` namespace.
- Tests use `django-expanded-test-cases` (`assertGetResponse`, `assertRedirects`, …). The decorator and mixin suites each have a `base_test_case.py` and one file per policy mode (`test_loose_mode.py`, `test_login_required_mode.py`, `test_strict_mode.py`, `test_isolated_*`). Keep the decorator and mixin suites in step with each other.
- Middleware warnings are asserted with `pytest.warns`.

### Docs

User-facing docs are in `docs/source` (rst) and published on Read the Docs. Changes to settings or auth behavior should also update `docs/source/configuration/` and `docs/source/authorization/`, plus `version_history.rst`.
