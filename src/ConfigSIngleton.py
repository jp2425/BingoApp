from config import config

class ConfigSingleton:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ConfigSingleton, cls).__new__(cls)
        return cls.instance

    def get_page_config(self, page:str) -> dict:
        """
        Returns the configuration of a webpage
        :param page: string in the config file used to specify the configuration for a webpage template
        :return: the configuration of the web page (dictionary. see src/config.py
        """

        try:
            return config["page"][page]
        except:
            raise ValueError("The page specified does not exist. See the configuration to get a valid name.")

    def get_message_available_commands(self):
        return config["message_available_commands"]


