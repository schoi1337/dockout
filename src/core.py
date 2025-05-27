import argparse
import docker
from attacks import test_cve_2019_5736
from report_generator import generate_html_report, generate_json_report

# Initialize the Docker client
client = docker.from_env()

def list_containers():
    # List all containers
    containers = client.containers.list(all=True)
    for container in containers:
        print(f"Container {container.id} - {container.name} - Status: {container.status}")

def get_container_details(container_id):
    # Get details of a specific container
    container = client.containers.get(container_id)
    print(f"Container {container.id} - {container.name}")
    print(f"Status: {container.status}")
    print(f"Image: {container.image.tags}")
    return container

def test_cve_on_container(container_id):
    # Test CVE-2019-5736 on a specific container
    container = client.containers.get(container_id)
    test_cve_2019_5736(container)

def generate_reports(attack_result, report_type):
    # Generate reports in HTML or JSON format
    if report_type == 'html':
        generate_html_report(attack_result)
    elif report_type == 'json':
        generate_json_report(attack_result)

def parse_args():
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='CVE Detection and Docker Breakout Tool')

    parser.add_argument('--attack', action='store_true', help='Perform the attack')
    parser.add_argument('--report', choices=['html', 'json'], help='Generate report in specified format (html/json)')
    parser.add_argument('--container', type=str, help='Specify the container ID to test')
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    if args.attack:
        if args.container:
            print(f"Testing CVE-2019-5736 on container {args.container}...")
            test_cve_on_container(args.container)
            attack_result = f"Test successful: CVE-2019-5736 test > /tmp/test.txt"
            
            if args.report:
                print(f"Generating {args.report} report...")
                generate_reports(attack_result, args.report)
        else:
            print("Error: You must specify a container ID using --container")
    
    elif args.report:
        print("Error: You must specify --attack before generating a report.")
    else:
        print("Error: No action specified. Use --attack to perform an attack or --report to generate a report.")
