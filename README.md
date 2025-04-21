# Embrapa Viticulture API

This project is a Flask application that provides data extraction services and user authentication using JWT. It also includes Swagger documentation for API endpoints.

## Project Structure

```
.
├── app.py                  # Main application file
├── config/                 # Configuration files
│   ├── auth.py            # Authentication configurations
│   └── swagger.py         # Swagger UI configuration
├── routes/                 # API route definitions
│   ├── auth.py            # Authentication routes
│   ├── api_default.py     # Default API routes
│   ├── api_processing.py  # Processing data routes
│   ├── api_exporting.py   # Export data routes
│   ├── api_import.py      # Import data routes
│   └── api_routes.py      # Main API routes
├── service/                # Business logic and services
│   ├── auth.py            # Authentication service
│   ├── scrapper.py        # Web scraping service
│   ├── duck_db.py         # Database operations
│   └── extractor.py       # Data extraction service
├── test/                   # Unit tests
├── logger_serialize.py     # Logging configuration
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## Requirements

- Python 3.x
- pip
- DuckDB (for local database operations)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/ManoelSilva/embrapa-viticulture-api
    cd embrapa-viticulture-api
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv .venv
    .venv\Scripts\activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

Create a `.env` file in the project root and define the following environment variables:
```env
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
```

## Running the Application

### Development Environment:
1. Start the Flask application:
    ```sh
    flask run
    ```

2. Access the API documentation on Swagger at [http://127.0.0.1:5000/swagger](http://127.0.0.1:5000/swagger).

### Production Environment:
1. Start the application using Waitress:
    ```sh
    waitress-serve --port=8000 app:app
    ```

2. Access the application at [http://127.0.0.1:8000/swagger](http://127.0.0.1:8000).

## Tests

Unit tests are located in the `test/` folder. To run them, use the command:
```sh
pytest -cov
```

The coverage report will be displayed in the terminal.

## API Endpoints

The API provides the following endpoints:

### Authentication
- `POST /login`: Authenticates users and returns a JWT token

### Data Endpoints
- Production Data
- Commercialization Data
- Processing Data (Vines, Hybrid Americans, Table Grapes, Unclassified)
- Importation Data (Table Wines, Sparkling, Fresh Grapes, Raisins, Grape Juice)
- Exportation Data (Table Wines, Sparkling, Fresh Grapes, Grape Juice)

Each endpoint supports optional query parameters:
- `year`: Filter data by specific year

## Data Sources

The application extracts data from various sources:
- Embrapa Uva e Vinho
- IBGE (Brazilian Institute of Geography and Statistics)
- MAPA (Ministry of Agriculture, Livestock and Supply)

## Dependencies

The project dependencies are listed in the `requirements.txt` file:
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

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
