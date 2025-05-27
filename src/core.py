# Path: src/core.py

import argparse
import asyncio
import os
import docker
from report_generator import generate_html_report, generate_json_report
from plugin_loader import load_attack_module
from env_check import get_docker_info

client = docker.from_env()
MAX_PARALLEL_TASKS = 5  # Maximum number of concurrent CVE executions

def list_containers():
    containers = client.containers.list(all=True)
    for container in containers:
        print(f"Container {container.id} - {container.name} - Status: {container.status}")

def generate_reports(results_dict, report_type):
    # Generate report in the specified format
    if report_type == 'html':
        generate_html_report(results_dict)
    elif report_type == 'json':
        generate_json_report(results_dict)

def parse_args():
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description='CVE Detection and Docker Breakout Tool')
    parser.add_argument('--attack', type=str, help='Specify CVE ID to run, e.g. CVE-2019-5736')
    parser.add_argument('--auto', action='store_true', help='Automatically run all known CVE modules')
    parser.add_argument('--container', type=str, help='Specify the container name or ID')
    parser.add_argument('--report', choices=['html', 'json'], help='Generate report in specified format')
    parser.add_argument('--simulate', action='store_true', help='Simulate the exploit without executing real changes')
    return parser.parse_args()

async def async_run_module_with_env(module, container, cve_id, env_info, semaphore, simulate):
    # Run a single attack module with environment-aware vulnerability check
    async with semaphore:
        loop = asyncio.get_event_loop()

        def _exec():
            if hasattr(module, "is_vulnerable"):
                if not module.is_vulnerable(env_info):
                    print(f"[!] {cve_id} skipped: not vulnerable under current environment.")
                    return (cve_id, "Skipped (not vulnerable)")
            return (cve_id, module.run(container, simulate=simulate))  # Pass simulate flag

        return await loop.run_in_executor(None, _exec)

async def run_all_attacks_async(container, simulate):
    # Run all CVE modules concurrently (with environment check)
    results = {}
    env_info = get_docker_info()
    attack_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'attacks'))
    semaphore = asyncio.Semaphore(MAX_PARALLEL_TASKS)
    tasks = []

    for fname in os.listdir(attack_dir):
        if fname.startswith('cve_') and fname.endswith('.py'):
            cve_id = fname.replace('.py', '').upper().replace('_', '-')
            module = load_attack_module(cve_id)
            if module and hasattr(module, 'run'):
                tasks.append(async_run_module_with_env(module, container, cve_id, env_info, semaphore, simulate))
            else:
                results[cve_id] = "Module invalid or missing run()"

    for coro in asyncio.as_completed(tasks):
        cve_id, result = await coro
        results[cve_id] = result

    return results

if __name__ == "__main__":
    args = parse_args()

    if not args.simulate:
        print("\n[!] WARNING: You are about to execute real exploits on the container.")
        print("This may modify system files, overwrite binaries, or cause instability.")
        confirm = input("Are you sure you want to continue? Type 'yes' to proceed: ")
        if confirm.strip().lower() != "yes":
            print("[-] Confirmation failed. Aborting execution.")
            exit(1)

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
        results = asyncio.run(run_all_attacks_async(container, simulate=args.simulate))
        if args.report:
            generate_reports(results, args.report)

    elif args.attack:
        module = load_attack_module(args.attack)
        if module and hasattr(module, 'run'):
            result = module.run(container, simulate=args.simulate)
            if args.report:
                generate_reports({args.attack: result}, args.report)
        else:
            print("[-] Attack module is invalid or missing 'run' function.")
    else:
        print("[-] No action specified. Use --attack <CVE-ID> or --auto")
