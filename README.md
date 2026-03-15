# Manikeys Keyboard

[3D Model (STL)](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main.stl)

## Views

| Perspective | Back View |
| :---: | :---: |
| ![Perspective](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main.png) | ![Back View](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main_back.png) |

| Top View | Side View | Side View (Inverse) |
| :---: | :---: | :---: |
| ![Top View](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main_top.png) | ![Side View](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main_side.png) | ![Side View (Inverse)](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main_side_inv.png) |

This project uses [PythonSCAD](https://pythonscad.org) to design a custom 3D-printable keyboard based on spherical projections.

## Requirements

- **PythonSCAD**: Required for core CAD operations.
- **F3D**: Required **only** for the `render` step (generating PNGs).

## Development

- `make build`: Generate the STL and 3MF files for `src/main.py`.
- `make render`: Generate PNG renderings (Front, Back, Top, Side) for `src/main.py`.
- `make build/ANY_FILE.stl`: Generate STL file for `src/ANY_FILE.py`.
- `make build/ANY_FILE.3mf`: Generate 3MF file for `src/ANY_FILE.py`.
- `make build/ANY_FILE.png`: Generate PNG rendering for `src/ANY_FILE.py`.
- `make test`: Run tests.
- `make lint`: Check code quality.
