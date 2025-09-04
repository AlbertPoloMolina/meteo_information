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

Copyright 2025, Albert Polo

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
