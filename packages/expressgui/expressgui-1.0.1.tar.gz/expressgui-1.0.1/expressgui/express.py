#!/usr/bin/env python

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
import subprocess
import urllib.request, urllib.parse, urllib.error
import pandas as pd
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.path = os.path.dirname(os.path.abspath(__file__))
        self.files = self.path + '/files/'

        uic.loadUi(self.path + '/design2.ui', self)

        self.setWindowIcon(QIcon(self.files + 'expressvpn3.png'))

        self.configuration()
        self.tray()
        self.create_serverlist()
        self.server_combo()
        self.checkstatus()
        self.statusdetail()
        self.seticon()
        self.autoconnect()
        self.showapp()
        self.check_network()
        self.version()

    def configuration(self):
        self.settings = QSettings(self.path + '/' + 'setting.ini', QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)

        self.autoconn = self.settings.value('auto')
        self.showapp2 = self.settings.value('showapp')

        if self.autoconn == 'true':
            self.settings.setValue('auto', self.chB_auto.setChecked(True))

        if self.showapp2 == 'true':
            self.settings.setValue('showapp', self.chB_showapp.setChecked(True))

    def tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.tray_icon.show()
        self.tray_icon.setIcon(QIcon(self.files + "expressvpn3.png"))
        show_action = QAction("Show", self)
        hide_action = QAction("Hide", self)
        disconnect_action = QAction("Disconnect", self)
        checkstatus_action = QAction("Status", self)
        quit_action = QAction("Exit", self)

        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        disconnect_action.triggered.connect(self.disconnect)
        checkstatus_action.triggered.connect(self.statusdetail)
        quit_action.triggered.connect(qApp.quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addSeparator()
        tray_menu.addAction(checkstatus_action)
        tray_menu.addAction(disconnect_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def create_serverlist(self):
        self.server = pd.read_csv(self.files + 'express.csv')
        self.server = self.server.set_index(['alias'])
        self.server = self.server.sort_index()
        self.server['path'] = self.files
        self.server['icon2'] = self.server['path'] + self.server['icon']

    def server_combo(self):
        self.create_serverlist()
        self.subset = self.server[['location', 'icon2']]
        self.tuples = [tuple(x) for x in self.subset.values]

        for i in self.tuples:
            text, icon = i[0], i[1]
            self.cB_Server.addItem(QIcon(icon), text)

        self.combo_loc = str(self.cB_Server.currentText())
        self.combo_alias = (self.server[self.server.location == self.combo_loc].index[0])

    def checkstatus(self):
        statuscheck = '/usr/bin/expressvpn status'
        self.stdoutdata = subprocess.getoutput(statuscheck)
        self.conn = self.stdoutdata.startswith('Connected')
        return self.conn

    def statusdetail(self):
        self.checkstatus()
        if self.conn:
            self.status_loc = self.stdoutdata[13:]
            self.status_alias = (self.server[self.server.location == self.status_loc].index[0])
            self.status_loc = self.server.ix[self.status_alias, 'location']
            self.status_icon = self.server.ix[self.status_alias, 'icon2']
            self.lb_status.setText('VPN OK')

        else:
            self.status_loc = 'no vpn connection'
            self.status_icon = self.files + 'novpn1.png'
            self.lb_status.setText('No VPN')

        self.tray_icon.showMessage(
            "ExpressVPN Status",
            self.status_loc,
            QSystemTrayIcon.Information, 2000)
        self.seticon()

    def seticon(self):
        pixmap = QPixmap(self.status_icon)
        self.lb_conn_icon.setPixmap(pixmap)
        self.lb_conn.setText(self.status_loc)
        self.tray_icon.setIcon(QIcon(self.status_icon))
        self.setWindowIcon(QIcon(self.status_icon))

    def connect(self):
        self.server_combo()
        if self.conn:
            os.system('/usr/bin/expressvpn disconnect')
            os.system('/usr/bin/expressvpn connect ' + self.combo_alias)
        else:
            os.system('/usr/bin/expressvpn connect ' + self.combo_alias)
        self.checkstatus()
        self.statusdetail()
        self.seticon()

    def autoconnect(self):
        if self.chB_auto.isChecked():
            os.system('/usr/bin/expressvpn connect defr1')
            self.checkstatus()
            self.statusdetail()
            self.seticon()

    def disconnect(self):
        os.system('/usr/bin/expressvpn disconnect')
        self.checkstatus()
        self.statusdetail()
        self.seticon()

    def check_network(self):
        try:
            urllib.request.urlopen("http://www.google.com", timeout=1)
            self.lb_internet.setText("Internet OK")
            return True

        except urllib.error.URLError as e:
            self.lb_internet.setText("No Internet")
            self.lb_status.setText("Try to connect internet")

            return False

    def version(self):
        stdoutdata = subprocess.getoutput('/usr/bin/expressvpn -v')
        self.lb_version.setText(stdoutdata)

    def showapp(self):
        if self.chB_showapp.isChecked():
            self.hide()
        else:
            self.show()

    @pyqtSlot()
    def on_btn_connect_clicked(self):
        self.connect()

    @pyqtSlot()
    def on_btn_disconnect_clicked(self):
        self.disconnect()

    @pyqtSlot()
    def on_btn_status_clicked(self):
        self.statusdetail()

    def closeEvent(self, e):
        self.settings.setValue('auto', self.chB_auto.isChecked())
        self.settings.setValue('showapp', self.chB_showapp.isChecked())

            #       if self.check_box.isChecked():
        e.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "ExpressVPN",
            "Application was minimized to Tray",
            QSystemTrayIcon.Information, 2000
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MainWindow()

    myapp.hide()
    sys.exit(app.exec_())
