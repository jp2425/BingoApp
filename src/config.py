config = {
    "page":{ #all configs used in web page templates
        "last":{ #the /last endpoint
           "title":"Last Number",
            "container_title":"Last number drawn",
            "default_last_message_empty_values": "No number drawn"
        },
        "history":{ #the /history endpoint
            "title":"Last number",
            "container_title":"History of numbers drawn"
        },
        "number":{ #the /number endpoint
            "title":"Bingo",
            "button_reset":"Reset",
            "button_change_ui":"Manual UI",
            "allowed_IP":["127.0.0.1", "::1"] #only these IPs can access the endpoint. Empty for any IP
        },
        "backup_restore":{
            "allowed_IP":["127.0.0.1", "::1"] #only these IPs can access the endpoint. Empty for any IP
        }
    },
    "message_available_commands": """
        [*] Available commands:

            i-{number} - inserts the number into the database and sends it to customers.
                         Example: i-20 (adds the number 20)
            d-{number} - Removes a number that has already gone out and updates the data in the clients.
                         Good for correcting problems with numbers going out incorrectly.
                         Example: d-20 (deletes the number 20)
        """
}