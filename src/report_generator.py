import json
import os
from jinja2 import Template

reports_dir = 'reports'
if not os.path.exists(reports_dir):
    os.makedirs(reports_dir)

def generate_html_report(results):
    template = """
    <html>
    <head><title>Dockout Report</title></head>
    <body>
        <h1>Automated CVE Test Results</h1>
        <ul>
        {% for cve, result in results.items() %}
            <li><b>{{ cve }}</b>: {{ result }}</li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """
    html = Template(template).render(results=results)
    with open(f'{reports_dir}/attack_report.html', 'w') as f:
        f.write(html)

def generate_json_report(results):
    with open(f'{reports_dir}/attack_report.json', 'w') as f:
        json.dump(results, f, indent=4)
