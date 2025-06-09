import tempfile
import subprocess
import os
import re
import codecs

def extract_check_result(ansible_stdout):
    match = re.search(r'"check_result.stdout":\s*"((?:[^"\\]|\\.)*)"', ansible_stdout)
    if match:
        return codecs.decode(match.group(1), 'unicode_escape')
    return ansible_stdout

def run_os_check_script(ip, username, password, os_info, host_id=None, hostname=None):
    BASE_PATH = "/home/user/ansible-manager/backend/playbooks"
    if "Ubuntu" in os_info:
        script_path = f"{BASE_PATH}/ubuntu_check.sh"
    elif "CentOS" in os_info:
        script_path = f"{BASE_PATH}/centos_check.sh"
    else:
        script_path = f"{BASE_PATH}/generic_check.sh"

    inventory_content = f"""[target]
{ip} ansible_user={username} ansible_password={password} ansible_become=yes ansible_become_method=sudo ansible_become_password={password} ansible_ssh_common_args='-o StrictHostKeyChecking=no'
"""
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as inv_file:
        inv_file.write(inventory_content)
        inv_path = inv_file.name

    # 플레이북에 전달할 extra_vars 준비
    extra_vars = [
        "-e", f"script_path={script_path}",
        "-e", f"username={username}"
    ]
    if host_id is not None:
        extra_vars.extend(["-e", f"host_id={host_id}"])
    if hostname is not None:
        extra_vars.extend(["-e", f"hostname={hostname}"])

    try:
        result = subprocess.run(
            [
                "ansible-playbook",
                "-i", inv_path,
                f"{BASE_PATH}/run_script.yml",
            ] + extra_vars,
            capture_output=True,
            text=True,
            timeout=300
        )
        clean_stdout = extract_check_result(result.stdout)
        return {
            "stdout": clean_stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    finally:
        os.remove(inv_path)
