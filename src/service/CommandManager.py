import asyncio
from ConfigSIngleton import ConfigSingleton
from repo.RepoAbsClass import RepoAbsClass
from service.ConnectionManager import ConnectionManager


class CommandManager:
    """
    Class for managing commands entered in the terminal.
    This class runs in a thread and is responsible for inserting/removing numbers from the database.
    """

    def __init__(self, db_repo:RepoAbsClass, manager: ConnectionManager):
        self._repo = db_repo
        self._manager = manager

    def print_available_commands(self):
        print(ConfigSingleton().get_message_available_commands())


    def process_command(self, command: str):
        """
        Function for processing the command entered by the user.
        """
        try:


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

            # sends the last number to the client (if it exists). IF there is no "last number", it will send the default message specified in the configuration ("default_last_message_empty_values" key)
            last_number = self._repo.get_last()
            asyncio.run(self._manager.send_last(str(last_number)))


            # Sends the complete history to the history client
            numbers = self._repo.get_all_numbers()
            history_str = ""

            # if we got no numbers stored in the database we should not send anything with a comma to the client.
            if len(numbers) > 0:
                history = [str(n[0]) for n in numbers]
                history_str = ','.join(history)

            asyncio.run(self._manager.send_history(history_str))

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
