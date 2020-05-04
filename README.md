## Very basic peer to peer technology code.
- create a environment using the following command.
    ```
    python3 -m venv <path/to/env> 
    ex: 
    python3 -m venv /tmp/peer_env
    ```

- now activate the environment.
    ```
    source <path/to/env-bin>
    source /tmp/peer_env/bin/activate
    ```
- install requirements.txt
    ```
    pip install -r requirements.text
    ```
- run  ` python peer_node_1.py`
- Then run `python peer_node.py`
- Now you can observe both of them sending files to each other in a synchronised manner.

