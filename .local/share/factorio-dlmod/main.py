#!/usr/bin/env python3
"""
Factorio Mod Downloader - Headless CLI Edition
Version-Locked (Target or Older) Mod Support
"""

import os
import sys
from typing import Final, Set, Optional, List
import requests

API_MOD_URL: Final = "https://mods.factorio.com/api/mods"
BASE_DOWNLOAD_URL: Final = "https://mods-storage.re146.dev"


def parse_ver(ver_str: str) -> List[int]:
    """Convert version string like "1.1.100" to integer list for comparison"""
    try:
        return [int(part) for part in ver_str.split(".")]
    except (ValueError, AttributeError):
        return []


def ver_less_or_equal(v1: List[int], v2: List[int]) -> bool:
    """Check if v1 <= v2 (semantic version compare)"""
    for a, b in zip(v1, v2):
        if a < b:
            return True
        if a > b:
            return False
    # One is prefix of the other (e.g. 1.1 vs 1.1.2)
    return len(v1) <= len(v2)


class ModDownloader:
    def __init__(self, target_input: str, output_path: str, factorio_version: Optional[str] = None):
        self.mod_name = target_input.rstrip("/").split("/")[-1]
        self.output_path = os.path.abspath(os.path.expanduser(output_path))
        self.raw_factorio_ver = factorio_version
        self.target_ver_list = parse_ver(factorio_version) if factorio_version else None
        self.downloaded_mods: Set[str] = set()
        self.analyzed_mods: Set[str] = set()

    def log(self, text: str):
        print(text, flush=True)

    def run(self):
        self.log(f"[*] Starting deployment sequence for: {self.mod_name}")
        if self.raw_factorio_ver:
            self.log(f"[*] Locked to Factorio v{self.raw_factorio_ver} or older")
        self.log(f"[*] Target Directory: {self.output_path}\n")
        self.fetch_and_download(self.mod_name)
        self.log("[+] All processing blocks complete.")

    def find_compatible_release(self, releases: List[dict]) -> dict:
        if not self.target_ver_list:
            print("************ debug: find_compatible_release: early return")
            return None

        for rel in reversed(releases):
            mod_fac_ver = rel.get("info_json").get("factorio_version")
            if not mod_fac_ver:
                print("************ debug: find_compatible_release: not mod_fac_ver")
                continue
            rel_ver = parse_ver(mod_fac_ver)
            if not rel_ver:
                print("************ debug: find_compatible_release: not rel_ver")
                continue
            if ver_less_or_equal(rel_ver, self.target_ver_list):
                return rel
        return None

    def fetch_and_download(self, mod_id: str):
        builtin = ("base", "space-age", "elevator", "quality", "vulcanus", "gleba", "fulgora")
        if mod_id in builtin:
            return

        if mod_id in self.analyzed_mods:
            self.log(f"[=] Dependency '{mod_id}' already resolved. Skipping.")
            return

        self.analyzed_mods.add(mod_id)
        self.log(f"[*] Querying API for mod: {mod_id}")

        try:
            res = requests.get(f"{API_MOD_URL}/{mod_id}/full", timeout=10)
            # Print status immediately after request
            if res.status_code == 404:
                self.log(f"    -> Status: Not Found (404)")
                self.log(f"[-] Mod '{mod_id}' not found. Skipping.")
                return
            res.raise_for_status()
            data = res.json()

            all_releases = data.get("releases", [])
            compatible_release = self.find_compatible_release(all_releases)

            # Print version info right after successful query
            if not compatible_release:
                self.log(f"    -> No compatible releases found")
                self.log(f"[-] No releases compatible with Factorio v{self.raw_factorio_ver} for {mod_id}")
                return

            mod_ver = compatible_release.get("version")
            fac_compat_ver = compatible_release.get("info_json").get("factorio_version")
            self.log(f"    -> Found: Mod v{mod_ver} | Factorio Compatibility: v{fac_compat_ver}")

        except Exception as e:
            self.log(f"    -> API request error: {str(e)}")
            self.log(f"[!] API request failed for {mod_id}: {e}")
            return

        file_name = f"{mod_id}_{mod_ver}.zip"
        target_file_path = os.path.join(self.output_path, file_name)

        if file_name not in self.downloaded_mods and not os.path.exists(target_file_path):
            dl_url = f"{BASE_DOWNLOAD_URL}/{mod_id}/{mod_ver}.zip"
            self.log(f"    -> Downloading...")

            os.makedirs(self.output_path, exist_ok=True)
            if self.download_asset(dl_url, target_file_path):
                self.log(f"    [+] Saved: {file_name}")
                self.downloaded_mods.add(file_name)
        else:
            self.log(f"    -> {file_name} already exists locally. Skipping.")
            self.downloaded_mods.add(file_name)

        info_json = compatible_release.get("info_json") or {}
        dependencies = compatible_release.get("dependencies") or info_json.get("dependencies") or []

        for dep_string in dependencies:
            clean_dep = dep_string.strip()
            if clean_dep.startswith(("!", "~", "?")) or "(" in clean_dep:
                continue

            parts = clean_dep.split()
            if not parts:
                continue
            dep_id = parts[0].strip()
            self.log(f"  -> Dependency found: {mod_id} requires {dep_id}")
            self.fetch_and_download(dep_id)

    def download_asset(self, url: str, path: str) -> bool:
        try:
            res = requests.get(url, stream=True, timeout=30)
            res.raise_for_status()
            with open(path, "wb") as f:
                for chunk in res.iter_content(chunk_size=256 * 1024):
                    if chunk:
                        f.write(chunk)
            return True
        except Exception as e:
            self.log(f"    [!] Download failed: {e}")
        if os.path.exists(path):
            os.remove(path)
        return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: factorio-dlmod <mod_name_or_url> <output_path> [factorio_version]")
        print("Example: factorio-dlmod bobmods-lib ./mods 1.1.100")
        sys.exit(1)

    target_mod = sys.argv[1]
    out_dir = sys.argv[2]
    ver_lock = sys.argv[3] if len(sys.argv) > 3 else None

    downloader = ModDownloader(target_mod, out_dir, ver_lock)
    downloader.run()
