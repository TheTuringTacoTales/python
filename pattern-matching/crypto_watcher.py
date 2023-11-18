import requests
import time
from rich.console import Console
from rich.table import Table

console = Console()

# Function to fetch real data from CoinGecko API
def fetch_crypto_data(crypto):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true"
    response = requests.get(url)
    data = response.json()[crypto]
    return {
        'name': crypto.capitalize(),
        'price': data['usd'],
        'volume': data['usd_24h_vol'],
        'market_cap': data['usd_market_cap'],
        'change_24h': data['usd_24h_change']
    }

# Enhanced mock function to simulate fetching detailed data from an API
def process_data(data):
    trend = ''
    if data['volume'] > 1000000:
        if data['change_24h'] > 0:
            trend = 'High Volume, Rising Price'
        elif data['change_24h'] < 0:
            trend = 'High Volume, Falling Price'
        else:
            trend = 'High Volume, Stable Price'
    else:
        if data['market_cap'] > 500000000:
            trend = 'Normal Volume, Large Cap'
        else:
            trend = 'Normal Volume, Small Cap'

    return trend

# Function to display data using rich library
def display_data(crypto_data):
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Cryptocurrency", style="dim")
    table.add_column("Price", justify="right")
    table.add_column("24h Change", justify="right")
    table.add_column("Trend", justify="left")

    for data in crypto_data:
        trend = process_data(data)
        table.add_row(data['name'], f"${data['price']:,}", f"{data['change_24h']}%", trend)

    console.clear()
    console.print(table)


# Function to display data using rich library
def display_data(crypto_data):
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Cryptocurrency", style="dim")
    table.add_column("Price", justify="right")
    table.add_column("24h Change", justify="right")
    table.add_column("Trend", justify="left")

    for data in crypto_data:
        trend = process_data(data)
        table.add_row(data['name'], f"${data['price']:,}", f"{data['change_24h']}%", trend)

    console.clear()
    console.print(table)

def main():
    cryptos = ['bitcoin', 'ethereum', 'litecoin']
    try:
        while True:
            crypto_data = []
            for crypto in cryptos:
                try:
                    data = fetch_crypto_data(crypto)
                    crypto_data.append(data)
                except Exception as e:
                    console.print(f"Error fetching data for {crypto}: {e}", style="bold red")
            display_data(crypto_data)
            time.sleep(30)  # Update every 30 seconds
    except KeyboardInterrupt:
        console.print("\nProgram stopped.")

if __name__ == "__main__":
    main()
