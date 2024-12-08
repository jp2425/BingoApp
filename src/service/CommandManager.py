import asyncio
from ConfigSIngleton import ConfigSingleton
from repo.RepoAbsClass import RepoAbsClass
from service.ConnectionManager import ConnectionManager

from service.NumberService import NumberService


class CommandManager:
    """
    Class for managing commands entered in the terminal.
    This class runs in a thread and is responsible for inserting/removing numbers from the database.
    """

    def __init__(self, db_repo:RepoAbsClass, service: NumberService):
        self._repo = db_repo
        self._service = service

    def print_available_commands(self):
        print(ConfigSingleton().get_message_available_commands())


    def process_command(self, command: str):
        """
        Function for processing the command entered by the user.
        """
        try:

            if command.upper() == "CLEAR ALL":
                self._repo.clear_all()
            else:
                # parsing
                parameters = command.split("-")
                if len(parameters) > 2:
                    raise ValueError("The command has too many '-'!\nEnter again please.")

                action = parameters[0]
                number = parameters[1]

                try:
                    if str(action).upper() == "I":
                        self._repo.insert_number_action(int(number))
                    elif str(action).upper() == "D":
                        self._repo.delete_number_action(int(number))
                    else:
                        raise ValueError("The command is wrong! It must be in the format i-{number} or d-{number} '-'!\nEnter again please.")
                except Exception as e:
                    raise ValueError(f"The command is not valid! {e}")

            asyncio.run(self._service.update_clients())

        except Exception as e:
            print(f"Error processing the command.\nMessage: {e}")




    def read_command(self):
        """
        Method for continuously reading commands.
        """
        while True:
            try:
                self.print_available_commands()
                command = input("Enter the command: ")
                self.process_command(command)
            except Exception as e:
                print(f"Error processing the command: {e}")

        # for testing
        #for n in range(0,90):
        #    self.process_command(f"i-{n}")
        #    from time import sleep
        #    sleep(1)
