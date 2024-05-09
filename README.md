[![tests](https://github.com/schwallergroup/mc-peptide/actions/workflows/tests.yml/badge.svg)](https://github.com/schwallergroup/mc-peptide)
[![PyPI](https://img.shields.io/pypi/v/mc-peptide)](https://img.shields.io/pypi/v/mc-peptide)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mc-peptide)](https://img.shields.io/pypi/pyversions/mc-peptide)
[![Documentation Status](https://readthedocs.org/projects/mc_peptide/badge/?version=latest)](https://mc_peptide.readthedocs.io/en/latest/?badge=latest)
[![Cookiecutter template from @SchwallerGroup](https://img.shields.io/badge/Cookiecutter-schwallergroup-blue)](https://github.com/schwallergroup/liac-repo)
[![Learn more @SchwallerGroup](https://img.shields.io/badge/Learn%20%0Amore-schwallergroup-blue)](https://schwallergroup.github.io)


<p align="center">
  <img src="./assets/repo_logo_dark.png" height="250">
</p>


<br>

Gather, modify, and model MacroCyclic Peptide data with LLMs!


## 🔥 Usage

Extract macrocyclic peptide data out of a single paper.

```bash
mc_peptide extract -f data/papers/wang/ --llm=gpt-4-turbo
```


## 👩‍💻 Installation

<!-- Uncomment this section after your first ``tox -e finish``
The most recent release can be installed from
[PyPI](https://pypi.org/project/mc_peptide/) with:

```shell
$ pip install mc_peptide
```
-->

The most recent code and data can be installed directly from GitHub with:

```bash
$ pip install git+https://github.com/schwallergroup/mc-peptide.git
```

## ✅ Citation

```bibtex

@Misc{mc_peptide,
  author = {  },
  title = { mc_peptide -  },
  howpublished = {Github},
  year = {2023},
  url = {https://github.com/schwallergroup/mc-peptide }
}
```


## 🛠️ For Developers


<details>
  <summary>See developer instructions</summary>



### 👐 Contributing

Contributions, whether filing an issue, making a pull request, or forking, are appreciated. See
[CONTRIBUTING.md](https://github.com/schwallergroup/mc-peptide/blob/master/.github/CONTRIBUTING.md) for more information on getting involved.


### Development Installation

To install in development mode, use the following:

```bash
$ git clone git+https://github.com/schwallergroup/mc-peptide.git
$ cd mc-peptide
$ pip install -e .
```

### 🥼 Testing

After cloning the repository and installing `tox` with `pip install tox`, the unit tests in the `tests/` folder can be
run reproducibly with:

```shell
$ tox
```

Additionally, these tests are automatically re-run with each commit in a [GitHub Action](https://github.com/schwallergroup/mc-peptide/actions?query=workflow%3ATests).

### 📖 Building the Documentation

The documentation can be built locally using the following:

```shell
$ git clone git+https://github.com/schwallergroup/mc-peptide.git
$ cd mc-peptide
$ tox -e docs
$ open docs/build/html/index.html
```

The documentation automatically installs the package as well as the `docs`
extra specified in the [`setup.cfg`](setup.cfg). `sphinx` plugins
like `texext` can be added there. Additionally, they need to be added to the
`extensions` list in [`docs/source/conf.py`](docs/source/conf.py).

### 📦 Making a Release

After installing the package in development mode and installing
`tox` with `pip install tox`, the commands for making a new release are contained within the `finish` environment
in `tox.ini`. Run the following from the shell:

```shell
$ tox -e finish
```

This script does the following:

1. Uses [Bump2Version](https://github.com/c4urself/bump2version) to switch the version number in the `setup.cfg`,
   `src/mc_peptide/version.py`, and [`docs/source/conf.py`](docs/source/conf.py) to not have the `-dev` suffix
2. Packages the code in both a tar archive and a wheel using [`build`](https://github.com/pypa/build)
3. Uploads to PyPI using [`twine`](https://github.com/pypa/twine). Be sure to have a `.pypirc` file configured to avoid the need for manual input at this
   step
4. Push to GitHub. You'll need to make a release going with the commit where the version was bumped.
5. Bump the version to the next patch. If you made big changes and want to bump the version by minor, you can
   use `tox -e bumpversion -- minor` after.
</details>
