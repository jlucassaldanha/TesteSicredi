import json
import unittest
from pathlib import Path

from core_processor import validate_and_filter_record
from file_processor import export_csv, load_json
from logger_setup import setup_logger

class TestProcessadorSolicitacoes(unittest.TestCase):
  def setUp(self):
    self.logger = setup_logger("test_execucao.log")

  def test_validacao_registro_aprovado_valido(self):
    rec = {"id": 1, "nome": "Maria Silva", "cpf": "123.456.789-00", "status": "APROVADO"}
    is_valid, reason = validate_and_filter_record(rec)
    self.assertTrue(is_valid)
    self.assertEqual(rec['cpf'], '12345678900')

  def test_validacao_status_pendente(self):
    rec = {"id": 1, "nome": "Maria Silva", "cpf": "123.456.789-00", "status": "PENDENTE"}
    is_valid, reason = validate_and_filter_record(rec)
    self.assertFalse(is_valid)

  def test_validacao_cpf_vazio(self):
    rec = {"id": 1, "nome": "Maria Silva", "cpf": "", "status": "APROVADO"}
    is_valid, reason = validate_and_filter_record(rec)
    self.assertFalse(is_valid)

  def test_json_nao_encontrado(self):
    with self.assertRaises(FileNotFoundError):
      load_json(Path("arquivo_que_nao_existe.json"), self.logger)

  def test_validacao_campos_ausentes(self):
    rec = {"id": 1, "nome": "Maria Silva", "cpf": "123.456.789-00"}
    is_valid, reason = validate_and_filter_record(rec)
    self.assertFalse(is_valid)
    self.assertIn("campos obrigatórios ausentes", reason)

  def test_json_sintaxe_invalida(self):
    path_corrupted = Path("corrompido.json")
    with open(path_corrupted, "w", encoding="utf-8") as file:
      file.write("{ json_invalido: true ")

    with self.assertRaises(ValueError):
      load_json(path_corrupted, self.logger)

    if path_corrupted.exists():
      path_corrupted.unlink()

if __name__ == "__main__":
  unittest.main()