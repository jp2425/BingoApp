from abc import ABC, abstractmethod


class RepoAbsClass(ABC):
    """
    Abstract class that must be used by any repository implemented.
    """

    @abstractmethod
    def insert_number_action(self, number: int):
        """
        Function to insert a number into the database.
        :param number: Number to insert in the database
        """
        pass

    @abstractmethod
    def delete_number_action(self, number:int):
        """
        Function to delete a number into the database.
        :param number: Number to delete in the database
        """
        pass

    @abstractmethod
    def get_all_numbers(self):
        """
        Function used to get all numbers in the database.
        """
        pass

    @abstractmethod
    def get_last(self):
        """
        Function to get the last number inserted in the database
        """
        pass