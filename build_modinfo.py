from __future__ import annotations

from copy import deepcopy
from pathlib import Path, PurePosixPath
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
TEXTS_DIR = ROOT / "Texts"
PROPERTIES_FILE = ROOT / "Properties.xml"
OUTPUT_FILE = ROOT / "Civ6_JP_Localization.modinfo"

MOD_ID = "d8920739-5ce8-439a-a41c-3d405bdf291e"
MOD_VERSION = "1"
MOD_AUTHOR = "Civ6 JP modding community"

SAFE_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def parse_xml(path: Path) -> ET.ElementTree:
    try:
        return ET.parse(path)
    except ET.ParseError as exc:
        raise RuntimeError(f"XMLの解析に失敗しました: {path}\n{exc}") from exc


def add_unique_id(used_ids: set[str], value: str, source: Path) -> None:
    if value in used_ids:
        raise RuntimeError(f"Criteria ID が重複しました: {value}\n発生元: {source}")
    used_ids.add(value)


def rewrite_file_path(
    file_element: ET.Element,
    mod_folder: Path,
    used_files: set[str],
) -> None:
    if not file_element.text or not file_element.text.strip():
        raise RuntimeError(f"<File> が空です: {mod_folder / 'modinfo.xml'}")

    raw = file_element.text.strip().replace("\\", "/")
    relative = PurePosixPath(raw)

    if relative.is_absolute() or ".." in relative.parts:
        raise RuntimeError(
            f"親MODフォルダ外を参照する<File>は使用できません: {raw}\n"
            f"発生元: {mod_folder / 'modinfo.xml'}"
        )

    actual_file = mod_folder.joinpath(*relative.parts)

    if not actual_file.is_file():
        raise RuntimeError(
            f"<File> で指定されたファイルが見つかりません:\n  {actual_file}"
        )

    output_path = actual_file.relative_to(ROOT).as_posix()
    file_element.text = output_path
    used_files.add(output_path)


def namespace_fragment_criteria(
    fragment_root: ET.Element,
    folder_name: str,
    final_action_criteria: ET.Element,
    used_criteria_ids: set[str],
    source: Path,
) -> dict[str, str]:
    mapping: dict[str, str] = {}

    section = fragment_root.find("ActionCriteria")
    if section is None:
        return mapping

    for criterion in section.findall("Criteria"):
        old_id = criterion.get("id")
        if not old_id:
            raise RuntimeError(f"idのない<Criteria>があります: {source}")

        new_id = f"{folder_name}_{old_id}"
        add_unique_id(used_criteria_ids, new_id, source)

        copied = deepcopy(criterion)
        copied.set("id", new_id)

        final_action_criteria.append(copied)
        mapping[old_id] = new_id

    return mapping


def make_parent_criterion(
    criterion_id: str,
    condition_name: str,
    parent_mod_id: str,
    final_action_criteria: ET.Element,
    used_criteria_ids: set[str],
    source: Path,
) -> None:
    add_unique_id(used_criteria_ids, criterion_id, source)

    criterion = ET.SubElement(
        final_action_criteria,
        "Criteria",
        {"id": criterion_id},
    )
    condition = ET.SubElement(criterion, condition_name)
    condition.text = parent_mod_id


def copy_actions(
    source_section: ET.Element | None,
    target_section: ET.Element,
    parent_criterion_id: str,
    criteria_mapping: dict[str, str],
    mod_folder: Path,
    used_files: set[str],
) -> int:
    if source_section is None:
        return 0

    count = 0

    for original_action in source_section:
        action = deepcopy(original_action)

        for criterion_ref in action.findall("Criteria"):
            if not criterion_ref.text:
                continue

            old_ref = criterion_ref.text.strip()
            if old_ref in criteria_mapping:
                criterion_ref.text = criteria_mapping[old_ref]

        parent_ref = ET.Element("Criteria")
        parent_ref.text = parent_criterion_id

        action.insert(0, parent_ref)

        for file_element in action.findall("File"):
            rewrite_file_path(file_element, mod_folder, used_files)

        target_section.append(action)
        count += 1

    return count


def collect_automatic_files(mod_folder: Path) -> list[str]:
    return sorted(
        path.relative_to(ROOT).as_posix()
        for path in mod_folder.rglob("*")
        if path.is_file() and path.suffix.lower() in {".xml", ".sql"}
    )


def add_automatic_actions(
    folder_name: str,
    files: list[str],
    frontend_section: ET.Element,
    ingame_section: ET.Element,
    used_files: set[str],
) -> None:
    for section in (frontend_section, ingame_section):
        action = ET.SubElement(section, "UpdateText", {"id": folder_name})
        for file_path in files:
            ET.SubElement(action, "File").text = file_path

    used_files.update(files)


def main() -> None:
    if not PROPERTIES_FILE.is_file():
        raise RuntimeError(f"Properties.xml がありません: {PROPERTIES_FILE}")

    if not TEXTS_DIR.is_dir():
        raise RuntimeError(f"Texts フォルダがありません: {TEXTS_DIR}")

    properties_tree = parse_xml(PROPERTIES_FILE)
    properties_root = properties_tree.getroot()

    if properties_root.tag != "Properties":
        raise RuntimeError(
            "Properties.xml のルート要素は <Properties> にしてください。"
        )

    final_root = ET.Element(
        "Mod",
        {
            "id": MOD_ID,
            "version": MOD_VERSION,
        },
    )

    final_properties = deepcopy(properties_root)
    for element in final_properties.findall("Authors"):
        final_properties.remove(element)
    ET.SubElement(final_properties, "Authors").text = MOD_AUTHOR
    final_root.append(final_properties)

    final_action_criteria = ET.SubElement(final_root, "ActionCriteria")
    final_frontend_actions = ET.SubElement(final_root, "FrontEndActions")
    final_ingame_actions = ET.SubElement(final_root, "InGameActions")
    final_files = ET.SubElement(final_root, "Files")

    used_files: set[str] = set()
    used_criteria_ids: set[str] = set()

    mod_folders = sorted(path for path in TEXTS_DIR.iterdir() if path.is_dir())

    if not mod_folders:
        raise RuntimeError(f"親MODフォルダが見つかりません: {TEXTS_DIR}")

    processed_count = 0

    for mod_folder in mod_folders:
        fragment_path = mod_folder / "modinfo.xml"

        automatic_files = None
        if not fragment_path.is_file():
            automatic_files = collect_automatic_files(mod_folder)
            if not automatic_files:
                continue

        folder_name = mod_folder.name

        if not SAFE_NAME.fullmatch(folder_name):
            raise RuntimeError(
                "親MODフォルダ名に使用できない文字があります:\n"
                f"  {folder_name}\n"
                "使用可能: 英数字と _ ／ 先頭は数字不可"
            )

        if not fragment_path.is_file():
            add_automatic_actions(
                folder_name,
                automatic_files,
                final_frontend_actions,
                final_ingame_actions,
                used_files,
            )
            processed_count += 1
            continue

        processed_count += 1
        fragment_tree = parse_xml(fragment_path)
        fragment_root = fragment_tree.getroot()

        if fragment_root.tag != "Mod":
            raise RuntimeError(f"{fragment_path} のルート要素は <Mod> にしてください。")

        parent_mod_id = fragment_root.get("id")
        if not parent_mod_id:
            raise RuntimeError(f"親MODの id がありません: {fragment_path}")

        criteria_mapping = namespace_fragment_criteria(
            fragment_root,
            folder_name,
            final_action_criteria,
            used_criteria_ids,
            fragment_path,
        )

        frontend_source = fragment_root.find("FrontEndActions")
        ingame_source = fragment_root.find("InGameActions")

        frontend_actions = list(frontend_source) if frontend_source is not None else []
        ingame_actions = list(ingame_source) if ingame_source is not None else []

        if frontend_actions:
            frontend_criterion_id = f"{folder_name}_FrontEndCriteria"

            make_parent_criterion(
                frontend_criterion_id,
                "ModIsEnabled",
                parent_mod_id,
                final_action_criteria,
                used_criteria_ids,
                fragment_path,
            )

            copy_actions(
                frontend_source,
                final_frontend_actions,
                frontend_criterion_id,
                criteria_mapping,
                mod_folder,
                used_files,
            )

        if ingame_actions:
            ingame_criterion_id = f"{folder_name}_InGameCriteria"

            make_parent_criterion(
                ingame_criterion_id,
                "ModInUse",
                parent_mod_id,
                final_action_criteria,
                used_criteria_ids,
                fragment_path,
            )

            copy_actions(
                ingame_source,
                final_ingame_actions,
                ingame_criterion_id,
                criteria_mapping,
                mod_folder,
                used_files,
            )

    for path in sorted(used_files):
        ET.SubElement(final_files, "File").text = path

    tree = ET.ElementTree(final_root)
    ET.indent(tree, space="\t")

    tree.write(
        OUTPUT_FILE,
        encoding="utf-8",
        xml_declaration=True,
        short_empty_elements=False,
    )

    print(f"生成完了: {OUTPUT_FILE}")
    print(f"親MOD数: {processed_count}")
    print(f"Authors: {MOD_AUTHOR}")
    print(f"Files: {len(used_files)}")


if __name__ == "__main__":
    main()
