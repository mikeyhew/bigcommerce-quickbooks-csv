import bigcommerce
import os
import decimal
decimal.getcontext().prec = 2
from decimal import Decimal
import csv

api = bigcommerce.api.BigcommerceApi(
    host=os.environ['BIGCOMMERCE_HOST'],
    basic_auth=(os.environ['BIGCOMMERCE_USER'],
                os.environ['BIGCOMMERCE_APIKEY']))

print('Testing BigCommerce Api - if your credentials check out,')
print('the next line should be the time')
print(repr(api.Time.all()))
print()

# Helper function for finding an element in a list or other iteratable object.
# @param iterable
# @param {Function} predicate - a function that is given an element from the 
#                   list and returns true if it is in the list.
def find(iterable, predicate):
    for el in iterable:
        if predicate(el):
            return el
    raise LookupError

productsCount = api.Products.count()
productsLeft = productsCount
print("Downloading {} products".format(productsCount))
products = []
page=1
while productsLeft > 0:
    products += api.Products.all(limit=200, page=page)
    productsLeft -= 200
    page += 1

print("Successfully downloaded {} products".format(len(products)))

outfile = open('./output.csv', 'w')
fieldnames = ['Product/Service Name',
              'Sales Description',
              'Sales Price/Rate',
              'Income Account',
              'Purchase Description',
              'Purchase Cost',
              'Expense Account',
              'Inventory Asset Account',
              'Quantity On Hand',
              'Quantity as-of Date']
              
csvwriter = csv.DictWriter(outfile, fieldnames, delimiter=',')
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
def recordVariant(variant):
    csvwriter.writerow(variant)


for product in products:
    if (not product.is_visible) or product.availability == 'disabled':
        continue
    variant = dict()
    variant['Sales Description'] = product.name
    variant['Purchase Description'] = variant['Sales Description']
    variant['Sales Price/Rate'] = Decimal(product.price)
    sale_price = Decimal(product.sale_price)
    if sale_price > 0:
        variant["Sales Price/Rate"] = sale_price    
    
    skus = product.skus()
    if isinstance(skus, list):
        print('Product "{}" has option skus. Will create multiple variants for this product.'.format(product.name))
        options = product.options()
        for option in options:
            option.vals = api.OptionValues.all(option.option_id)
        variantToClone = variant
        for sku in skus:
            variant = dict(variantToClone)
            variant['Product/Service Name'] = sku.sku
            
            for optDict in sku.options:
                option_id = optDict['product_option_id']
                value_id = optDict['option_value_id']
                option = find(options, lambda option: option.id == option_id)
                value = find(option.vals, lambda value: value['id'] == value_id)
                variant['Sales Description'] += '\n' + option.display_name + ': ' + value['value']
            variant['Purchase Description'] = variant['Sales Description']
            recordVariant(variant)
    else:
        print('Product "{}" does not have option skus. Will create a single variant for this product.'.format(product.name))
        variant['Product/Service Name'] = product.sku
        recordVariant(variant)

outfile.close()