# Todo CLI App - Phase 1

## Running the Application

To run the Todo CLI application:

```bash
# Install dependencies using uv
uv sync

# Run the application directly
python -m src.cli [command]

# Or if installed as a package
todo [command]
```

## Available Commands

### Add a task
```bash
python -m src.cli add "Task Title" "Optional Description"
```

### List all tasks
```bash
python -m src.cli list
```

### Update a task
```bash
python -m src.cli update 1 --title "New Title" --description "New Description"
```

### Complete a task
```bash
python -m src.cli complete 1
```

### Delete a task
```bash
python -m src.cli delete 1
```

## Running Tests

To run the unit tests:

```bash
python -m pytest tests/test_service.py -v
```

Or to run all tests in the tests directory:

```bash
python -m pytest tests/ -v
```

## Project Structure

- `src/models.py` - Data model (Task dataclass)
- `src/repository.py` - Repository interface and in-memory implementation
- `src/service.py` - Business logic service layer (TodoService)
- `src/cli.py` - Command-line interface
- `tests/test_service.py` - Unit tests for the service layer
- `pyproject.toml` - Project dependencies and metadata