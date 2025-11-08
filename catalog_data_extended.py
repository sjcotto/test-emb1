"""
Extended synthetic catalog data for comprehensive embedding model testing
Includes 100+ products and 100 search queries for thorough evaluation
"""

CATEGORIES = {
    "Ropa Mujer": {
        "subcategories": ["Vestidos", "Blusas", "Pantalones", "Faldas", "Ropa de Oficina",
                         "Ropa Casual", "Ropa Deportiva", "Ropa de Noche", "Jeans"],
        "description": "Colección completa de ropa para mujer"
    },
    "Ropa Hombre": {
        "subcategories": ["Camisas", "Pantalones", "Trajes", "Ropa Casual", "Ropa Deportiva",
                         "Ropa de Oficina", "Jeans", "Ropa de Noche"],
        "description": "Ropa masculina para todas las ocasiones"
    },
    "Calzado Mujer": {
        "subcategories": ["Zapatos Formales", "Zapatillas", "Botas", "Sandalias", "Zapatos Casual"],
        "description": "Calzado femenino para cada ocasión"
    },
    "Calzado Hombre": {
        "subcategories": ["Zapatos Formales", "Zapatillas", "Botas", "Zapatos Casual"],
        "description": "Calzado masculino de calidad"
    },
    "Accesorios": {
        "subcategories": ["Carteras", "Cinturones", "Bufandas", "Gorros", "Guantes", "Joyas",
                         "Relojes", "Gafas de Sol", "Mochilas"],
        "description": "Accesorios para complementar tu estilo"
    },
    "Niños": {
        "subcategories": ["Ropa Bebé", "Ropa Niño", "Ropa Niña", "Calzado Infantil",
                         "Accesorios Niños", "Ropa Deportiva Niños"],
        "description": "Moda infantil y para bebés"
    },
    "Deportes": {
        "subcategories": ["Ropa Deportiva", "Calzado Deportivo", "Equipamiento",
                         "Accesorios Deportivos", "Yoga", "Running", "Gimnasio"],
        "description": "Todo para tu actividad física"
    },
    "Hogar": {
        "subcategories": ["Decoración", "Textiles", "Cocina", "Baño", "Organización", "Muebles"],
        "description": "Artículos para el hogar"
    },
    "Temporada": {
        "subcategories": ["Verano", "Invierno", "Otoño", "Primavera", "Playa", "Nieve"],
        "description": "Productos por temporada"
    },
    "Ocasiones Especiales": {
        "subcategories": ["Fiesta", "Boda", "Graduación", "Casual Elegante", "Cóctel"],
        "description": "Ropa y accesorios para eventos especiales"
    }
}

# 100+ Products with diverse categories
PRODUCTS = [
    # ROPA MUJER - OFICINA (15 products)
    {"id": 1, "name": "Camisa blanca formal mujer manga larga", "category": "Ropa Mujer", "subcategory": "Ropa de Oficina",
     "description": "Camisa elegante de algodón egipcio para la oficina", "price": 1200,
     "tags": ["formal", "oficina", "trabajo", "elegante", "blanco", "manga larga"]},

    {"id": 2, "name": "Pantalón de vestir negro mujer corte recto", "category": "Ropa Mujer", "subcategory": "Ropa de Oficina",
     "description": "Pantalón formal de gabardina con corte recto", "price": 1800,
     "tags": ["formal", "oficina", "trabajo", "negro", "elegante"]},

    {"id": 3, "name": "Blazer gris mujer slim fit", "category": "Ropa Mujer", "subcategory": "Ropa de Oficina",
     "description": "Blazer ejecutivo para look profesional slim fit", "price": 2500,
     "tags": ["formal", "oficina", "ejecutivo", "profesional", "gris"]},

    {"id": 4, "name": "Vestido camisero azul marino oficina", "category": "Ropa Mujer", "subcategory": "Vestidos",
     "description": "Vestido estilo camisero ideal para oficina", "price": 2200,
     "tags": ["vestido", "oficina", "elegante", "azul", "formal"]},

    {"id": 5, "name": "Blusa seda beige cuello alto", "category": "Ropa Mujer", "subcategory": "Blusas",
     "description": "Blusa de seda premium con cuello alto", "price": 1600,
     "tags": ["blusa", "seda", "elegante", "beige", "oficina"]},

    {"id": 6, "name": "Falda tubo negra oficina", "category": "Ropa Mujer", "subcategory": "Faldas",
     "description": "Falda formal hasta la rodilla corte tubo", "price": 1400,
     "tags": ["falda", "formal", "oficina", "negro", "elegante"]},

    {"id": 7, "name": "Sweater fino mujer beige cuello V", "category": "Ropa Mujer", "subcategory": "Ropa de Oficina",
     "description": "Sweater elegante de lana merino para oficina", "price": 1600,
     "tags": ["sweater", "oficina", "elegante", "trabajo", "beige"]},

    {"id": 8, "name": "Pantalón palazzo gris mujer", "category": "Ropa Mujer", "subcategory": "Pantalones",
     "description": "Pantalón palazzo de tela fluida para oficina", "price": 1700,
     "tags": ["palazzo", "elegante", "gris", "oficina", "cómodo"]},

    {"id": 9, "name": "Camisa rayada azul blanco mujer", "category": "Ropa Mujer", "subcategory": "Blusas",
     "description": "Camisa a rayas verticales estilo ejecutivo", "price": 1300,
     "tags": ["camisa", "rayas", "azul", "oficina", "formal"]},

    {"id": 10, "name": "Blazer negro mujer doble botonadura", "category": "Ropa Mujer", "subcategory": "Ropa de Oficina",
     "description": "Blazer clásico negro con doble botonadura", "price": 2800,
     "tags": ["blazer", "negro", "formal", "ejecutivo", "clásico"]},

    {"id": 11, "name": "Vestido tubo negro oficina", "category": "Ropa Mujer", "subcategory": "Vestidos",
     "description": "Vestido tubo negro hasta la rodilla", "price": 2100,
     "tags": ["vestido", "negro", "oficina", "formal", "elegante"]},

    {"id": 12, "name": "Pantalón pinzado beige mujer", "category": "Ropa Mujer", "subcategory": "Pantalones",
     "description": "Pantalón formal con pinzas estilo clásico", "price": 1650,
     "tags": ["pantalón", "beige", "formal", "oficina", "pinzas"]},

    {"id": 13, "name": "Blusa satinada blanca mujer", "category": "Ropa Mujer", "subcategory": "Blusas",
     "description": "Blusa satinada con acabado brillante", "price": 1450,
     "tags": ["blusa", "satinada", "blanco", "elegante", "oficina"]},

    {"id": 14, "name": "Cardigan largo gris mujer", "category": "Ropa Mujer", "subcategory": "Ropa de Oficina",
     "description": "Cardigan largo ideal para oficina", "price": 1850,
     "tags": ["cardigan", "gris", "oficina", "elegante", "largo"]},

    {"id": 15, "name": "Conjunto blazer y pantalón mujer", "category": "Ropa Mujer", "subcategory": "Ropa de Oficina",
     "description": "Conjunto ejecutivo blazer y pantalón a juego", "price": 3900,
     "tags": ["conjunto", "blazer", "pantalón", "ejecutivo", "formal"]},

    # ROPA MUJER - CASUAL (15 products)
    {"id": 16, "name": "Jean skinny mujer azul oscuro", "category": "Ropa Mujer", "subcategory": "Jeans",
     "description": "Jean ajustado de mezclilla premium", "price": 1500,
     "tags": ["casual", "jean", "denim", "diario", "azul"]},

    {"id": 17, "name": "Remera básica blanca algodón", "category": "Ropa Mujer", "subcategory": "Ropa Casual",
     "description": "Remera de algodón 100% básica", "price": 600,
     "tags": ["casual", "básico", "diario", "blanco", "algodón"]},

    {"id": 18, "name": "Vestido floreado verano corto", "category": "Ropa Mujer", "subcategory": "Vestidos",
     "description": "Vestido fresco con estampado floral", "price": 1800,
     "tags": ["verano", "floral", "casual", "fresco", "corto"]},

    {"id": 19, "name": "Campera jean mujer clásica", "category": "Ropa Mujer", "subcategory": "Ropa Casual",
     "description": "Campera de jean clásica azul", "price": 2200,
     "tags": ["campera", "jean", "casual", "denim", "clásico"]},

    {"id": 20, "name": "Buzo algodón mujer gris", "category": "Ropa Mujer", "subcategory": "Ropa Casual",
     "description": "Buzo básico de algodón con capucha", "price": 1200,
     "tags": ["buzo", "casual", "algodón", "cómodo", "gris"]},

    {"id": 21, "name": "Legging negro mujer", "category": "Ropa Mujer", "subcategory": "Ropa Casual",
     "description": "Legging de algodón elastizado", "price": 900,
     "tags": ["legging", "negro", "cómodo", "casual", "elastizado"]},

    {"id": 22, "name": "Remera estampada mujer colores", "category": "Ropa Mujer", "subcategory": "Ropa Casual",
     "description": "Remera con estampado colorido moderno", "price": 750,
     "tags": ["remera", "estampado", "colores", "casual", "moderno"]},

    {"id": 23, "name": "Short jean mujer", "category": "Ropa Mujer", "subcategory": "Ropa Casual",
     "description": "Short de jean para verano", "price": 1100,
     "tags": ["short", "jean", "verano", "casual", "denim"]},

    {"id": 24, "name": "Vestido midi casual rayas", "category": "Ropa Mujer", "subcategory": "Vestidos",
     "description": "Vestido largo casual a rayas", "price": 1900,
     "tags": ["vestido", "midi", "rayas", "casual", "cómodo"]},

    {"id": 25, "name": "Sweater oversize mujer", "category": "Ropa Mujer", "subcategory": "Ropa Casual",
     "description": "Sweater tejido oversize cómodo", "price": 1650,
     "tags": ["sweater", "oversize", "tejido", "cómodo", "casual"]},

    {"id": 26, "name": "Jean mom fit mujer", "category": "Ropa Mujer", "subcategory": "Jeans",
     "description": "Jean mom fit tiro alto", "price": 1600,
     "tags": ["jean", "mom fit", "tiro alto", "casual", "cómodo"]},

    {"id": 27, "name": "Musculosa básica negra", "category": "Ropa Mujer", "subcategory": "Ropa Casual",
     "description": "Musculosa de algodón básica", "price": 500,
     "tags": ["musculosa", "básico", "negro", "verano", "casual"]},

    {"id": 28, "name": "Pantalón jogger mujer", "category": "Ropa Mujer", "subcategory": "Ropa Casual",
     "description": "Pantalón jogger cómodo urbano", "price": 1400,
     "tags": ["jogger", "cómodo", "urbano", "casual", "deportivo"]},

    {"id": 29, "name": "Pijama mujer algodón estampado", "category": "Ropa Mujer", "subcategory": "Ropa Casual",
     "description": "Pijama cómodo de algodón con estampado", "price": 1400,
     "tags": ["pijama", "dormir", "algodón", "cómodo", "estampado"]},

    {"id": 30, "name": "Chomba mujer colores", "category": "Ropa Mujer", "subcategory": "Ropa Casual",
     "description": "Chomba de piqué varios colores", "price": 950,
     "tags": ["chomba", "piqué", "casual", "colores", "cómodo"]},

    # ROPA HOMBRE - OFICINA (15 products)
    {"id": 31, "name": "Camisa formal hombre blanca slim", "category": "Ropa Hombre", "subcategory": "Ropa de Oficina",
     "description": "Camisa de vestir slim fit premium", "price": 1300,
     "tags": ["formal", "oficina", "trabajo", "elegante", "blanco", "slim"]},

    {"id": 32, "name": "Pantalón vestir gris hombre", "category": "Ropa Hombre", "subcategory": "Ropa de Oficina",
     "description": "Pantalón formal de gabardina gris", "price": 2000,
     "tags": ["formal", "oficina", "trabajo", "gris", "gabardina"]},

    {"id": 33, "name": "Traje completo azul marino hombre", "category": "Ropa Hombre", "subcategory": "Trajes",
     "description": "Traje ejecutivo completo dos piezas", "price": 5500,
     "tags": ["traje", "formal", "ejecutivo", "marino", "completo"]},

    {"id": 34, "name": "Corbata seda roja elegante", "category": "Accesorios", "subcategory": "Accesorios",
     "description": "Corbata de seda italiana premium", "price": 800,
     "tags": ["corbata", "formal", "seda", "elegante", "rojo"]},

    {"id": 35, "name": "Camisa rayada hombre azul", "category": "Ropa Hombre", "subcategory": "Ropa de Oficina",
     "description": "Camisa formal a rayas finas", "price": 1400,
     "tags": ["camisa", "formal", "rayas", "oficina", "azul"]},

    {"id": 36, "name": "Pantalón vestir negro hombre", "category": "Ropa Hombre", "subcategory": "Ropa de Oficina",
     "description": "Pantalón de vestir negro clásico", "price": 1900,
     "tags": ["pantalón", "formal", "negro", "oficina", "clásico"]},

    {"id": 37, "name": "Saco sport hombre beige", "category": "Ropa Hombre", "subcategory": "Ropa de Oficina",
     "description": "Saco sport elegante casual", "price": 3200,
     "tags": ["saco", "sport", "elegante", "beige", "casual"]},

    {"id": 38, "name": "Sweater cuello V hombre gris", "category": "Ropa Hombre", "subcategory": "Ropa de Oficina",
     "description": "Sweater fino para oficina", "price": 1500,
     "tags": ["sweater", "oficina", "elegante", "gris", "cuello V"]},

    {"id": 39, "name": "Camisa celeste hombre formal", "category": "Ropa Hombre", "subcategory": "Camisas",
     "description": "Camisa celeste de vestir", "price": 1250,
     "tags": ["camisa", "formal", "celeste", "oficina", "elegante"]},

    {"id": 40, "name": "Chaleco vestir hombre negro", "category": "Ropa Hombre", "subcategory": "Ropa de Oficina",
     "description": "Chaleco formal para traje", "price": 1700,
     "tags": ["chaleco", "formal", "negro", "traje", "elegante"]},

    {"id": 41, "name": "Pantalón chino beige hombre", "category": "Ropa Hombre", "subcategory": "Pantalones",
     "description": "Pantalón chino elegante casual", "price": 1750,
     "tags": ["chino", "beige", "elegante", "casual", "oficina"]},

    {"id": 42, "name": "Camisa lino blanca hombre", "category": "Ropa Hombre", "subcategory": "Camisas",
     "description": "Camisa de lino para verano", "price": 1600,
     "tags": ["camisa", "lino", "blanco", "verano", "elegante"]},

    {"id": 43, "name": "Traje gris claro hombre", "category": "Ropa Hombre", "subcategory": "Trajes",
     "description": "Traje completo gris claro", "price": 5200,
     "tags": ["traje", "gris", "formal", "completo", "elegante"]},

    {"id": 44, "name": "Cardigan hombre azul oscuro", "category": "Ropa Hombre", "subcategory": "Ropa de Oficina",
     "description": "Cardigan de lana para oficina", "price": 1800,
     "tags": ["cardigan", "lana", "azul", "oficina", "cómodo"]},

    {"id": 45, "name": "Conjunto camisa pantalón hombre", "category": "Ropa Hombre", "subcategory": "Ropa de Oficina",
     "description": "Conjunto formal camisa y pantalón", "price": 3100,
     "tags": ["conjunto", "formal", "camisa", "pantalón", "oficina"]},

    # ROPA HOMBRE - CASUAL (15 products)
    {"id": 46, "name": "Jean regular fit hombre", "category": "Ropa Hombre", "subcategory": "Jeans",
     "description": "Jean clásico de corte regular", "price": 1600,
     "tags": ["casual", "jean", "denim", "diario", "regular"]},

    {"id": 47, "name": "Remera polo verde hombre", "category": "Ropa Hombre", "subcategory": "Ropa Casual",
     "description": "Polo de algodón piqué", "price": 900,
     "tags": ["polo", "casual", "verde", "diario", "piqué"]},

    {"id": 48, "name": "Buzo capucha negro hombre", "category": "Ropa Hombre", "subcategory": "Ropa Casual",
     "description": "Buzo urbano con capucha", "price": 1400,
     "tags": ["buzo", "casual", "urbano", "negro", "capucha"]},

    {"id": 49, "name": "Bermuda jean hombre", "category": "Ropa Hombre", "subcategory": "Ropa Casual",
     "description": "Bermuda de jean para verano", "price": 1200,
     "tags": ["bermuda", "jean", "verano", "casual", "cómodo"]},

    {"id": 50, "name": "Remera básica gris hombre", "category": "Ropa Hombre", "subcategory": "Ropa Casual",
     "description": "Remera lisa de algodón", "price": 650,
     "tags": ["remera", "básico", "gris", "casual", "algodón"]},

    {"id": 51, "name": "Chaqueta cuero hombre negra", "category": "Ropa Hombre", "subcategory": "Ropa Casual",
     "description": "Chaqueta de cuero estilo biker", "price": 5500,
     "tags": ["chaqueta", "cuero", "urbano", "biker", "negro"]},

    {"id": 52, "name": "Camisa franela cuadros hombre", "category": "Ropa Hombre", "subcategory": "Camisas",
     "description": "Camisa de franela a cuadros", "price": 1300,
     "tags": ["camisa", "franela", "cuadros", "casual", "cómodo"]},

    {"id": 53, "name": "Pantalón cargo hombre verde", "category": "Ropa Hombre", "subcategory": "Pantalones",
     "description": "Pantalón cargo con bolsillos", "price": 1650,
     "tags": ["cargo", "verde", "bolsillos", "casual", "urbano"]},

    {"id": 54, "name": "Sweater cuello redondo hombre", "category": "Ropa Hombre", "subcategory": "Ropa Casual",
     "description": "Sweater básico cuello redondo", "price": 1350,
     "tags": ["sweater", "casual", "cuello redondo", "básico", "cómodo"]},

    {"id": 55, "name": "Jean slim negro hombre", "category": "Ropa Hombre", "subcategory": "Jeans",
     "description": "Jean ajustado negro", "price": 1700,
     "tags": ["jean", "slim", "negro", "ajustado", "casual"]},

    {"id": 56, "name": "Musculosa deportiva hombre", "category": "Ropa Hombre", "subcategory": "Ropa Deportiva",
     "description": "Musculosa para gimnasio", "price": 600,
     "tags": ["musculosa", "deportivo", "gimnasio", "cómodo", "transpirable"]},

    {"id": 57, "name": "Campera rompe viento hombre", "category": "Ropa Hombre", "subcategory": "Ropa Casual",
     "description": "Campera liviana rompe viento", "price": 2100,
     "tags": ["campera", "rompe viento", "liviana", "casual", "deportivo"]},

    {"id": 58, "name": "Pijama hombre franela", "category": "Ropa Hombre", "subcategory": "Ropa Casual",
     "description": "Pijama abrigado de franela", "price": 1500,
     "tags": ["pijama", "dormir", "franela", "abrigado", "cómodo"]},

    {"id": 59, "name": "Short deportivo hombre", "category": "Ropa Hombre", "subcategory": "Ropa Deportiva",
     "description": "Short para entrenamiento", "price": 900,
     "tags": ["short", "deportivo", "entrenamiento", "fitness", "cómodo"]},

    {"id": 60, "name": "Remera cuello redondo blanca", "category": "Ropa Hombre", "subcategory": "Ropa Casual",
     "description": "Remera básica blanca pack x3", "price": 1200,
     "tags": ["remera", "básico", "blanco", "pack", "casual"]},

    # CALZADO (20 products)
    {"id": 61, "name": "Zapatos taco alto mujer negros", "category": "Calzado Mujer", "subcategory": "Zapatos Formales",
     "description": "Stilettos elegantes para oficina", "price": 2200,
     "tags": ["zapatos", "taco", "formal", "oficina", "negro", "elegante"]},

    {"id": 62, "name": "Zapatillas deportivas mujer running", "category": "Calzado Mujer", "subcategory": "Zapatillas",
     "description": "Zapatillas running con amortiguación", "price": 2800,
     "tags": ["zapatillas", "deportivo", "running", "cómodas", "amortiguación"]},

    {"id": 63, "name": "Botas cuero negras mujer", "category": "Calzado Mujer", "subcategory": "Botas",
     "description": "Botas largas de cuero genuino", "price": 3500,
     "tags": ["botas", "cuero", "invierno", "elegante", "negro"]},

    {"id": 64, "name": "Sandalias planas verano mujer", "category": "Calzado Mujer", "subcategory": "Sandalias",
     "description": "Sandalias cómodas para el verano", "price": 1200,
     "tags": ["sandalias", "verano", "planas", "cómodas", "casual"]},

    {"id": 65, "name": "Zapatos vestir hombre cuero", "category": "Calzado Hombre", "subcategory": "Zapatos Formales",
     "description": "Zapatos formales de cuero negro", "price": 2500,
     "tags": ["zapatos", "formal", "cuero", "oficina", "negro"]},

    {"id": 66, "name": "Zapatillas urbanas hombre", "category": "Calzado Hombre", "subcategory": "Zapatillas",
     "description": "Zapatillas casual urbanas", "price": 2400,
     "tags": ["zapatillas", "casual", "urbano", "cómodas", "diario"]},

    {"id": 67, "name": "Mocasines hombre marrón", "category": "Calzado Hombre", "subcategory": "Zapatos Casual",
     "description": "Mocasines de cuero marrón", "price": 2100,
     "tags": ["mocasines", "cuero", "marrón", "casual", "elegante"]},

    {"id": 68, "name": "Zapatos taco bajo mujer", "category": "Calzado Mujer", "subcategory": "Zapatos Formales",
     "description": "Zapatos formales taco bajo", "price": 1900,
     "tags": ["zapatos", "taco bajo", "formal", "cómodo", "oficina"]},

    {"id": 69, "name": "Zapatillas blancas mujer", "category": "Calzado Mujer", "subcategory": "Zapatillas",
     "description": "Zapatillas urbanas blancas", "price": 2200,
     "tags": ["zapatillas", "blanco", "urbano", "casual", "cómodas"]},

    {"id": 70, "name": "Botas trabajo hombre", "category": "Calzado Hombre", "subcategory": "Botas",
     "description": "Botas resistentes para trabajo", "price": 3200,
     "tags": ["botas", "trabajo", "resistentes", "seguridad", "cuero"]},

    {"id": 71, "name": "Sandalias taco mujer", "category": "Calzado Mujer", "subcategory": "Sandalias",
     "description": "Sandalias elegantes con taco", "price": 1800,
     "tags": ["sandalias", "taco", "elegante", "verano", "fiesta"]},

    {"id": 72, "name": "Pantuflas casa mujer", "category": "Calzado Mujer", "subcategory": "Zapatos Casual",
     "description": "Pantuflas cómodas para casa", "price": 800,
     "tags": ["pantuflas", "casa", "cómodas", "descanso", "suave"]},

    {"id": 73, "name": "Zapatillas running profesional", "category": "Deportes", "subcategory": "Calzado Deportivo",
     "description": "Zapatillas técnicas para running", "price": 4200,
     "tags": ["zapatillas", "running", "profesional", "técnicas", "deportivo"]},

    {"id": 74, "name": "Zapatos charol hombre", "category": "Calzado Hombre", "subcategory": "Zapatos Formales",
     "description": "Zapatos de charol para eventos", "price": 2800,
     "tags": ["zapatos", "charol", "formal", "fiesta", "elegante"]},

    {"id": 75, "name": "Borcegos mujer", "category": "Calzado Mujer", "subcategory": "Botas",
     "description": "Borcegos urbanos estilo militar", "price": 2600,
     "tags": ["borcegos", "urbano", "militar", "casual", "resistente"]},

    {"id": 76, "name": "Ojotas hombre playa", "category": "Calzado Hombre", "subcategory": "Zapatos Casual",
     "description": "Ojotas cómodas para playa", "price": 600,
     "tags": ["ojotas", "playa", "verano", "cómodas", "casual"]},

    {"id": 77, "name": "Ballerinas mujer negras", "category": "Calzado Mujer", "subcategory": "Zapatos Casual",
     "description": "Ballerinas planas elegantes", "price": 1500,
     "tags": ["ballerinas", "planas", "elegante", "cómodo", "negro"]},

    {"id": 78, "name": "Zapatillas trekking hombre", "category": "Deportes", "subcategory": "Calzado Deportivo",
     "description": "Zapatillas impermeables para trekking", "price": 3800,
     "tags": ["zapatillas", "trekking", "impermeables", "montaña", "deportivo"]},

    {"id": 79, "name": "Zapatos plataforma mujer", "category": "Calzado Mujer", "subcategory": "Zapatos Casual",
     "description": "Zapatos con plataforma modernos", "price": 2400,
     "tags": ["zapatos", "plataforma", "moderno", "casual", "alto"]},

    {"id": 80, "name": "Zapatillas basket hombre", "category": "Deportes", "subcategory": "Calzado Deportivo",
     "description": "Zapatillas para basketball", "price": 3500,
     "tags": ["zapatillas", "basketball", "deportivo", "alto", "amortiguación"]},

    # ACCESORIOS (15 products)
    {"id": 81, "name": "Cartera cuero marrón ejecutiva", "category": "Accesorios", "subcategory": "Carteras",
     "description": "Cartera ejecutiva de cuero genuino", "price": 3200,
     "tags": ["cartera", "cuero", "ejecutiva", "oficina", "marrón"]},

    {"id": 82, "name": "Cinturón cuero negro hombre", "category": "Accesorios", "subcategory": "Cinturones",
     "description": "Cinturón formal de cuero", "price": 900,
     "tags": ["cinturón", "cuero", "formal", "negro", "elegante"]},

    {"id": 83, "name": "Bufanda lana gris", "category": "Accesorios", "subcategory": "Bufandas",
     "description": "Bufanda tejida de lana merino", "price": 700,
     "tags": ["bufanda", "lana", "invierno", "abrigo", "gris"]},

    {"id": 84, "name": "Reloj ejecutivo plateado", "category": "Accesorios", "subcategory": "Relojes",
     "description": "Reloj de acero inoxidable", "price": 4500,
     "tags": ["reloj", "ejecutivo", "formal", "acero", "plateado"]},

    {"id": 85, "name": "Mochila urbana negra laptop", "category": "Accesorios", "subcategory": "Mochilas",
     "description": "Mochila para laptop y uso diario", "price": 2200,
     "tags": ["mochila", "urbano", "laptop", "diario", "negro"]},

    {"id": 86, "name": "Gafas sol mujer", "category": "Accesorios", "subcategory": "Gafas de Sol",
     "description": "Gafas de sol UV protection", "price": 1500,
     "tags": ["gafas", "sol", "UV", "mujer", "elegante"]},

    {"id": 87, "name": "Maletín ejecutivo cuero", "category": "Accesorios", "subcategory": "Carteras",
     "description": "Maletín para laptop y documentos", "price": 4500,
     "tags": ["maletín", "ejecutivo", "cuero", "trabajo", "laptop"]},

    {"id": 88, "name": "Gorro lana invierno", "category": "Accesorios", "subcategory": "Gorros",
     "description": "Gorro tejido para invierno", "price": 600,
     "tags": ["gorro", "lana", "invierno", "abrigo", "tejido"]},

    {"id": 89, "name": "Guantes cuero hombre", "category": "Accesorios", "subcategory": "Guantes",
     "description": "Guantes de cuero para invierno", "price": 1200,
     "tags": ["guantes", "cuero", "invierno", "elegante", "abrigo"]},

    {"id": 90, "name": "Billetera cuero hombre", "category": "Accesorios", "subcategory": "Carteras",
     "description": "Billetera de cuero genuino", "price": 1100,
     "tags": ["billetera", "cuero", "hombre", "elegante", "práctica"]},

    {"id": 91, "name": "Pañuelo seda mujer", "category": "Accesorios", "subcategory": "Bufandas",
     "description": "Pañuelo de seda estampado", "price": 850,
     "tags": ["pañuelo", "seda", "estampado", "elegante", "mujer"]},

    {"id": 92, "name": "Gorra deportiva ajustable", "category": "Accesorios", "subcategory": "Gorros",
     "description": "Gorra ajustable para deporte", "price": 500,
     "tags": ["gorra", "deportivo", "sol", "casual", "ajustable"]},

    {"id": 93, "name": "Reloj deportivo digital", "category": "Accesorios", "subcategory": "Relojes",
     "description": "Reloj digital para deporte", "price": 2200,
     "tags": ["reloj", "deportivo", "digital", "fitness", "resistente"]},

    {"id": 94, "name": "Cartera pequeña mujer", "category": "Accesorios", "subcategory": "Carteras",
     "description": "Cartera cruzada pequeña", "price": 1800,
     "tags": ["cartera", "pequeña", "cruzada", "casual", "mujer"]},

    {"id": 95, "name": "Gafas sol hombre deportivas", "category": "Accesorios", "subcategory": "Gafas de Sol",
     "description": "Gafas deportivas polarizadas", "price": 1700,
     "tags": ["gafas", "sol", "deportivo", "polarizadas", "hombre"]},

    # DEPORTES (10 products)
    {"id": 96, "name": "Calza deportiva mujer", "category": "Deportes", "subcategory": "Ropa Deportiva",
     "description": "Calza legging para yoga y fitness", "price": 1100,
     "tags": ["deportivo", "yoga", "fitness", "legging", "mujer"]},

    {"id": 97, "name": "Remera técnica running", "category": "Deportes", "subcategory": "Ropa Deportiva",
     "description": "Remera dry-fit para correr", "price": 800,
     "tags": ["running", "deportivo", "técnica", "transpirable", "dry-fit"]},

    {"id": 98, "name": "Top deportivo mujer", "category": "Deportes", "subcategory": "Ropa Deportiva",
     "description": "Top con soporte para entrenamiento", "price": 950,
     "tags": ["top", "deportivo", "soporte", "fitness", "mujer"]},

    {"id": 99, "name": "Campera deportiva hombre", "category": "Deportes", "subcategory": "Ropa Deportiva",
     "description": "Campera técnica para running", "price": 2800,
     "tags": ["campera", "deportivo", "running", "técnica", "impermeable"]},

    {"id": 100, "name": "Medias deportivas pack x3", "category": "Deportes", "subcategory": "Accesorios Deportivos",
     "description": "Pack de medias técnicas", "price": 600,
     "tags": ["medias", "deportivo", "pack", "técnicas", "transpirables"]},

    {"id": 101, "name": "Bolso deportivo gimnasio", "category": "Deportes", "subcategory": "Accesorios Deportivos",
     "description": "Bolso grande para gimnasio", "price": 1600,
     "tags": ["bolso", "gimnasio", "deportivo", "grande", "compartimentos"]},

    {"id": 102, "name": "Guantes gimnasio", "category": "Deportes", "subcategory": "Accesorios Deportivos",
     "description": "Guantes para entrenamiento con pesas", "price": 700,
     "tags": ["guantes", "gimnasio", "pesas", "entrenamiento", "protección"]},

    {"id": 103, "name": "Botella agua deportiva", "category": "Deportes", "subcategory": "Accesorios Deportivos",
     "description": "Botella térmica para deportes", "price": 900,
     "tags": ["botella", "agua", "deportivo", "térmica", "práctica"]},

    {"id": 104, "name": "Conjunto deportivo mujer", "category": "Deportes", "subcategory": "Ropa Deportiva",
     "description": "Conjunto top y calza a juego", "price": 2400,
     "tags": ["conjunto", "deportivo", "mujer", "top", "calza"]},

    {"id": 105, "name": "Short running hombre", "category": "Deportes", "subcategory": "Ropa Deportiva",
     "description": "Short liviano para running", "price": 1000,
     "tags": ["short", "running", "liviano", "deportivo", "transpirable"]},

    # NIÑOS (10 products)
    {"id": 106, "name": "Conjunto bebé celeste", "category": "Niños", "subcategory": "Ropa Bebé",
     "description": "Conjunto de algodón para bebé", "price": 1200,
     "tags": ["bebé", "conjunto", "algodón", "suave", "celeste"]},

    {"id": 107, "name": "Remera infantil estampado superhéroes", "category": "Niños", "subcategory": "Ropa Niño",
     "description": "Remera con estampado de superhéroes", "price": 600,
     "tags": ["niño", "remera", "estampado", "superhéroes", "divertido"]},

    {"id": 108, "name": "Vestido niña flores", "category": "Niños", "subcategory": "Ropa Niña",
     "description": "Vestido floreado para niña", "price": 1400,
     "tags": ["niña", "vestido", "flores", "fiesta", "elegante"]},

    {"id": 109, "name": "Zapatillas luminosas niño LED", "category": "Niños", "subcategory": "Calzado Infantil",
     "description": "Zapatillas con luces LED", "price": 1800,
     "tags": ["zapatillas", "niño", "luces", "LED", "divertidas"]},

    {"id": 110, "name": "Campera abrigo niño", "category": "Niños", "subcategory": "Ropa Niño",
     "description": "Campera abrigada para invierno", "price": 2200,
     "tags": ["campera", "niño", "abrigo", "invierno", "cálida"]},

    {"id": 111, "name": "Jean niña", "category": "Niños", "subcategory": "Ropa Niña",
     "description": "Jean infantil cómodo", "price": 1100,
     "tags": ["jean", "niña", "cómodo", "casual", "resistente"]},

    {"id": 112, "name": "Conjunto deportivo niño", "category": "Niños", "subcategory": "Ropa Deportiva Niños",
     "description": "Conjunto deportivo completo", "price": 1600,
     "tags": ["conjunto", "deportivo", "niño", "cómodo", "práctico"]},

    {"id": 113, "name": "Mochila escolar", "category": "Niños", "subcategory": "Accesorios Niños",
     "description": "Mochila con diseño infantil", "price": 1400,
     "tags": ["mochila", "escolar", "niños", "práctica", "colorida"]},

    {"id": 114, "name": "Pijama niño dinosaurios", "category": "Niños", "subcategory": "Ropa Niño",
     "description": "Pijama con estampado de dinosaurios", "price": 1000,
     "tags": ["pijama", "niño", "dinosaurios", "cómodo", "divertido"]},

    {"id": 115, "name": "Sandalias niña verano", "category": "Niños", "subcategory": "Calzado Infantil",
     "description": "Sandalias cómodas para verano", "price": 900,
     "tags": ["sandalias", "niña", "verano", "cómodas", "frescas"]},

    # HOGAR (5 products)
    {"id": 116, "name": "Juego sábanas matrimonial", "category": "Hogar", "subcategory": "Textiles",
     "description": "Sábanas de algodón 180 hilos", "price": 2500,
     "tags": ["sábanas", "textil", "hogar", "algodón", "matrimonial"]},

    {"id": 117, "name": "Toalla baño grande", "category": "Hogar", "subcategory": "Baño",
     "description": "Toalla de algodón suave", "price": 800,
     "tags": ["toalla", "baño", "algodón", "suave", "grande"]},

    {"id": 118, "name": "Cortina blackout beige", "category": "Hogar", "subcategory": "Decoración",
     "description": "Cortina opaca para dormitorio", "price": 1900,
     "tags": ["cortina", "blackout", "decoración", "dormitorio", "beige"]},

    {"id": 119, "name": "Almohadón decorativo gris", "category": "Hogar", "subcategory": "Decoración",
     "description": "Almohadón para sofá", "price": 600,
     "tags": ["almohadón", "decoración", "sofá", "gris", "moderno"]},

    {"id": 120, "name": "Alfombra sala estar", "category": "Hogar", "subcategory": "Decoración",
     "description": "Alfombra moderna para sala", "price": 3500,
     "tags": ["alfombra", "sala", "decoración", "moderna", "grande"]},
]

# 100 comprehensive search queries
SEARCH_QUERIES = [
    # OFFICE/FORMAL QUERIES (20 queries)
    {"id": 1, "query": "ropa para oficina", "expected_categories": ["Ropa Mujer > Ropa de Oficina", "Ropa Hombre > Ropa de Oficina"], "expected_products": [1, 2, 3, 31, 32]},
    {"id": 2, "query": "traje para trabajo", "expected_categories": ["Ropa Hombre > Trajes"], "expected_products": [33, 43]},
    {"id": 3, "query": "ropa ejecutiva mujer", "expected_categories": ["Ropa Mujer > Ropa de Oficina"], "expected_products": [3, 10, 15]},
    {"id": 4, "query": "vestir formal hombre", "expected_categories": ["Ropa Hombre > Ropa de Oficina", "Ropa Hombre > Trajes"], "expected_products": [31, 32, 33]},
    {"id": 5, "query": "zapatos para la oficina", "expected_categories": ["Calzado Mujer > Zapatos Formales", "Calzado Hombre > Zapatos Formales"], "expected_products": [61, 65]},
    {"id": 6, "query": "camisa blanca formal", "expected_categories": ["Ropa Mujer > Ropa de Oficina", "Ropa Hombre > Ropa de Oficina"], "expected_products": [1, 31]},
    {"id": 7, "query": "pantalón de vestir", "expected_categories": ["Ropa Mujer > Ropa de Oficina", "Ropa Hombre > Ropa de Oficina"], "expected_products": [2, 32, 36]},
    {"id": 8, "query": "blazer mujer", "expected_categories": ["Ropa Mujer > Ropa de Oficina"], "expected_products": [3, 10]},
    {"id": 9, "query": "traje completo", "expected_categories": ["Ropa Hombre > Trajes"], "expected_products": [33, 43]},
    {"id": 10, "query": "ropa negra formal", "expected_categories": ["Ropa Mujer > Ropa de Oficina", "Ropa Hombre > Ropa de Oficina"], "expected_products": [2, 10, 36]},
    {"id": 11, "query": "corbata elegante", "expected_categories": ["Accesorios"], "expected_products": [34]},
    {"id": 12, "query": "vestido para trabajo", "expected_categories": ["Ropa Mujer > Vestidos"], "expected_products": [4, 11]},
    {"id": 13, "query": "saco sport hombre", "expected_categories": ["Ropa Hombre > Ropa de Oficina"], "expected_products": [37]},
    {"id": 14, "query": "blusa seda oficina", "expected_categories": ["Ropa Mujer > Blusas"], "expected_products": [5, 13]},
    {"id": 15, "query": "zapatos taco mujer", "expected_categories": ["Calzado Mujer > Zapatos Formales"], "expected_products": [61]},
    {"id": 16, "query": "conjunto ejecutivo", "expected_categories": ["Ropa Mujer > Ropa de Oficina", "Ropa Hombre > Ropa de Oficina"], "expected_products": [15, 45]},
    {"id": 17, "query": "maletín trabajo", "expected_categories": ["Accesorios > Carteras"], "expected_products": [87]},
    {"id": 18, "query": "sweater oficina", "expected_categories": ["Ropa Mujer > Ropa de Oficina", "Ropa Hombre > Ropa de Oficina"], "expected_products": [7, 38]},
    {"id": 19, "query": "falda formal", "expected_categories": ["Ropa Mujer > Faldas"], "expected_products": [6]},
    {"id": 20, "query": "chaleco traje", "expected_categories": ["Ropa Hombre > Ropa de Oficina"], "expected_products": [40]},

    # CASUAL/DAILY QUERIES (20 queries)
    {"id": 21, "query": "ropa casual diaria", "expected_categories": ["Ropa Mujer > Ropa Casual", "Ropa Hombre > Ropa Casual"], "expected_products": [16, 17, 46, 47]},
    {"id": 22, "query": "jean mujer", "expected_categories": ["Ropa Mujer > Jeans"], "expected_products": [16, 26]},
    {"id": 23, "query": "jean hombre", "expected_categories": ["Ropa Hombre > Jeans"], "expected_products": [46, 55]},
    {"id": 24, "query": "remera básica", "expected_categories": ["Ropa Mujer > Ropa Casual", "Ropa Hombre > Ropa Casual"], "expected_products": [17, 50]},
    {"id": 25, "query": "buzo con capucha", "expected_categories": ["Ropa Hombre > Ropa Casual"], "expected_products": [48]},
    {"id": 26, "query": "vestido casual", "expected_categories": ["Ropa Mujer > Vestidos"], "expected_products": [18, 24]},
    {"id": 27, "query": "campera jean", "expected_categories": ["Ropa Mujer > Ropa Casual"], "expected_products": [19]},
    {"id": 28, "query": "pantalón cómodo", "expected_categories": ["Ropa Mujer > Ropa Casual", "Ropa Hombre > Ropa Casual"], "expected_products": [28, 53]},
    {"id": 29, "query": "remera polo", "expected_categories": ["Ropa Hombre > Ropa Casual"], "expected_products": [47]},
    {"id": 30, "query": "short verano", "expected_categories": ["Ropa Mujer > Ropa Casual", "Ropa Hombre > Ropa Casual"], "expected_products": [23, 49]},
    {"id": 31, "query": "sweater tejido", "expected_categories": ["Ropa Mujer > Ropa Casual", "Ropa Hombre > Ropa Casual"], "expected_products": [25, 54]},
    {"id": 32, "query": "legging negro", "expected_categories": ["Ropa Mujer > Ropa Casual"], "expected_products": [21]},
    {"id": 33, "query": "chaqueta cuero", "expected_categories": ["Ropa Hombre > Ropa Casual"], "expected_products": [51]},
    {"id": 34, "query": "camisa cuadros", "expected_categories": ["Ropa Hombre > Camisas"], "expected_products": [52]},
    {"id": 35, "query": "pantalón cargo", "expected_categories": ["Ropa Hombre > Pantalones"], "expected_products": [53]},
    {"id": 36, "query": "ropa para dormir", "expected_categories": ["Ropa Mujer > Ropa Casual", "Ropa Hombre > Ropa Casual"], "expected_products": [29, 58]},
    {"id": 37, "query": "vestido floreado", "expected_categories": ["Ropa Mujer > Vestidos"], "expected_products": [18]},
    {"id": 38, "query": "musculosa básica", "expected_categories": ["Ropa Mujer > Ropa Casual", "Ropa Hombre > Ropa Deportiva"], "expected_products": [27, 56]},
    {"id": 39, "query": "pantalón jogger", "expected_categories": ["Ropa Mujer > Ropa Casual"], "expected_products": [28]},
    {"id": 40, "query": "chomba casual", "expected_categories": ["Ropa Mujer > Ropa Casual"], "expected_products": [30]},

    # SPORTS/FITNESS QUERIES (15 queries)
    {"id": 41, "query": "ropa deportiva", "expected_categories": ["Deportes > Ropa Deportiva"], "expected_products": [96, 97, 99]},
    {"id": 42, "query": "zapatillas running", "expected_categories": ["Deportes > Calzado Deportivo", "Calzado Mujer > Zapatillas"], "expected_products": [62, 73]},
    {"id": 43, "query": "ropa para gimnasio", "expected_categories": ["Deportes > Ropa Deportiva"], "expected_products": [96, 98, 104]},
    {"id": 44, "query": "calza yoga", "expected_categories": ["Deportes > Ropa Deportiva"], "expected_products": [96]},
    {"id": 45, "query": "equipamiento deportivo", "expected_categories": ["Deportes > Equipamiento"], "expected_products": [100, 101, 102]},
    {"id": 46, "query": "remera técnica", "expected_categories": ["Deportes > Ropa Deportiva"], "expected_products": [97]},
    {"id": 47, "query": "short running", "expected_categories": ["Ropa Hombre > Ropa Deportiva", "Deportes > Ropa Deportiva"], "expected_products": [59, 105]},
    {"id": 48, "query": "top deportivo", "expected_categories": ["Deportes > Ropa Deportiva"], "expected_products": [98]},
    {"id": 49, "query": "campera deportiva", "expected_categories": ["Deportes > Ropa Deportiva"], "expected_products": [99]},
    {"id": 50, "query": "conjunto deportivo", "expected_categories": ["Deportes > Ropa Deportiva"], "expected_products": [104]},
    {"id": 51, "query": "zapatillas trekking", "expected_categories": ["Deportes > Calzado Deportivo"], "expected_products": [78]},
    {"id": 52, "query": "bolso gimnasio", "expected_categories": ["Deportes > Accesorios Deportivos"], "expected_products": [101]},
    {"id": 53, "query": "guantes entrenamiento", "expected_categories": ["Deportes > Accesorios Deportivos"], "expected_products": [102]},
    {"id": 54, "query": "medias deportivas", "expected_categories": ["Deportes > Accesorios Deportivos"], "expected_products": [100]},
    {"id": 55, "query": "zapatillas basketball", "expected_categories": ["Deportes > Calzado Deportivo"], "expected_products": [80]},

    # FOOTWEAR QUERIES (15 queries)
    {"id": 56, "query": "zapatos elegantes", "expected_categories": ["Calzado Mujer > Zapatos Formales", "Calzado Hombre > Zapatos Formales"], "expected_products": [61, 65]},
    {"id": 57, "query": "zapatillas cómodas", "expected_categories": ["Calzado Mujer > Zapatillas", "Calzado Hombre > Zapatillas"], "expected_products": [62, 66, 69]},
    {"id": 58, "query": "botas mujer", "expected_categories": ["Calzado Mujer > Botas"], "expected_products": [63, 75]},
    {"id": 59, "query": "sandalias verano", "expected_categories": ["Calzado Mujer > Sandalias"], "expected_products": [64, 71]},
    {"id": 60, "query": "calzado deportivo", "expected_categories": ["Deportes > Calzado Deportivo", "Calzado Mujer > Zapatillas"], "expected_products": [62, 73, 78]},
    {"id": 61, "query": "mocasines cuero", "expected_categories": ["Calzado Hombre > Zapatos Casual"], "expected_products": [67]},
    {"id": 62, "query": "zapatos taco bajo", "expected_categories": ["Calzado Mujer > Zapatos Formales"], "expected_products": [68]},
    {"id": 63, "query": "zapatillas blancas", "expected_categories": ["Calzado Mujer > Zapatillas"], "expected_products": [69]},
    {"id": 64, "query": "botas trabajo", "expected_categories": ["Calzado Hombre > Botas"], "expected_products": [70]},
    {"id": 65, "query": "ballerinas planas", "expected_categories": ["Calzado Mujer > Zapatos Casual"], "expected_products": [77]},
    {"id": 66, "query": "zapatos charol", "expected_categories": ["Calzado Hombre > Zapatos Formales"], "expected_products": [74]},
    {"id": 67, "query": "ojotas playa", "expected_categories": ["Calzado Hombre > Zapatos Casual"], "expected_products": [76]},
    {"id": 68, "query": "pantuflas casa", "expected_categories": ["Calzado Mujer > Zapatos Casual"], "expected_products": [72]},
    {"id": 69, "query": "borcegos urbanos", "expected_categories": ["Calzado Mujer > Botas"], "expected_products": [75]},
    {"id": 70, "query": "zapatos plataforma", "expected_categories": ["Calzado Mujer > Zapatos Casual"], "expected_products": [79]},

    # ACCESSORIES QUERIES (12 queries)
    {"id": 71, "query": "accesorios para oficina", "expected_categories": ["Accesorios > Carteras"], "expected_products": [81, 87]},
    {"id": 72, "query": "cartera de cuero", "expected_categories": ["Accesorios > Carteras"], "expected_products": [81, 87]},
    {"id": 73, "query": "accesorios elegantes", "expected_categories": ["Accesorios > Joyas", "Accesorios > Relojes"], "expected_products": [84]},
    {"id": 74, "query": "mochila para laptop", "expected_categories": ["Accesorios > Mochilas"], "expected_products": [85]},
    {"id": 75, "query": "bufanda lana", "expected_categories": ["Accesorios > Bufandas"], "expected_products": [83]},
    {"id": 76, "query": "reloj ejecutivo", "expected_categories": ["Accesorios > Relojes"], "expected_products": [84]},
    {"id": 77, "query": "gafas de sol", "expected_categories": ["Accesorios > Gafas de Sol"], "expected_products": [86, 95]},
    {"id": 78, "query": "cinturón cuero", "expected_categories": ["Accesorios > Cinturones"], "expected_products": [82]},
    {"id": 79, "query": "billetera hombre", "expected_categories": ["Accesorios > Carteras"], "expected_products": [90]},
    {"id": 80, "query": "gorro invierno", "expected_categories": ["Accesorios > Gorros"], "expected_products": [88]},
    {"id": 81, "query": "guantes cuero", "expected_categories": ["Accesorios > Guantes"], "expected_products": [89]},
    {"id": 82, "query": "gorra deportiva", "expected_categories": ["Accesorios > Gorros"], "expected_products": [92]},

    # KIDS QUERIES (8 queries)
    {"id": 83, "query": "ropa para bebé", "expected_categories": ["Niños > Ropa Bebé"], "expected_products": [106]},
    {"id": 84, "query": "ropa infantil", "expected_categories": ["Niños > Ropa Niño", "Niños > Ropa Niña"], "expected_products": [107, 108]},
    {"id": 85, "query": "zapatillas para niños", "expected_categories": ["Niños > Calzado Infantil"], "expected_products": [109]},
    {"id": 86, "query": "vestido niña fiesta", "expected_categories": ["Niños > Ropa Niña"], "expected_products": [108]},
    {"id": 87, "query": "campera niño abrigo", "expected_categories": ["Niños > Ropa Niño"], "expected_products": [110]},
    {"id": 88, "query": "mochila escolar", "expected_categories": ["Niños > Accesorios Niños"], "expected_products": [113]},
    {"id": 89, "query": "conjunto deportivo niño", "expected_categories": ["Niños > Ropa Deportiva Niños"], "expected_products": [112]},
    {"id": 90, "query": "pijama infantil", "expected_categories": ["Niños > Ropa Niño"], "expected_products": [114]},

    # HOME QUERIES (5 queries)
    {"id": 91, "query": "textiles para el hogar", "expected_categories": ["Hogar > Textiles"], "expected_products": [116]},
    {"id": 92, "query": "decoración dormitorio", "expected_categories": ["Hogar > Decoración"], "expected_products": [118, 119]},
    {"id": 93, "query": "sábanas matrimonial", "expected_categories": ["Hogar > Textiles"], "expected_products": [116]},
    {"id": 94, "query": "toallas de baño", "expected_categories": ["Hogar > Baño"], "expected_products": [117]},
    {"id": 95, "query": "alfombra sala", "expected_categories": ["Hogar > Decoración"], "expected_products": [120]},

    # MIXED/COMPLEX QUERIES (5 queries)
    {"id": 96, "query": "regalo ejecutivo", "expected_categories": ["Accesorios > Relojes", "Accesorios > Carteras"], "expected_products": [84, 87]},
    {"id": 97, "query": "look profesional", "expected_categories": ["Ropa Mujer > Ropa de Oficina", "Ropa Hombre > Ropa de Oficina"], "expected_products": [3, 15, 31, 33]},
    {"id": 98, "query": "outfit casual urbano", "expected_categories": ["Ropa Mujer > Ropa Casual", "Ropa Hombre > Ropa Casual"], "expected_products": [16, 19, 46, 51]},
    {"id": 99, "query": "estilo deportivo", "expected_categories": ["Deportes > Ropa Deportiva"], "expected_products": [96, 97, 99, 104]},
    {"id": 100, "query": "ropa invierno abrigo", "expected_categories": ["Accesorios > Bufandas"], "expected_products": [83, 88, 89]},
]

print(f"Loaded {len(PRODUCTS)} products across {len(CATEGORIES)} categories with {len(SEARCH_QUERIES)} test queries")
