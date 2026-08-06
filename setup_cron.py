"""
Installe automatiquement le job cron pour lancer le bot de veille.

Usage :
    python3 setup_cron.py                 # toutes les 30 minutes (défaut)
    python3 setup_cron.py --interval 15    # toutes les 15 minutes

Ce script est idempotent : le relancer ne crée pas de doublon dans la crontab.
"""

import argparse
import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_PY = os.path.join(SCRIPT_DIR, "main.py")
LOG_FILE = os.path.join(SCRIPT_DIR, "cron.log")

# Marqueur unique pour identifier notre ligne dans la crontab
CRON_TAG = "# bot-veille-pap"


def find_python_executable() -> str:
    """Retourne le python du venv du projet s'il existe, sinon le python courant."""
    venv_python = os.path.join(SCRIPT_DIR, "venv", "bin", "python3")
    if os.path.exists(venv_python):
        return venv_python
    return sys.executable


def get_current_crontab() -> str:
    """Récupère la crontab actuelle de l'utilisateur (chaîne vide si aucune)."""
    result = subprocess.run(
        ["crontab", "-l"], capture_output=True, text=True
    )
    # crontab -l renvoie un code d'erreur si aucune crontab n'existe encore : pas un problème
    if result.returncode != 0:
        return ""
    return result.stdout


def build_cron_line(interval_minutes: int) -> str:
    python_exe = find_python_executable()
    return (
        f"*/{interval_minutes} * * * * "
        f"{python_exe} {MAIN_PY} >> {LOG_FILE} 2>&1 {CRON_TAG}\n"
    )


def install_cron_job(interval_minutes: int) -> None:
    current = get_current_crontab()

    # Retire une éventuelle ancienne ligne du bot pour éviter les doublons
    lines = [
        line for line in current.splitlines(keepends=True)
        if CRON_TAG not in line
    ]

    new_line = build_cron_line(interval_minutes)
    lines.append(new_line)
    new_crontab = "".join(lines)

    process = subprocess.run(
        ["crontab", "-"], input=new_crontab, text=True
    )
    if process.returncode != 0:
        print("Erreur lors de l'installation de la crontab.")
        sys.exit(1)

    print("Cron job installé avec succès :")
    print(new_line.strip())
    print(f"\nLogs disponibles dans : {LOG_FILE}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Installe le cron du bot de veille PAP.")
    parser.add_argument(
        "--interval", type=int, default=30,
        help="Fréquence d'exécution en minutes (défaut : 30)"
    )
    args = parser.parse_args()
    install_cron_job(args.interval) 