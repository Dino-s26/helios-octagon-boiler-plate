## How to use the script

1. Install requirement library on `requirements.txt`, use:

```
pip install -r requirements.txt 
```

2. There are 2 Scripts, `data-scrape-elasticache.py` and `elasticache-exporter.py`

> `data-scrape-elasticache.py` will be use to scrape all the data collected on `.json` format that already collected with `elasticache-exporter.py` and transform it into `.xlsx` format

> `elasticache-exporter.py` will be use to colled the elasticache cluster and all the configuration and export it into `.json` format


3. To use :

> 3.1. Run the `python3 elasticache-exporter.py` to get the elasticache cluster information, make sure you have aws-vault configure as it require it to check your existing profile to login

> 3.2. Once done, run `python3 data-scrape-elasicache.py` to transform the data into `.xlsx` file to be check later on

> 3.3. Done, you can check the data in the `.xlsx` format

