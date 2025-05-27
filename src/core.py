import argparse
import docker
from report_generator import generate_html_report, generate_json_report
from plugin_loader import load_attack_module

client = docker.from_env()

def list_containers():
    containers = client.containers.list(all=True)
    for container in containers:
        print(f"Container {container.id} - {container.name} - Status: {container.status}")

def generate_reports(attack_result, report_type):
    if report_type == 'html':
        generate_html_report(attack_result)
    elif report_type == 'json':
        generate_json_report(attack_result)

def parse_args():
    parser = argparse.ArgumentParser(description='CVE Detection and Docker Breakout Tool')

    parser.add_argument('--attack', type=str, help='Specify CVE ID to run, e.g. CVE-2019-5736')
    parser.add_argument('--container', type=str, help='Specify the container name or ID')
    parser.add_argument('--report', choices=['html', 'json'], help='Generate report in specified format')

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    if args.attack:
        if args.container:
            try:
                container = client.containers.get(args.container)
            except docker.errors.NotFound:
                print(f"[-] Container '{args.container}' not found.")
                exit(1)

            print(f"[+] Running attack {args.attack} on container {args.container}")
            module = load_attack_module(args.attack)

            if module and hasattr(module, 'run'):
                attack_result = module.run(container)
                if args.report:
                    generate_reports(attack_result, args.report)
            else:
                print("[-] Attack module is invalid or missing 'run' function.")
        else:
            print("[-] Please specify --container")
    else:
        print("[-] No attack specified. Use --attack <CVE-ID>")
