import csv
import json
import logging
from pathlib import Path
from typing import Any


def load_json(file_path: Path, logger: logging.Logger) -> list[dict[str, Any]]:
  """Lê e valida a estrutura inicial do arquivo JSON."""
  if not file_path.exists():
    logger.error(f"Arquivo não encontrado: {file_path.name}")
    raise FileNotFoundError(f"O arquivo {file_path.name} não foi encontrado")

  try:
    with open(file_path, "r", encoding="utf-8") as file:
      data = json.load(file)
      if not isinstance(data, list):
        logger.error("Formato JSON invélido: o conteúdo raiz deve ser uma lista")
        raise TypeError("O JSON precisa ser uma lista de registros")
      return data
  except json.JSONDecodeError as e:
    logger.error(f"Erro de sintaxe no JSON: {e}")
    raise ValueError(f"O arquivo {file_path.name} contém um JSON inválido")

def export_csv(
  records: list[dict[str, Any]],
  exit_path: Path,
  logger: logging.Logger
) -> None:
  """Gera o arquivo CSV em UTF-8 com os registros aprovados."""
  fields = ["id", "nome", "cpf"]

  try:
    with open(exit_path, mode="w", newline="", encoding="utf-8") as file:
      writer = csv.DictWriter(
        file, fieldnames=fields, delimiter=";", extrasaction="ignore"
      )
      writer.writeheader()
      writer.writerows(records)
    logger.info(f"Arquivo CSV '{exit_path.name}' gerado com sucesso")
  except Exception as e:
    logger.error(f"Falha ao gerar arquivo CSV: {e}")
    raise IOError(f"Não foi possível salvar o CSV: {e}")