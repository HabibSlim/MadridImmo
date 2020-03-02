# MadridImmo
Webscraping of house prices in Madrid, using Python and BeautifulSoup

# Dependencies
Below are the dependencies needed to run the project:

- `pandas`
- `BeautifulSoup`
- `fake_headers`

# Usage
After installing dependencies, the script can be run with:

`python3 main.py [options]`

Positional arguments:

- `name`: website to scrape (`pisos`, `tucasa` or `habitaclia`).
- `type`: type of dwellings to target (`houses` or `flats`).

Example:

`python3 main.py pisos houses`

# Example dataset
Some extracted data can be found in the folder `/dataset` (~30.000 entries in total).