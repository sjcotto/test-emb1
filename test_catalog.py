"""
Quick test script to verify catalog data and show sample queries
Run this to verify the setup without downloading embedding models
"""

from catalog_data import CATEGORIES, PRODUCTS, SEARCH_QUERIES
import json


def print_section(title: str):
    """Print formatted section header"""
    print("\n" + "="*80)
    print(title)
    print("="*80)


def show_catalog_stats():
    """Display catalog statistics"""
    print_section("CATALOG STATISTICS")

    print(f"\nTotal Products: {len(PRODUCTS)}")
    print(f"Total Main Categories: {len(CATEGORIES)}")

    # Count subcategories
    total_subcats = sum(len(cat['subcategories']) for cat in CATEGORIES.values())
    print(f"Total Subcategories: {total_subcats}")

    print("\nMain Categories:")
    for cat_name, cat_data in CATEGORIES.items():
        print(f"  - {cat_name} ({len(cat_data['subcategories'])} subcategories)")


def show_sample_products():
    """Display sample products"""
    print_section("SAMPLE PRODUCTS")

    # Show a few products from different categories
    categories_shown = set()
    products_shown = 0

    for product in PRODUCTS:
        if product['category'] not in categories_shown and products_shown < 10:
            print(f"\n{product['name']}")
            print(f"  Category: {product['category']} > {product['subcategory']}")
            print(f"  Price: ${product['price']}")
            print(f"  Description: {product['description']}")
            print(f"  Tags: {', '.join(product['tags'])}")
            categories_shown.add(product['category'])
            products_shown += 1


def show_sample_queries():
    """Display sample queries"""
    print_section("SAMPLE TEST QUERIES")

    query_types = {
        'Office/Work': ['oficina', 'trabajo', 'ejecutiv', 'formal'],
        'Sports': ['deportiv', 'running', 'gimnasio'],
        'Casual': ['casual', 'diario', 'jean'],
        'Accessories': ['accesorios', 'cartera', 'mochila'],
        'Kids': ['bebé', 'niño', 'infantil']
    }

    for query_type, keywords in query_types.items():
        print(f"\n{query_type} Queries:")
        matching_queries = [
            q for q in SEARCH_QUERIES
            if any(kw in q['query'].lower() for kw in keywords)
        ][:3]  # Show max 3 per type

        for q in matching_queries:
            print(f"  • '{q['query']}'")
            if q.get('expected_categories'):
                print(f"    Expected categories: {', '.join(q['expected_categories'][:2])}")


def show_query_distribution():
    """Show distribution of query types"""
    print_section("QUERY DISTRIBUTION")

    print(f"\nTotal Test Queries: {len(SEARCH_QUERIES)}")

    # Count queries by expected results
    has_products = sum(1 for q in SEARCH_QUERIES if q.get('expected_products'))
    has_categories = sum(1 for q in SEARCH_QUERIES if q.get('expected_categories'))

    print(f"Queries with expected products: {has_products}")
    print(f"Queries with expected categories: {has_categories}")

    # Sample specific query details
    print("\nSample Query Details:")
    sample_query = SEARCH_QUERIES[0]  # "ropa para oficina"
    print(f"\nQuery: '{sample_query['query']}'")
    print(f"Expected categories ({len(sample_query['expected_categories'])}):")
    for cat in sample_query['expected_categories']:
        print(f"  - {cat}")
    print(f"Expected products ({len(sample_query['expected_products'])}):")
    for pid in sample_query['expected_products'][:5]:
        product = next(p for p in PRODUCTS if p['id'] == pid)
        print(f"  - [{pid}] {product['name']}")


def validate_data():
    """Validate catalog data integrity"""
    print_section("DATA VALIDATION")

    errors = []

    # Check products
    product_ids = set()
    for product in PRODUCTS:
        # Check required fields
        required = ['id', 'name', 'category', 'subcategory', 'description', 'price', 'tags']
        for field in required:
            if field not in product:
                errors.append(f"Product {product.get('id', '?')} missing field: {field}")

        # Check duplicate IDs
        if product['id'] in product_ids:
            errors.append(f"Duplicate product ID: {product['id']}")
        product_ids.add(product['id'])

        # Check category exists
        if product['category'] not in CATEGORIES:
            errors.append(f"Product {product['id']} has invalid category: {product['category']}")

    # Check queries
    for i, query in enumerate(SEARCH_QUERIES):
        if 'query' not in query:
            errors.append(f"Query {i} missing 'query' field")

        # Check expected products exist
        for pid in query.get('expected_products', []):
            if pid not in product_ids:
                errors.append(f"Query '{query.get('query', '?')}' references non-existent product ID: {pid}")

    if errors:
        print("\n❌ VALIDATION ERRORS FOUND:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\n✓ All data validated successfully!")
        print(f"  ✓ {len(PRODUCTS)} products")
        print(f"  ✓ {len(CATEGORIES)} categories")
        print(f"  ✓ {len(SEARCH_QUERIES)} test queries")


def main():
    """Main test execution"""
    print("\n" + "="*80)
    print("E-COMMERCE CATALOG TEST")
    print("="*80)

    validate_data()
    show_catalog_stats()
    show_sample_products()
    show_sample_queries()
    show_query_distribution()

    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("\n1. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("\n2. Run the full embedding test:")
    print("   python embedding_tester.py")
    print("\n3. Visualize results:")
    print("   python visualize_results.py")
    print("\n4. (Optional) Scrape real catalog:")
    print("   python scrape_catalog.py")


if __name__ == "__main__":
    main()
