# EventSync - Backend
O EventSync é uma API robusta desenvolvida em Python com FastAPI para a gestão completa de eventos. O sistema permite que organizadores criem e giram eventos, enquanto os participantes podem inscrever-se, interagir socialmente, realizar check-ins e obter certificados.

## Tecnologias Utilizadas
* Linguagem: Python 3
* Framework Web: FastAPI
* Banco de Dados: PostgreSQL
* ORM: SQLAlchemy
* Autenticação: JWT e Bcrypt
* Geração de PDF: ReportLab

## Arquitetura do Projeto
```bash
src/
├── application/      # Regras de negócio e casos de uso (Services)
├── core/             # Configurações globais e segurança (Config, Security)
├── domain/           # Modelos da base de dados e schemas Pydantic
├── infra/            # Infraestrutura (Conexão com Base de Dados)
├── persistence/      # Camada de acesso a dados (Repositories)
└── presentation/     # Camada de API (Rotas, Controllers, Middlewares)
```

## Documentação da API
* Swagger UI: http://127.0.0.1:8000/docs

## Uso de Inteligência Artificial
Foi utilizada a ferramenta Google Gemini para auxiliar na estruturação e geração de trechos de código no projeto.
