from typing import Any


def validate_and_filter_record(record: dict[str, Any]) -> tuple[bool, str]:
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

