import os
import shutil

from docker.api import container

from utils import load_challenge
from utils import verify_solution_and_cleanup
from docker_util import start_challenge
from utils import del_challenge_directory
from utils import start_ctf_container
from utils import start_ctf_container_interactively
from docker_util import start_challenge_container
from utils import shutdown_container
from docker_util import interactive_container_shell


"""

Note to future Ryder, I need to stop for now because stupid mandarin midterm but the current issue seems to be with 
how the permissions are configured in the docker container. That is what is causing the weird bash issues.


"""


def generate_challenge(challenge_number):
    challenge_module, solution_module = load_challenge(challenge_number)
    print("Challenge generated successfully.")
    challenge_module.create_disk_image()
    print("Challenge generated successfully.")
    challenge_id = 1
    start_challenge_container(challenge_id)
    return start_challenge(challenge_id)


def main_menu():
    # temp console menu
    while True:
        print("\nCTF Challenge Manager")
        choice = input("Enter the file_carving_2 number to work with (or 'exit' to quit): ")

        if choice.lower() == 'exit':
            print("Exiting...")
            break

        try:

            challenge_number = int(choice)
            challenge_module, solution_module = load_challenge(challenge_number)



            action = input(
                f"Select action for Challenge {challenge_number}: (web_1) Generate, (2) Del Local Directory:, (3) Back ")

            if action == 'web_1':
                print(f"Generating Challenge {challenge_number}...")
                challenge_module.create_disk_image()
                print("Challenge generated successfully.")
                challenge_id = 1
                start_challenge_container(challenge_id)
                start_challenge(challenge_id)
                cont_id = input("id")
                interactive_container_shell(cont_id)


                while True:
                    user_answer = input("Flag: ")

                    print(f"Verifying Solution for Challenge {challenge_number}...")
                    ans = solution_module.extract_answer()
                    print(ans)

                    if verify_solution_and_cleanup(challenge_number, user_answer,
                                                   solution_module.extract_answer()) == 0:
                        print("Correct answer!")
                        break

                    else:
                        continue
            else:
                print("Invalid action.")

            if action == '2':
                del_challenge_directory(challenge_number)
            if action == '3':
                break
        except ValueError:
            print("Please enter a valid file_carving_2 number.")
        except ModuleNotFoundError:
            print(f"Challenge {choice} does not exist.")


if __name__ == "__main__":
    main_menu()