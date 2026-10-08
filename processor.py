import logging
from pathlib import Path
from typing import Any
import json
import csv


def setup_logger(log_file: str = "processamento.log") -> logging.Logger:
  """Configura o logger para registrar eventos tanto no arquivo quanto no console."""
  logger = logging.getLogger("ProcessadorSolicitacoes")
  logger.setLevel(logging.INFO)

  if logger.handlers:
    return logger

  formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
  )

  file_handler = logging.FileHandler(log_file, encoding="utf-8")
  file_handler.setFormatter(formatter)

  console_handler = logging.StreamHandler()
  console_handler.setFormatter(formatter)

  logger.addHandler(file_handler)
  logger.addHandler(console_handler)

  return logger

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

def validate_and_filter_record(record: dict[str, Any], logger: logging.Logger) -> tuple[bool, str]:
  """
  Valida as regras de negócio:
  - Presença dos campos obrigatórios (id, nome, cpf, status)
  - status == 'APROVADO'
  - CPF não nulo, não vazio e sanitizado
  """
  required_fields = {"id", "nome", "cpf", "status"}
  if not required_fields.issubset(record.keys()):
    reason = f"Registro ID {record.get('id', 'N/A')}: campos obrigatórios ausentes"
    return False, reason

  rec_id = record["id"]
  status = str(record.get("status", "")).strip().upper()
  cpf = str(record.get("cpf", "")).strip()

  clean_cpf = "".join(filter(str.isdigit, cpf))

  if status != "APROVADO":
    return False, f"ID {rec_id}: status '{status}' diferente de APROVADO"

  if not clean_cpf:
    return False, f"ID {rec_id} ({record.get('nome')}): CPF nulo ou vazio"

  record["cpf"] = clean_cpf
  return True, "Válido"

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