[English version](README.md)

# Embrapa Viticulture API

Este projeto é uma aplicação Flask que fornece serviços de extração de dados e autenticação de usuários usando JWT. Também inclui documentação Swagger para os endpoints da API.

## Estrutura do Projeto

```
.
├── src/                    # Código-fonte principal
│   ├── app.py                  # Arquivo principal da aplicação
│   ├── config/                 # Arquivos de configuração
│   │   ├── auth.py            # Configurações de autenticação
│   │   └── swagger.py         # Configuração do Swagger UI
│   ├── routes/                 # Definições das rotas da API
│   │   ├── auth.py            # Rotas de autenticação
│   │   ├── api_default.py     # Rotas padrão da API
│   │   ├── api_processing.py  # Rotas de processamento de dados
│   │   ├── api_exporting.py   # Rotas de exportação de dados
│   │   ├── api_import.py      # Rotas de importação de dados
│   │   └── api_routes.py      # Rotas principais da API
│   ├── service/                # Lógica de negócio e serviços
│   │   ├── auth.py            # Serviço de autenticação
│   │   ├── scrapper.py        # Serviço de web scraping
│   │   ├── duck_db.py         # Operações de banco de dados
│   │   └── extractor.py       # Serviço de extração de dados
│   ├── logger_serialize.py     # Configuração de logging
└── test/                   # Testes unitários
├── requirements.txt        # Dependências do projeto
└── README.md              # Documentação do projeto
```

## Requisitos

- Python 3.x
- pip
- DuckDB (para operações locais de banco de dados)

## Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/ManoelSilva/embrapa-viticulture-api
    cd embrapa-viticulture-api
    ```

2. Crie e ative um ambiente virtual:
    ```sh
    python -m venv .venv
    .venv\Scripts\activate
    ```

3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

## Configuração

Crie um arquivo `.env` na raiz do projeto e defina as seguintes variáveis de ambiente:
```env
SECRET_KEY=sua_chave_secreta
JWT_SECRET_KEY=sua_jwt_secreta
```

## Executando a Aplicação

### Ambiente de Desenvolvimento:
1. Inicie a aplicação Flask:
    ```sh
    flask run
    ```

2. Acesse a documentação da API no Swagger em [http://127.0.0.1:5000/swagger](http://127.0.0.1:5000/swagger).

### Ambiente de Produção:
1. Inicie a aplicação usando o Waitress:
    ```sh
    waitress-serve --port=8000 app:app
    ```

2. Acesse a aplicação em [http://127.0.0.1:8000/swagger](http://127.0.0.1:8000).

## Testes

Os testes unitários estão localizados na pasta `test/`. Para executá-los, utilize o comando:
```sh
pytest -cov
```

O relatório de cobertura será exibido no terminal.

## Endpoints da API

A API fornece os seguintes endpoints:

### Autenticação
- `POST /login`: Autentica usuários e retorna um token JWT

### Endpoints de Dados
- Dados de Produção
- Dados de Comercialização
- Dados de Processamento (Vinhas, Híbridos Americanos, Uvas de Mesa, Não Classificados)
- Dados de Importação (Vinhos de Mesa, Espumantes, Uvas Frescas, Passas, Suco de Uva)
- Dados de Exportação (Vinhos de Mesa, Espumantes, Uvas Frescas, Suco de Uva)

Cada endpoint suporta parâmetros de consulta opcionais:
- `year`: Filtra dados por ano específico

## Fontes de Dados

A aplicação extrai dados de várias fontes:
- Embrapa Uva e Vinho
- IBGE (Instituto Brasileiro de Geografia e Estatística)
- MAPA (Ministério da Agricultura, Pecuária e Abastecimento)

## Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt`:
- Flask
- Flask-JWT-Extended
- Flask-Swagger-UI
- requests
- BeautifulSoup4
- lxml
- pandas
- numpy
- pytest
- coverage
- loguru
- duckdb
- waitress

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contribuindo

1. Faça um fork do repositório
2. Crie sua branch de feature (`git checkout -b feature/SuaFeatureIncrivel`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona SuaFeatureIncrivel'`)
4. Faça push para a branch (`git push origin feature/SuaFeatureIncrivel`)
5. Abra um Pull Request 