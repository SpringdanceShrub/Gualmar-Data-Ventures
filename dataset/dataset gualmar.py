import argparse
import csv
import random
from collections import Counter
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

SUCURSALES = ["San Salvador", "Santa Ana", "San Miguel", "La Libertad", "Sonsonate"]
FECHA_CORTE = "2026-10-22"

CATALOGO = """Abarrotes|Arroz blanco|Suli|Bolsa 1 kg|1.65
Abarrotes|Frijol rojo|Suli|Bolsa 900 g|2.20
Abarrotes|Azúcar blanca|La Cabaña|Bolsa 1 kg|1.10
Abarrotes|Sal yodada|Suli|Bolsa 454 g|0.45
Abarrotes|Harina de maíz|Maseca|Bolsa 1 kg|1.55
Abarrotes|Pasta espagueti|Ina|Paquete 200 g|0.65
Abarrotes|Aceite vegetal|Mazola|Botella 900 ml|2.75
Abarrotes|Avena en hojuelas|Quaker|Bolsa 400 g|2.10
Abarrotes|Atún en agua|Sardimar|Lata 140 g|1.60
Abarrotes|Salsa de tomate|Natura's|Doypack 200 g|0.75
Bebidas|Agua purificada|Cristal|Botella 1.5 L|0.70
Bebidas|Gaseosa cola|Coca-Cola|Botella 2 L|2.15
Bebidas|Gaseosa de limón|Sprite|Botella 1.5 L|1.65
Bebidas|Jugo de naranja|Del Valle|Caja 1 L|1.95
Bebidas|Néctar de durazno|Del Frutal|Lata 330 ml|0.60
Bebidas|Café molido|Musun|Bolsa 400 g|4.25
Bebidas|Café instantáneo|Nescafé|Frasco 100 g|4.50
Bebidas|Té de manzanilla|McCormick|Caja 20 sobres|2.15
Bebidas|Bebida deportiva|Gatorade|Botella 600 ml|1.30
Bebidas|Agua mineral|Salutaris|Botella 600 ml|0.90
Lácteos y huevos|Leche entera UHT|Salud|Caja 1 L|1.65
Lácteos y huevos|Leche descremada UHT|Dos Pinos|Caja 1 L|1.85
Lácteos y huevos|Yogur de fresa|Yes|Vaso 125 g|0.65
Lácteos y huevos|Yogur natural|Dos Pinos|Envase 1 L|3.75
Lácteos y huevos|Queso fresco|Petacones|Paquete 400 g|3.50
Lácteos y huevos|Queso mozzarella|Dos Pinos|Paquete 400 g|4.75
Lácteos y huevos|Crema láctea|Salud|Bolsa 400 ml|2.25
Lácteos y huevos|Mantequilla con sal|Dos Pinos|Barra 115 g|1.80
Lácteos y huevos|Huevos blancos|El Granjero|Cartón 30 unidades|5.25
Lácteos y huevos|Leche condensada|La Lechera|Lata 395 g|2.15
Frutas y verduras|Manzana roja|Gualmart Frescos|Bolsa 4 unidades|2.25
Frutas y verduras|Banano|Gualmart Frescos|Bolsa 1 kg|1.10
Frutas y verduras|Naranja|Gualmart Frescos|Malla 6 unidades|1.75
Frutas y verduras|Limón|Gualmart Frescos|Malla 12 unidades|1.50
Frutas y verduras|Tomate de cocina|Gualmart Frescos|Bandeja 500 g|0.95
Frutas y verduras|Cebolla blanca|Gualmart Frescos|Malla 1 kg|1.45
Frutas y verduras|Papa blanca|Gualmart Frescos|Bolsa 1 kg|1.60
Frutas y verduras|Zanahoria|Gualmart Frescos|Bolsa 500 g|0.75
Frutas y verduras|Lechuga romana|Gualmart Frescos|Unidad empacada|0.85
Frutas y verduras|Pepino|Gualmart Frescos|Paquete 3 unidades|1.00
Carnes y congelados|Pechuga de pollo|Pollo Indio|Bandeja 1 kg|5.25
Carnes y congelados|Muslos de pollo|Pollo Indio|Bandeja 1 kg|3.90
Carnes y congelados|Carne molida de res|Gualmart Frescos|Bandeja 500 g|4.25
Carnes y congelados|Lomo de cerdo|Gualmart Frescos|Bandeja 500 g|3.75
Carnes y congelados|Filete de tilapia|Gualmart Frescos|Bolsa 500 g|4.90
Carnes y congelados|Camarón congelado|Gualmart Frescos|Bolsa 400 g|6.50
Carnes y congelados|Nuggets de pollo|Toledo|Bolsa 400 g|3.95
Carnes y congelados|Papas congeladas|McCain|Bolsa 750 g|3.50
Carnes y congelados|Vegetales mixtos congelados|Great Value|Bolsa 500 g|2.25
Carnes y congelados|Helado de vainilla|Sarita|Envase 1 L|4.25
Panadería y snacks|Pan de caja blanco|Bimbo|Bolsa 560 g|2.10
Panadería y snacks|Pan integral|Bimbo|Bolsa 560 g|2.75
Panadería y snacks|Tortillas de harina|Tía Rosa|Paquete 10 unidades|1.65
Panadería y snacks|Galletas de chocolate|Oreo|Paquete 144 g|1.20
Panadería y snacks|Galletas saladas|Pozuelo|Paquete 240 g|1.45
Panadería y snacks|Papas fritas|Lay's|Bolsa 150 g|1.85
Panadería y snacks|Nachos de queso|Doritos|Bolsa 150 g|1.85
Panadería y snacks|Cereal de maíz|Kellogg's|Caja 300 g|3.65
Panadería y snacks|Chocolate con leche|Hershey's|Barra 43 g|1.10
Panadería y snacks|Maní salado|Diana|Bolsa 150 g|1.25
Limpieza|Detergente en polvo|Rinso|Bolsa 1 kg|2.75
Limpieza|Detergente líquido|Ariel|Botella 1 L|4.25
Limpieza|Suavizante de ropa|Downy|Botella 800 ml|2.95
Limpieza|Cloro|Magia Blanca|Botella 1 L|1.10
Limpieza|Desinfectante de pisos|Fabuloso|Botella 1 L|1.95
Limpieza|Lavaplatos líquido|Axion|Botella 750 ml|2.15
Limpieza|Esponjas para platos|Scotch-Brite|Paquete 3 unidades|1.75
Limpieza|Bolsas para basura|Great Value|Paquete 20 unidades|2.45
Limpieza|Limpiavidrios|Windex|Atomizador 650 ml|3.25
Limpieza|Escoba multiusos|Suli|Unidad|3.50
Cuidado personal|Champú hidratante|Pantene|Botella 400 ml|4.95
Cuidado personal|Acondicionador|Sedal|Botella 340 ml|3.75
Cuidado personal|Jabón de tocador|Dove|Paquete 3 barras|3.25
Cuidado personal|Pasta dental|Colgate|Tubo 150 ml|2.65
Cuidado personal|Cepillo dental|Oral-B|Unidad|1.85
Cuidado personal|Desodorante en barra|Rexona|Barra 50 g|3.25
Cuidado personal|Papel higiénico|Scott|Paquete 12 rollos|5.75
Cuidado personal|Toallas sanitarias|Saba|Paquete 10 unidades|1.75
Cuidado personal|Pañales talla M|Huggies|Paquete 40 unidades|10.95
Cuidado personal|Protector solar FPS 50|Nivea|Tubo 200 ml|12.50
Hogar y cocina|Sartén antiadherente|Mainstays|Unidad 24 cm|12.95
Hogar y cocina|Olla con tapa|Mainstays|Unidad 3 L|17.50
Hogar y cocina|Vasos de vidrio|Crisa|Juego 6 unidades|6.95
Hogar y cocina|Platos de cerámica|Mainstays|Juego 4 unidades|9.95
Hogar y cocina|Cubiertos de acero|Mainstays|Juego 16 piezas|8.50
Hogar y cocina|Recipientes herméticos|Great Value|Juego 3 unidades|4.75
Hogar y cocina|Toalla de baño|Mainstays|Unidad 70 x 140 cm|6.50
Hogar y cocina|Almohada estándar|Mainstays|Unidad|7.95
Hogar y cocina|Sábanas matrimoniales|Mainstays|Juego 3 piezas|19.95
Hogar y cocina|Bombilla LED|Philips|Unidad 9 W|2.50
Electrónica y electrodomésticos|Audífonos alámbricos|Sony|Unidad|12.95
Electrónica y electrodomésticos|Audífonos Bluetooth|JBL|Unidad|39.95
Electrónica y electrodomésticos|Cable USB-C|Onn|Unidad 1 m|4.95
Electrónica y electrodomésticos|Cargador USB|Onn|Unidad 20 W|9.95
Electrónica y electrodomésticos|Memoria USB|Kingston|Unidad 64 GB|7.95
Electrónica y electrodomésticos|Mouse inalámbrico|Logitech|Unidad|14.95
Electrónica y electrodomésticos|Licuadora|Oster|Unidad 1.5 L|49.95
Electrónica y electrodomésticos|Cafetera de goteo|Black+Decker|Unidad 12 tazas|29.95
Electrónica y electrodomésticos|Plancha de vapor|Oster|Unidad|24.95
Electrónica y electrodomésticos|Ventilador de pedestal|Durabrand|Unidad 16 pulgadas|34.95
Ropa y accesorios|Camiseta blanca talla M|George|Unidad|5.95
Ropa y accesorios|Camiseta negra talla L|George|Unidad|5.95
Ropa y accesorios|Blusa beige talla M|George|Unidad|9.95
Ropa y accesorios|Pantalón de mezclilla talla 30|George|Unidad|18.95
Ropa y accesorios|Pantalón deportivo talla L|Athletic Works|Unidad|12.95
Ropa y accesorios|Calcetines talla 35-39|George|Paquete 3 pares|4.50
Ropa y accesorios|Pijama talla M|George|Juego 2 piezas|14.95
Ropa y accesorios|Sandalias talla 38|George|Par|7.95
Ropa y accesorios|Gorra ajustable|Athletic Works|Unidad|5.50
Ropa y accesorios|Mochila escolar|Onn|Unidad|16.95
Mascotas y jardín|Alimento para perro adulto|Dog Chow|Bolsa 2 kg|7.95
Mascotas y jardín|Alimento para gato adulto|Cat Chow|Bolsa 1.5 kg|8.50
Mascotas y jardín|Alimento húmedo para gato|Whiskas|Sobre 85 g|0.75
Mascotas y jardín|Arena para gato|Great Value|Bolsa 4 kg|5.95
Mascotas y jardín|Champú para perro|Hartz|Botella 532 ml|5.25
Mascotas y jardín|Plato para mascota|Mainstays|Unidad 500 ml|2.50
Mascotas y jardín|Maceta plástica|Mainstays|Unidad 20 cm|2.95
Mascotas y jardín|Tierra abonada|Gualmart Jardín|Bolsa 5 kg|3.50
Mascotas y jardín|Manguera de jardín|Mainstays|Unidad 15 m|14.95
Mascotas y jardín|Regadera de jardín|Mainstays|Unidad 5 L|6.95"""

COLUMNAS = [
    "id_inventario", "sucursal", "sku", "producto", "categoria", "marca",
    "presentacion", "cantidad", "stock_minimo", "costo_unitario_usd",
    "precio_venta_usd", "valor_inventario_usd", "estado_stock", "fecha_corte",
]


def dinero(valor):
    return Decimal(valor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def generar_inventario(semilla=42, fecha_corte=FECHA_CORTE):
    """Una fila por SKU y sucursal; cantidad = presentaciones completas."""
    date.fromisoformat(fecha_corte)
    rng = random.Random(semilla)
    catalogo = []
    for numero, linea in enumerate(CATALOGO.strip().splitlines(), start=1):
        categoria, producto, marca, presentacion, precio = linea.split("|")
        precio = dinero(precio)
        costo = dinero(precio * Decimal(rng.randint(65, 85)) / 100)
        minimo = 5 if precio >= 20 else (10 if precio >= 5 else 20)
        catalogo.append((f"GUA-{numero:04d}", producto, categoria, marca,
                         presentacion, precio, costo, minimo))

    filas = []
    factores = [1.35, 1.00, 1.10, 1.20, 0.90]
    for sucursal, factor in zip(SUCURSALES, factores):
        for sku, producto, categoria, marca, presentacion, precio, costo, minimo in catalogo:
            escenario = rng.random()
            if escenario < 0.05:
                cantidad = 0
            elif escenario < 0.20:
                cantidad = rng.randint(1, minimo)
            else:
                cantidad = rng.randint(minimo + 1, max(minimo + 1, int(minimo * 8 * factor)))
            estado = "Agotado" if cantidad == 0 else (
                "Stock bajo" if cantidad <= minimo else "Disponible")
            filas.append({
                "id_inventario": f"INV-{len(filas) + 1:05d}",
                "sucursal": sucursal, "sku": sku, "producto": producto,
                "categoria": categoria, "marca": marca, "presentacion": presentacion,
                "cantidad": cantidad, "stock_minimo": minimo,
                "costo_unitario_usd": format(costo, ".2f"),
                "precio_venta_usd": format(precio, ".2f"),
                "valor_inventario_usd": format(dinero(costo * cantidad), ".2f"),
                "estado_stock": estado, "fecha_corte": fecha_corte,
            })
    return filas


def guardar_csv(filas, destino):
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", encoding="utf-8-sig", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        escritor.writeheader()
        escritor.writerows(filas)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", default="inventario_gualmart.csv")
    parser.add_argument("--semilla", type=int, default=42)
    parser.add_argument("--fecha-corte", default=FECHA_CORTE)
    args = parser.parse_args()
    filas = generar_inventario(args.semilla, args.fecha_corte)
    guardar_csv(filas, args.salida)
    print(f"Archivo generado: {Path(args.salida).resolve()}")
    print(f"Registros: {len(filas)} | Columnas: {len(COLUMNAS)}")
    for sucursal, cantidad in Counter(fila["sucursal"] for fila in filas).items():
        print(f"  {sucursal}: {cantidad} registros")


if __name__ == "__main__":
    main()
