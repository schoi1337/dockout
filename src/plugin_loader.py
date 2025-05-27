# src/plugin_loader.py

import importlib
import sys
import os

def load_attack_module(cve_id):
    """
    Dynamically import the attack module for the given CVE ID.
    Example: "CVE-2019-5736" -> attacks/cve_2019_5736.py
    """
    module_name = cve_id.lower().replace('-', '_')  # cve_2019_5736
    module_path = f"attacks.{module_name}"

    # Add root path of project to sys.path to allow 'attacks' import
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)

    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as e:
        print(f"[-] No module found for {cve_id} ({module_path}.py)")
        return None
