#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Korrigiert den Hintergrundbild-Pfad in allen HTML-Dateien
von "/images/DesignTitel.jpeg" zu "DesignTitel.jpeg".
"""

import re
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import sys
from datetime import datetime


def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Bitte wähle den Hauptordner aus")
    root.destroy()
    return Path(folder) if folder else None


def fix_path_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ersetze "/images/DesignTitel.jpeg" durch "DesignTitel.jpeg"
    new_content = content.replace('/images/DesignTitel.jpeg', 'DesignTitel.jpeg')
    
    if new_content == content:
        return False
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True


def main():
    print("=" * 80)
    print("🔧 KORRIGIERE HINTERGRUNDBILD-PFAD")
    print("=" * 80)
    
    base_path = select_folder()
    if base_path is None:
        print("Kein Ordner ausgewählt.")
        sys.exit(0)
    
    print(f"\nBasisordner: {base_path}\n")
    
    changed = 0
    total = 0
    
    for lang_dir in ["de", "en", "ds", "usa"]:
        dir_path = base_path / lang_dir
        if not dir_path.exists():
            continue
        for html_file in dir_path.glob("*.html"):
            total += 1
            if fix_path_in_file(html_file):
                changed += 1
                print(f"  ✅ Geändert: {lang_dir}/{html_file.name}")
    
    print(f"\n📊 Geändert: {changed} von {total} Dateien")
    print("\n✅ Fertig! Jetzt sollte das Bild angezeigt werden.")
    input("\nENTER zum Beenden...")


if __name__ == "__main__":
    main()