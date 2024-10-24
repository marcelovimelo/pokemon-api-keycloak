
## Demonstração do Projeto

[![Demonstração do Projeto](https://img.youtube.com/vi/oFiyGCT6P78/0.jpg)](https://youtu.be/oFiyGCT6P78)

# Pokémon API Keycloak

Este projeto é um exemplo de API protegida com o **Keycloak** usando OAuth 2.0 e autenticação via Authorization Code Flow. Ele demonstra como gerenciar identidades e permissões em uma API simulando operações no universo Pokémon.

## 🚀 Tecnologias Utilizadas

- **Python**: Backend da API  
- **Keycloak**: Gerenciamento de identidade e autenticação  
- **Postman**: Teste de requisições e geração de tokens OAuth  
- **Docker** (opcional): Para executar o Keycloak localmente  
- **Git**: Controle de versão  

---

## 📋 Pré-requisitos

- **Python 3.x**  
- **Docker** (se preferir rodar Keycloak em container)  
- **Postman** (para testar o fluxo OAuth)  

---

## 🔧 Configuração do Ambiente

### 1. Configurar Keycloak

1. Baixe e instale o **Keycloak** ou execute via Docker:
   ```bash
   docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:latest start-dev
   ```

2. Crie um **Realm** chamado `pokemon-api`.

3. Adicione um **Client**:
   - **Client ID**: `pokemon-api`  
   - **Access Type**: Public  
   - **Redirect URI**: `http://localhost:8082/*`  

4. Crie um **usuário** no Realm e atribua permissões adequadas.

---

## 📬 Solicitando Tokens com o Postman

1. Abra o Postman e crie uma nova requisição.

2. Na aba **Auth**, escolha **OAuth 2.0** como tipo.

3. Em **Configure New Token**, preencha com as informações:
   - **Auth URL**: `http://localhost:8082/realms/pokemon-api/protocol/openid-connect/auth`  
   - **Access Token URL**: `http://localhost:8082/realms/pokemon-api/protocol/openid-connect/token`  
   - **Client ID**: `pokemon-api`  
   - **Scope**: `openid`  
   - **Grant Type**: Authorization Code  
   - **Authorize using browser**: ✅

4. Clique em **Get New Access Token** e siga o fluxo de autenticação.  
   Quando retornar ao Postman, selecione **Use Token** para aplicar o token na requisição.

---

## 📝 Endpoints da API

1. **Obter o tipo de um Pokémon pelo nome**  
   - **Endpoint:** `/pokemon/type/<name>`  
   - **Método:** `GET`  
   - **Descrição:** Retorna o(s) tipo(s) de um Pokémon com base no nome fornecido. Requer que o usuário tenha o grupo de acesso `Pokemon_type_view`.

2. **Obter um Pokémon aleatório de um tipo específico**  
   - **Endpoint:** `/pokemon/random/<pokemon_type>`  
   - **Método:** `GET`  
   - **Descrição:** Retorna um Pokémon aleatório de um tipo específico (como fire, water, etc.). Requer que o usuário tenha o grupo de acesso `Pokemon_random_view`.

3. **Obter o Pokémon com o nome mais longo de um tipo específico**  
   - **Endpoint:** `/pokemon/longest-name/<pokemon_type>`  
   - **Método:** `GET`  
   - **Descrição:** Retorna o Pokémon com o nome mais longo de um tipo específico. Requer que o usuário tenha o grupo de acesso `Pokemon_advance_view`.

---

## ⚠️ Controle de Acesso

A API utiliza o **Keycloak** para controlar quem pode acessar:

- **Pokemon_type_view**: Acesso para visualizar o(s) tipo(s) de um Pokémon pelo nome.
- **Pokemon_random_view**: Acesso para obter um Pokémon aleatório de um tipo específico. 
- **Pokemon_advance_view**: Acesso para obter o Pokémon com o nome mais longo de um tipo específico.

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---
