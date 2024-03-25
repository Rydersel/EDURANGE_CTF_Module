from flask import Flask, jsonify, request
from kubernetes import client, config

app = Flask(__name__)

def create_kctf_challenge_manifest(challenge_name):
    # Example Deployment manifest. You should adjust this according to your challenge needs.
    # This includes setting the right Docker image for your challenge.
    return {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": challenge_name
        },
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                    "app": challenge_name
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": challenge_name
                    }
                },
                "spec": {
                    "containers": [{
                        "name": challenge_name,
                        "image": "your_docker_image_here",  # Specify your Docker image
                        "ports": [{
                            "containerPort": 1337  # Adjust the port based on your challenge configuration
                        }]
                    }]
                }
            }
        }
    }

@app.route('/create_challenge', methods=['POST'])
def create_challenge():
    # Load Kubernetes configuration. Adjust this if your app runs inside a Kubernetes cluster.
    config.load_kube_config()

    # Extract challenge name from the request
    data = request.get_json()
    challenge_name = data.get('challenge_name')

    # Kubernetes client setup
    api_instance = client.AppsV1Api()

    # Create Kubernetes Deployment for the challenge
    deployment_manifest = create_kctf_challenge_manifest(challenge_name)
    api_response = api_instance.create_namespaced_deployment(
        body=deployment_manifest,
        namespace='default'  # Specify the namespace if not 'default'
    )

    return jsonify({"message": f"Challenge '{challenge_name}' created", "deployment": api_response.metadata.name}), 201

if __name__ == "__main__":
    app.run(debug=True)
