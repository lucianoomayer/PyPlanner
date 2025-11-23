import datetime
import csv
import os
from typing import Any

class Planner:
    """
    Classe responsável por gerenciar um plano de tarefas.
    Cada tarefa possui nome, data e estado.
    """

    def __init__(self):
        """Inicializa a lista interna de tarefas."""
        self._tarefas = []

    @staticmethod
    def _formata_data(data: str | None) -> datetime.date | None:
        """
        Converte uma string no formato 'dd/mm/yyyy' para um objeto datetime.date.

        Args:
            data (str | None): Data em formato string ou None.

        Returns:
            datetime.date | None: Objeto de data convertido ou None se vazio.
        """
        if not data:
            return None
        try:
            return datetime.datetime.strptime(data, "%d/%m/%Y").date()
        except ValueError:
            raise ValueError("Data inválida. Use o formato dd/mm/yyyy.")

    def add(self, tarefa: Any, *args) -> None:
        """
        Adiciona uma ou mais tarefas ao plano.

        Args:
            tarefa (Any): Pode ser uma tupla (nome, data), uma string (nome) ou uma lista de tuplas.
            *args: Argumentos adicionais (usado para passar data quando tarefa é string).
        """
        estado = "Incompleto"
        if isinstance(tarefa, tuple):
            nome, data = tarefa
            self._tarefas.append({
                "nome": nome,
                "data": Planner._formata_data(data),
                "estado": estado,
            })
        elif isinstance(tarefa, str):
            data = Planner._formata_data(args[0]) if args else None
            self._tarefas.append({
                "nome": tarefa,
                "data": data,
                "estado": estado,
            })
        elif isinstance(tarefa, list):
            for nome, data in tarefa:
                self._tarefas.append({
                    "nome": nome,
                    "data": Planner._formata_data(data),
                    "estado": estado,
                })
        else:
            raise TypeError("Tipo de tarefa inválido. Insira na forma de string, tupla ou lista.")
        print("Tarefa(s) adicionada(s) com sucesso!")

    def get(self) -> list[dict[str, Any]]:
        """
        Retorna todas as tarefas cadastradas.

        Returns:
            list[dict[str, Any]]: Lista de dicionários com tarefas.
        """
        return self._tarefas

    def find(self, nome: str) -> int | None:
        """
        Busca o índice de uma tarefa pelo nome.

        Args:
            nome (str): Nome da tarefa.

        Returns:
            int | None: Índice da tarefa ou None se não encontrada.
        """
        for i, tarefa in enumerate(self._tarefas):
            if tarefa["nome"] == nome:
                return i
        return None

    def remove(self, nome: str) -> bool:
        """
        Remove uma tarefa pelo nome.

        Args:
            nome (str): Nome da tarefa a ser removida.

        Returns:
            bool: True se removida, False se não encontrada.
        """
        indice = self.find(nome)
        if indice is not None:
            tarefa_removida = self._tarefas.pop(indice)
            print(f"Tarefa '{tarefa_removida['nome']}' removida com sucesso!")
            return True
        print("Tarefa não encontrada!")
        return False

    def update(self, tarefa: str, campo_alvo: str, novo_valor: str) -> bool:
        """
        Atualiza um campo específico de uma tarefa.

        Args:
            tarefa (str): Nome da tarefa a ser atualizada.
            campo_alvo (str): Campo a ser atualizado ('Nome', 'Data' ou 'Estado').
            novo_valor (str): Novo valor para o campo.

        Returns:
            bool: True se atualizado, False se não encontrada.
        """
        indice = self.find(tarefa)
        if indice is None:
            print("Tarefa não encontrada!")
            return False

        if campo_alvo in ["nome", "data", "estado"]:
            if campo_alvo == "data":
                self._tarefas[indice]["data"] = Planner._formata_data(novo_valor)
            else:
                self._tarefas[indice][campo_alvo] = novo_valor    
        else:
            raise ValueError("Campo inválido. Use 'Tarefa', 'Data' ou 'Estado'.")
        print(f"Tarefa '{self._tarefas[indice]['nome']}' atualizada com sucesso!")
        return True

class CSVFile:
    """
    Classe utilitária para manipulação de arquivos CSV relacionados às tarefas.
    """

    @staticmethod
    def _full_path(file_name: str, path: str | None) -> str:
        """
        Retorna o caminho completo para o arquivo CSV, garantindo que o diretório exista.

        Args:
            file_name (str): Nome do arquivo CSV.
            path (str | None): Caminho do diretório onde o arquivo será salvo.
                Se None, o caminho padrão será o Desktop do usuário.

        Returns:
            str: Caminho completo (absoluto) para o arquivo.
        """
        if path is None:
            path = os.path.join(os.path.expanduser("~"), "Desktop")

        if not os.path.isdir(path):
            raise FileNotFoundError(f"Caminho inválido: {path}")    
            
        return os.path.join(path, file_name)

    @staticmethod
    def create(file_name: str, plano: Planner, path=None) -> None:
        """
        Cria um arquivo CSV com todas as tarefas do plano.

        Args:
            file_name (str): Nome do arquivo.
            plano (Planner): Instância da classe Planner.
            path (str, optional): Caminho onde salvar. Default: Desktop.
        """
        if not plano:
            raise ValueError("Informe um plano válido.")
        
        tarefas = plano.get()
        if not tarefas:
            raise ValueError("O plano informado não pode estar vazio.")

        full_path = CSVFile._full_path(file_name, path)

        try:
            with open(full_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(["Tarefa", "Data", "Estado"])
                for tarefa in plano.get():
                    data_str = tarefa["data"].strftime("%d/%m/%Y") if tarefa.get("data") else ""
                    writer.writerow([tarefa["nome"], data_str, tarefa["estado"]])
        except Exception as e:
            raise RuntimeError(f"Erro ao criar o arquivo CSV em '{full_path}'.") from e
        print(f"Arquivo '{file_name}' criado com sucesso.")

    @staticmethod
    def insert(file_name: str, tarefa: str, data: str = None, estado: str = "Incompleto", path=None) -> None:
        """
        Insere uma nova tarefa em um arquivo CSV.

        Args:
            file_name (str): Nome do arquivo.
            tarefa (str): Nome da tarefa.
            data (str): Data da tarefa.
            estado (str, optional): Estado da tarefa. Default: "Incompleto".
            path (str, optional): Caminho onde salvar. Default: Desktop.
        """
        if not tarefa:
            raise ValueError("O nome da tarefa não pode ser vazio.")

        full_path = CSVFile._full_path(file_name, path)

        try:
            with open(full_path, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow([tarefa, data, estado])
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Arquivo '{full_path}' não encontrado.") from e 
        except Exception as e:
            raise RuntimeError(f"Erro ao inserir a tarefa '{tarefa}' no arquivo '{full_path}'.") from e      
        print(f"Tarefa '{tarefa}' inserida com sucesso.")

    @staticmethod
    def remove(file_name: str, tarefa: str, path=None) -> None:
        """
        Remove uma tarefa de um arquivo CSV.

        Args:
            file_name (str): Nome do arquivo.
            tarefa (str): Nome da tarefa a ser removida.
            path (str, optional): Caminho onde salvar. Default: Desktop.
        """
        if not tarefa:
            raise ValueError("O nome da tarefa não pode ser vazio.")

        full_path = CSVFile._full_path(file_name, path)

        try:
            with open(full_path, "r", newline="", encoding="utf-8") as file:
                conteudo = csv.DictReader(file, delimiter=";")
                colunas = conteudo.fieldnames
                linhas_mantidas = [linha for linha in conteudo if linha.get("Tarefa") != tarefa]
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Arquivo '{full_path}' não encontrado.") from e
        except Exception as e:
            raise RuntimeError(f"Erro ao ler o arquivo '{full_path}'.") from e
        try:
            with open(full_path, "w", newline="", encoding="utf-8") as file:
                escritor = csv.DictWriter(file, fieldnames=colunas, delimiter=";")
                escritor.writeheader()
                escritor.writerows(linhas_mantidas)
        except Exception as e:
            raise RuntimeError(f"Erro ao remover a tarefa '{tarefa}'.") from e
        print(f"Tarefa '{tarefa}' removida com sucesso.")

    @staticmethod
    def update(file_name: str, tarefa: str, campo_alvo: str, novo_valor: str, path=None) -> None:
        """
        Atualiza um campo específico de uma tarefa em um arquivo CSV.

        Args:
            file_name (str): Nome do arquivo CSV.
            tarefa (str): Nome da tarefa a ser atualizada.
            campo_alvo (str): Campo a ser atualizado ('Tarefa', 'Data' ou 'Estado').
            novo_valor (str): Novo valor para o campo.
            path (str, optional): Caminho onde salvar. Default: Desktop.
        """
        if not tarefa or not campo_alvo or not novo_valor:
            raise ValueError("Parâmetros obrigatórios não podem estar vazios")          

        full_path = CSVFile._full_path(file_name, path)

        try:
            with open(full_path, "r", newline="", encoding="utf-8") as file:
                conteudo = csv.DictReader(file, delimiter=";")
                colunas = conteudo.fieldnames
                if campo_alvo not in colunas:
                    raise ValueError(f"Campo inválido: '{campo_alvo}'.")
                linhas = list(conteudo)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Arquivo '{full_path}' não encontrado.") from e
        except Exception as e:
            raise RuntimeError(f"Erro ao abrir o arquivo '{full_path}'.") from e

        atualizado = False
        for linha in linhas:
            if linha["Tarefa"] == tarefa:
                linha[campo_alvo] = novo_valor
                atualizado = True
                break

        if not atualizado:
            raise ValueError(f"Tarefa '{tarefa}' não encontrada no arquivo.")

        try:
            with open(full_path, "w", newline="", encoding="utf-8") as file:
                escritor = csv.DictWriter(file, fieldnames=colunas, delimiter=";")
                escritor.writeheader()
                escritor.writerows(linhas)
        except Exception as e:
            raise RuntimeError(f"Erro ao atualizar o arquivo '{full_path}'.") from e
        print(f"Tarefa '{tarefa}' atualizada no campo '{campo_alvo}'.")
