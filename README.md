# Data Extraction and Authentication Project

This project is a Flask application that provides data extraction services and user authentication using JWT. It also includes Swagger documentation for API endpoints.

## Project Structure

- `app.py`: Main file that initializes the Flask application and configures the routes.
- `config/`: Contains configuration files for the application.
  - `auth.py`: Authentication-related configurations.
  - `swagger.py`: Swagger UI configuration.
- `routes/`: Contains route definitions for the application.
  - `auth.py`: Routes for user authentication.
  - `data.py`: Routes for data extraction and manipulation.
- `service/`: Contains service logic for the application.
  - `auth.py`: Service for user authentication.
  - `data_service.py`: Service for data extraction and transformation.
  - `database.py`: Service for database operations.
- `swagger.yml`: Defines the API documentation for Swagger.
- `test/`: Contains unit tests for the application.

## Requirements

- Python 3.x
- pip

## Installation

1. Clone the repository:
    ```sh
    git clone <REPOSITORY_URL>
    cd <REPOSITORY_NAME>
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
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

2. Access the application at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Tests

Unit tests are located in the `test/` folder. To run them, use the command:
```sh
pytest --cov=service
```

The coverage report will be displayed in the terminal.

## Endpoints

The API endpoints are defined in the `swagger.yml` file. Below is a summary of the main routes:

### 1. Authentication
#### POST /login
Authenticates the user and returns a JWT token.

**Request Body:**
```json
{
    "username": "admin",
    "password": "admin"
}
```

**Success Response:**
```json
{
    "access_token": "your_jwt_token"
}
```

**Error Response:**
```json
{
    "error": "Invalid credentials"
}
```

### 2. Production
#### GET /api/production
Returns production data for the specified year.

**Query Parameters (optional):**
- `year`: Year to filter the data.

**Success Response (200):**
```json
{
    "data": [...]
}
```

**Error Response (401):**
```json
{
    "error": "Unauthorized"
}
```

### 3. Commercialization
#### GET /api/commercialization
Returns commercialization data for the specified year.

**Query Parameters (optional):**
- `year`: Year to filter the data.

**Success Response (200):**
```json
{
    "data": [...]
}
```

**Error Response (401):**
```json
{
    "error": "Unauthorized"
}
```

### 4. Processing
#### GET /api/processing/vines
Returns processing data for the "Vines" resource.

#### GET /api/processing/hybrid_americans
Returns processing data for the "Hybrid Americans" resource.

#### GET /api/processing/table_grapes
Returns processing data for the "Table Grapes" resource.

#### GET /api/processing/unclassified
Returns processing data for the "Unclassified" resource.

**Query Parameters (optional):**
- `year`: Year to filter the data.

**Success Response (200):**
```json
{
    "data": [...]
}
```

**Error Response (401):**
```json
{
    "error": "Unauthorized"
}
```

### 5. Importation
#### GET /api/import/table_wines
Returns importation data for the "Table Wines" resource.

#### GET /api/import/sparkling
Returns importation data for the "Sparkling" resource.

#### GET /api/import/fresh_grapes
Returns importation data for the "Fresh Grapes" resource.

#### GET /api/import/raisins
Returns importation data for the "Raisins" resource.

#### GET /api/import/grape_juice
Returns importation data for the "Grape Juice" resource.

**Query Parameters (optional):**
- `year`: Year to filter the data.

**Success Response (200):**
```json
{
    "data": [...]
}
```

**Error Response (401):**
```json
{
    "error": "Unauthorized"
}
```

### 6. Exportation
#### GET /api/exporting/table_wines
Returns exportation data for the "Table Wines" resource.

#### GET /api/exporting/sparkling
Returns exportation data for the "Sparkling" resource.

#### GET /api/exporting/fresh_grapes
Returns exportation data for the "Fresh Grapes" resource.

#### GET /api/exporting/grape_juice
Returns exportation data for the "Grape Juice" resource.

**Query Parameters (optional):**
- `year`: Year to filter the data.

**Success Response (200):**
```json
{
    "data": [...]
}
```

**Error Response (401):**
```json
{
    "error": "Unauthorized"
}
```

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

This project is licensed under the MIT License. See the `LICENSE` file for more details.
