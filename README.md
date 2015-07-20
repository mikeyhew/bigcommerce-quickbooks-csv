# bigcommerce-quickbooks-csv

A python script that connects to a BigCommerce Store's API and creates a .csv file of the products in the store, for importing into Quickbooks Online.

This program was written specifically for use with a certain BigCommerce store, and will probably not work for any other store. You will probably have to edit the script for your specific use case. Here are some assumptions it makes:

- Note: this list is not exhaustive. You should look at the source and see what you need to change.
- Only visible products (ie: products that haven't been deliberately hidden) are added to the csv file.
- All products to be added should have either a main sku or options skus.
- If a product doesn't have any options skus defined, then a single variant will be added to the .csv file, with that product's sku as the product name and the product's name as the description.
- If a product has option skus, a separate variant will be added for each sku, with the sku as the product name and the product name + selected options as the description. (A newline (\n) will be added before each "optionname: optionvalue")
- The script assumes that each variant of a given product will be the same price.

## Usage

This script was written for Python 3.4. You can install python and pip at [python.org/downloads](https://www.python.org/downloads/).

Install the Bigcommerce Api Client Library for Python:
```bash
pip3 install bigcommerce
```

Run the script, passing your bigcommerce store's credentials as environment variables.
```bash
BIGCOMMERCE_HOST='mybigcommercestore.com' \
BIGCOMMERCE_USER='admin' \
BIGCOMMERCE_APIKEY='myapikey' \
python3 main.py
```
Import the output file, "output.csv", to Quickbooks Online (outside of the scope of this ReadMe).