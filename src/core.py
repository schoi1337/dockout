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

def generate_reports(attack_result):
    # Generate HTML and JSON reports in 'reports' directory
    generate_html_report(attack_result)
    generate_json_report(attack_result)

if __name__ == "__main__":
    # Example usage
    print("Listing all containers:")
    list_containers()

    # Test CVE-2019-5736 on the test container
    container_id = "test-container"  # Replace with your actual container ID
    attack_result = "Test successful: CVE-2019-5736 test > /tmp/test.txt"
    generate_reports(attack_result)
