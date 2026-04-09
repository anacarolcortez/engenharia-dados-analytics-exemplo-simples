from pydantic import BaseModel, Field
from typing import Optional

class Processo(BaseModel):
    numero_processo: str = Field(..., description="Número único do processo")
    assunto_codigo: Optional[int] = None
    assunto: Optional[str] = None
    jurisdicao: Optional[str] = None
    orgao_nome: Optional[str] = None
    classe_judicial: Optional[str] = None
    estado: Optional[str] = Field(None, min_length=2, max_length=2)
    status: Optional[str] = None
    ano_distribuicao: Optional[int] = None
    ano_ultima_movimentacao: Optional[int] = None
    tempo_processo_dias: Optional[float] = None
    finalizado: bool = False
    qtd_partes_ativas: int = 0
    tipo_parte_passiva: Optional[str] = None
    empresa_nome: Optional[str] = None
    empresa_cnpj: Optional[str] = None
    tem_advogado: bool = False

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "numero_processo": "10092185920174013400",
                "assunto": "DIREITO TRIBUTÁRIO",
                "finalizado": True
            }
        }
    }