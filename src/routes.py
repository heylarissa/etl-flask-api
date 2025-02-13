from flask import Blueprint, jsonify
from utils.utils import load_types

api_bp = Blueprint("api", __name__)

# Carregar os tipos na memória para evitar leituras repetidas
TYPES_DATA = load_types()


@api_bp.route("/tipo/<int:tipo_id>", methods=["GET"])
def get_tipo(tipo_id):
    """Retorna o nome do tipo baseado no ID informado."""
    tipo_nome = TYPES_DATA.get(tipo_id)

    if tipo_nome:
        return jsonify({"id": tipo_id, "nome": tipo_nome})
    return jsonify({"error": "Tipo não encontrado"}), 404
