import requests
import time
from rich.console import Console
from rich.table import Table

console = Console()

def fetch_crypto_data(crypto):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true"
    response = requests.get(url)
    data = response.json()
    return data[crypto]

def process_data(data):
    match data:
        case {"usd": price, "usd_market_cap": market_cap, "usd_24h_vol": volume, "usd_24h_change": change} if volume > 1000000:
            trend = "High Volume"
        case {"usd": price, "usd_market_cap": market_cap, "usd_24h_vol": volume, "usd_24h_change": change} if market_cap > 500000000:
            trend = "Large Market Cap"
        case {"usd": price, "usd_market_cap": market_cap, "usd_24h_vol": volume, "usd_24h_change": change}:
            trend = "Standard"
        case _:
            trend = "Data Unavailable"
    return data["usd"], trend

def display_data(crypto_data):
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Cryptocurrency", style="dim")
    table.add_column("Price", justify="right")
    table.add_column("Trend", justify="left")

    for name, (price, trend) in crypto_data.items():
        table.add_row(name.capitalize(), f"${price:,.2f}", trend)

    console.clear()
    console.print(table)

def main():
    cryptos = ['bitcoin', 'ethereum', 'litecoin']
    try:
        while True:
            crypto_data = {}
            for crypto in cryptos:
                try:
                    data = fetch_crypto_data(crypto)
                    processed_data = process_data(data)
                    crypto_data[crypto] = processed_data
                except Exception as e:
                    console.print(f"Error fetching data for {crypto}: {e}", style="bold red")
            display_data(crypto_data)
            time.sleep(60)  # Update every minute
    except KeyboardInterrupt:
        console.print("\nProgram stopped.")

if __name__ == "__main__":
    main()
