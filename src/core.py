import argparse
import docker
from report_generator import generate_html_report, generate_json_report
from plugin_loader import load_attack_module
import os

client = docker.from_env()

def list_containers():
    containers = client.containers.list(all=True)
    for container in containers:
        print(f"Container {container.id} - {container.name} - Status: {container.status}")

def generate_reports(results_dict, report_type):
    if report_type == 'html':
        generate_html_report(results_dict)
    elif report_type == 'json':
        generate_json_report(results_dict)

def parse_args():
    parser = argparse.ArgumentParser(description='CVE Detection and Docker Breakout Tool')
    parser.add_argument('--attack', type=str, help='Specify CVE ID to run, e.g. CVE-2019-5736')
    parser.add_argument('--auto', action='store_true', help='Automatically run all known CVE modules')
    parser.add_argument('--container', type=str, help='Specify the container name or ID')
    parser.add_argument('--report', choices=['html', 'json'], help='Generate report in specified format')
    return parser.parse_args()

def run_all_attacks(container):
    results = {}
    attack_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'attacks'))
    for fname in os.listdir(attack_dir):
        if fname.startswith('cve_') and fname.endswith('.py'):
            cve_id = fname.replace('.py', '').upper().replace('_', '-')
            module = load_attack_module(cve_id)
            if module and hasattr(module, 'run'):
                print(f"[+] Running {cve_id}...")
                result = module.run(container)
                results[cve_id] = result
            else:
                results[cve_id] = "Module invalid or missing run()"
    return results

if __name__ == "__main__":
    args = parse_args()

    if args.container:
        try:
            container = client.containers.get(args.container)
        except docker.errors.NotFound:
            print(f"[-] Container '{args.container}' not found.")
            exit(1)
    else:
        print("[-] Please specify --container")
        exit(1)

    if args.auto:
        results = run_all_attacks(container)
        if args.report:
            generate_reports(results, args.report)
    elif args.attack:
        module = load_attack_module(args.attack)
        if module and hasattr(module, 'run'):
            result = module.run(container)
            if args.report:
                generate_reports({args.attack: result}, args.report)
        else:
            print("[-] Attack module is invalid or missing 'run' function.")
    else:
        print("[-] No action specified. Use --attack <CVE-ID> or --auto")
