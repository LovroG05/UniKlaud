from PyQt5 import QtWidgets, QtGui
import sys
from ui.mainWindow import Ui_MainWindow
from objects.File import File
from objects.Folder import Folder

class UniKlaudWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(UniKlaudWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)

        

    def buildFileTree(self, node, srcFolder):
        for i in srcFolder.getFiles():
            child = QtWidgets.QTreeWidgetItem()
            child.setText(0, i)
            child.setIcon(0, QtGui.QIcon(":/1/file.png"))
            node.addChild(child)

        for i in srcFolder.getFolders():
            child = QtWidgets.QTreeWidgetItem()
            child.setText(0, i)
            child.setIcon(0, QtGui.QIcon(":/1/folder.png"))
            self.buildFileTree(child, srcFolder.getFolder(i))
            node.addChild(child)

    def updateFiles(self, filesys):
        rootNode = QtWidgets.QTreeWidgetItem()
        rootNode.setText(0, "/")
        rootNode.setIcon(0, QtGui.QIcon(":/1/folder.png"))
        self.ui.treeWidget.addTopLevelItem(rootNode)
        self.buildFileTree(rootNode, filesys)
        rootNode.setExpanded(True)

    def updateDrives(self, drives):
        self.ui.tableWidget.setRowCount(len(drives))
        self.ui.tableWidget.setColumnCount(3)
        # self.ui.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("name"))
        # self.ui.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem("provider"))
        # self.ui.tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem("used[B]"))
        drivecnt = 0
        for drive in drives:
            print(drive)
            self.ui.tableWidget.setItem(drivecnt, 0, QtWidgets.QTableWidgetItem(drive.storageName))
            self.ui.tableWidget.setItem(drivecnt, 1, QtWidgets.QTableWidgetItem(drive.provider))
            self.ui.tableWidget.setItem(drivecnt, 2, QtWidgets.QTableWidgetItem(drive.getUsedB()))
            drivecnt += 1

    def updateUsedPercentage(self, usedPercentage):
        self.ui.progressBar.setValue(usedPercentage)

class UniKlaudGUI:
    def __init__(self, uniklaud):
        self.uniklaud = uniklaud

        self.app = QtWidgets.QApplication(sys.argv)
        self.window = UniKlaudWindow()
        self.window.updateDrives(self.uniklaud.mountedStorageObjects)
        self.window.updateUsedPercentage(self.uniklaud.getUsedPercentage()*100)
        print(self.uniklaud.getUsedPercentage()*100)
        self.window.updateFiles(self.uniklaud.filesystem)
        self.window.show()
        sys.exit(self.app.exec_())