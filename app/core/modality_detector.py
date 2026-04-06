# app/core/modality_detector.py
import re
from pathlib import Path

# خريطة الـ patterns لكل modality - مرتبة من الأكثر تحديداً للأقل
MODALITY_PATTERNS: dict[str, list] = {
    "t1ce": [
        r"t1ce", r"t1_ce", r"t1\+c", r"t1c(?!e)",
        r"ce_t1", r"contrast", r"gad", r"post"
    ],
    "t1": [
        r"(?<![a-z])t1(?!ce|c\b|_ce)",
        r"mprage", r"spgr"
    ],
    "t2": [
        r"(?<![a-z])t2(?!flair|_flair)",
        r"t2w"
    ],
    "flair": [
        r"flair", r"t2_flair", r"t2flair", r"fluid"
    ],
}


def detect_modality(filename: str) -> str | None:
    """
    يتعرف على modality الملف من اسمه.
    يرجع: 't1' | 't1ce' | 't2' | 'flair' | None
    """
    name = Path(filename).name.lower()
    for ext in [".nii.gz", ".nii"]:
        if name.endswith(ext):
            name = name[: -len(ext)]

    # t1ce لازم يتحقق قبل t1
    for modality in ["t1ce", "flair", "t2", "t1"]:
        for pattern in MODALITY_PATTERNS[modality]:
            if re.search(pattern, name, re.IGNORECASE):
                return modality

    return None


def detect_modalities_from_folder(folder_path: str) -> dict[str, str]:
    """
    يمسح الـ folder ويرجع dict:
    { 't1': '/path/file_t1.nii', 't1ce': '...', 't2': '...', 'flair': '...' }
    """
    folder = Path(folder_path)
    nii_files = list(folder.glob("*.nii")) + list(folder.glob("*.nii.gz"))

    if not nii_files:
        raise ValueError(f"لا توجد ملفات .nii أو .nii.gz في: {folder_path}")

    detected: dict[str, str] = {}
    conflicts: dict[str, list] = {}

    for f in nii_files:
        modality = detect_modality(f.name)
        if modality:
            if modality not in detected:
                detected[modality] = str(f)
            else:
                conflicts.setdefault(modality, [detected[modality]]).append(str(f))

    if conflicts:
        raise ValueError(
            f"تعارض في الـ modalities: {conflicts}\n"
            "يوجد أكثر من ملف لنفس الـ modality. يرجى التحقق من الـ folder."
        )

    return detected


def validate_modalities(modalities: dict[str, str]) -> None:
    """يتحقق أن الـ 4 modalities الأساسية موجودة"""
    required = {"t1", "t1ce", "t2", "flair"}
    missing = required - set(modalities.keys())
    if missing:
        raise ValueError(
            f"الـ modalities الناقصة: {missing}\n"
            f"الملفات المكتشفة فقط: {list(modalities.keys())}"
        )