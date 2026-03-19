# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to Semantic Versioning.

## [0.12] - 2026-03-18

### Added
- **`autogobble` option**: Introduced a feature that automatically calculates and strips common leading whitespace from code snippets, allowing `pygmented` environments to be indented natively in the LaTeX source.
- **Output Directory Support**: The package now actively takes into account the `$TEXMF_OUTPUT_DIRECTORY` environment variable when calling `pygmentex`.

### Fixed
- **Environment Parsing**: Rewrote the internal `pygmented` environment parser to safely preserve active newlines (`^^M`). This resolves the "Extraneous input" error that occurred when a snippet started immediately on the next line.
- **Macro Par-breaks**: The environment option parser is now defined as `\long\def`, safely allowing `\par` commands within complex styling options.
- **`\tcbox` Crash**: Injected `parbox=true` locally into inline snippets to shield them from global `\tcbset{parbox=false}` preferences, preventing a critical `\thetcolorboxnumber` collision.
- **Python Option Parsing**: The `pygmentex.py` script now aggressively strips whitespace from parsed keys and values, preventing trailing LaTeX spaces (e.g., `[lang=c  ]`) from crashing Pygments.
- **Missing Import**: Added the missing `ClassNotFound` import to `pygmentex.py`, allowing the script to gracefully report invalid language names rather than throwing a traceback.

### Changed
- **Python CLI Refactor**: Migrated command-line argument parsing in `pygmentex.py` from the older `getopt` module to the modern `argparse` library.
- **LaTeX3 Modernization**: Replaced the custom recursive `\widest` dimension-calculating macro with a modern, scoped `expl3` implementation (`\clist_map_inline:nn`).
- **Documentation**: Renamed `README` to `README.md` and comprehensively expanded it. Renamed demo files to explicitly reflect their role as the package manual.

---

## [0.11] - 2022-08-16

### Added
- **Automatic Shell Execution**: Added support for `--shell-escape`. When enabled, `pdflatex` will automatically run the `pygmentex` Python script at the end of the compilation, removing the need for a manual intermediate step.
- **`.gitignore`**: Added PygmenTeX-specific suffixes (`*.pygmented`, `*.snippets`, `*.tmp`) to the repository ignore list.

### Changed
- **Command Renaming**: Changed the `\includepygmented` command to `\inputpygmented` for better alignment with standard LaTeX naming conventions.
- **Documentation Overhaul**: Extensive documentation tweaks contributed by Barry Rountree. Added a "Requirements" section, a "Debugging" section (with notes about file paths), broke out options into logical subsections, and clarified compilation steps. 

---

## [0.10] - 2020-12-21

### Changed
- Minor internal updates and rename of demonstration files to `pygmentex_demo.pdf`.

---

## [0.9] - 2020-02-05

### Added
- Added a new, simplified example document to ease onboarding for new users.

### Changed
- **Python 3 Migration**: Fully migrated the external `pygmentex.py` script from Python 2 to Python 3.

### Fixed
- Updated package dependency name from `fvrb-ex` to the modern `fancyvrb-ex`.

---

## [0.8] - 2014-08-12

### Added
- **License**: Officially added LaTeX Project Public License (LPPL) information.
- Incorporated backported formatting code from the Pygments development branch.

### Changed
- **Option Renaming**: Renamed the `texcl` option to `texcomments`, and `style` to `sty`.
- Removed the dependency/reference to the `boites` package.
- Reworked the enclosing environment mechanism to factor out common code between inline and displayed snippets.

### Fixed
- Resolved verbatim output errors regarding Unicode characters.
- Fixed escaping for specific characters (single quotes, double quotes, and hyphens).
- Fixed option parsing logic, particularly for `tabsize`, `fvset`, and line numbering.
- Fixed an issue where some languages were unavailable when using less recent versions of the Pygments library.

---

## [Pre-0.8] - 2012 to 2014
*(Initial development and release iterations. See git history for detailed atomic changes regarding the original creation of `pygmentex.sty` and `pygmentex.py`.)*
