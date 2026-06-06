<p align="center">
  <img alt="bluetex" src="logo/logo.png" width="60%">
  <p align="center">Clean up your LaTeX files.</p>
</p>

<p>
  <a href="https://github.com/dvolgyes/bluetex/actions/workflows/ci-cd.yml"><img alt="CI" src="https://github.com/dvolgyes/bluetex/actions/workflows/ci-cd.yml/badge.svg" /></a>
  <a href="https://coveralls.io/github/dvolgyes/bluetex?branch=main"><img alt="Coverage Status" src="https://coveralls.io/repos/github/dvolgyes/bluetex/badge.svg?branch=main" /></a>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://pypi.org/project/bluetex/"><img alt="Version: 0.6.2" src="https://img.shields.io/badge/version-0.6.2-orange.svg" /></a>
  <a href="https://pypi.org/project/bluetex/"><img alt="Status: Beta" src="https://img.shields.io/badge/status-beta-yellow.svg" /></a>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <a href="LICENSE"><img alt="License: GPLv3" src="https://img.shields.io/badge/license-GPLv3-green.svg" /></a>
  <a href="https://www.python.org/"><img alt="Python: >=3.12" src="https://img.shields.io/badge/python-%3E=3.12-blue.svg" /></a>
</p>

## Fork Notice

**Bluetex** is a fork of the original [Blacktex](https://github.com/texworld/blacktex/) project by Nico Schlömer. The original project moved to a non-public development style, so this fork was created to continue public development under the name "Bluetex" to avoid confusion with the original project.

- **Original author**: Nico Schlömer (up to commit 9df96918bd9075ddd659a9e272e16c6426011e31, 2022-02-16)
- **Fork maintainer**: David Völgyes (from 2025 onwards)
- **Original project**: https://github.com/texworld/blacktex/

Bluetex is a command-line tool that helps with article editing in LaTeX. It removes all
comments from a given file and corrects [some common
anti-patterns](http://mirrors.ctan.org/info/l2tabu/english/l2tabuen.pdf).

## Usage

Run the package directly with `uvx`:

```bash
uvx bluetex in.tex > out.tex
```

For example, this input file

```latex
Because   of $$a+b=c$$ ({\it Pythogoras}),
% @johnny remember to insert name
and $y=2^ng$ with $n=1,...,10$, we have ${\Gamma \over 2}=8.$
```

is converted to

```latex
Because of
\[
a+b = c
\]
(\textit{Pythogoras}),
and \(y = 2^n g\) with \(n = 1,\dots,10\), we have \(\frac{\Gamma}{2} = 8\).
```

You can use

```bash
uvx bluetex -i in0.tex in1.tex ...
```

to modify files in-place. See `uvx bluetex --help` for all options.

## Pre-commit hooks

You can clean LaTeX files automatically before committing them to git.

```yaml
repos:
- repo: https://github.com/dvolgyes/bluetex
  rev: v0.6.2
  hooks:
  - id: bluetex
```

The hook runs `bluetex --in-place` on staged `.tex` files.

## License

This software is published under the [GPLv3
license](https://www.gnu.org/licenses/gpl-3.0.en.html).
