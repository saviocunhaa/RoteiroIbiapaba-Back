# Documentação do Backend - Roteiro Ibiapaba

## 1. Visão Geral do Projeto
O **Roteiro Ibiapaba** é um sistema web que permite aos usuários visualizar pontos turísticos da região da Serra da Ibiapaba, no Ceará. Usuários autenticados podem favoritar locais e gerenciar suas preferências. O backend será desenvolvido utilizando **Django REST Framework (DRF)**, com banco de dados **PostgreSQL** e autenticação JWT.

## 2. Tecnologias Utilizadas
- **Linguagem:** Python 3.x
- **Framework:** Django + Django REST Framework (DRF)
- **Banco de Dados:** PostgreSQL
- **Autenticação:** JWT (JSON Web Token)
- **Implantação:** Docker + AWS/GCP
- **Documentação da API:** Swagger/ReDoc

## 3. Requisitos do Sistema
### 3.1 Requisitos Funcionais (RF)
#### Módulo de Usuário
- **RF001**: O sistema deve permitir o cadastro de usuários.
- **RF002**: O sistema deve permitir que usuários se autentiquem via JWT.
- **RF003**: O usuário pode atualizar seu perfil (nome, email, foto, etc.).
- **RF004**: O sistema deve permitir a recuperação de senha via email.

#### Módulo de Pontos Turísticos
- **RF005**: O sistema deve permitir o cadastro de pontos turísticos com informações como nome, descrição, cidade, localização (latitude/longitude), imagens e categoria.
- **RF006**: Os usuários devem conseguir visualizar uma lista de pontos turísticos.
- **RF007**: O sistema deve permitir a busca e filtrar pontos turísticos por nome, categoria, cidade ou localização.
- **RF008**: O sistema deve permitir a visualização dos detalhes de um ponto turístico.
- **RF009**: O sistema deve permitir inserir, editar e remover pontos turísticos (somente admin).

#### Módulo de Favoritos
- **RF010**: Usuários autenticados podem favoritar pontos turísticos.
- **RF011**: O sistema deve permitir listar todos os pontos favoritados por um usuário.
- **RF012**: O usuário pode remover um ponto turístico de sua lista de favoritos.

### 3.2 Requisitos Não Funcionais (RNF)
- **RNF001**: O sistema deve ser responsivo e escalável.
- **RNF002**: O backend deve garantir a segurança dos dados dos usuários.
- **RNF003**: As respostas da API devem ser retornadas em formato JSON.
- **RNF004**: A API deve seguir os padrões RESTful.
- **RNF005**: O tempo de resposta das requisições não deve ultrapassar 500ms em condições normais de uso.

## 4. Modelagem do Banco de Dados
### 4.1 Modelos Principais
#### Usuário (`User`)
- `id`: UUID
- `nome`: string
- `email`: string (único)
- `senha`: hash
- `foto`: URL
- `data_criacao`: timestamp

#### Ponto Turístico (`TouristSpot`)
- `id`: UUID
- `nome`: string
- `descrição`: string
- `cidade`: string
- `localização`: latitude/longitude
- `categoria`: string
- `imagens`: lista de URLs
- `data_criacao`: timestamp

#### Favoritos (`Favorite`)
- `id`: UUID
- `usuario`: FK para `User`
- `ponto_turistico`: FK para `TouristSpot`
- `data_adicionado`: timestamp

## 5. Endpoints da API
### 5.1 Autenticação
| Método | Endpoint | Descrição |
|---------|----------|------------|
| POST | `/api/auth/signup/` | Cadastra um novo usuário |
| POST | `/api/auth/login/` | Autentica usuário e retorna JWT |
| POST | `/api/auth/logout/` | Encerra a sessão do usuário |
| POST | `/api/auth/password-reset/` | Solicita redefinição de senha |

### 5.2 Pontos Turísticos
| Método | Endpoint | Descrição |
|---------|----------|------------|
| GET | `/api/tourist-spots/` | Lista pontos turísticos |
| POST | `/api/tourist-spots/` | Cria um ponto turístico (Admin) |
| GET | `/api/tourist-spots/{id}/` | Exibe detalhes de um ponto turístico |
| PUT | `/api/tourist-spots/{id}/` | Atualiza um ponto turístico (Admin) |
| DELETE | `/api/tourist-spots/{id}/` | Remove um ponto turístico (Admin) |

### 5.3 Favoritos
| Método | Endpoint | Descrição |
|---------|----------|------------|
| POST | `/api/favorites/` | Adiciona um ponto turístico aos favoritos |
| GET | `/api/favorites/` | Lista os pontos turísticos favoritados |
| DELETE | `/api/favorites/{id}/` | Remove um favorito |

## 6. Regras de Negócio
- Apenas usuários autenticados podem favoritar pontos turísticos.
- Apenas administradores podem adicionar, editar ou remover pontos turísticos.
- Um ponto turístico não pode ser adicionado mais de uma vez na lista de favoritos de um usuário.
- O sistema deve validar se um ponto turístico existe antes de permitir favoritá-lo.

## 7. Considerações Finais
Este documento serve como base para o desenvolvimento do backend do **Roteiro Ibiapaba**. Durante a implementação, ajustes podem ser necessários conforme feedback e testes do sistema. O próximo passo é iniciar o desenvolvimento do backend conforme esta documentação.

