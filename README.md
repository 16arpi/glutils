# glutils

Small lib for very useful things in Python specially built for my own needs.

## Enricher

A csv enricher built on top of `DictReader` and `DictWriter`. Allows user to add new columns to a csv file while iterating through its rows.

### Usage

```python
import requests

from glutils import Enricher

with Enricher(["status", "size"], keep_old_header=True) as enricher:
    for row in enricher:
        url = row["url"]
        response = requests.get(url)
        status = response.status_code
        size = len(response.text)

        enricher.writerow({
            "status": status,
            "size": size
        })
```

Execute with :

```bash
$ python script.py < urls.csv > result.csv
```

### Arguments

- **fieldnames** *List[str]*: fieldnames of the columns to add.
- **source** *TextIO* `sys.stdin`: the the stream of the csv source, stdin by default.
- **export** *TextIO* `sys.stdout`: the the stream of the csv target, stdout by default.
- **keep_old_header** *boolean* `False`: whether the source fieldnames must be explicitly declared for new rows.



