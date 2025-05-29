import subprocess

def test_cve_2019_5736(container):
    # Testing CVE-2019-5736 on a container
    print(f"Testing CVE-2019-5736 on container {container.id}")
    
    # Running a simple command to simulate the exploit
    attack_command = "echo 'CVE-2019-5736 test' > /tmp/test.txt"
    result = container.exec_run(attack_command)
    
    if result.exit_code == 0:
        print(f"Test successful: {result.output.decode()}")
    else:
        print(f"Test failed: {result.output.decode()}")
