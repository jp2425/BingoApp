import asyncio
from multiprocessing.managers import Value

from repo.RepoAbsClass import RepoAbsClass
from service.ConnectionManager import ConnectionManager

class NumberService:

    def __init__(self, db: RepoAbsClass, manager: ConnectionManager):
        self._repo = db
        self._manager = manager

    async def update_clients(self):
        # Sends the last number to the client (if it exists).
        # If there is no "last number", it will send the default message specified in the configuration ("default_last_message_empty_values" key)
        last_number = self._repo.get_last()
        await self._manager.send_last(str(last_number))  # Await instead of asyncio.run()

        # Sends the complete history to the history client
        numbers = self._repo.get_all_numbers()
        history_str = ""

        # If we got no numbers stored in the database we should not send anything with a comma to the client.
        if len(numbers) > 0:
            history = [str(n[0]) for n in numbers]
            history_str = ','.join(history)

        await self._manager.send_history(history_str)  # Await instead of asyncio.run()

    async def insert_number_db(self, number):
        try:
            number = int(number)
        except ValueError:
            raise ValueError("One value is not a valid number! Value: ", str(number))

        self._repo.insert_number_action(number)
        await self.update_clients()
    async def delete_number_db(self, number):
        try:
            number = int(number)
        except ValueError:
            raise ValueError("One value is not a valid number! Value: ", str(number))

        self._repo.delete_number_action(number)
        await self.update_clients()

    async def clear_db(self):


        self._repo.clear_all()
        await self.update_clients()

    async def get_all_numbers(self):
        nums = self._repo.get_all_numbers()
        return [num[0] for num in nums]
