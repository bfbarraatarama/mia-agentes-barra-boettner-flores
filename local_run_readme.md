Steps to run locally with Ollama 3.1

in a terminal session execute 
```shell
ollama serve
```

in another terminal session execute
```shell
ollama pull llama3.1
```

in another terminal session run to set proper env vars and python environment
```shell
source .venv/bin/activate
export OLLAMA_HOST="http://localhost:11434"
export OLLAMA_MODEL="llama3.1"
```

TEST:
```shell
python -m mia_agents.cli run --module student_framework --message "¿Cuánto es 17 * 23? Usá la calculadora."
```