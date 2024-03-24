from flask import Flask, request, render_template, jsonify
import subprocess
from main import generate_challenge

app = Flask(__name__)

global docker_id
@app.route('/execute_command', methods=['POST'])
def execute_command():
    user_command = request.form['command']
    challenge_number = request.form['challenge_number']
    result = subprocess.run(user_command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(result.stdout)
        output = (result.stdout)
    else:
        output = ("Error:", result.stderr)
        print("error")



    return jsonify({'output': output})




@app.route('/')
def home():
    #TODO dynamically list challenges (maybe split it into catagorized modules
    challenges = [1, 2, 3]
    return render_template('index.html', challenges=challenges)

@app.route('/start_challenge/<int:challenge_number>', methods=['GET'])
def start_challenge(challenge_number):


    docker_id = (generate_challenge(challenge_number))
    return render_template('challenge_started.html', challenge_number=challenge_number)



if __name__ == "__main__":
    app.run(debug=True)

