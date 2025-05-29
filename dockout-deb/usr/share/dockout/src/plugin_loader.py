# src/plugin_loader.py

import importlib
import sys
import os

def load_attack_module(name):
    """
    Dynamically import the attack module by name.
    Examples:
      - "CVE-2019-5736" => attacks.cve_2019_5736
      - "writable-cgroup-escape" => attacks.writable_cgroup_escape
    """
    module_name = name.lower().replace('-', '_')  # normalize
    module_path = f"attacks.{module_name}"

    # Add root to sys.path
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)

    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError:
        print(f"[-] No module found for {name} ({module_path}.py)")
        return None
