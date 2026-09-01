# PrusaSlicer print profiles

One folder per printer. Each folder is self-contained: vendor bundle, importable profiles, scripts, tests, and the G-code that profile was derived from.

| Folder | Machine | Status |
| --- | --- | --- |
| [Raise3D](Raise3D/README.md) | Pro2 Plus Hyper Speed, 0.4 mm dual | Experimental PrusaSlicer bundle |
| [Potterbot](Potterbot/README.md) | 3D Potterbot 9 (Duet 2 WiFi) | Source files only; no PrusaSlicer profile yet |

Add a new printer as a sibling folder with the same layout (`vendor/`, `profiles/`, `docs/`, `reference/`). Do not put printer-specific G-code or post-process scripts at the repo root.

## Lab PC path

Clone or copy this repo to:

```text
C:\Repos\Prusa-Slicer-Print-Profiles
```

Raise3D print profiles call post-process scripts by that absolute path. If the folder lives anywhere else, edit `post_process` in `Raise3D/vendor/Raise3D.ini` (and the matching bundle) before slicing.

## Tests

```text
python -m unittest discover -s Raise3D/tests -v
```
