"""
Sample catalog structure for Pimenton e-commerce testing.
Replace with actual scraped data when available.
"""

CATEGORIES = {
    "Ropa Mujer": {
        "subcategories": ["Vestidos", "Blusas", "Pantalones", "Faldas", "Ropa de Oficina", "Ropa Casual", "Ropa Deportiva"],
        "description": "Colección completa de ropa para mujer"
    },
    "Ropa Hombre": {
        "subcategories": ["Camisas", "Pantalones", "Trajes", "Ropa Casual", "Ropa Deportiva", "Ropa de Oficina"],
        "description": "Ropa masculina para todas las ocasiones"
    },
    "Accesorios": {
        "subcategories": ["Carteras", "Cinturones", "Bufandas", "Gorros", "Guantes", "Joyas"],
        "description": "Accesorios para complementar tu estilo"
    },
    "Calzado": {
        "subcategories": ["Zapatos Mujer", "Zapatos Hombre", "Zapatillas", "Botas", "Sandalias"],
        "description": "Calzado para cada ocasión"
    },
    "Niños": {
        "subcategories": ["Ropa Bebé", "Ropa Niño", "Ropa Niña", "Calzado Infantil", "Accesorios Niños"],
        "description": "Moda infantil y para bebés"
    },
    "Hogar": {
        "subcategories": ["Decoración", "Textiles", "Cocina", "Baño", "Organización"],
        "description": "Artículos para el hogar"
    },
    "Deportes": {
        "subcategories": ["Ropa Deportiva", "Calzado Deportivo", "Equipamiento", "Accesorios Deportivos"],
        "description": "Todo para tu actividad física"
    }
}

PRODUCTS = [
    # Ropa Mujer - Oficina
    {"id": 1, "name": "Camisa blanca formal mujer", "category": "Ropa Mujer", "subcategory": "Ropa de Oficina", "description": "Camisa elegante de algodón para la oficina", "price": 1200, "tags": ["formal", "oficina", "trabajo", "elegante"]},
    {"id": 2, "name": "Pantalón de vestir negro mujer", "category": "Ropa Mujer", "subcategory": "Ropa de Oficina", "description": "Pantalón formal de corte recto", "price": 1800, "tags": ["formal", "oficina", "trabajo", "negro"]},
    {"id": 3, "name": "Blazer gris mujer", "category": "Ropa Mujer", "subcategory": "Ropa de Oficina", "description": "Blazer ejecutivo para look profesional", "price": 2500, "tags": ["formal", "oficina", "ejecutivo", "profesional"]},
    {"id": 4, "name": "Vestido camisero azul", "category": "Ropa Mujer", "subcategory": "Vestidos", "description": "Vestido estilo camisero ideal para oficina", "price": 2200, "tags": ["vestido", "oficina", "elegante", "azul"]},

    # Ropa Mujer - Casual
    {"id": 5, "name": "Jean skinny mujer", "category": "Ropa Mujer", "subcategory": "Ropa Casual", "description": "Jean ajustado de mezclilla", "price": 1500, "tags": ["casual", "jean", "denim", "diario"]},
    {"id": 6, "name": "Remera básica blanca", "category": "Ropa Mujer", "subcategory": "Ropa Casual", "description": "Remera de algodón básica", "price": 600, "tags": ["casual", "básico", "diario", "blanco"]},
    {"id": 7, "name": "Vestido floreado verano", "category": "Ropa Mujer", "subcategory": "Vestidos", "description": "Vestido fresco con estampado floral", "price": 1800, "tags": ["verano", "floral", "casual", "fresco"]},

    # Ropa Hombre - Oficina
    {"id": 8, "name": "Camisa formal hombre blanca", "category": "Ropa Hombre", "subcategory": "Ropa de Oficina", "description": "Camisa de vestir slim fit", "price": 1300, "tags": ["formal", "oficina", "trabajo", "elegante"]},
    {"id": 9, "name": "Pantalón de vestir gris hombre", "category": "Ropa Hombre", "subcategory": "Ropa de Oficina", "description": "Pantalón formal de gabardina", "price": 2000, "tags": ["formal", "oficina", "trabajo", "gris"]},
    {"id": 10, "name": "Traje completo azul marino", "category": "Ropa Hombre", "subcategory": "Trajes", "description": "Traje ejecutivo completo", "price": 5500, "tags": ["traje", "formal", "ejecutivo", "marino"]},
    {"id": 11, "name": "Corbata seda roja", "category": "Accesorios", "subcategory": "Accesorios", "description": "Corbata de seda italiana", "price": 800, "tags": ["corbata", "formal", "seda", "elegante"]},

    # Ropa Hombre - Casual
    {"id": 12, "name": "Jean regular fit hombre", "category": "Ropa Hombre", "subcategory": "Ropa Casual", "description": "Jean clásico de corte regular", "price": 1600, "tags": ["casual", "jean", "denim", "diario"]},
    {"id": 13, "name": "Remera polo verde", "category": "Ropa Hombre", "subcategory": "Ropa Casual", "description": "Polo de algodón piqué", "price": 900, "tags": ["polo", "casual", "verde", "diario"]},
    {"id": 14, "name": "Buzo con capucha negro", "category": "Ropa Hombre", "subcategory": "Ropa Casual", "description": "Buzo urbano con capucha", "price": 1400, "tags": ["buzo", "casual", "urbano", "negro"]},

    # Calzado Mujer
    {"id": 15, "name": "Zapatos taco mujer negros", "category": "Calzado", "subcategory": "Zapatos Mujer", "description": "Stilettos elegantes para oficina", "price": 2200, "tags": ["zapatos", "taco", "formal", "oficina"]},
    {"id": 16, "name": "Zapatillas deportivas mujer", "category": "Calzado", "subcategory": "Zapatillas", "description": "Zapatillas running mujer", "price": 2800, "tags": ["zapatillas", "deportivo", "running", "comodas"]},
    {"id": 17, "name": "Botas de cuero negras", "category": "Calzado", "subcategory": "Botas", "description": "Botas largas de cuero", "price": 3500, "tags": ["botas", "cuero", "invierno", "elegante"]},
    {"id": 18, "name": "Sandalias planas verano", "category": "Calzado", "subcategory": "Sandalias", "description": "Sandalias cómodas para el verano", "price": 1200, "tags": ["sandalias", "verano", "planas", "comodas"]},

    # Calzado Hombre
    {"id": 19, "name": "Zapatos de vestir hombre", "category": "Calzado", "subcategory": "Zapatos Hombre", "description": "Zapatos formales de cuero", "price": 2500, "tags": ["zapatos", "formal", "cuero", "oficina"]},
    {"id": 20, "name": "Zapatillas urbanas hombre", "category": "Calzado", "subcategory": "Zapatillas", "description": "Zapatillas casual urbanas", "price": 2400, "tags": ["zapatillas", "casual", "urbano", "comodas"]},

    # Accesorios
    {"id": 21, "name": "Cartera de cuero marrón", "category": "Accesorios", "subcategory": "Carteras", "description": "Cartera ejecutiva de cuero genuino", "price": 3200, "tags": ["cartera", "cuero", "ejecutiva", "oficina"]},
    {"id": 22, "name": "Cinturón de cuero negro", "category": "Accesorios", "subcategory": "Cinturones", "description": "Cinturón formal de cuero", "price": 900, "tags": ["cinturón", "cuero", "formal", "negro"]},
    {"id": 23, "name": "Bufanda lana gris", "category": "Accesorios", "subcategory": "Bufandas", "description": "Bufanda tejida de lana", "price": 700, "tags": ["bufanda", "lana", "invierno", "abrigo"]},
    {"id": 24, "name": "Reloj ejecutivo plateado", "category": "Accesorios", "subcategory": "Joyas", "description": "Reloj de acero inoxidable", "price": 4500, "tags": ["reloj", "ejecutivo", "formal", "acero"]},

    # Deportes
    {"id": 25, "name": "Calza deportiva mujer", "category": "Deportes", "subcategory": "Ropa Deportiva", "description": "Calza legging para yoga y fitness", "price": 1100, "tags": ["deportivo", "yoga", "fitness", "legging"]},
    {"id": 26, "name": "Remera técnica running", "category": "Deportes", "subcategory": "Ropa Deportiva", "description": "Remera dry-fit para correr", "price": 800, "tags": ["running", "deportivo", "técnica", "transpirable"]},
    {"id": 27, "name": "Short deportivo hombre", "category": "Deportes", "subcategory": "Ropa Deportiva", "description": "Short para entrenamiento", "price": 900, "tags": ["short", "deportivo", "entrenamiento", "fitness"]},
    {"id": 28, "name": "Zapatillas running profesional", "category": "Deportes", "subcategory": "Calzado Deportivo", "description": "Zapatillas técnicas para running", "price": 4200, "tags": ["zapatillas", "running", "profesional", "técnicas"]},

    # Niños
    {"id": 29, "name": "Conjunto bebé celeste", "category": "Niños", "subcategory": "Ropa Bebé", "description": "Conjunto de algodón para bebé", "price": 1200, "tags": ["bebé", "conjunto", "algodón", "suave"]},
    {"id": 30, "name": "Remera infantil con estampado", "category": "Niños", "subcategory": "Ropa Niño", "description": "Remera con estampado de superhéroes", "price": 600, "tags": ["niño", "remera", "estampado", "superhéroes"]},
    {"id": 31, "name": "Vestido niña con flores", "category": "Niños", "subcategory": "Ropa Niña", "description": "Vestido floreado para niña", "price": 1400, "tags": ["niña", "vestido", "flores", "fiesta"]},
    {"id": 32, "name": "Zapatillas luminosas niño", "category": "Niños", "subcategory": "Calzado Infantil", "description": "Zapatillas con luces LED", "price": 1800, "tags": ["zapatillas", "niño", "luces", "led"]},

    # Hogar
    {"id": 33, "name": "Juego de sábanas matrimonial", "category": "Hogar", "subcategory": "Textiles", "description": "Sábanas de algodón 180 hilos", "price": 2500, "tags": ["sábanas", "textil", "hogar", "algodón"]},
    {"id": 34, "name": "Toalla de baño grande", "category": "Hogar", "subcategory": "Baño", "description": "Toalla de algodón suave", "price": 800, "tags": ["toalla", "baño", "algodón", "suave"]},
    {"id": 35, "name": "Cortina blackout beige", "category": "Hogar", "subcategory": "Decoración", "description": "Cortina opaca para dormitorio", "price": 1900, "tags": ["cortina", "blackout", "decoración", "dormitorio"]},
    {"id": 36, "name": "Almohadón decorativo gris", "category": "Hogar", "subcategory": "Decoración", "description": "Almohadón para sofá", "price": 600, "tags": ["almohadón", "decoración", "sofá", "gris"]},

    # Más productos de oficina/trabajo
    {"id": 37, "name": "Sweater fino mujer beige", "category": "Ropa Mujer", "subcategory": "Ropa de Oficina", "description": "Sweater elegante para oficina", "price": 1600, "tags": ["sweater", "oficina", "elegante", "trabajo"]},
    {"id": 38, "name": "Falda tubo negra", "category": "Ropa Mujer", "subcategory": "Faldas", "description": "Falda formal hasta la rodilla", "price": 1400, "tags": ["falda", "formal", "oficina", "negro"]},
    {"id": 39, "name": "Camisa rayada hombre", "category": "Ropa Hombre", "subcategory": "Ropa de Oficina", "description": "Camisa formal a rayas", "price": 1400, "tags": ["camisa", "formal", "rayas", "oficina"]},
    {"id": 40, "name": "Maletín ejecutivo cuero", "category": "Accesorios", "subcategory": "Carteras", "description": "Maletín para laptop y documentos", "price": 4500, "tags": ["maletín", "ejecutivo", "cuero", "trabajo"]},

    # Más variedad
    {"id": 41, "name": "Campera jean mujer", "category": "Ropa Mujer", "subcategory": "Ropa Casual", "description": "Campera de jean clásica", "price": 2200, "tags": ["campera", "jean", "casual", "denim"]},
    {"id": 42, "name": "Buzo de algodón mujer", "category": "Ropa Mujer", "subcategory": "Ropa Casual", "description": "Buzo básico de algodón", "price": 1200, "tags": ["buzo", "casual", "algodón", "cómodo"]},
    {"id": 43, "name": "Chaqueta cuero hombre", "category": "Ropa Hombre", "subcategory": "Ropa Casual", "description": "Chaqueta de cuero estilo biker", "price": 5500, "tags": ["chaqueta", "cuero", "urbano", "biker"]},
    {"id": 44, "name": "Mochila urbana negra", "category": "Accesorios", "subcategory": "Carteras", "description": "Mochila para laptop y uso diario", "price": 2200, "tags": ["mochila", "urbano", "laptop", "diario"]},
    {"id": 45, "name": "Gorra deportiva", "category": "Accesorios", "subcategory": "Gorros", "description": "Gorra ajustable para deporte", "price": 500, "tags": ["gorra", "deportivo", "sol", "casual"]},
    {"id": 46, "name": "Medias deportivas pack x3", "category": "Deportes", "subcategory": "Accesorios Deportivos", "description": "Pack de medias técnicas", "price": 600, "tags": ["medias", "deportivo", "pack", "técnicas"]},
    {"id": 47, "name": "Pijama mujer algodón", "category": "Ropa Mujer", "subcategory": "Ropa Casual", "description": "Pijama cómodo para dormir", "price": 1400, "tags": ["pijama", "dormir", "algodón", "cómodo"]},
    {"id": 48, "name": "Pijama hombre franela", "category": "Ropa Hombre", "subcategory": "Ropa Casual", "description": "Pijama abrigado de franela", "price": 1500, "tags": ["pijama", "dormir", "franela", "abrigado"]},
    {"id": 49, "name": "Bikini estampado", "category": "Ropa Mujer", "subcategory": "Ropa Deportiva", "description": "Bikini para playa y piscina", "price": 1800, "tags": ["bikini", "playa", "verano", "natación"]},
    {"id": 50, "name": "Traje de baño hombre", "category": "Ropa Hombre", "subcategory": "Ropa Deportiva", "description": "Short de baño secado rápido", "price": 1200, "tags": ["baño", "playa", "verano", "natación"]},
]

# 50 search queries for testing
SEARCH_QUERIES = [
    # Queries for office/work (should match office categories and products)
    {"query": "ropa para oficina", "expected_categories": ["Ropa Mujer > Ropa de Oficina", "Ropa Hombre > Ropa de Oficina"], "expected_products": [1, 2, 3, 4, 8, 9, 37, 38, 39]},
    {"query": "traje para trabajo", "expected_categories": ["Ropa Hombre > Trajes", "Ropa Hombre > Ropa de Oficina"], "expected_products": [10, 8, 9]},
    {"query": "ropa ejecutiva mujer", "expected_categories": ["Ropa Mujer > Ropa de Oficina"], "expected_products": [3, 1, 2, 4]},
    {"query": "vestir formal hombre", "expected_categories": ["Ropa Hombre > Ropa de Oficina", "Ropa Hombre > Trajes"], "expected_products": [8, 9, 10]},
    {"query": "zapatos para la oficina", "expected_categories": ["Calzado > Zapatos Mujer", "Calzado > Zapatos Hombre"], "expected_products": [15, 19]},

    # Casual/daily wear
    {"query": "ropa casual diaria", "expected_categories": ["Ropa Mujer > Ropa Casual", "Ropa Hombre > Ropa Casual"], "expected_products": [5, 6, 12, 13, 14]},
    {"query": "jean mujer", "expected_categories": ["Ropa Mujer > Ropa Casual"], "expected_products": [5]},
    {"query": "jean hombre", "expected_categories": ["Ropa Hombre > Ropa Casual"], "expected_products": [12]},
    {"query": "remera básica", "expected_categories": ["Ropa Mujer > Ropa Casual", "Ropa Hombre > Ropa Casual"], "expected_products": [6, 13]},
    {"query": "buzo con capucha", "expected_categories": ["Ropa Hombre > Ropa Casual"], "expected_products": [14]},

    # Sports/athletic
    {"query": "ropa deportiva", "expected_categories": ["Deportes > Ropa Deportiva", "Ropa Mujer > Ropa Deportiva"], "expected_products": [25, 26, 27]},
    {"query": "zapatillas running", "expected_categories": ["Deportes > Calzado Deportivo", "Calzado > Zapatillas"], "expected_products": [28, 16]},
    {"query": "ropa para gimnasio", "expected_categories": ["Deportes > Ropa Deportiva"], "expected_products": [25, 26, 27]},
    {"query": "calza yoga", "expected_categories": ["Deportes > Ropa Deportiva"], "expected_products": [25]},
    {"query": "equipamiento deportivo", "expected_categories": ["Deportes > Equipamiento"], "expected_products": [28, 46]},

    # Seasonal
    {"query": "ropa de verano", "expected_categories": ["Ropa Mujer > Vestidos", "Ropa Mujer > Ropa Casual"], "expected_products": [7, 18, 49, 50]},
    {"query": "ropa de invierno", "expected_categories": ["Accesorios > Bufandas"], "expected_products": [17, 23, 48]},
    {"query": "ropa para la playa", "expected_categories": ["Ropa Mujer > Ropa Deportiva", "Ropa Hombre > Ropa Deportiva"], "expected_products": [49, 50]},
    {"query": "abrigo invierno", "expected_categories": ["Accesorios > Bufandas"], "expected_products": [23, 43]},

    # Footwear specific
    {"query": "zapatos elegantes", "expected_categories": ["Calzado > Zapatos Mujer", "Calzado > Zapatos Hombre"], "expected_products": [15, 19]},
    {"query": "zapatillas cómodas", "expected_categories": ["Calzado > Zapatillas"], "expected_products": [16, 20]},
    {"query": "botas mujer", "expected_categories": ["Calzado > Botas"], "expected_products": [17]},
    {"query": "sandalias verano", "expected_categories": ["Calzado > Sandalias"], "expected_products": [18]},
    {"query": "calzado deportivo", "expected_categories": ["Deportes > Calzado Deportivo", "Calzado > Zapatillas"], "expected_products": [28, 16, 20]},

    # Accessories
    {"query": "accesorios para oficina", "expected_categories": ["Accesorios > Carteras"], "expected_products": [21, 40]},
    {"query": "cartera de cuero", "expected_categories": ["Accesorios > Carteras"], "expected_products": [21, 40]},
    {"query": "accesorios elegantes", "expected_categories": ["Accesorios > Joyas", "Accesorios > Carteras"], "expected_products": [24, 21]},
    {"query": "mochila para laptop", "expected_categories": ["Accesorios > Carteras"], "expected_products": [44, 40]},
    {"query": "bufanda lana", "expected_categories": ["Accesorios > Bufandas"], "expected_products": [23]},

    # Kids
    {"query": "ropa para bebé", "expected_categories": ["Niños > Ropa Bebé"], "expected_products": [29]},
    {"query": "ropa infantil", "expected_categories": ["Niños > Ropa Niño", "Niños > Ropa Niña"], "expected_products": [30, 31]},
    {"query": "zapatillas para niños", "expected_categories": ["Niños > Calzado Infantil"], "expected_products": [32]},
    {"query": "vestido niña fiesta", "expected_categories": ["Niños > Ropa Niña"], "expected_products": [31]},

    # Home
    {"query": "textiles para el hogar", "expected_categories": ["Hogar > Textiles"], "expected_products": [33]},
    {"query": "decoración dormitorio", "expected_categories": ["Hogar > Decoración"], "expected_products": [35, 36]},
    {"query": "sábanas matrimonial", "expected_categories": ["Hogar > Textiles"], "expected_products": [33]},
    {"query": "toallas de baño", "expected_categories": ["Hogar > Baño"], "expected_products": [34]},

    # Specific product types
    {"query": "vestidos elegantes", "expected_categories": ["Ropa Mujer > Vestidos"], "expected_products": [4, 7]},
    {"query": "camisa formal", "expected_categories": ["Ropa Mujer > Ropa de Oficina", "Ropa Hombre > Ropa de Oficina"], "expected_products": [1, 8, 39]},
    {"query": "pantalón de vestir", "expected_categories": ["Ropa Mujer > Ropa de Oficina", "Ropa Hombre > Ropa de Oficina"], "expected_products": [2, 9]},
    {"query": "blazer mujer", "expected_categories": ["Ropa Mujer > Ropa de Oficina"], "expected_products": [3]},
    {"query": "traje completo", "expected_categories": ["Ropa Hombre > Trajes"], "expected_products": [10]},

    # Color-specific
    {"query": "ropa negra formal", "expected_categories": ["Ropa Mujer > Ropa de Oficina", "Ropa Hombre > Ropa de Oficina"], "expected_products": [2, 38, 15, 19]},
    {"query": "ropa blanca básica", "expected_categories": ["Ropa Mujer > Ropa Casual", "Ropa Hombre > Ropa de Oficina"], "expected_products": [1, 6, 8]},

    # Sleep/comfort
    {"query": "ropa para dormir", "expected_categories": ["Ropa Mujer > Ropa Casual", "Ropa Hombre > Ropa Casual"], "expected_products": [47, 48]},
    {"query": "pijama cómodo", "expected_categories": ["Ropa Mujer > Ropa Casual", "Ropa Hombre > Ropa Casual"], "expected_products": [47, 48]},

    # Mixed/ambiguous queries
    {"query": "regalo ejecutivo", "expected_categories": ["Accesorios > Joyas", "Accesorios > Carteras"], "expected_products": [24, 40, 21]},
    {"query": "look profesional", "expected_categories": ["Ropa Mujer > Ropa de Oficina", "Ropa Hombre > Ropa de Oficina"], "expected_products": [3, 1, 8, 10]},
    {"query": "outfit casual urbano", "expected_categories": ["Ropa Mujer > Ropa Casual", "Ropa Hombre > Ropa Casual"], "expected_products": [5, 6, 12, 13, 43]},
    {"query": "estilo deportivo", "expected_categories": ["Deportes > Ropa Deportiva"], "expected_products": [25, 26, 27, 28]},
]
