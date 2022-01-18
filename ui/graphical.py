from PyQt5 import QtWidgets, QtGui
import sys
from ui.mainWindow import Ui_MainWindow
from ui.addDriveDialog import Ui_Dialog
from objects.File import File
from objects.Folder import Folder


class AddDriveDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = Ui_Dialog()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

        self.ui.comboBox.addItem("googleDrive")
        self.ui.comboBox.addItem("dropbox")

        self.ui.comboBox_2.addItem("Bytes")
        self.ui.comboBox_2.addItem("MegaBytes")
        self.ui.comboBox_2.addItem("GigaBytes")


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
        self.window.ui.pushButton_5.clicked.connect(self.addDrive)
        self.window.show()
        sys.exit(self.app.exec_())


    def bytesto(self, bytes, to, bsize=1024): 
        a = {'KiloBytes' : 1, 'MegaBytes': 2, 'GigaBytes' : 3}
        r = float(bytes)
        return bytes / (bsize ** a[to])


    def addDrive(self):
        dialog = AddDriveDialog(self.window)
        if dialog.exec():
            drivename = dialog.ui.lineEdit.text()
            driveprovider = dialog.ui.comboBox.currentText()
            unit = dialog.ui.comboBox_2.currentText()
            size = int(dialog.ui.lineEdit_2.text())
            if unit != "Bytes":
                size = self.bytesto(size, unit)
            self.uniklaud.mountStorage(drivename, driveprovider, size)
            self.window.updateDrives(self.uniklaud.mountedStorageObjects)
            self.window.updateUsedPercentage(self.uniklaud.getUsedPercentage()*100)