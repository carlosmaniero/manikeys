# Manikeys Keyboard

![Manikeys](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/render_angle0.png)

[3D Model (STL)](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main.stl)

## Views

| | | |
| :---: | :---: | :---: |
| ![0°](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/render_angle0.png) | ![45°](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/render_angle45.png) | ![90°](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/render_angle90.png) |
| ![135°](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/render_angle135.png) | ![180°](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/render_angle180.png) | ![225°](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/render_angle225.png) |
| ![270°](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/render_angle270.png) | ![315°](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/render_angle315.png) | ![Top](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/render_top.png) |
| ![Side](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/render_side.png) | ![Side Inv](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/render_side_inv.png) | ![Back](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/render_back.png) |

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
