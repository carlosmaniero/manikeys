from __future__ import annotations
import argparse
import sys
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / "templates"


def snake_to_pascal(name: str) -> str:
    return "".join(word.capitalize() for word in name.split("_"))


def render_template(template_name: str, **kwargs: str) -> str:
    template_path = TEMPLATES_DIR / template_name
    template_content = template_path.read_text()
    return template_content.format(**kwargs)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate boilerplate code for CAD components."
    )
    parser.add_argument(
        "target_file",
        type=str,
        help="Target CAD python file path (e.g. src/assembly/base_plate/cad/base_plate.py)",
    )
    parser.add_argument(
        "--with-model",
        action="store_true",
        help="Generate model.py alongside CAD file",
    )
    parser.add_argument(
        "--with-parameters",
        action="store_true",
        help="Generate parameters.py alongside CAD file",
    )
    parser.add_argument(
        "--skip-cad-check",
        action="store_true",
        help="Skip verification that target file is inside a 'cad' directory",
    )

    args = parser.parse_args()
    target_path = Path(args.target_file).resolve()

    if "cad" not in target_path.parts[:-1]:
        print("Warning: Target file is not inside a 'cad' folder.")
        if not args.skip_cad_check:
            sys.stderr.write(
                "Error: Target file must be inside a 'cad' directory. Use --skip-cad-check to bypass.\n"
            )
            sys.exit(1)

        if args.with_model or args.with_parameters:
            print(
                "Warning: --with-model and --with-parameters flags are ignored when --skip-cad-check is active."
            )
            args.with_model = False
            args.with_parameters = False

    # Extract component details
    stem = target_path.stem
    class_name = snake_to_pascal(stem)
    var_name = stem

    # Create target directory if needed
    target_path.parent.mkdir(parents=True, exist_ok=True)

    # Determine import prefix
    parts = list(target_path.parts)
    if "src" in parts:
        src_index = parts.index("src")
        if "cad" in parts[src_index:]:
            cad_index = parts.index("cad", src_index)
            rel_parts = parts[src_index + 1 : cad_index]
        else:
            rel_parts = parts[src_index + 1 : -1]
        import_prefix = ".".join(rel_parts)
    else:
        import_prefix = target_path.parent.parent.name

    if not target_path.exists():
        template_name = (
            "cad.py.template"
            if args.with_model
            else "cad_without_model.py.template"
        )
        cad_code = render_template(
            template_name,
            class_name=class_name,
            import_prefix=import_prefix,
            var_name=var_name,
        )
        target_path.write_text(cad_code)
        print(f"Created: {target_path}")
    else:
        print(f"Skipped existing: {target_path}")

    component_dir = (
        target_path.parent.parent
        if "cad" in target_path.parts[:-1]
        else target_path.parent
    )

    if args.with_model:
        model_path = component_dir / "model.py"
        if not model_path.exists():
            model_code = render_template(
                "model.py.template",
                class_name=class_name,
                import_prefix=import_prefix,
            )
            model_path.write_text(model_code)
            print(f"Created: {model_path}")
        else:
            print(f"Skipped existing: {model_path}")

    if args.with_parameters:
        params_path = component_dir / "parameters.py"
        if not params_path.exists():
            params_code = render_template(
                "parameters.py.template",
                class_name=class_name,
            )
            params_path.write_text(params_code)
            print(f"Created: {params_path}")
        else:
            print(f"Skipped existing: {params_path}")


if __name__ == "__main__":
    main()
