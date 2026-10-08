from processor import setup_logger, load_json, validate_and_filter_record, export_csv
from pathlib import Path

def process_file(
  entry_file_path: str = "solicitacoes.json",
  exit_file_path: str = "aprovados.csv"
) -> None:
  logger = setup_logger()
  logger.info("=== Início do processamento de solicitações ===")

  path_in = Path(entry_file_path)
  path_out = Path(exit_file_path)

  try:
    data = load_json(path_in, logger)
  except Exception as e:
    logger.error(f"Execução interrompida: {e}")
    logger.info("=== Processamento finalizado com erros ===")
    return

  total_read = len(data)
  approved_records = []
  total_failed = 0

  for rec in data:
    is_valid, reason =  validate_and_filter_record(rec, logger)
    if is_valid:
      approved_records.append(rec)
    else:
      total_failed += 1
      logger.warning(f"Registro ignorado -> {reason}")

  try:
    export_csv(approved_records, path_out, logger)
  except Exception as e:
    logger.error(f"Erro ao exportar dados: {e}")
    logger.info("=== Processamento finalizado com erros ===")
    return

  logger.info("=== Resumo do Processamento ===")
  logger.info(f"Total de registros lidos: {total_read}")
  logger.info(f"Total de registros aprovados: {len(approved_records)}")
  logger.info(f"Total de registros ignorados: {total_failed}")
  logger.info("=== Processamento concluído com sucesso ===")

if __name__ == "__main__":
  process_file()