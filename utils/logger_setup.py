import logging
from pathlib import Path


def setup_logger(log_file: str = "logs/processamento.log") -> logging.Logger:
  """Configura o logger para registrar eventos tanto no arquivo quanto no console."""
  logger = logging.getLogger("ProcessadorSolicitacoes")
  logger.setLevel(logging.INFO)

  if logger.handlers:
    return logger

  formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
  )

  log_path = Path(log_file)
  log_path.parent.mkdir(parents=True, exist_ok=True)

  file_handler = logging.FileHandler(log_file, encoding="utf-8")
  file_handler.setFormatter(formatter)

  console_handler = logging.StreamHandler()
  console_handler.setFormatter(formatter)

  logger.addHandler(file_handler)
  logger.addHandler(console_handler)

  return logger