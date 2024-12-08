<h1 style="text-align: center;">
Bingo management APP<br>
<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
</h1>  

This project aims to create a simple application to manage the numbers in a bingo game.  
It allows to have **multiple clients connected at the same time and getting the same information at the same time**.  
This functionality is usefull in case of projecting the numbers drawn in one device and using other to project an history of the past numbers drawn.  

## The app  
  
This app provides multiple endpoints:  
* An endpoint to present the last number drawn (`http://IP:PORT/last`).  
* An endpoint to show the history of numbers drawn (`http://IP:PORT/history`)
* Endpoint to quickly insert numbers drawn (`http://IP:PORT/number`)
* Endpoint to restore database backups (`http://IP:PORT/number_manual`)

The server allows the operator to insert or delete numbers via terminal, but it is not the recommended method. The information is stored in a local database (sqlite), to avoid data loss in case of application failure.  
The webpages served by the application also implement a reconnect mechanism to overcome possible network problems, which may lead to the connection loss between the clients/server.

## Configuration  

This app has a simple configuration system. All configuration is stored in the [config.py](src/config.py) file.  
A sample configuration can be analyzed bellow:  
```python
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
```  

The `/number` and `/number_manual` endpoind can only accept connections from specific IPs. To do this, simply add the allowed IP to the `allowed_IP` array in the settings. **Note:** empty array allows any IP to connect
## Testing the app

Just run:  
```bash
pip install -r requirements.txt
python main.py
```  
  
## Gallery

![img1](img/backup_restore.png)  
![img2](img/history.png)  
![img3](img/last.png)
![img4](img/number.png)