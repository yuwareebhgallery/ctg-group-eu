#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skript zum Einfügen eines absoluten Hintergrundbild-Pfads in alle HTML-Dateien
in den Ordnern de/, en/, ds/, usa/ (und allen Unterordnern).

Das Skript:
1. Öffnet einen Explorer-Dialog zur Auswahl des Hauptordners.
2. Durchsucht alle Unterordner nach HTML-Dateien.
3. Fügt in den .column-5-Container ein style-Attribut mit background-image ein.
4. Entfernt dabei keine bestehenden Styles, sondern ergänzt sie.
"""

import re
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import sys
from datetime import datetime


# ============================================================
# KONFIGURATION
# ============================================================

# Absolute Pfad zum Bild (ab Domain-Root)
IMAGE_PATH = "/images/DesignTitel.jpeg"

# Diese Unterordner werden durchsucht (kann erweitert werden)
TARGET_SUBDIRS = ["de", "en", "ds", "usa"]

# Dateiendungen, die bearbeitet werden sollen
HTML_EXTENSIONS = {".html", ".htm"}


# ============================================================
# HILFSFUNKTIONEN
# ============================================================

def select_folder() -> Path | None:
    """Öffnet einen Explorer-Dialog zur Auswahl eines Ordners."""
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Bitte wähle den Hauptordner aus")
    root.destroy()
    return Path(folder) if folder else None


def add_background_image_to_element(html_content: str, image_path: str) -> tuple[str, bool]:
    """
    Fügt einem HTML-Element mit der Klasse .column-5 ein style-Attribut
    mit background-image hinzu.

    Rückgabe: (neuer_HTML_Inhalt, wurde_geändert)
    """
    # Suchmuster für <div class="...column-5..."> oder <div class="...col-xs-...column-5...">
    # oder jedes Element mit einer Klasse, die "column-5" enthält
    pattern = re.compile(
        r'(<[^>]*\bclass\s*=\s*["\'][^"\']*column-5[^"\']*["\'][^>]*?)>',
        re.IGNORECASE | re.DOTALL
    )

    def replace_tag(match):
        tag_open = match.group(1)
        # Prüfen, ob bereits ein style-Attribut existiert
        if 'style=' in tag_open:
            # style existiert – background-image ergänzen
            # Suche nach style="..." und füge background-image ein
            style_pattern = re.compile(r'(style\s*=\s*["\'])([^"\']*)(["\'])', re.IGNORECASE)
            def style_replacer(m):
                prefix = m.group(1)
                style_content = m.group(2)
                suffix = m.group(3)
                # Prüfen, ob bereits background-image vorhanden ist
                if 'background-image' in style_content:
                    return m.group(0)  # nichts ändern
                # background-image am Ende hinzufügen (mit Semikolon, falls nötig)
                if style_content and not style_content.endswith(';'):
                    style_content += ';'
                style_content += f' background-image: url("{image_path}"); background-size: cover; background-position: center center; background-repeat: no-repeat;'
                return f'{prefix}{style_content}{suffix}'
            return style_pattern.sub(style_replacer, tag_open) + '>'
        else:
            # Kein style-Attribut vorhanden – neues hinzufügen
            return f'{tag_open} style="background-image: url(\'{image_path}\'); background-size: cover; background-position: center center; background-repeat: no-repeat; min-height: 200px;">'

    new_content, count = pattern.subn(replace_tag, html_content)
    return new_content, count > 0


def process_html_file(file_path: Path, image_path: str, log_lines: list) -> bool:
    """
    Verarbeitet eine einzelne HTML-Datei.
    Rückgabe: True, wenn Datei geändert wurde.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        log_lines.append(f"[FEHLER] {file_path}: {e}")
        return False

    original_content = content
    new_content, changed = add_background_image_to_element(content, image_path)

    if not changed:
        return False

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        log_lines.append(f"[GEÄNDERT] {file_path}")
        return True
    except Exception as e:
        log_lines.append(f"[FEHLER] {file_path}: {e}")
        return False


# ============================================================
# HAUPTFUNKTION
# ============================================================

def main():
    print("=" * 80)
    print("🔧 FÜGE ABSOLUTEN HINTERGRUNDBILD-PFAD IN HTML EIN")
    print("=" * 80)

    # Ordner auswählen
    base_path = select_folder()
    if base_path is None:
        print("Kein Ordner ausgewählt. Programm wird beendet.")
        sys.exit(0)

    print(f"\nGewählter Ordner: {base_path}\n")

    # Log-Datei
    log_file = base_path / "background_image_fix_log.txt"
    log_lines = []
    log_lines.append("=" * 80)
    log_lines.append("HINTERGRUNDBILD-FIX LOG")
    log_lines.append("=" * 80)
    log_lines.append(f"Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append(f"Bild-Pfad: {IMAGE_PATH}")
    log_lines.append(f"Basisordner: {base_path}")
    log_lines.append("")
    log_lines.append("GEÄNDERTE DATEIEN:")

    changed_files = 0
    total_files = 0
    skipped_files = 0
    error_files = 0

    # Alle Unterordner durchsuchen
    for target_dir in TARGET_SUBDIRS:
        dir_path = base_path / target_dir
        if not dir_path.exists() or not dir_path.is_dir():
            print(f"⚠️  Ordner nicht gefunden: {target_dir}/ (wird übersprungen)")
            continue

        print(f"\n📁 Durchsuche: {target_dir}/")
        html_files = list(dir_path.rglob("*"))
        html_files = [f for f in html_files if f.is_file() and f.suffix.lower() in HTML_EXTENSIONS]

        for file_path in html_files:
            total_files += 1
            if process_html_file(file_path, IMAGE_PATH, log_lines):
                changed_files += 1
                print(f"  ✅ Geändert: {file_path.relative_to(base_path)}")
            else:
                skipped_files += 1
                print(f"  ⏭️ Unverändert: {file_path.relative_to(base_path)}")

    # Zusammenfassung
    print("\n" + "=" * 80)
    print("📊 ZUSAMMENFASSUNG")
    print("=" * 80)
    print(f"Dateien insgesamt:      {total_files}")
    print(f"Geändert:               {changed_files}")
    print(f"Unverändert:            {skipped_files}")
    print(f"Fehler:                 {error_files}")

    # Log schreiben
    log_lines.append("")
    log_lines.append("=" * 80)
    log_lines.append("ZUSAMMENFASSUNG")
    log_lines.append("=" * 80)
    log_lines.append(f"Dateien insgesamt:      {total_files}")
    log_lines.append(f"Geändert:               {changed_files}")
    log_lines.append(f"Unverändert:            {skipped_files}")
    log_lines.append(f"Fehler:                 {error_files}")
    log_lines.append("")
    log_lines.append(f"Ende: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(log_lines))
        print(f"\n📄 Log-Datei: {log_file}")
    except Exception as e:
        print(f"\n⚠️  Log-Datei konnte nicht geschrieben werden: {e}")

    print("\n✅ Fertig!")
    input("\nENTER zum Beenden...")


if __name__ == "__main__":
    main()