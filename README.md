# Meteo Updater

This Python script fetches daily meteorological data from the AEMET Open Data API and updates a local CSV file with the latest information. It is designed to be used with GitHub Actions for automated daily updates.

## Features

- Retrieves daily climate data for the last 30 days from AEMET.
- Appends new data to `datos_meteorologicos.csv`.
- Removes duplicate entries based on the date.
- Can be scheduled to run automatically using GitHub Actions.

## Requirements

- Python 3.10 or higher
- `requests` library
- `pandas` library

Install dependencies with:

```
pip install -r requirements.txt
```

## Usage

Run the script manually:

```
python src/update_meteo.py
```

Or set up the provided GitHub Actions workflow to run it automatically every day at 09:00 UTC.

## Configuration

- Make sure to set your AEMET API key in the script (`api_key` field).
- The output CSV file (`datos_meteorologicos.csv`) will be created or updated in the same directory as the script.

## License

This project is licensed under MIT License
