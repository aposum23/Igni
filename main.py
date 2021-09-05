import folium
import geopandas as gpd
import shapely.wkt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
from misha_funcs import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(180, 10, 600, 20))
        self.label.setObjectName("label")

        self.Poligone = QtWidgets.QLineEdit(self.centralwidget)
        self.Poligone.setGeometry(QtCore.QRect(200, 40, 400, 25))
        self.Poligone.setObjectName("Poligone")

        self.Calculate = QtWidgets.QPushButton(self.centralwidget)
        self.Calculate.setGeometry(QtCore.QRect(630, 40, 150, 25))
        self.Calculate.setObjectName("Calculate")

        self.Delete = QtWidgets.QPushButton(self.centralwidget)
        self.Delete.setGeometry(QtCore.QRect(20, 40, 150, 25))
        self.Delete.setObjectName("Delete")

        self.Map = QWebView(self.centralwidget)
        self.Map.setGeometry(QtCore.QRect(10, 80, 781, 471))
        self.Map.setObjectName("Map")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.calculate_func()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Игни - умный помошник для тушения пожаров"))
        self.label.setText(_translate("MainWindow",
                                      "<html><head/><body><p>Введите данные полигона в формате y0 x0, y1 x1, ..., "
                                      "yn xn:</p></body></html>"))
        self.Calculate.setText(_translate("MainWindow", "Расчитать"))
        self.Delete.setText(_translate("MainWindow", "Очистить"))
        # self.Map.setTitle(_translate("MainWindow", "Карта"))

    def calculate_func(self):
        self.Calculate.clicked.connect(lambda: self.make_map(self.Poligone.text()))
        self.Delete.clicked.connect(lambda: self.Poligone.clear())

    def make_map(self, txt):
        cord_arr = CalculateSqr(txt)
        cord_str = ''
        i = 0
        while i < len(cord_arr):
            cord_str += cord_arr[i]
            if len(cord_arr) - i > 1:
                cord_str += ','
            i += 1
        temp_txt = "POLYGON((" + cord_str + "))"
        print(temp_txt)
        status = True
        p = 0
        try:
            p = shapely.wkt.loads(temp_txt)
        except Exception as e:
            status = False
        if status:
            sim_geo = gpd.GeoSeries(p)
            cord = [sim_geo.centroid.y, sim_geo.centroid.x]
            m = folium.Map(location=cord, zoom_start=11, tiles="Stamen Terrain")
            geo_j = sim_geo.to_json()
            geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'red'})
            geo_j.add_to(m)
            m.save("map1.html")
            html = open("map1.html", 'r').read()
        else:
            html = open("error.html", 'r', encoding="utf-8").read()

        self.Map.setHtml(html)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

