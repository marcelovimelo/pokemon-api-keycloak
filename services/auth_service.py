from keycloak import KeycloakOpenID
from flask import request, jsonify
import os

# Configuração do Keycloak
keycloak_openid = KeycloakOpenID(
    server_url="http://localhost:8082/",
    client_id="pokemon-api",
    realm_name="pokemon-api",
    client_secret_key=os.getenv("KEYCLOAK_CLIENT_SECRET"),
)

def get_public_key():
    public_key = keycloak_openid.public_key()
    return f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"

def verify_token():
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return jsonify({"message": "Token não fornecido!"}), 401

    try:
        token = token.split(" ")[1]
        key = get_public_key()
        user_info = keycloak_openid.decode_token(token, key, algorithms=["RS256"])
        return user_info
    except Exception as e:
        return jsonify({"message": "Token inválido!", "error": str(e)}), 401
