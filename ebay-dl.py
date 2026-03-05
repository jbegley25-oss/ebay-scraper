import argparse
import requests
from bs4 import BeautifulSoup
import json
import csv


def parse_price(text):
    '''
    Takes a price string from eBay and returns the price in cents as an integer.
    Returns None if the price cannot be parsed.

    >>> parse_price('$12.99')
    1299
    >>> parse_price('$1,299.00')
    129900
    >>> parse_price('$0.99 to $39.99')
    99
    >>> parse_price('Tap item to see current priceSee price')

    '''
    if not text or text[0] != '$':
        return None
    numbers = ''
    for c in text[1:]:
        if c in '0123456789':
            numbers += c
        elif c == ' ':
            break
    if numbers:
        return int(numbers)
    return None


def parse_shipping(text):
    '''
    Takes a shipping string from eBay and returns the shipping cost in cents.
    Returns 0 for free shipping.

    >>> parse_shipping('Free shipping')
    0
    >>> parse_shipping('+$4.99 shipping')
    499
    >>> parse_shipping('+$12.50 shipping')
    1250
    '''
    if 'free' in text.lower():
        return 0
    numbers = ''
    for c in text:
        if c in '0123456789':
            numbers += c
        elif c == ' ' and numbers:
            break
    if numbers:
        return int(numbers)
    return 0


def parse_items_sold(text):
    '''
    Takes a string like "872 sold" and returns the number as an integer.
    Returns None if the string does not mention items sold.

    >>> parse_items_sold('872 sold')
    872
    >>> parse_items_sold('2 watchers')

    >>> parse_items_sold('Almost gone')

    '''
    numbers = ''
    for c in text:
        if c in '0123456789':
            numbers += c
    if 'sold' in text and numbers:
        return int(numbers)
    return None


if __name__ == '__main__':

    # get command line arguments
    parser = argparse.ArgumentParser(description='Download eBay search results and save as JSON (or CSV).')
    parser.add_argument('search_term', help='the term to search for on eBay')
    parser.add_argument('--num_pages', default=10, type=int, help='number of pages to scrape (default 10)')
    parser.add_argument('--csv', action='store_true', help='save results as CSV instead of JSON')
    args = parser.parse_args()

    print(f'args.search_term= {args.search_term}')

    items = []

    for page_number in range(1, args.num_pages + 1):
        print(f'scraping page {page_number}...')

        url = (
            'https://www.ebay.com/sch/i.html?_from=R40&_nkw='
            + args.search_term.replace(' ', '+')
            + '&_sacat=0&LH_TitleDesc=0&_pgn='
            + str(page_number)
            + '&rt=nc'
        )

        r = requests.get(url)
        html = r.text

        soup = BeautifulSoup(html, 'html.parser')
        tags_items = soup.select('.s-item')

        # skip the first result — eBay inserts a fake "Shop on eBay" placeholder
        for tag_item in tags_items[1:]:

            # name
            name = None
            for tag in tag_item.select('.s-item__title'):
                name = tag.text

            # price
            price = None
            for tag in tag_item.select('.s-item__price'):
                price = parse_price(tag.text)

            # condition / status
            status = None
            for tag in tag_item.select('.SECONDARY_INFO'):
                status = tag.text

            # shipping
            shipping = None
            for tag in tag_item.select('.s-item__shipping, .s-item__freeXDays'):
                shipping = parse_shipping(tag.text)

            # free returns
            free_returns = False
            for tag in tag_item.select('.s-item__free-returns'):
                free_returns = True

            # items sold
            items_sold = None
            for tag in tag_item.select('.s-item__hotness, .s-item__additionalItemHotness'):
                items_sold = parse_items_sold(tag.text)

            item = {
                'name': name,
                'price': price,
                'status': status,
                'shipping': shipping,
                'free_returns': free_returns,
                'items_sold': items_sold,
            }
            items.append(item)

    print(f'total items scraped: {len(items)}')

    # save output
    if args.csv:
        filename = args.search_term + '.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'price', 'status', 'shipping', 'free_returns', 'items_sold'])
            writer.writeheader()
            writer.writerows(items)
        print(f'saved to {filename}')
    else:
        filename = args.search_term + '.json'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(items, indent=2))
        print(f'saved to {filename}')
