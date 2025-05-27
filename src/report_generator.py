import json
import os
from jinja2 import Template

reports_dir = 'reports'
if not os.path.exists(reports_dir):
    os.makedirs(reports_dir)

# CVE Metadata for risk and recommendation
RISK_DB = {
    "CVE-2019-5736": {"risk_level": "High", "recommendation": "Rebuild container with read-only FS."},
    "CVE-2020-15257": {"risk_level": "High", "recommendation": "Avoid privileged containers."},
    "DOCKER-SOCKET-ABUSE": {"risk_level": "Critical", "recommendation": "Never mount docker.sock into containers."},
    "OVERLAYFS-EXPLOIT": {"risk_level": "High", "recommendation": "Upgrade kernel; avoid writable overlay mounts."},
    "CAP-SYS-PTRACE-ABUSE": {"risk_level": "High", "recommendation": "Drop CAP_SYS_PTRACE or use seccomp."},
    "WRITABLE-CGROUP-ESCAPE": {"risk_level": "Medium", "recommendation": "Harden cgroup mounts."},
    "DIRTY-PIPE-ESCALATION": {"risk_level": "Critical", "recommendation": "Upgrade to kernel > 5.10.102."},
    "CVE-2021-3156": {"risk_level": "High", "recommendation": "Update sudo to patched version."}
}

def format_entry(cve, result, simulate):
    meta = RISK_DB.get(cve.upper(), {})
    return {
        "cve_id": cve,
        "result": result,
        "mode": "simulate" if simulate else "real",
        "risk_level": meta.get("risk_level", "Unknown"),
        "recommendation": meta.get("recommendation", "No recommendation.")
    }

def generate_json_report(results_dict, simulate=False):
    enriched = {cve: format_entry(cve, result, simulate) for cve, result in results_dict.items()}
    with open(f'{reports_dir}/attack_report.json', 'w') as f:
        json.dump(enriched, f, indent=4)

def generate_html_report(results_dict, simulate=False):
    enriched = {cve: format_entry(cve, result, simulate) for cve, result in results_dict.items()}
    template = """
    <html>
    <head><title>Dockout Report</title>
    <style>
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
    .simulate { background-color: #eef; }
    .real { background-color: #fee; }
    </style>
    </head>
    <body>
        <h1>Dockout Exploit Report</h1>
        <table>
            <tr>
                <th>CVE</th><th>Result</th><th>Mode</th><th>Risk Level</th><th>Recommendation</th>
            </tr>
            {% for cve, data in results.items() %}
            <tr class="{{ data.mode }}">
                <td>{{ cve }}</td>
                <td>{{ data.result }}</td>
                <td>{{ data.mode }}</td>
                <td>{{ data.risk_level }}</td>
                <td>{{ data.recommendation }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    html = Template(template).render(results=enriched)
    with open(f'{reports_dir}/attack_report.html', 'w') as f:
        f.write(html)
