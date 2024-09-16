# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tela.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(508, 432)
        font = QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        Dialog.setFont(font)
        Dialog.setMouseTracking(False)
        Dialog.setAutoFillBackground(False)
        Dialog.setStyleSheet(u" background-color: rgba(179, 179, 179, 255)")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 491, 41))
        font1 = QFont()
        font1.setFamilies([u"Malgun Gothic"])
        font1.setPointSize(20)
        font1.setBold(False)
        font1.setItalic(False)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 20pt \"Malgun Gothic\";\n"
"")
        self.SelecionarPasta = QPushButton(Dialog)
        self.SelecionarPasta.setObjectName(u"SelecionarPasta")
        self.SelecionarPasta.setGeometry(QRect(60, 70, 101, 31))
        self.SelecionarPasta.setAutoFillBackground(False)
        self.SelecionarPasta.setStyleSheet(u"background-color: rgb(223, 223, 223)\n"
"\n"
"")
        self.RealizarLancamento = QPushButton(Dialog)
        self.RealizarLancamento.setObjectName(u"RealizarLancamento")
        self.RealizarLancamento.setGeometry(QRect(320, 330, 121, 31))
        self.RealizarLancamento.setStyleSheet(u"background-color: rgb(223, 223, 223)\n"
"\n"
"")
        self.BarraProgresso = QProgressBar(Dialog)
        self.BarraProgresso.setObjectName(u"BarraProgresso")
        self.BarraProgresso.setEnabled(True)
        self.BarraProgresso.setGeometry(QRect(60, 370, 381, 23))
        font2 = QFont()
        font2.setKerning(True)
        self.BarraProgresso.setFont(font2)
        self.BarraProgresso.setAutoFillBackground(False)
        self.BarraProgresso.setValue(0)
        self.BarraProgresso.setAlignment(Qt.AlignCenter)
        self.BarraProgresso.setTextVisible(True)
        self.BarraProgresso.setOrientation(Qt.Horizontal)
        self.logdelancamento = QPlainTextEdit(Dialog)
        self.logdelancamento.setObjectName(u"logdelancamento")
        self.logdelancamento.setGeometry(QRect(60, 120, 381, 201))
        self.logdelancamento.setStyleSheet(u"background-color: rgb(223, 223, 223)\n"
"\n"
"")

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"KMD", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Lan\u00e7amento autom\u00e1tico de NF-e de abastecimento</span></p></body></html>", None))
        self.SelecionarPasta.setText(QCoreApplication.translate("Dialog", u"Selecionar Pasta", None))
        self.RealizarLancamento.setText(QCoreApplication.translate("Dialog", u"Realizar lan\u00e7amento", None))
        self.BarraProgresso.setFormat(QCoreApplication.translate("Dialog", u"%p%", None))
    # retranslateUi

