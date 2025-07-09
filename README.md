<p align="center">
  <img alt="bluetex" src="logo/logo.png" width="60%">
  <p align="center">Clean up your LaTeX files.</p>
</p>

## Fork Notice

**Bluetex** is a fork of the original [Blacktex](https://github.com/texworld/blacktex/) project by Nico Schlömer. The original project moved to a non-public development style, so this fork was created to continue public development under the name "Bluetex" to avoid confusion with the original project.

- **Original author**: Nico Schlömer (up to commit 9df96918bd9075ddd659a9e272e16c6426011e31, 2022-02-16)
- **Fork maintainer**: David Völgyes (from 2025 onwards)
- **Original project**: https://github.com/texworld/blacktex/

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

Bluetex is a command-line tool that helps with article editing in LaTeX. It removes all
comments from a given file and corrects [some common
anti-patterns](http://mirrors.ctan.org/info/l2tabu/english/l2tabuen.pdf).

Install with:

```
pip install -U bluetex
```

Then, with

```
bluetex in.tex > out.tex
```

the input file

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

```
bluetex -i in0.tex in1.tex ...
```

to modify files in-place. See `bluetex -h` for all options.

### License

This software is published under the [GPLv3
license](https://www.gnu.org/licenses/gpl-3.0.en.html).
