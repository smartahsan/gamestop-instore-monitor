# EB Games Instore Monitor

A simple monitor that will monitor all EB Games/Gamestop CA stores in Canada for any availabity changes for a product the EB Games/Gamestop CA sell instore. The reason for developing this monitor was to be able to aid people in purchasing a PS5 from a local EB Games as due to the global chip shortage and high demand due to Covid-19 PS5s were extremely hard to find.

## Installation

To start, install the requirements, run:

```cmd
pip install -r requirements.txt
```

## Usage

- In the config.csv file add your discord webhook and a delay for each request in seconds.
- In the products.csv file add the productId of a the product you wish to monitor, this can be found in the product link. In example https://www.gamestop.ca/PS5/Games/877522 the productId being 877522. Also add the product image link which can be found on the product page.
- You can now run EbGames.py

## FAQ

#### Do I need proxies?

Not at the current time as EB Games does not ban at all almost just keep a reasonable delay. For a future extension proxy support may come.

## Screenshots

![Webhook Screenshot](https://i.imgur.com/kO2EEz9.png)

## Authors

- [@smartahsan](https://github.com/smartahsan)
- anhbro#5695 on discord
