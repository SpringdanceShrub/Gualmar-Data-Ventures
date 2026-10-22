import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


df = pd.read_csv('dataset/inventario_gualmart.csv')


print('PRIMERAS 5 FILAS')
print(df.head())

print('\nULTIMAS 5 FILAS')
print(df.tail())

print('\nDIMENSIONES DEL INVENTARIO')
print(df.shape)

print('\nNOMBRES DE LAS COLUMNAS')
print(df.columns)

print('\nTIPOS DE DATOS')
print(df.dtypes)

print('\nINFORMACION GENERAL')
df.info()

print('\nESTADISTICAS BASICAS')
print(df.describe())


#Interfaz grafica con PyQt5 y Matplotlib
class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Inventario Gualmart')
        self.resize(900, 700)

        stock_sucursal = df.groupby('sucursal')['cantidad'].sum()
        valor_categoria = df.groupby('categoria')['valor_inventario_usd'].sum()

        self.figura = Figure(figsize=(8, 7))
        self.canvas = FigureCanvas(self.figura)

        ax1 = self.figura.add_subplot(211)
        ax1.bar(stock_sucursal.index, stock_sucursal.values)
        ax1.set_title('Cantidad total de productos por sucursal')
        ax1.set_xlabel('Sucursal')
        ax1.set_ylabel('Cantidad')
        ax1.tick_params(axis='x', rotation=15)

        ax2 = self.figura.add_subplot(212)
        ax2.bar(valor_categoria.index, valor_categoria.values)
        ax2.set_title('Valor del inventario por categoria')
        ax2.set_xlabel('Categoria')
        ax2.set_ylabel('Valor en USD')
        ax2.tick_params(axis='x', rotation=45)

        self.figura.tight_layout()

        texto = QLabel(
            'Registros: ' + str(df.shape[0]) +
            '   |   Columnas: ' + str(df.shape[1]) +
            '   |   Sucursales: ' + str(df['sucursal'].nunique())
        )

        layout = QVBoxLayout()
        layout.addWidget(texto)
        layout.addWidget(self.canvas)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

# Bloque principal de ejecución de la aplicación
app = QApplication(sys.argv)
ventana = Ventana()
ventana.show()
sys.exit(app.exec_())