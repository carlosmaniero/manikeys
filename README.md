# Manikeys Keyboard

![Keyboard Rendering](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main.png)

## Views

| Top View | Side View |
| :---: | :---: |
| ![Top View](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main_top.png) | ![Side View](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main_side.png) |

This project uses PythonSCAD to design a custom 3D-printable keyboard based on spherical projections.

## Development

- `make build`: Generate the STL and 3MF files for `src/main.py`.
- `make render`: Generate PNG renderings for `src/main.py`.
- `make build/ANY_FILE.stl`: Generate STL file for `src/ANY_FILE.py`.
- `make build/ANY_FILE.3mf`: Generate 3MF file for `src/ANY_FILE.py`.
- `make build/ANY_FILE.png`: Generate PNG rendering for `src/ANY_FILE.py`.
- `make test`: Run tests.
- `make lint`: Check code quality.
