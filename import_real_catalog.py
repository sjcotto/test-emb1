"""
Import script for real catalog data from JSON file
This script converts external catalog data into the format used by the testing framework
"""

import json
import sys
from typing import Dict, List, Any


def load_json_catalog(filepath: str) -> Dict:
    """Load catalog from JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File {filepath} not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None


def convert_catalog_format(raw_data: Any) -> Dict[str, Any]:
    """
    Convert external catalog format to our testing format

    Handles various possible input structures:
    - Direct list of products
    - Object with 'products' array
    - Nested category structure
    """

    converted = {
        'categories': {},
        'products': [],
        'metadata': {}
    }

    # Detect format and parse
    if isinstance(raw_data, list):
        # Direct list of products
        converted['products'] = parse_products_list(raw_data)
        converted['categories'] = extract_categories_from_products(converted['products'])

    elif isinstance(raw_data, dict):
        # Check for common structures
        if 'products' in raw_data:
            converted['products'] = parse_products_list(raw_data['products'])

        if 'categories' in raw_data:
            converted['categories'] = parse_categories(raw_data['categories'])

        if 'metadata' in raw_data:
            converted['metadata'] = raw_data['metadata']

        # If we got products but no categories, extract from products
        if converted['products'] and not converted['categories']:
            converted['categories'] = extract_categories_from_products(converted['products'])

    return converted


def parse_products_list(products_raw: List[Any]) -> List[Dict]:
    """Parse list of products into standardized format"""
    products = []

    for i, prod in enumerate(products_raw):
        if not isinstance(prod, dict):
            continue

        # Try to map common field names
        product = {
            'id': i + 1,  # Default ID
            'name': '',
            'description': '',
            'category': '',
            'subcategory': '',
            'price': 0,
            'tags': []
        }

        # Name variations
        for name_field in ['name', 'title', 'nombre', 'producto']:
            if name_field in prod:
                product['name'] = str(prod[name_field])
                break

        # ID variations
        for id_field in ['id', '_id', 'productId', 'product_id', 'sku']:
            if id_field in prod:
                product['id'] = prod[id_field]
                break

        # Description variations
        for desc_field in ['description', 'desc', 'descripcion', 'details']:
            if desc_field in prod:
                product['description'] = str(prod[desc_field])
                break

        # Category variations
        for cat_field in ['category', 'categoria', 'type', 'tipo']:
            if cat_field in prod:
                product['category'] = str(prod[cat_field])
                break

        # Subcategory variations
        for subcat_field in ['subcategory', 'subcategoria', 'subtype', 'subtipo']:
            if subcat_field in prod:
                product['subcategory'] = str(prod[subcat_field])
                break

        # Price variations
        for price_field in ['price', 'precio', 'cost', 'costo', 'value']:
            if price_field in prod:
                try:
                    product['price'] = float(prod[price_field])
                except (ValueError, TypeError):
                    product['price'] = 0
                break

        # Tags variations
        for tags_field in ['tags', 'etiquetas', 'keywords', 'labels']:
            if tags_field in prod:
                if isinstance(prod[tags_field], list):
                    product['tags'] = [str(t) for t in prod[tags_field]]
                elif isinstance(prod[tags_field], str):
                    product['tags'] = [t.strip() for t in prod[tags_field].split(',')]
                break

        # Additional fields that might be useful
        if 'brand' in prod or 'marca' in prod:
            brand = prod.get('brand') or prod.get('marca')
            if brand:
                product['tags'].append(f"brand:{brand}")

        if 'color' in prod:
            product['tags'].append(f"color:{prod['color']}")

        # Only add if we have at least a name
        if product['name']:
            products.append(product)

    return products


def parse_categories(categories_raw: Any) -> Dict[str, Dict]:
    """Parse categories into standardized format"""
    categories = {}

    if isinstance(categories_raw, list):
        for cat in categories_raw:
            if isinstance(cat, dict):
                name = cat.get('name') or cat.get('nombre', '')
                if name:
                    categories[name] = {
                        'subcategories': cat.get('subcategories', cat.get('subcategorias', [])),
                        'description': cat.get('description', cat.get('descripcion', ''))
                    }
            elif isinstance(cat, str):
                categories[cat] = {
                    'subcategories': [],
                    'description': ''
                }

    elif isinstance(categories_raw, dict):
        for name, data in categories_raw.items():
            if isinstance(data, dict):
                categories[name] = {
                    'subcategories': data.get('subcategories', data.get('subcategorias', [])),
                    'description': data.get('description', data.get('descripcion', ''))
                }
            elif isinstance(data, list):
                categories[name] = {
                    'subcategories': data,
                    'description': ''
                }

    return categories


def extract_categories_from_products(products: List[Dict]) -> Dict[str, Dict]:
    """Extract category structure from products"""
    categories = {}

    for product in products:
        cat = product['category']
        subcat = product['subcategory']

        if cat and cat not in categories:
            categories[cat] = {
                'subcategories': [],
                'description': ''
            }

        if cat and subcat and subcat not in categories[cat]['subcategories']:
            categories[cat]['subcategories'].append(subcat)

    return categories


def save_converted_catalog(catalog: Dict, output_file: str = 'catalog_data_real.py'):
    """Save converted catalog as Python module"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('"""\n')
        f.write('Real catalog data imported from external source\n')
        f.write('Auto-generated by import_real_catalog.py\n')
        f.write('"""\n\n')

        # Write categories
        f.write('CATEGORIES = ')
        f.write(json.dumps(catalog['categories'], indent=4, ensure_ascii=False))
        f.write('\n\n')

        # Write products
        f.write('PRODUCTS = ')
        f.write(json.dumps(catalog['products'], indent=4, ensure_ascii=False))
        f.write('\n\n')

        # Placeholder for queries (to be filled)
        f.write('# Search queries - to be customized based on your catalog\n')
        f.write('SEARCH_QUERIES = []\n')

    print(f"✓ Converted catalog saved to {output_file}")
    print(f"  - {len(catalog['categories'])} categories")
    print(f"  - {len(catalog['products'])} products")


def generate_stats(catalog: Dict):
    """Generate statistics about the imported catalog"""
    print("\n" + "="*80)
    print("CATALOG STATISTICS")
    print("="*80)

    print(f"\nTotal Categories: {len(catalog['categories'])}")
    print(f"Total Products: {len(catalog['products'])}")

    if catalog['categories']:
        print("\nCategories:")
        for cat_name, cat_data in list(catalog['categories'].items())[:10]:
            subcats = len(cat_data['subcategories'])
            print(f"  - {cat_name} ({subcats} subcategories)")

    if catalog['products']:
        print("\nSample Products:")
        for product in catalog['products'][:5]:
            print(f"  - {product['name']} (${product['price']})")
            if product['category']:
                print(f"    Category: {product['category']} > {product['subcategory']}")


def main():
    """Main import execution"""
    print("\n" + "="*80)
    print("CATALOG DATA IMPORT")
    print("="*80)

    if len(sys.argv) < 2:
        print("\nUsage: python import_real_catalog.py <catalog.json>")
        print("\nThis script will:")
        print("  1. Load your JSON catalog file")
        print("  2. Convert it to the testing framework format")
        print("  3. Save as catalog_data_real.py")
        print("\nYou can then use this with the embedding tester.")
        return

    input_file = sys.argv[1]

    # Load JSON
    print(f"\nLoading {input_file}...")
    raw_data = load_json_catalog(input_file)

    if not raw_data:
        return

    print("✓ JSON loaded successfully")

    # Convert format
    print("\nConverting to testing format...")
    catalog = convert_catalog_format(raw_data)

    # Show stats
    generate_stats(catalog)

    # Save
    print("\nSaving converted catalog...")
    save_converted_catalog(catalog)

    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("\n1. Review catalog_data_real.py to verify the data")
    print("2. Add search queries to SEARCH_QUERIES in that file")
    print("3. Update embedding_tester.py to import from catalog_data_real")
    print("4. Run: python embedding_tester.py")


if __name__ == "__main__":
    main()
