from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from GenerateData import *
import sys, datetime

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Data Generator For Machine Learning"

        self.width = QDesktopWidget().screenGeometry(0).width()/2
        self.height = QDesktopWidget().screenGeometry(0).height()*0.8

        self.initWindows()

    # Initiate Windows
    def initWindows(self):
        self.setWindowIcon(QIcon('Images/Logo.png'))
        self.setWindowTitle(self.title)
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)

        self.CentralWidget = QWidget(self)
        self.CentralWidget.setStyleSheet('background-color: #ffffff')
        self.setCentralWidget(self.CentralWidget)

        self.ButtonCSS = """
                        QPushButton{
                            background-color: #005072;
                            color: #ffffff;
                            border-width: 1px;
                            border-color: #1e1e1e;
                            border-style: solid;
                            border-radius: 10;
                            padding: 3px;
                            font-weight: 700;
                            font-family: 'Kristen ITC'; 
                            font-size: 12px;
                            padding-left: 5px;
                            padding-right: 5px;
                            min-width: 40px;
                        }
                        QPushButton:hover{
                            border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #005b82, stop: 1 #d4e8f2);
                            background-color: #ffffff;
                            color: #005072;
                        }                                    
                    """

        self.CentralWidgetLayout = QVBoxLayout(self.CentralWidget)
        self.CentralWidgetLayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.CentralWidgetLayout.setContentsMargins(self.width*0.125, self.height*0.1, self.width*0.125, self.height*0.1)
        self.CentralWidgetLayout.setSpacing(50)

        # Image Label
        ImageLabel = QLabel()
        ImageLabel.setAlignment(Qt.AlignCenter)
        ImageLabel.setPixmap(QPixmap('Images/Logo.png').scaled(ImageLabel.width()/2, ImageLabel.height()/2, Qt.KeepAspectRatio))
        self.CentralWidgetLayout.addWidget(ImageLabel)


        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        font.setFamily('Kristen ITC')

        # Software Title Label
        TitleLabel = QLabel()
        TitleLabel.setText(self.title)
        TitleLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        TitleLabel.setFont(font)
        self.CentralWidgetLayout.addWidget(TitleLabel)

        font.setPointSize(10)

        # ************************************************************
        # ******************** Load DataBase *************************
        # ************************************************************

        # Load DataBase Label
        LoadDataBaseLabel = QLabel()
        LoadDataBaseLabel.setText("Load DataBase")
        LoadDataBaseLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        LoadDataBaseLabel.setFont(font)
        self.CentralWidgetLayout.addWidget(LoadDataBaseLabel)

        LoadDataBaseFileWidget = QWidget()
        LoadDataBaseFileLayout = QHBoxLayout(LoadDataBaseFileWidget)
        LoadDataBaseFileLayout.setAlignment(Qt.AlignVCenter)

        # Demand File Path LineEdit
        LoadDataBasePathLineEdit = QLineEdit()
        LoadDataBasePathLineEdit.setPlaceholderText("Load DataBase")
        LoadDataBasePathLineEdit.setReadOnly(True)
        LoadDataBasePathLineEdit.setDisabled(True)
        LoadDataBaseFileLayout.addWidget(LoadDataBasePathLineEdit)

        # Load DataBase Browse Button
        LoadDataBaseBrowseButton = QPushButton()
        LoadDataBaseBrowseButton.setText("Choose File")
        LoadDataBaseBrowseButton.clicked.connect(lambda: self.ChooseFileButton(LoadDataBasePathLineEdit))
        LoadDataBaseBrowseButton.setStyleSheet(self.ButtonCSS)

        LoadDataBaseFileLayout.addWidget(LoadDataBaseBrowseButton)
        self.CentralWidgetLayout.addWidget(LoadDataBaseFileWidget)

        # ************************************************************
        # ************************** Year ****************************
        # ************************************************************

        CountWidget = QWidget()
        CountWidgetLayout = QHBoxLayout(CountWidget)
        CountWidgetLayout.setContentsMargins(100, 0, 100, 0)

        # Year Label
        CountLabel = QLabel()
        CountLabel.setText("Count")
        CountLabel.setAlignment(Qt.AlignCenter)
        CountLabel.setFont(font)
        CountWidgetLayout.addWidget(CountLabel, 50)

        # Count LineEdit
        CountLineEdit = QLineEdit()
        CountLineEdit.setValidator(QIntValidator(0, 1000, self))
        CountLineEdit.setAlignment(Qt.AlignCenter)
        CountWidgetLayout.addWidget(CountLineEdit, 50)

        self.CentralWidgetLayout.addWidget(CountWidget)

        # ************************************************************
        # ********************* Button Widget ************************
        # ************************************************************

        # Run Push Button
        GenerateButton = QPushButton()
        GenerateButton.setText("Generate")
        GenerateButton.adjustSize()
        GenerateButton.setDisabled(True)
        GenerateButton.clicked.connect(lambda: self.GenerateData(LoadDataBasePathLineEdit.text(), CountLineEdit.text()))
        GenerateButton.setStyleSheet(self.ButtonCSS)
        self.CentralWidgetLayout.addWidget(GenerateButton)

        LoadDataBasePathLineEdit.textChanged.connect(lambda: self.ToggleButton(LoadDataBasePathLineEdit, CountLineEdit, GenerateButton))
        CountLineEdit.textChanged.connect(lambda: self.ToggleButton(LoadDataBasePathLineEdit, CountLineEdit, GenerateButton))

    # Choose File
    def ChooseFileButton(self, PathLineEdit):
        path = QFileDialog.getOpenFileName(self, 'Open CSV File', "",
                                           'CSV files (*.csv)')

        if all(path):
            PathLineEdit.setText(path[0])

    # Toggle Button
    def ToggleButton(self, LoadDataBasePathLineEdit, CountLineEdit, GenerateButton):
        if len(LoadDataBasePathLineEdit.text()) == 0 or len(CountLineEdit.text()) == 0:
            GenerateButton.setDisabled(True)
        else:
            GenerateButton.setDisabled(False)

    # Generate Data
    def GenerateData(self, Path, Count):
        try:
            df = pd.read_csv(Path)
        except UnicodeDecodeError:
            df = pd.read_csv(Path, engine='python')

        try:
            GenerateData(df, int(Count))
            df.to_csv('Random_Generated.csv', header=True, index=False)

            QMessageBox.information(self, 'Successful',
                                    'Random Rows Generated', QMessageBox.Ok)

        except Exception as e:
            print(str(e))
            QMessageBox.critical(self, 'Error',
                                 'An Unexpected Error Occur', QMessageBox.Ok)

    # Close Application / Exit
    def closeEvent(self, event):
        ExitWindowChoice = QMessageBox.question(self, 'Exit',
                                                "Are you sure you want to exit?",
                                                QMessageBox.Yes | QMessageBox.No)
        # If user chooses Yes
        if ExitWindowChoice == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    App = QApplication(sys.argv)

    Window = Window()
    Window.setStyleSheet(
        """
            QPushButton::menu-indicator 
            {
                image: url(myindicator.png);
                subcontrol-position: right center;
                subcontrol-origin: padding;
                left: -2px;
            }

            QToolTip
            {
                 border: 1px solid black;
                 padding: 1px;
                 border-radius: 3px;
                 opacity: 100;
            }


            QTreeView, QListView
            {
                margin-left: 5px;
            }

            QMenuBar::item
            {
                background: transparent;
            }


            QMenu
            {
                border: 1px solid #cae6ef;
            }

            QMenuBar::item:selected
            {
                background: #cae6ef;
                border: 1px solid #cae6ef;
            }
            QMenuBar::item:pressed
            {
                background: #444;
                border: 1px solid #cae6ef;
                background-color: QLinearGradient(
                    x1:0, y1:0,
                    x2:0, y2:1,
                    stop:1 #cae6ef,
                    stop:0.4 #cae6ef/*,
                    stop:0.2 #343434,
                    stop:0.1 #ffaa00*/
                );
                margin-bottom:-1px;
                padding-bottom:1px;
            }

            QMenu::item
            {
                padding: 2px 20px 2px 20px;
            }

            QMenu::item:selected
            {
                background: #cae6ef;
                color: #000000;
            }

            QMessageBox
            {
                background-color: #ffffff;
                color: #005072;
            }

            QWidget:focus, QMessageBox:focus
            {
                border: 1px solid darkgray;
            }

            QLineEdit
            {
                padding: 1px;
                border-style: solid;
                color: #005072;
                border: 1px solid #005072;
                border-radius: 5;
            }

            QPushButton
            {
                border-width: 1px;
                border-color: #1e1e1e;
                border-style: solid;
                border-radius: 6;
                padding: 3px;
                font-size: 12px;
                padding-left: 5px;
                padding-right: 5px;
                min-width: 40px;
            }


            QComboBox
            {
                border-style: solid;
                border: 1px solid #005072;
                border-radius: 5;
                color: #005072;                
            }

            QComboBox:hover,QPushButton:hover
            {
                border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #005b82, stop: 1 #d4e8f2);
            }


            QComboBox:on
            {
                padding-top: 3px;
                padding-left: 4px;
            }

            QComboBox QAbstractItemView
            {
                border: 2px solid darkgray;
            }

            QComboBox::drop-down
            {
                 subcontrol-origin: padding;
                 subcontrol-position: top right;
                 width: 15px;

                 border-left-width: 0px;
                 border-left-color: darkgray;
                 border-left-style: solid; /* just a single line */
                 border-top-right-radius: 3px; /* same radius as the QComboBox */
                 border-bottom-right-radius: 3px;
             }

            QComboBox::down-arrow
            {
                 image: url(:/dark_orange/img/down_arrow.png);
            }

            QGroupBox
            {
                border: 1px solid darkgray;
                margin-top: 10px;
            }

            QGroupBox:focus
            {
                border: 1px solid darkgray;
            }
            QTextEdit
            {
                color: #005072;
                border: 1px solid #005072;
            }            
            QTextEdit:focus
            {
                border: 1px solid darkgray;
            }

            QScrollBar:horizontal {
                 border: 1px solid #222222;
                 background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 #ffffff, stop: 0.2 #ffffff, stop: 1 #ffffff);
                 height: 7px;
                 margin: 0px 16px 0 16px;
            }

            QScrollBar::handle:horizontal
            {
                  background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #D3D3D3, stop: 0.5 #a9a9a9, stop: 1 #D3D3D3);
                  min-height: 20px;
                  border-radius: 2px;
            }

            QScrollBar::add-line:horizontal {
                  border: 1px solid #1b1b19;
                  border-radius: 2px;
                  background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #D3D3D3, stop: 1 #a9a9a9);
                  width: 14px;
                  subcontrol-position: right;
                  subcontrol-origin: margin;
            }

            QScrollBar::sub-line:horizontal {
                  border: 1px solid #1b1b19;
                  border-radius: 2px;
                  background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #D3D3D3, stop: 1 #a9a9a9);
                  width: 14px;
                 subcontrol-position: left;
                 subcontrol-origin: margin;
            }

            QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal
            {
                  border: 1px solid black;
                  width: 1px;
                  height: 1px;
                  background: white;
            }

            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
            {
                  background: none;
            }

            QScrollBar:vertical
            {
                  background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0.0 #ffffff, stop: 0.2 #ffffff, stop: 1 #ffffff);
                  width: 7px;
                  margin: 16px 0 16px 0;
                  border: 1px solid #222222;
            }

            QScrollBar::handle:vertical
            {
                  background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #D3D3D3, stop: 0.5 #a9a9a9, stop: 1 #D3D3D3);
                  min-height: 20px;
                  border-radius: 2px;
            }

            QScrollBar::add-line:vertical
            {
                  border: 1px solid #1b1b19;
                  border-radius: 2px;
                  background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #D3D3D3, stop: 1 #a9a9a9);
                  height: 14px;
                  subcontrol-position: bottom;
                  subcontrol-origin: margin;
            }

            QScrollBar::sub-line:vertical
            {
                  border: 1px solid #1b1b19;
                  border-radius: 2px;
                  background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #a9a9a9, stop: 1 #D3D3D3);
                  height: 14px;
                  subcontrol-position: top;
                  subcontrol-origin: margin;
            }

            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
            {
                  border: 1px solid black;
                  width: 1px;
                  height: 1px;
                  background: white;
            }


            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
            {
                  background: none;
            }

            QHeaderView::section
            {
                padding-left: 4px;
                border: 1px solid #6c6c6c;
            }

            QDockWidget::title
            {
                text-align: center;
                spacing: 3px; /* spacing between items in the tool bar */
            }

            QDockWidget::close-button, QDockWidget::float-button
            {
                text-align: center;
                spacing: 1px; /* spacing between items in the tool bar */
            }

            QDockWidget::close-button:pressed, QDockWidget::float-button:pressed
            {
                padding: 1px -1px -1px 1px;
            }

            QMainWindow::separator
            {
                padding-left: 4px;
                border: 1px solid #4c4c4c;
                spacing: 3px; /* spacing between items in the tool bar */
            }

            QMainWindow::separator:hover
            {
                padding-left: 4px;
                border: 1px solid #6c6c6c;
                spacing: 3px; /* spacing between items in the tool bar */
            }

            QToolBar::handle
            {
                 spacing: 3px; /* spacing between items in the tool bar */
                 background: url(:/dark_orange/img/handle.png);
            }

            QMenu::separator
            {
                height: 2px;
                padding-left: 4px;
                margin-left: 10px;
                margin-right: 5px;
            }

            QProgressBar
            {
                border: 2px solid grey;
                border-radius:8px;
                padding:1px
            }

            QTabBar::tab {
                border: 1px solid #444;
                border-bottom-style: none;
                padding-left: 10px;
                padding-right: 10px;
                padding-top: 3px;
                padding-bottom: 2px;
                margin-right: -1px;
            }

            QTabWidget::pane {
                border: 1px solid #444;
                top: 1px;
            }

            QTabBar::tab:last
            {
                margin-right: 0; /* the last selected tab has nothing to overlap with on the right */
                border-top-right-radius: 3px;
            }

            QTabBar::tab:first:!selected{
                margin-left: 0px; /* the last selected tab has nothing to overlap with on the right */
                border-top-left-radius: 3px;
            }

            QTabBar::tab:!selected
            {
                border-bottom-style: solid;
                margin-top: 3px;
            }

            QTabBar::tab:selected
            {
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
                margin-bottom: 0px;
            }

            QTabBar::tab:!selected:hover
            {
                /*border-top: 2px solid #ffaa00;
                padding-bottom: 3px;*/
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
            }

            QRadioButton::indicator:checked, QRadioButton::indicator:unchecked{
                color: #b1b1b1;
                background-color: #ffffff;
                border: 1px solid #b1b1b1;
                border-radius: 6px;
            }

            QRadioButton::indicator:checked
            {
                background-color: qradialgradient(
                    cx: 0.5, cy: 0.5,
                    fx: 0.5, fy: 0.5,
                    radius: 1.0,
                    stop: 0.25 #323232,
                    stop: 0.3 #ffffff
                );
            }

            QRadioButton::indicator
            {
                border-radius: 6px;
            }

            /*
            QCheckBox::indicator{
                border: 1px solid #b1b1b1;
                width: 9px;
                height: 9px;
            }

            QRadioButton::indicator:hover, QCheckBox::indicator:hover
            {
                border: 1px solid #121212;
            }

            QCheckBox::indicator:checked
            {
                image:url(:/dark_orange/img/checkbox.png);
            }


            QCheckBox::indicator:disabled, QRadioButton::indicator:disabled
            {
                border: 1px solid #444;
            }
            */
            QSlider::groove:horizontal {
                border: 1px solid #3A3939;
                height: 8px;
                margin: 2px 0;
                border-radius: 2px;
            }

            QSlider::handle:horizontal {
                border: 1px solid #3A3939;
                width: 14px;
                height: 14px;
                margin: -4px 0;
                border-radius: 2px;
            }

            QSlider::groove:vertical {
                border: 1px solid #3A3939;
                width: 8px;
                margin: 0 0px;
                border-radius: 2px;
            }

            QSlider::handle:vertical {
                border: 1px solid #3A3939;
                width: 14px;
                height: 14px;
                margin: 0 -4px;
                border-radius: 2px;
            }

            QAbstractSpinBox {
                padding-top: 2px;
                padding-bottom: 2px;
                border: 1px solid darkgray;

                border-radius: 2px;
                min-width: 50px;
            }

        """
    )
    Window.show()
    sys.exit(App.exec())