import json
import os
from jinja2 import Template

# Ensure the 'reports' directory exists
reports_dir = 'reports'

# Check if the directory exists or not and create it
if not os.path.exists(reports_dir):
    print(f"Directory '{reports_dir}' does not exist. Creating it now.")
    os.makedirs(reports_dir)  # This will create the directory if it doesn't exist
else:
    print(f"Directory '{reports_dir}' already exists.")

def generate_html_report(attack_result):
    # Generate HTML report for the attack result
    template = """
    <html>
    <head><title>Attack Report</title></head>
    <body>
        <h1>Attack Result</h1>
        <p>{{ attack_result }}</p>
    </body>
    </html>
    """
    t = Template(template)
    html_content = t.render(attack_result=attack_result)
    
    # Save the report inside the 'reports' directory
    with open(f'{reports_dir}/attack_report.html', 'w') as f:
        f.write(html_content)

def generate_json_report(attack_result):
    # Generate JSON report for the attack result
    with open(f'{reports_dir}/attack_report.json', 'w') as f:
        json.dump(attack_result, f, indent=4)
