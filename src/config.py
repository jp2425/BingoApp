config = {
    "page":{ #all configs used in web page templates
        "last":{ #the /last endpoint
           "title":"Último número",
            "container_title":"Último número sorteado",
            "default_last_message_empty_values": "Nenhum número sorteado"
        },
        "history":{ #the /history endpoint
            "title":"Último número",
            "container_title":"Histórico de números sorteados"
        }
    },
    "message_available_commands": """
        [*] Comandos disponíveis:

            i-{número} - insere o número na base de dados e envia aos clientes.
                         Exemplo: i-20 (adiciona o número 20)
            d-{número} - Remove um número que já tenha saido e atualiza os dados nos clientes.
                         Bom para corrigir problemas de números a sairem de forma errada.
                         Exemplo: d-20 (apaga o número 20)
        """
}