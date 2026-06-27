Steps to run locally with llama 3.1

1. In a terminal session execute 
    ```shell
    ollama serve
    ```

2. In another terminal session execute
    ```shell
    ollama pull llama3.1
    ```

3. In another terminal session run to set proper env vars and python environment
    ```shell
    source .venv/bin/activate
    export OLLAMA_HOST="http://localhost:11434"
    export OLLAMA_MODEL="llama3.1"
    ```

4. TEST:
    - Calculator:
        ```shell
        python -m mia_agents.cli run --module student_framework --message "¿Cuánto es 17 * 23? Usá la calculadora."
        ```

    - File reader:
        ```bash
        python -m mia_agents.cli run --module student_framework --message "Leé el archivo student_framework/examples/file_reader_demo.txt y decime qué contiene."
        ```

