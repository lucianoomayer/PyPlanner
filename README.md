# 📝 Gerenciador de Tarefas (Plano + CSV)

Um pequeno projeto Python que implementa um **gerenciador de tarefas** capaz de:

✔ Criar e gerenciar tarefas em memória  
✔ Salvar tarefas em arquivos **CSV**  
✔ Atualizar, remover e inserir linhas em arquivos CSV  
✔ Manipular datas no formato **dd/mm/yyyy**  
✔ Criar um sistema de persistência simples e funcional  

O projeto foi dividido em duas classes principais:

- **Planner** → gerencia as tarefas em memória  
- **CSVFile** → controla operações em CSV 

Para instalar a biblioteca:
```bash
pip install -i https://test.pypi.org/simple/ pyplanner
```

## Como funciona

### 🔹 Classe `Planner`

Armazena tarefas em memória. Cada tarefa possui:

- `nome` — Nome da tarefa  
- `data` — Data no formato dd/mm/yyyy (opcional)  
- `estado` — "Incompleto" ou "Completo"

Permite:

- adicionar (`add`)
- buscar (`find`)
- editar (`update`)
- remover (`remove`)
- listar (`get`)

### 🔹 Classe `CSVFile`

Manipula arquivos CSV contendo tarefas.

| Método | O que faz |
|--------|-----------|
| `create()` | Cria ou sobrescreve um CSV com todas as tarefas do plano |
| `insert()` | Insere uma nova tarefa no CSV |
| `remove()` | Remove uma tarefa específica do CSV |
| `update()` | Atualiza um campo de uma tarefa no CSV |

Todos usam o **Desktop como caminho padrão**, mas você pode passar qualquer diretório.

# 📚 Exemplos de Uso

## 1. Criar um plano e adicionar tarefas

```python
from pyplanner import Planner, CSVFile

plano = Planner()

plano.add("Estudar Python", "01/12/2025")

tarefas_tupla = ("Ir à academia", "03/12/2025")
plano.add(tarefas_tupla)

tarefas_list = [("Pagar contas", "10/12/2025"), ("Mercado", "05/12/2025")]
plano.add(tarefas_list)
```

## 2. Criar um arquivo CSV 

```python
CSVFile.create("tarefas.csv", plano)
```

## 3. Inserir, atualizar e remover tarefas do CSV

```python
CSVFile.insert("tarefas.csv", "Comprar presente", "15/12/2025")

CSVFile.update("tarefas.csv", "Ir à academia", "Estado", "Completo")

CSVFile.remove("tarefas.csv", "Pagar contas")
```
