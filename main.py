import datetime
import csv
import os
from typing import Any

# São duas classes nesse arquivo: Plano e CSVFile
# Para usar essa biblioteca:

# 1º. deve-se instanciar um objeto da classe Plano ---> Ex: plano1 = Plano()
# 2º. Em seguida, usa-se o metodo ".add" para adicionar as tarefas. Elas podem ser adicionadas de 3 formas:
# String padrão --> Ex: plano1.add("Prova de Python", "24/12/2025")
# Tupla (armezando em uma variavel e depois adicionar ela)---> Ex: tarefa = ("Prova de Java", "21/04/2003") -->  plano1.add(tarefa)
# Lista de tuplas ---> lista = [("Prova de Calculo", "12/12/2012"), ("Trabalho 1", "13/13/2013")....]

# 3º. Depois de adicionadas as tarefas, usamos a classe CSVFile com o metodo ".create" para criar o arquivo --->
# Ex: CSVFile.create(nome_arquivo, nome_plano, caminho_arquivo)  Obs: O caminho do arquivo é opcional, então não precisa passar ele

# 4º. Para atualizar o arquivo, usa-se o metodo ".update" --->
# Ex: CSVFile.update(nome_arquivo, nome_tarefa, campo_alvo, novo_valor, caminho_arquivo) Obs: caminho do arquivo é opcional

# Falta fazer os metodos insert e remove/delete do CSVFile
# Provavel que tenha como juntar os metodos update_date e update_state em 1 metodo só, talvez eu faça outra hora

class Plano:
    def __init__(self):
        self._tarefas = []

    def formata_data(self, data: str | None) -> datetime.date | None:
        if not data:
            return None
        return datetime.datetime.strptime(data, "%d/%m/%Y").date()

    def add(self, tarefa: Any, *args) -> None:
        estado = "Incompleto"
        if isinstance(tarefa, tuple):
            nome, data= tarefa
            self._tarefas.append({
                "nome": nome,
                "data": self.formata_data(data),
                "estado": estado,
            })
        elif isinstance(tarefa, str):
            data = self.formata_data(args[0]) if args else None
            self._tarefas.append({
                "nome": tarefa,
                "data": data,
                "estado": estado,
            })
        elif isinstance(tarefa, list):
            for nome, data in tarefa:
                self._tarefas.append({
                    "nome": nome,
                    "data": self.formata_data(data),
                    "estado": estado,
                })

    def get(self) -> list[dict[str, Any]]:
        return self._tarefas

    def find(self, nome: str) -> int | None:
        for i, tarefa in enumerate(self._tarefas):
            if tarefa["nome"] == nome:
                return i
        return None

    def remove(self, nome: str) -> bool:
        indice = self.find(nome)
        if indice is not None:
            self._tarefas.pop(indice)
            return True
        return False

    def update_date(self, nome: str, nova_data: str) -> bool:
        indice = self.find(nome)
        if indice is None:
            return False
        self._tarefas[indice]["data"] = self.formata_data(nova_data)
        return True

    def update_state(self, nome: str, novo_estado: str) -> bool:
        indice = self.find(nome)
        if indice is None:
            return False
        self._tarefas[indice]["estado"] = novo_estado
        return True


class CSVFile:
    @staticmethod
    def create(file_name: str, plano: Plano, path=None) -> None:
        if path is None:
            path = os.path.join(os.path.expanduser("~"), "Desktop")
        full_path = os.path.join(path, file_name)
        with open(full_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["Tarefa", "Data", "Estado"])
            for tarefa in plano.get():
                data_str = tarefa["data"].strftime("%d/%m/%Y") if tarefa["data"] else ""
                writer.writerow([tarefa["nome"], data_str, tarefa["estado"]])

    @staticmethod
    def insert(file_name: str, tarefa: str, data: str, estado: str = "Incompleto", path=None):
        if path is None:
            path = os.path.join(os.path.expanduser("~"), "Desktop")
        full_path = os.path.join(path, file_name)
        #FALTA TERMINAR

    @staticmethod
    def remove(file_name: str, tarefa: str, path=None):
        if path is None:
            path = os.path.join(os.path.expanduser("~"), "Desktop")
        full_path = os.path.join(path, file_name)
        #FALTA TERMINAR

    @staticmethod
    def update(file_name: str, tarefa: str, campo_alvo: str, novo_valor: str, path=None):
        if path is None:
            path = os.path.join(os.path.expanduser("~"), "Desktop")
        full_path = os.path.join(path, file_name)

        linhas = []
        with open(full_path, mode="r", newline="", encoding="utf-8") as file:
            conteudo = csv.DictReader(file, delimiter=";")
            colunas = conteudo.fieldnames
            for linha in conteudo:
                linhas.append(linha)

        for linha in linhas:
            if linha["Tarefa"] == tarefa:
                linha[campo_alvo] = novo_valor
                break

        with open(full_path, mode="w", newline="", encoding="utf-8") as file:
            escritor = csv.DictWriter(file, fieldnames=colunas, delimiter=";")
            escritor.writeheader()
            escritor.writerows(linhas)

