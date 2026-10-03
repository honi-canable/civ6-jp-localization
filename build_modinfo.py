from __future__ import annotations

from copy import deepcopy
from pathlib import Path, PurePosixPath
import re
import xml.etree.ElementTree as ET

# ── 全体設定 ──────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent
TEXTS_DIR = ROOT / "Texts"
PROPERTIES_FILE = ROOT / "Properties.xml"
OUTPUT_FILE = ROOT / "Civ6_JP_Localization.modinfo"

# この日本語化MOD自身のID。以後は変えない。
MOD_ID = "d8920739-5ce8-439a-a41c-3d405bdf291e"
MOD_VERSION = "1"

# 親MODフォルダ名に使える文字。
SAFE_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


# ── 補助関数 ──────────────────────────────────────────────


def parse_xml(path: Path) -> ET.ElementTree:
    try:
        return ET.parse(path)
    except ET.ParseError as exc:
        raise RuntimeError(f"XMLの解析に失敗しました: {path}\n{exc}") from exc


def add_unique_id(used_ids: set[str], value: str, source: Path) -> None:
    if value in used_ids:
        raise RuntimeError(f"Criteria ID が重複しました: {value}\n" f"発生元: {source}")
    used_ids.add(value)


def rewrite_file_path(
    file_element: ET.Element,
    mod_folder: Path,
    used_files: set[str],
) -> None:
    """Action直下の<File>を完成modinfo基準の相対パスに変換する。"""
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
            f"<File> で指定されたファイルが見つかりません:\n" f"  {actual_file}"
        )

    output_path = actual_file.relative_to(ROOT).as_posix()
    file_element.text = output_path
    used_files.add(output_path)


def collect_authors(fragment_root: ET.Element, authors: list[str]) -> None:
    """各fragmentの<Properties><Authors>を初出順で集約する。"""
    properties = fragment_root.find("Properties")
    if properties is None:
        return

    for element in properties.findall("Authors"):
        if not element.text:
            continue

        author = element.text.strip()
        if author and author not in authors:
            authors.append(author)


def namespace_fragment_criteria(
    fragment_root: ET.Element,
    folder_name: str,
    final_action_criteria: ET.Element,
    used_criteria_ids: set[str],
    source: Path,
) -> dict[str, str]:
    """
    fragment内の既存Criteriaを
      OldCriteria -> <FolderName>_OldCriteria
    の形でユニーク化して、完成modinfoへコピーする。
    """
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
    """親MODが有効なときだけActionを実行するCriteriaを作る。"""
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
    """
    FrontEndActions / InGameActions の直下要素を
    Action種別に関係なくそのままコピーする。
    """
    if source_section is None:
        return 0

    count = 0

    for original_action in source_section:
        action = deepcopy(original_action)

        # fragment内で定義された既存Criteriaの参照名を書き換える。
        # 未定義のCriteria参照は外部・共通Criteriaの可能性があるためそのまま残す。
        for criterion_ref in action.findall("Criteria"):
            if not criterion_ref.text:
                continue

            old_ref = criterion_ref.text.strip()
            if old_ref in criteria_mapping:
                criterion_ref.text = criteria_mapping[old_ref]

        # 親MOD判定Criteriaを追加。
        parent_ref = ET.Element("Criteria")
        parent_ref.text = parent_criterion_id

        # 見やすいよう、Actionの先頭に置く。
        action.insert(0, parent_ref)

        # Action直下の<File>だけを対象にする。
        for file_element in action.findall("File"):
            rewrite_file_path(file_element, mod_folder, used_files)

        target_section.append(action)
        count += 1

    return count


# ── メイン処理 ────────────────────────────────────────────


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

    # 完成modinfoの骨格。
    final_root = ET.Element(
        "Mod",
        {
            "id": MOD_ID,
            "version": MOD_VERSION,
        },
    )

    final_properties = deepcopy(properties_root)
    final_root.append(final_properties)

    final_action_criteria = ET.SubElement(final_root, "ActionCriteria")
    final_frontend_actions = ET.SubElement(final_root, "FrontEndActions")
    final_ingame_actions = ET.SubElement(final_root, "InGameActions")
    final_files = ET.SubElement(final_root, "Files")

    authors: list[str] = []
    used_files: set[str] = set()
    used_criteria_ids: set[str] = set()

    fragment_paths = sorted(TEXTS_DIR.glob("*/modinfo.xml"))

    if not fragment_paths:
        raise RuntimeError(f"親MOD用 modinfo.xml が見つかりません: {TEXTS_DIR}")

    for fragment_path in fragment_paths:
        mod_folder = fragment_path.parent
        folder_name = mod_folder.name

        if not SAFE_NAME.fullmatch(folder_name):
            raise RuntimeError(
                "親MODフォルダ名に使用できない文字があります:\n"
                f"  {folder_name}\n"
                "使用可能: 英数字と _ ／ 先頭は数字不可"
            )

        fragment_tree = parse_xml(fragment_path)
        fragment_root = fragment_tree.getroot()

        if fragment_root.tag != "Mod":
            raise RuntimeError(f"{fragment_path} のルート要素は <Mod> にしてください。")

        parent_mod_id = fragment_root.get("id")
        if not parent_mod_id:
            raise RuntimeError(f"親MODの id がありません: {fragment_path}")

        collect_authors(fragment_root, authors)

        # fragment内に元から存在するCriteriaをユニーク化。
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

        # FrontEndActionsが存在するときだけ親Criteriaを生成。
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

        # InGameActionsが存在するときだけ親Criteriaを生成。
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

    # AuthorsをProperties.xml由来のPropertiesへ追加。
    # Properties.xml側にAuthorsが書かれていた場合も重複しないようにする。
    existing_author_elements = final_properties.findall("Authors")
    existing_authors = [
        e.text.strip() for e in existing_author_elements if e.text and e.text.strip()
    ]

    for element in existing_author_elements:
        final_properties.remove(element)

    merged_authors: list[str] = []
    for author in existing_authors + authors:
        if author not in merged_authors:
            merged_authors.append(author)

    if merged_authors:
        authors_element = ET.Element("Authors")
        authors_element.text = ", ".join(merged_authors)
        final_properties.append(authors_element)

    # 各Actionで実際に使用されているファイルだけを列挙。
    for path in sorted(used_files):
        element = ET.SubElement(final_files, "File")
        element.text = path

    tree = ET.ElementTree(final_root)
    ET.indent(tree, space="\t")

    tree.write(
        OUTPUT_FILE,
        encoding="utf-8",
        xml_declaration=True,
        short_empty_elements=False,
    )

    print(f"生成完了: {OUTPUT_FILE}")
    print(f"親MOD数: {len(fragment_paths)}")
    print(f"Authors: {len(merged_authors)}")
    print(f"Files: {len(used_files)}")


if __name__ == "__main__":
    main()
