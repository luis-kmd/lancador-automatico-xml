# ARQUIVO .UI CONVERTIDO PARA .PY

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tela.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPlainTextEdit,
    QProgressBar, QPushButton, QSizePolicy, QWidget)
import logo_transvicon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(490, 410)
        Dialog.setMinimumSize(QSize(490, 410))
        Dialog.setMaximumSize(QSize(490, 410))
        font = QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        Dialog.setFont(font)
        Dialog.setMouseTracking(False)
        icon = QIcon()
        icon.addFile(u":/kmd/logokmdzin", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setAutoFillBackground(False)
        Dialog.setStyleSheet(u"background-color: qconicalgradient(cx:0, cy:0, angle:135,\n"
"    stop:0 rgba(255, 0, 0, 69),\n"
"    stop:0.375 rgba(255, 0, 0, 69),\n"
"    stop:0.423533 rgba(255, 51, 51, 145),\n"
"    stop:0.45 rgba(255, 102, 102, 208),\n"
"    stop:0.477581 rgba(255, 71, 71, 130),\n"
"    stop:0.518717 rgba(218, 0, 0, 130),\n"
"    stop:0.55 rgba(255, 0, 0, 255),\n"
"    stop:0.57754 rgba(203, 0, 0, 130),\n"
"    stop:0.625 rgba(255, 0, 0, 69),\n"
"    stop:1 rgba(255, 0, 0, 69)\n"
");\n"
"")
        self.SelecionarPasta = QPushButton(Dialog)
        self.SelecionarPasta.setObjectName(u"SelecionarPasta")
        self.SelecionarPasta.setGeometry(QRect(50, 80, 111, 31))
        font1 = QFont()
        font1.setFamilies([u"Malgun Gothic"])
        font1.setPointSize(9)
        font1.setBold(True)
        self.SelecionarPasta.setFont(font1)
        self.SelecionarPasta.setAutoFillBackground(False)
        self.SelecionarPasta.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: black;\n"
"\n"
"")
        self.RealizarLancamento = QPushButton(Dialog)
        self.RealizarLancamento.setObjectName(u"RealizarLancamento")
        self.RealizarLancamento.setGeometry(QRect(300, 330, 131, 31))
        self.RealizarLancamento.setFont(font1)
        self.RealizarLancamento.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: black;\n"
"\n"
"")
        self.BarraProgresso = QProgressBar(Dialog)
        self.BarraProgresso.setObjectName(u"BarraProgresso")
        self.BarraProgresso.setEnabled(True)
        self.BarraProgresso.setGeometry(QRect(50, 370, 381, 23))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BarraProgresso.sizePolicy().hasHeightForWidth())
        self.BarraProgresso.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setFamilies([u"Malgun Gothic"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setUnderline(False)
        font2.setStrikeOut(False)
        self.BarraProgresso.setFont(font2)
        self.BarraProgresso.setAutoFillBackground(False)
        self.BarraProgresso.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: black;\n"
"\n"
"")
        self.BarraProgresso.setValue(0)
        self.BarraProgresso.setAlignment(Qt.AlignCenter)
        self.BarraProgresso.setTextVisible(True)
        self.BarraProgresso.setOrientation(Qt.Horizontal)
        self.logdelancamento = QPlainTextEdit(Dialog)
        self.logdelancamento.setObjectName(u"logdelancamento")
        self.logdelancamento.setGeometry(QRect(50, 120, 381, 201))
        sizePolicy.setHeightForWidth(self.logdelancamento.sizePolicy().hasHeightForWidth())
        self.logdelancamento.setSizePolicy(sizePolicy)
        font3 = QFont()
        font3.setFamilies([u"Microsoft JhengHei"])
        font3.setPointSize(9)
        font3.setBold(True)
        self.logdelancamento.setFont(font3)
        self.logdelancamento.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: black;\n"
"\n"
"")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(60, 10, 391, 41))
        font4 = QFont()
        font4.setFamilies([u"Haettenschweiler"])
        font4.setPointSize(28)
        font4.setBold(False)
        font4.setItalic(False)
        font4.setUnderline(False)
        font4.setStrikeOut(False)
        self.label.setFont(font4)
        self.label.setStyleSheet(u"background-color: transparent;\n"
"color: rgb(248, 230, 255);\n"
"\n"
"")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(60, 40, 371, 20))
        self.label_2.setStyleSheet(u"background-color:transparent;\n"
"color: white;")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(40, 250, 241, 201))
        self.label_3.setStyleSheet(u"background-image: url(:/kmd/kmdlogooficial);\n"
"background-color: transparent;\n"
"background-repeat: no-repeat;\n"
"background-position: center;\n"
"")
        self.label_3.raise_()
        self.SelecionarPasta.raise_()
        self.RealizarLancamento.raise_()
        self.BarraProgresso.raise_()
        self.logdelancamento.raise_()
        self.label.raise_()
        self.label_2.raise_()

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"KMD", None))
        self.SelecionarPasta.setText(QCoreApplication.translate("Dialog", u"Selecionar Pasta", None))
        self.RealizarLancamento.setText(QCoreApplication.translate("Dialog", u"Realizar lan\u00e7amento", None))
        self.BarraProgresso.setFormat(QCoreApplication.translate("Dialog", u"%p%", None))
        self.logdelancamento.setPlainText("")
        self.logdelancamento.setPlaceholderText("")
        self.label.setText(QCoreApplication.translate("Dialog", u"Lan\u00e7ador de Nota Fiscal de Posto", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">_______________________________________________________________</p></body></html>", None))
        self.label_3.setText("")
    # retranslateUi

