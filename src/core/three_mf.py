from __future__ import annotations
import os
import re
import zipfile
from typing import Any


def get_mesh_color(mesh: Any) -> str:
    color = None
    if hasattr(mesh, "visual") and mesh.visual is not None:
        if (
            hasattr(mesh.visual, "face_colors")
            and len(mesh.visual.face_colors) > 0
        ):
            c = mesh.visual.face_colors[0]
            color = f"#{c[0]:02x}{c[1]:02x}{c[2]:02x}ff"
    if color is None:
        color = "#c0b89bff"
    return color


def inject_3mf_metadata(path: str, mesh_colors: dict[str, str]) -> None:
    with zipfile.ZipFile(path, "r") as zip_read:
        model_filename = None
        for name in zip_read.namelist():
            if name in ("3D/3dmodel.model", "3dmodel.model"):
                model_filename = name
                break
        if not model_filename:
            return
        model_xml = zip_read.read(model_filename).decode("utf-8")

    unique_colors = []
    mesh_color_indices = {}

    for name, color in mesh_colors.items():
        if color not in unique_colors:
            unique_colors.append(color)
        mesh_color_indices[name] = unique_colors.index(color)

    basemats_xml = '    <basematerials id="999">\n'
    for idx, color in enumerate(unique_colors):
        basemats_xml += (
            f'      <base name="color_{idx}" displaycolor="{color}" />\n'
        )
    basemats_xml += "    </basematerials>\n"

    model_xml = model_xml.replace("<resources>", f"<resources>\n{basemats_xml}")

    def process_object(match: re.Match[str]) -> str:
        obj_tag = match.group(1)
        obj_content = match.group(0)
        obj_name_match = re.search(r'name="([^"]+)"', obj_tag)
        if obj_name_match:
            name = obj_name_match.group(1)
            if name in mesh_color_indices:
                color_idx = mesh_color_indices[name]
                new_tag = (
                    obj_tag.rstrip(">") + f' pid="999" pindex="{color_idx}">'
                )
                obj_content = obj_content.replace(obj_tag, new_tag)
                obj_content = re.sub(
                    r"<triangle\b([^>]*?)/>",
                    rf'<triangle\1 pid="999" pindex="{color_idx}"/>',
                    obj_content,
                )
        return obj_content

    model_xml = re.sub(
        r"(<object\b[^>]*>).*?</object>",
        process_object,
        model_xml,
        flags=re.DOTALL,
    )

    assembly_name = os.path.splitext(os.path.basename(path))[0]
    parent_xml = f'    <object id="1000" type="model" name="{assembly_name}">\n      <components>\n'
    for name in mesh_colors.keys():
        match = re.search(
            rf'<object\s+id="(\d+)"\s+name="{re.escape(name)}"', model_xml
        )
        if match:
            obj_id = match.group(1)
            parent_xml += f'        <component objectid="{obj_id}" />\n'
    parent_xml += "      </components>\n    </object>\n"

    model_xml = model_xml.replace("</resources>", f"{parent_xml}  </resources>")

    build_match = re.search(r"<build\b[^>]*>.*?</build>", model_xml, re.DOTALL)
    if build_match:
        original_build = build_match.group(0)
        build_start = re.match(r"<build\b[^>]*>", original_build).group(0)
        new_build = f'{build_start}\n    <item objectid="1000" />\n  </build>'
        model_xml = model_xml.replace(original_build, new_build)

    temp_path = path + ".tmp"
    with zipfile.ZipFile(path, "r") as zip_read:
        with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as zip_write:
            for item in zip_read.infolist():
                if item.filename == model_filename:
                    zip_write.writestr(item, model_xml.encode("utf-8"))
                else:
                    zip_write.writestr(item, zip_read.read(item.filename))
    os.replace(temp_path, path)
