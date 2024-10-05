import asyncio
from time import sleep

from ConnectionManager import ConnectionManager


class CommandManager:
    """
    Classe para gerir os comandos introduzidos no terminal.
    Esta classe é executada numa thread, e é responsável pela insersão/remoção de números na base de dados.
    """

    def __init__(self, cursor, connection_db, manager: ConnectionManager):
        self._cursor = cursor
        self._conn = connection_db
        self._manager = manager
        #self.loop = asyncio.new_event_loop()
        #asyncio.set_event_loop(self.loop)

    def print_available_commands(self):
        commands = """
        [*] Comandos disponíveis:

            i-{número} - insere o número na base de dados e envia aos clientes.
                         Exemplo: i-20 (adiciona o número 20)
            d-{número} - Remove um número que já tenha saido e atualiza os dados nos clientes.
                         Bom para corrigir problemas de números a sairem de forma errada.
                         Exemplo: d-20 (apaga o número 20)
        """
        print(commands)


    def process_command(self, command: str):
        """
        Função para processar o comando introduzido pelo utilizador.
        """
        try:


            # parsing
            parameters = command.split("-")
            if len(parameters) > 2:
                raise ValueError("O comando tem demasiados '-'!\nIntroduz de novo.")

            action = parameters[0]
            number = parameters[1]

            if str(action).upper() == "I":
                self.insert_number_action(number)
            elif str(action).upper() == "D":
                self.delete_number_action(number)
            else:
                raise ValueError("O comando está errado! Tem de ser no formato i-{numero} ou d-{numero} '-'!\nIntroduz de novo.")

            # Envia o último número atualizado aos clientes
            last_number = self.get_last()
            if last_number:

                #asyncio.run_coroutine_threadsafe(self._manager.send_last(str(last_number)), self.loop).result(2)  #dá erro
                asyncio.run(self._manager.send_last(str(last_number)))

            # Envia o histórico completo ao cliente do histórico
            numbers = self.get_all_numbers()
            history = [str(n[0]) for n in numbers]
            history_str = ','.join(history)
           # asyncio.run_coroutine_threadsafe(self._manager.send_history(history_str), self.loop).result(2) #dá erro
            asyncio.run(self._manager.send_history(history_str))

        except Exception as e:
            print(f"Erro ao processar o comando: {e}")


    def insert_number_action(self, number):
        """
        Função para inserir dados na base de dados.
        """
        self._cursor.execute("INSERT INTO numeros (numero) VALUES (?)", (number,))
        self._conn.commit()

    def delete_number_action(self, number):
        """
        Função para apagar dados na base de dados.
        """
        self._cursor.execute("DELETE FROM numeros WHERE numero = (?)", (number,))
        self._conn.commit()

    def get_all_numbers(self):
        """
        Função para obter todos os números da base de dados.
        """
        return self._conn.execute("SELECT numero FROM numeros").fetchall()

    def get_last(self):
        """
        Função para obter o último número da base de dados.
        """
        self._cursor.execute("SELECT numero FROM numeros ORDER BY id DESC LIMIT 1")
        return self._cursor.fetchone()[0]

    def read_command(self):
        """
        Método para leitura contínua de comandos.
        """
        while True:
            try:
                self.print_available_commands()
                command = input("Digite o comando: ")
                self.process_command(command)

            except Exception as e:
                print(f"Erro ao ler comando: {e}")
