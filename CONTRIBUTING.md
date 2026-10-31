## Contributing

[fork]: /fork
[pr]: /compare
[style]: https://pypi.org/project/black/
[code-of-conduct]: CODE_OF_CONDUCT.md

Hi there! We're thrilled that you'd like to contribute to this project. Your help is essential for keeping it great.

Please note that this project is released with a [Contributor Code of Conduct][code-of-conduct]. By participating in this project you agree to abide by its terms.

## Issues and PRs

If you have suggestions for how this project could be improved, or want to report a bug, open an issue! We'd love all and any contributions. If you have questions, too, we'd love to hear them.

We'd also love PRs. If you're thinking of a large PR, we advise opening up an issue first to talk about it, though! Look at the links below if you're not sure how to open a PR.

## Submitting a pull request

1. [Fork][fork] and clone the repository.
1. Configure and install Pipenv: `python -m pip install pipenv`.
1. Create a virtual environment using pipenv for the latest supported version of python.
1. Configure and install the dependencies: `pipenv sync --dev`.
1. Make sure the tests pass on your machine: `pipenv run python runtests.py`.
1. Ensure you are able to run tests with code coverage: `pipenv run python runtests.py --with-coverage`.
1. Create a new branch: `git checkout -b my-branch-name`.
1. Make your change, add tests, and make sure the tests still pass.
1. Push to your fork and [submit a pull request][pr].
1. Pat your self on the back and wait for your pull request to be reviewed and merged.

Here are a few things you can do that will increase the likelihood of your pull request being accepted:

- Follow the [style guide][style] which is using standard.
- Write and update tests.
- Verify new functionality and tests do not reduce test coverage.
- Keep your changes as focused as possible. If there are multiple changes you would like to make that are not dependent upon each other, consider submitting them as separate pull requests.
- Write a [good commit message](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).

Work in Progress pull requests are also welcome to get feedback early on, or if there is something blocking you.

## Tests

The tests live in `tests/django_adminlte2_pdq/tests/`, in two folders:

- `core/`: tests that don't depend on AdminLTE 2: authentication and authorization (`auth/`), which menu nodes a user can see (`menu/`), and settings (`settings/`).
- `ui/`: tests for the AdminLTE 2 side: template tags, CSS, views, and static files.

The test project in `tests/django_adminlte2_pdq/django_test_project/` has one test view for each decorator and mixin.

To run one file or one test:

```bash
pipenv run pytest tests/django_adminlte2_pdq/tests/core/menu/test_helpers.py
pipenv run pytest "tests/django_adminlte2_pdq/tests/core/auth/access/test_strict_mode.py::StrictModeAccessTestCase::test__strict_mode"
```

To run the full matrix of Python and Django versions, run `tox`.

### Tables of expected results

What each kind of user can open (`core/auth/access/`) and see in the menu (`core/menu/`) is tested with tables. Each policy setup (loose, login required, or strict, with or without whitelists) has a table. Each row is a kind of view or menu node, and each column a kind of user. Each table file has a legend of the cell values and columns. For example:

```python
STRICT_MODE = {
    #                                          user                   staff
    #                                     an in   no wp pp fp wg pg fg   no wp pp fp wg pg fg   su
    "none":                               (L, L,   H, H, H, H, H, H, H,   H, H, H, H, H, H, H,   H),
    "one_permission_required":            (L, L,   H, H, Y, Y, H, Y, Y,   H, H, Y, Y, H, Y, Y,   Y),
```

When you change what a user can open or see, change the cells in the table. When you add a kind of view or user, add a row or column. The tests check that every table has every row and column.

### subTest

Use `self.subTest` only to loop over data, and name the values with keywords, for example `self.subTest(view=..., user=...)`. A failure then shows which values failed. If a case needs its own setup, write it as a separate test method.

## Resources

- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [Using Pull Requests](https://help.github.com/articles/about-pull-requests/)
- [GitHub Help](https://help.github.com)
