#usr/bin/env python
import os, sys, csv, traceback, platform, types
from datetime import date
import numpy as np
import webbrowser
from graphicsview import imwin, resource_path

from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QSlider ,QColorDialog ,QComboBox, QMainWindow, QApplication,  QWidget, QToolBar, QPushButton, QLabel, QLineEdit, QPlainTextEdit, QGridLayout, QFileDialog, QMessageBox, QInputDialog, QDockWidget, QSizePolicy, QRadioButton
from PySide6.QtGui import QShortcut, QIcon, QIntValidator, QDoubleValidator
from PySide6.QtCore import Qt

# TODO: Update before every release
VERSION = "2.2.2"

# ------------------------------
#   MorphoMetrix - Developed By:
#       Walter Torres
#       Kevin Bierlich
#       Clara Bird
#       Elliott Chimienti
# ------------------------------
#   Packages (Used Universal2 Python install with universal2 Wheels for MacOS):
#   Python 3.10.8
#   PySide6 6.4.3
#   Numpy 1.21.6
#   Scipy 1.9.1
# ------------------------------

consts = types.SimpleNamespace()
# State case constants
consts.LENGTH = 1
consts.AREA = 2
consts.ANGLE = 3
consts.WIDTH = 4

class Window(QWidget):

    def __init__(self, iw):
        #init methods runs every time, use for core app stuff)
        super(Window, self).__init__()

        self.setWindowIcon(QIcon(resource_path("icon.PNG")))
        self.setWindowTitle("MorphoMetriX")
        self.iw = iw    # Reference for color picker

        self.label_id = QLabel("Image ID")
        self.id = QLineEdit()
        # self.id.setValidator(QIntValidator())
        self.id.setText('0000')

        #Define custom attributes for pixel -> SI conversion
        self.label_foc = QLabel("Focal Length (mm):")
        self.focal = QLineEdit()
        self.focal.setValidator(QDoubleValidator())
        self.focal.setText('25')

        self.label_alt = QLabel("Altitude (m):")
        self.altitude = QLineEdit()
        self.altitude.setValidator(QDoubleValidator())
        self.altitude.setText('50')
        
        self.label_pd = QLabel("Pixel Dimension (mm/pixel)")
        self.pixeldim = QLineEdit()
        self.pixeldim.setValidator(QDoubleValidator())
        self.pixeldim.setText('0.0045')

        self.label_widths = QLabel("# Width Segments:")
        self.numwidths = QLineEdit()
        self.numwidths.setValidator(QIntValidator())
        self.numwidths.setText('10')

        self.label_side = QLabel("Mirror Side:")
        self.side_bias = QComboBox()
        self.side_bias.addItems(["None","Side A", "Side B"])

        self.label_scale = QLabel("Crosshair Size")
        self.scale_slider = QSlider(orientation=Qt.Orientation.Horizontal)
        self.scale_slider.setMaximum(20)
        self.scale_slider.setValue(10)
        self.scale_slider.valueChanged.connect(self.slider_changed)

        self.label_opacity = QLabel("Crosshair Opacity")
        self.opacity_slider = QSlider(orientation=Qt.Orientation.Horizontal)
        self.opacity_slider.setMaximum(10)
        self.opacity_slider.setValue(10)
        self.opacity_slider.valueChanged.connect(self.slider_changed)

        self.label_widthtype =  QLabel("Crosshair Type:")
        self.width_tabs = QComboBox()
        self.width_tabs.addItems(["Crosshair", "Dot"])

        self.label_not = QLabel("Notes:")
        self.notes = QPlainTextEdit()

        self.label_color = QLabel("Crosshair Color: ")
        self.button_color = QPushButton()
        self.button_color.setStyleSheet("background-color: red")
        self.button_color.clicked.connect(self.color_changed)

        self.manual = QPushButton("Manual", self)
        self.manual.clicked.connect(lambda: webbrowser.open('https://github.com/ZappyMan/MorphoMetriX/blob/master/MorphoMetriX_v2_manual.pdf'))

        self.exit = QPushButton("Exit", self)
        self.exit.clicked.connect(self.close_application)

        self.grid = QGridLayout()
        self.grid.addWidget(self.label_id, 1, 0)
        self.grid.addWidget(self.id, 1, 1)
        self.grid.addWidget(self.label_foc, 2, 0)
        self.grid.addWidget(self.focal, 2, 1)
        self.grid.addWidget(self.label_alt, 3, 0)
        self.grid.addWidget(self.altitude, 3, 1)
        self.grid.addWidget(self.label_pd, 4, 0)
        self.grid.addWidget(self.pixeldim, 4, 1)
        self.grid.addWidget(self.label_widths, 5, 0)
        self.grid.addWidget(self.numwidths, 5, 1)
        self.grid.addWidget(self.label_side,6,0)
        self.grid.addWidget(self.side_bias,6,1)
        self.grid.addWidget(self.label_scale,7,0)
        self.grid.addWidget(self.scale_slider,7,1)
        self.grid.addWidget(self.label_opacity,8,0)
        self.grid.addWidget(self.opacity_slider,8,1)
        self.grid.addWidget(self.label_widthtype,9,0)
        self.grid.addWidget(self.width_tabs,9,1)
        self.grid.addWidget(self.label_not, 10, 0)
        self.grid.addWidget(self.notes, 10, 1)
        self.grid.addWidget(self.label_color,11,0)
        self.grid.addWidget(self.button_color,11,1)
        self.grid.addWidget(self.manual, 12, 1)
        self.grid.addWidget(self.exit, 13, 1)
        self.setLayout(self.grid)

    # Function used by color picker button
    # Waits for user color selection, then passes color to imwin function "picked_color"
    def color_changed(self):
        color = QColorDialog().getColor()   # Returns QColor
        self.button_color.setStyleSheet("background-color: "+color.name())
        self.iw.picked_color = color

    # Function called when "crosshair size" slider value changes
    # Passed new size to imwin function "slider_moved"
    def slider_changed(self):
        self.scale_slider.value() # Value grab lags behind actually value?
        self.opacity_slider.value()
        self.iw.slider_moved(self.scale_slider.value(),self.opacity_slider.value())


    # Called when user clicks "Exit" button 
    def close_application(self):
        choice = QMessageBox.question(self, 'exit', "Exit program?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if choice == QMessageBox.StandardButton.Yes:
            # self.parent().deleteLater()
            # self.parent().close()
            sys.exit()

#references:
#https://stackoverflow.com/questions/26901540/arc-in-qgraphicsscene/26903599#26903599
#https://stackoverflow.com/questions/27109629/how-can-i-resize-the-main-window-depending-on-screen-resolution-using-pyqt
class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QIcon(resource_path("icon.PNG")))
        self.setWindowTitle("MorphoMetriX")

        D = self.screen().availableGeometry()
        self.move(0,0)#center.x() + .25*D.width() , center.y() - .5*D.height() )
        self.resize( int(.95*D.width()), int(6*D.height()) )

        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowState.WindowMinimized
                            | QtCore.Qt.WindowState.WindowActive)
        self.activateWindow()

        self.iw = imwin()           # Image window
        self.subWin = Window(self.iw)
        self.setCentralWidget(self.iw)
        
        #Stacked dock widgets
        docked1 = QDockWidget("", self)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, docked1)
        docked1.setWidget(self.subWin)
        docked1.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetFloatable)

        self.setCorner(QtCore.Qt.Corner.TopLeftCorner, QtCore.Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.Corner.TopRightCorner, QtCore.Qt.DockWidgetArea.RightDockWidgetArea)
        self.setCorner(QtCore.Qt.Corner.BottomLeftCorner, QtCore.Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.Corner.BottomRightCorner, QtCore.Qt.DockWidgetArea.RightDockWidgetArea)
        self.resizeDocks( [docked1], [400], QtCore.Qt.Orientation.Horizontal )
        self.exportButton = QPushButton("Export Measurements", self)
        self.exportButton.clicked.connect(self.export_measurements)
        self.exportButton.setEnabled(False)

        self.importImage = QPushButton("New Image", self)
        self.importImage.clicked.connect(self.file_open)

        self.lengthButton = QPushButton("Measure Length", self)
        self.lengthButton.clicked.connect(self.measure_length)
        self.lengthButton.setEnabled(False)
        self.lengthButton.setCheckable(True)
        self.lengthNames = []

        self.widthsButton = QPushButton("Measure Widths", self)
        self.widthsButton.clicked.connect(self.measure_widths)
        self.widthsButton.setEnabled(False)
        self.widthNames = []

        self.areaButton = QPushButton("Measure Area", self)
        self.areaButton.clicked.connect(self.measure_area)
        self.areaButton.setEnabled(False)
        self.areaButton.setCheckable(True)
        self.areaNames = []

        self.angleButton = QPushButton("Measure Angle", self)
        self.angleButton.clicked.connect(self.measure_angle)
        self.angleButton.setEnabled(False)
        self.angleButton.setCheckable(True)
        self.angleNames = []

        shortcut_polyClose = QShortcut(QtGui.QKeySequence(QtCore.Qt.Key.Key_Tab), self)
        shortcut_polyClose.activated.connect(self.iw.polyClose)

        self.undoButton = QPushButton("Undo", self)
        self.undoButton.clicked.connect(self.undo)
        self.undoButton.setEnabled(False)

        shortcut_undo = QShortcut(QtGui.QKeySequence('Ctrl+Z'), self)
        shortcut_undo.activated.connect(self.undo)

        self.bezier = QRadioButton("Bezier fit", self)
        self.bezier.setEnabled(True)
        self.bezier.setChecked(True)

        self.piecewise = QRadioButton("Piecewise", self)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Select new image to begin')

        self.tb = QToolBar('Toolbar')
        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tb.addWidget(spacer)
        self.addToolBar(self.tb)
        self.tb.addWidget(self.importImage)
        self.tb.addWidget(self.exportButton)
        self.tb.addWidget(self.lengthButton)
        self.tb.addWidget(self.widthsButton)
        self.tb.addWidget(self.areaButton)
        self.tb.addWidget(self.angleButton)
        self.tb.addWidget(self.undoButton)
        self.tb.addWidget(self.bezier)
        self.tb.addWidget(self.piecewise)

    # New Project
    # Set all defaults and clear stored values
    def file_open(self):
        self.image_name = QFileDialog.getOpenFileName(self, 'Open File', filter="Images (*.png *.jpg *.PNG *.JPG)")

        if self.image_name[0]: # If user selected a file, create new project
            self.iw.new_project(self.image_name[0])
            self.statusbar.showMessage('Select a measurement to make from the toolbar')
            self.enable_all_measurements()
    
    # Enable all measurement buttons
    def enable_all_measurements(self):
        self.lengthButton.setEnabled(True)
        self.areaButton.setEnabled(True)
        self.angleButton.setEnabled(True)

    def enable_width_measurement(self):
        self.widthsButton.setEnabled(True)

    # Remove highlighted status from all buttons
    def clear_button_highlights(self):
        self.lengthButton.setChecked(False)
        self.areaButton.setChecked(False)
        self.angleButton.setChecked(False)
        self.widthsButton.setChecked(False)

    # Highlight selected button
    def highlight_measurement(self, measurement):
        match measurement:
            case consts.LENGTH:
                self.statusbar.showMessage('Click to place next point... double click to finish')
                self.lengthButton.setEnabled(True)
                self.lengthButton.setChecked(True)
            case consts.AREA:
                self.statusbar.showMessage('Click to place next point... close polygon to finish')
                self.areaButton.setEnabled(True)
                self.areaButton.setChecked(True)
            case consts.ANGLE:
                self.statusbar.showMessage('Click point to define vector')
                self.angleButton.setEnabled(True)
                self.angleButton.setChecked(True)

    # Disable all measurement buttons
    def disable_all_measurements(self):
        self.lengthButton.setEnabled(False)
        self.areaButton.setEnabled(False)
        self.angleButton.setEnabled(False)
        self.widthsButton.setEnabled(False)

    # Enable undo button
    def enable_undo(self):
        self.undoButton.setEnabled(True)

    # Disable undo button
    def disable_undo(self):
        self.undoButton.setEnabled(False)

    # Enable export button
    def enable_export(self):
        self.exportButton.setEnabled(True)

    # Disable export button
    def disable_export(self):
        self.exportButton.setEnabled(False)

    # Call length function within graphicsview
    def measure_length(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Length name')
        if ok:
            self.iw.push_stack(text,consts.LENGTH)
            self.statusbar.showMessage('Click initial point for length measurement')

    # Call widths function within graphicsview class
    def measure_widths(self):
        self.iw.measure_widths()  # Call width function within graphics view

    # Call angle function within graphicsview class
    def measure_angle(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Angle name')
        if ok:
            self.statusbar.showMessage('Click initial point for angle measurement')
            self.iw.push_stack(text,consts.ANGLE)
            
    # Call area function within graphicsview class
    def measure_area(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Area name')
        if ok:
            self.iw.push_stack(text,consts.AREA)               # 2 == AREA
            self.statusbar.showMessage('Click initial point for area measurement')

    # Call undo function within graphicsview class
    def undo(self):
        self.iw.undo()
        
    # Export measurements to csv
    # Collect measurements from graphicsview
    def export_measurements(self):
        # Popup to get user save file input
        
        try:
            pixeldim = float(self.subWin.pixeldim.text())
            altitude = float(self.subWin.altitude.text())
            focal = float(self.subWin.focal.text())
        except:
            QMessageBox.warning(self,"Warning","Focal Length, Altitude, or Pixel Dimension cannot be empty.",QMessageBox.StandardButton.Ok)
            return

        name = QFileDialog.getSaveFileName(
            self, 'Save File', self.image_name[0].split('.', 1)[0])[0]

        if name:
            meta_data = [["Object","Value","Value_unit"],
                        ['Image ID',self.subWin.id.text(),"Metadata"],
                        ['Image Path',self.image_name[0],"Metadata"],
                        ['Focal Length', focal,"Metadata"],
                        ['Altitude', altitude,"Metadata"],
                        ['Pixel Dimension', pixeldim,"Metadata"],
                        ['Mirror Side', self.subWin.side_bias.currentText(), "Metadata"],
                        ['Notes', self.subWin.notes.toPlainText(), "Metadata"]]

	        #Write .csv file
            with open(name + '.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)

                writer.writerows(meta_data)     # Writes flight data and metadata

                self.iw.calculate_widths(self.subWin.side_bias.currentText())      # Calculate widths of MovingEllipses at export
                m = pixeldim * (altitude / focal)
                pixel_measurements, unit_measurements = self.iw.get_measurement_names_and_values(m)
                
                writer.writerows(unit_measurements)
                writer.writerows(pixel_measurements)

            #Export image
            self.iw.fitInView(self.iw.scene.sceneRect(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            pix = QtGui.QPixmap(self.iw.viewport().size())
            self.iw.viewport().render(pix)
            pix.save(name + '-measurements.png')
            self.statusbar.showMessage('Export Complete!')

# Crash handler for error logging
def except_hook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    dialog = QMessageBox()
    dialog.setIcon(QMessageBox.Icon.Critical)
    dialog.setWindowTitle("Error")
    dialog.setText("Error: Crash caught, save details to file.")
    dialog.setDetailedText(tb)
    dialog.setStandardButtons(QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Cancel)
    ret = dialog.exec()   # Show dialog box
    if ret == QMessageBox.StandardButton.Save:
        path = QFileDialog().getExistingDirectory(dialog,'Select a directory')
        if(path):
            path += '/' + str(date.today()) + "_Morphometrix_Crashlog" + ".txt"
            print("saving: ", path)
            with open(path, 'w') as file:
                file.write("System: " + platform.system() + '\n')
                file.write("OS: " + os.name + '\n')
                file.write("Python Version: " + platform.python_version() + '\n')
                file.write("Python Implementation: " + platform.python_implementation() + '\n')
                file.write("Release: " + platform.release() + '\n')
                file.write("Version: " + platform.version() + '\n')
                file.write("MorphoMetrix Version: " + VERSION + '\n')
                file.write("Machine: " + platform.machine() + '\n')
                file.write("Processor: " + platform.processor() + '\n' + '\n')
                file.write(tb)

    QApplication.quit() # Quit application


def main():
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    app.exec()
    sys.exit()


if __name__ == "__main__":
    main()
