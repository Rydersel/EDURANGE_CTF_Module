import subprocess
import os


def run_command(command):
    """
    Executes a system command and returns the output.
    """
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def setup_kctf_environment(project_id, zone, cluster_name):
    """
    Configures gcloud and kubectl to use the specified GKE cluster.
    """
    print(f"Setting gcloud project to {project_id}...")
    run_command(f"gcloud config set project {project_id}")

    print(f"Getting credentials for GKE cluster {cluster_name}...")
    success, output = run_command(f"gcloud container clusters get-credentials {cluster_name} --zone {zone}")
    if not success:
        print(f"Failed to get credentials for GKE cluster: {output}")
        return False
    return True


def create_and_deploy_challenge(challenge_name, project_id, zone, cluster_name):
    """
    Creates a new kCTF challenge using gcloud and deploys it to the specified GKE cluster.

    Parameters:
    - challenge_name: The name of the challenge.
    - project_id: GCP project ID.
    - zone: GCP zone where the GKE cluster is located.
    - cluster_name: The name of the GKE cluster.
    """
    # Ensure the kCTF environment is correctly set up
    if not setup_kctf_environment(project_id, zone, cluster_name):
        return

    # Commands to create and deploy the challenge (placeholders)
    create_challenge_cmd = f"echo Creating challenge {challenge_name}"
    deploy_challenge_cmd = f"echo Deploying challenge {challenge_name}"

    # Execute commands (replace these placeholders with actual kCTF commands)
    print("Starting kCTF")

    success, output = run_command("source kctf/activate")
    if not success:
        print(f"Failed to start KCTF: {output}")
        return
    print("Creating challenge...")
    success, output = run_command(create_challenge_cmd)
    if not success:
        print(f"Failed to create challenge: {output}")
        return

    print("Deploying challenge...")
    success, output = run_command(deploy_challenge_cmd)
    if not success:
        print(f"Failed to deploy challenge: {output}")
        return

    print(f"Challenge '{challenge_name}' deployed successfully.")


if __name__ == "__main__":
    # Example usage
    challenge_name = "challenge-demo1"
    project_id = "edurangectf"
    zone = "europe-west4-b"
    cluster_name = "kctf-cluster"

    create_and_deploy_challenge(challenge_name, project_id, zone, cluster_name)
