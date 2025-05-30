import argparse
import asyncio
import os
import docker
from report_generator import generate_html_report, generate_json_report
from plugin_loader import load_attack_module
from env_check import get_docker_info
from rich.console import Console
from rich.panel import Panel

client = docker.from_env()
MAX_PARALLEL_TASKS = 5
console = Console()

def log(tag, message):
    styles = {
        "INFO": "cyan",
        "SUCCESS": "green",
        "SIMULATE": "yellow",
        "EXPLOIT": "bold red",
        "WARNING": "magenta"
    }
    console.print(f"[{tag}] {message}", style=styles.get(tag, "white"))

def banner():
    ascii_art = r"""
_|_|_|      _|_|      _|_|_|  _|    _|    _|_|    _|    _|  _|_|_|_|_|
_|    _|  _|    _|  _|        _|  _|    _|    _|  _|    _|      _|
_|    _|  _|    _|  _|        _|_|      _|    _|  _|    _|      _|
_|    _|  _|    _|  _|        _|  _|    _|    _|  _|    _|      _|
_|_|_|      _|_|      _|_|_|  _|    _|    _|_|      _|_|        _|

@Author: @schoi1337
"""
    console.print(ascii_art, style="bold cyan")
    console.print(Panel.fit(
        "[bold yellow]⚠ For authorized testing only!\nUse [green]--simulate[/green] for safe mode.\nUse [red]--unsafe[/red] for real exploits.",
        title="WARNING",
        border_style="bright_red"
    ))

def generate_reports(results_dict, report_type, simulate):
    if report_type == 'html':
        generate_html_report(results_dict, simulate=simulate)
    elif report_type == 'json':
        generate_json_report(results_dict, simulate=simulate)

def parse_args():
    parser = argparse.ArgumentParser(description='CVE Detection and Docker Breakout Tool')
    parser.add_argument('--attack', type=str, help='Specify CVE ID to run, e.g. CVE-2019-5736')
    parser.add_argument('--auto', action='store_true', help='Automatically run all known CVE modules')
    parser.add_argument('--container', type=str, help='Specify the container name or ID')
    parser.add_argument('--report', choices=['html', 'json'], help='Generate report in specified format')
    parser.add_argument('--simulate', action='store_true', help='Simulate the exploit without executing real changes')
    parser.add_argument('--unsafe', action='store_true', help='Actually execute real exploits (DANGEROUS)')
    return parser.parse_args()

async def async_run_module_with_env(module, container, cve_id, env_info, semaphore, simulate):
    async with semaphore:
        loop = asyncio.get_event_loop()

        def _exec():
            if hasattr(module, "is_vulnerable"):
                if not module.is_vulnerable(env_info):
                    log("INFO", f"{cve_id} skipped: not vulnerable under current environment.")
                    return (cve_id, "Skipped (not vulnerable)")
            if simulate:
                log("SIMULATE", f"Running {cve_id} in simulation mode...")
            else:
                log("EXPLOIT", f"Executing {cve_id} with real payload...")
            return (cve_id, module.run(container, simulate=simulate))

        return await loop.run_in_executor(None, _exec)

async def run_all_attacks_async(container, simulate):
    results = {}
    env_info = get_docker_info()
    attack_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'attacks'))
    semaphore = asyncio.Semaphore(MAX_PARALLEL_TASKS)
    tasks = []

    for fname in os.listdir(attack_dir):
        if fname.startswith('cve_') or fname.endswith('_abuse.py') or fname.endswith('_exploit.py'):
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
    banner()
    args = parse_args()

    if args.simulate and args.unsafe:
        log("WARNING", "You cannot use both --simulate and --unsafe at the same time.")
        exit(1)

    simulate = not args.unsafe

    if not simulate:
        log("EXPLOIT", "You are about to execute REAL exploits on the container.")
        confirm = input("Are you sure you want to continue? Type 'yes' to proceed: ")
        if confirm.strip().lower() != "yes":
            log("INFO", "Confirmation failed. Aborting execution.")
            exit(1)

    if args.container:
        try:
            container = client.containers.get(args.container)
        except docker.errors.NotFound:
            log("WARNING", f"Container '{args.container}' not found.")
            exit(1)
    else:
        log("WARNING", "Please specify --container")
        exit(1)

    if args.auto:
        results = asyncio.run(run_all_attacks_async(container, simulate=simulate))
        if args.report:
            generate_reports(results, args.report, simulate=simulate)
            log("SUCCESS", f"Report saved in {args.report.upper()} format")

    elif args.attack:
        module = load_attack_module(args.attack)
        if module and hasattr(module, 'run'):
            if simulate:
                log("SIMULATE", f"Running {args.attack} in simulation mode...")
            else:
                log("EXPLOIT", f"Executing {args.attack}...")
            result = module.run(container, simulate=simulate)
            if args.report:
                generate_reports({args.attack: result}, args.report, simulate=simulate)
                log("SUCCESS", f"Report saved in {args.report.upper()} format")
        else:
            log("WARNING", "Attack module is invalid or missing 'run' function.")
    else:
        log("WARNING", "No action specified. Use --attack <CVE-ID> or --auto")
