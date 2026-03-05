# eBay Scraper

[Project Instructions](https://github.com/mikeizbicki/cmc-csci040/tree/2026spring/project_02_webscraping)

This Python script scrapes eBay search results and saves the data as a JSON file (or CSV with the `--csv` flag). For each item it records the name, price, condition, shipping cost, whether free returns are offered, and how many have been sold.

## Generating the JSON files

The following commands were used to generate the 3 JSON files in this repo:

```
$ python3 ebay-dl.py lego
$ python3 ebay-dl.py 'nike shoes'
$ python3 ebay-dl.py 'vintage watch'
```

Each command downloads the first 10 pages of eBay results and saves them to a JSON file named after the search term.

## Generating the CSV files

The following commands were used to generate the 3 CSV files in this repo:

```
$ python3 ebay-dl.py lego --csv
$ python3 ebay-dl.py 'nike shoes' --csv
$ python3 ebay-dl.py 'vintage watch' --csv
```

## Optional flags

**`--num_pages`** — how many pages to scrape (default is 10):

```
$ python3 ebay-dl.py lego --num_pages 5
```

**`--csv`** — save results as a CSV file instead of JSON:

```
$ python3 ebay-dl.py lego --csv
```

## Example JSON output

```json
[
  {
    "name": "LEGO City Police Station 60316 Building Kit",
    "price": 4999,
    "status": "Brand New",
    "shipping": 0,
    "free_returns": true,
    "items_sold": 87
  },
  ...
]
```

- `price` and `shipping` are stored in **cents** (e.g. `4999` = $49.99)
- `free_returns` is a boolean
- `items_sold` is an integer, or `null` if not shown on the listing
- `status` is the item condition string from eBay (e.g. `"Pre-owned"`, `"Brand New"`)

## Files in this repo

| File | Format | Items |
| ---- | ------ | ----- |
| `lego.json` | JSON | 237 |
| `nike shoes.json` | JSON | 241 |
| `vintage watch.json` | JSON | 244 |
| `lego.csv` | CSV | 237 |
| `nike shoes.csv` | CSV | 241 |
| `vintage watch.csv` | CSV | 244 |
