from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.Qt import QSyntaxHighlighter
from untitled import Ui_MainWindow
from PyQt5 import Qt
import datetime
import sqlite3
import sys
import os

# Константы цветов
GRAY = (73, 77, 78)
DARK_GRAY = (34, 34, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 102, 0)
GREEN = (0, 155, 0)
PURPLE = (128, 0, 128)
SMOKE_WHITE = (245, 245, 245)


# Окно для создания папки
class CreateFolder(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(200, 95)
        self.setWindowIcon(QtGui.QIcon('troll.jpg'))
        self.label = QtWidgets.QLabel('Write a project address', self)
        self.label.resize(150, 22)
        self.label.move(40, 10)
        self.label.setStyleSheet('color: white;')
        self.lineEdit = QtWidgets.QLineEdit(self)  # поле для ввода названия (можно вводить и путь к той директории,
        # в которую вам нужно добавить папку)
        self.lineEdit.resize(135, 22)
        self.lineEdit.move(30, 32)
        self.setStyleSheet(f'background: rgb{GRAY}')
        self.lineEdit.setStyleSheet(f'color: rgb{WHITE};border: 1px solid rgb{DARK_GRAY}')
        self.pushButton = QtWidgets.QPushButton('Ok', self)  # кнопка для запуска метода createFolder
        self.pushButton.resize(75, 22)
        self.pushButton.move(60, 60)
        self.pushButton.setStyleSheet(f'color: rgb{WHITE};')
        self.pushButton.clicked.connect(self.createFolder)
        self.setWindowTitle('Create folder')

    # метод, создающий папку
    def createFolder(self):
        try:
            if self.lineEdit.text():
                os.mkdir(self.lineEdit.text())
                self.hide()
        except FileNotFoundError:
            msg = QtWidgets.QMessageBox()
            msg.setText('System can`t seek this address')
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            exec2 = msg.exec()
            if exec2 == QtWidgets.QMessageBox.Ok:
                msg.hide()


# начальное окно, в котором пользователь работает с проектами
class ChooseProject(QtWidgets.QMainWindow):
    def __init__(self, editor):
        super().__init__()
        self.setStyleSheet(f'background: rgb{DARK_GRAY};')
        self.setWindowIcon(QtGui.QIcon('troll.jpg'))
        self.editor = editor
        self.projects = {}
        self.setWindowTitle('Adequate')
        self.resize(235, 220)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(80, 20, 71, 20))
        self.label.setObjectName("label")
        # список проекта
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setStyleSheet(f'background: rgb{GRAY};color: rgb{WHITE}')
        self.comboBox.setGeometry(QtCore.QRect(50, 50, 131, 22))
        self.comboBox.setObjectName("comboBox")
        with sqlite3.connect('Folder.db') as self.con:  # программа берет данные с базы данных Folder, хранянящей
            # проекты
            self.cur = self.con.cursor()
            self.cur.execute('Create table IF NOT EXISTS folder (folder text)')
            folders = self.cur.execute('Select folder from folder').fetchall()
            if folders:
                for i in folders:
                    self.comboBox.addItem(i[0])
        # кнопка добавления проекта
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setStyleSheet(f'background: rgb{GRAY};color: rgb{WHITE}')
        self.pushButton.setGeometry(QtCore.QRect(10, 100, 101, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Insert project")
        self.pushButton.clicked.connect(self.insertProject)
        # кнопка удаления проекта
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setStyleSheet(f'background: rgb{GRAY};color: rgb{WHITE}')
        self.pushButton_2.setGeometry(QtCore.QRect(10, 130, 101, 23))
        self.pushButton_2.setText("Delete project")
        self.pushButton_2.clicked.connect(self.deleteProject)
        self.label.setText("Your projects")
        self.label.setStyleSheet('color: white;')
        # кнопка открытия проекта
        self.pushButton_3 = QtWidgets.QPushButton('Open project', self)
        self.pushButton_3.setStyleSheet(f'background: rgb{GRAY};;color: rgb{WHITE}')
        self.pushButton_3.setGeometry(QtCore.QRect(10, 190, 101, 23))
        self.pushButton_3.clicked.connect(self.open_Project)
        # кнопка создания нового проекта (проект автоматически не
        # добавляется к списку проектов и его нужно добавлять вручную)
        self.pushButton_4 = QtWidgets.QPushButton('Create project', self)
        self.pushButton_4.setStyleSheet(f'background: rgb{GRAY};;color: rgb{WHITE}')
        self.pushButton_4.setGeometry(QtCore.QRect(10, 160, 101, 23))
        self.pushButton_4.clicked.connect(self.createProject)

    # в этом методе вызывется вышеуказанное окно CreateFolder для создания новой папки
    def createProject(self):
        self.f = CreateFolder()
        self.f.show()

    # insertProject - метод для добавления проектов
    def insertProject(self):
        # диалог, получающий имя проекта
        text = QtWidgets.QFileDialog().getExistingDirectory(self, 'Folder', '')
        if text.split() != ' ' and text:
            # добавление проекта в базу
            self.cur.execute(f'Insert Into folder Values("{text}")')
            self.con.commit()
            folders = self.cur.execute('Select folder from folder').fetchall()
            self.comboBox.clear()
            for i in folders:
                self.comboBox.addItem(i[0])

    # deleteProject - метод, вызывающий окно для подтверждения того,
    # что пользователь действительно хочет удалить проект
    def deleteProject(self):
        msg = QtWidgets.QMessageBox()
        msg.setText('Are you want delete this project?')
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        exec2 = msg.exec()
        if exec2 == QtWidgets.QMessageBox.Ok:
            self.deleteButtonClicked()
        else:
            self.deleteButtonClicked()

    # в этом методе удаляется проект после выбора пользователя
    def deleteButtonClicked(self):
        self.cur.execute(f'''Delete from folder Where folder = "{self.comboBox.currentText()}"''')
        self.con.commit()
        folders = self.cur.execute('Select folder from folder').fetchall()
        self.comboBox.clear()
        for i in folders:
            self.comboBox.addItem(i[0])

    # основной метод, открывающий проект и главное окно
    def open_Project(self):
        try:
            if self.comboBox.count() > 0:
                self.editor = self.editor(self.comboBox.currentText())
                self.editor.show()
                self.hide()
        except FileNotFoundError:
            # сценарий в случае, что пользователь откроет несуществующий проет
            msg = QtWidgets.QMessageBox()
            msg.setText('Program can`t find this project')
            msg.setIcon(QtWidgets.QMessageBox.Question)
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            exec2 = msg.exec()
            if exec2 == QtWidgets.QMessageBox.Ok:
                msg.hide()


# Переопределенный класс для подсветки синтаксиса в редакторе кода
class SyntaxHighLighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        # команды, подсвечевающиеся оранжевым цветом
        keywords = [
            "and", "as", "assert", "break", "class",
            "continue", "def", "del", "elif", "else", "except",
            "exec", "finally", "for", "from", "global", "if",
            "import", "in", "is", "lambda", "not", "or", "pass",
            "raise", "return", "try", "while", "with", "yield", ",", "True", "False", "None"]
        # отдельный список для self
        self_ = ["self"]
        format1 = QtGui.QTextCharFormat()  # формат для self
        format1.setForeground(QtGui.QColor(*PURPLE))
        format2 = QtGui.QTextCharFormat()
        format2.setForeground(QtGui.QColor(*GREEN))  # формат для кавычек
        format3 = QtGui.QTextCharFormat()
        format3.setForeground(QtGui.QColor(*ORANGE))  # формат для keywords
        # списки pattern, хранящие в себе формат и слова для подсветки
        patterns1 = [([fr"\b{i}\b" for i in self_], format1)]
        patterns2 = [(("'([^'']*)'", '"([^""]*)"'), format2)]
        patterns3 = [([fr"\b{i}\b" for i in keywords], format3)]
        patterns_ = [patterns1, patterns3, patterns2]
        self.highlightingRules = []
        for style in patterns_:
            for pattern_, format_ in style:
                for pattern in pattern_:
                    self.highlightingRules += [(QtCore.QRegExp(pattern), format_)]

    def highlightBlock(self, text):
        # подсветка слов
        for pattern, _format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, _format)
                index = expression.indexIn(text, index + length)


# небольшой метод для Информации о проекте
class About(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('troll.jpg'))
        self.setWindowTitle('About Program')
        self.label = QtWidgets.QLabel(self)
        self.label.move(65, 30)
        self.label.setText('Adequate V1.0')
        self.label2 = QtWidgets.QLabel(self)
        self.label2.move(30, 50)
        self.label2.resize(157, 24)
        self.label2.setText('Топ 10 тысяч по адекватности')
        self.resize(200, 100)


# основной класс
class Adequate(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, project):
        super().__init__()
        # в конструкторе класса мы выполняем важнейшие методы
        self.resize(1600, 900)
        self.setWindowIcon(QtGui.QIcon('troll.jpg'))
        self.setupUi(self)  # метод из класса Ui_MainWindow, создающий основные виджеты
        self.project = project  # название файла
        self.initUI()
        self.createFolderActions()
        self.createFilesActions()
        self.createEditsActions()
        self.createExecuteActions()
        self.createViewAction()
        self.createReferenceAction()
        self.setStyleSheet(f'background: rgb{GRAY};')

    def initUI(self):
        # в этом методе мы создаем основные объекты класса
        self.ok = False
        self.flag = False
        self.setWindowTitle('Adequate')
        self.label = QtWidgets.QLabel('Откройте файл', self)
        self.label.move(1000, 400)
        self.menu = QtWidgets.QMenu(self)
        # меню редактора
        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.addMenu(self.menu)
        self.menuBar.setStyleSheet(f'background: rgb{GRAY};')
        self.setMenuBar(self.menuBar)
        # self.plainTextEdit - поле редактирования кода
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setStyleSheet(f'background: rgb{DARK_GRAY};color: white;border: 1px solid #808080;')
        self.plainTextEdit.hide()
        self.highlighter = SyntaxHighLighter(self.plainTextEdit.document())  # вызов SyntaxHighLighter
        # self.treeWidget панель, для просмотра проекта и выбора файлов
        self.treeWidget.setStyleSheet(f'background: rgb{GRAY};color: white;')
        self.AlphaItem = Qt.QTreeWidgetItem([os.path.basename(self.project)])  # главный элемент древа
        self.AlphaItem.setIcon(0, QtGui.QIcon('folder.png'))
        self.treeWidget.addTopLevelItem(self.AlphaItem)
        # скрытие лишнего в древе
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.itemDoubleClicked.connect(self.getFile)
        self.items = []  # список для удобной работы с элементами проекта
        self.CreateTree(self.project + '\\', self.AlphaItem)  # создание древа
        self.autoOpenFile()
        self.console = QtWidgets.QPlainTextEdit(self)  # консоль вывода
        self.console.hide()
        # установка размеров консоли
        self.console.resize(1600, 151)
        self.console.move(0, 592)
        self.console.setStyleSheet(f'background: rgb{GRAY};color: white;border: 1px solid #808080;')
        self.writeConsole = QtWidgets.QPlainTextEdit(self)  # консоль ввода
        self.writeConsole.hide()
        # установка размеров консоли
        self.writeConsole.resize(1600, 40)
        self.writeConsole.move(0, 742)
        self.writeConsole.setStyleSheet(f'background: rgb{GRAY};color: white;border: 1px solid #808080;')
        self.writeConsole.blockCountChanged.connect(self.write)
        # self.pushButton - кнопка отображения консоли
        self.pushButton.setText('console')
        self.pushButton.setStyleSheet(f'background: rgb{GRAY};color: white;border: 1px solid #808080;')
        self.pushButton.clicked.connect(self.showConsole)
        # self.pushButton - кнопка обновдения древа
        self.pushButton_2.setStyleSheet(f'background: rgb{GRAY};color: white;border: 1px solid #808080;')
        self.pushButton_2.clicked.connect(self.updateTree)
        # настройка табуляции
        self.plainTextEdit.setTabStopWidth(self.plainTextEdit.fontMetrics().width(' ', 1) * 4)
        self.console.setTabStopWidth(self.plainTextEdit.fontMetrics().width(' ', 1) * 4)
        self.writeConsole.setTabStopWidth(self.plainTextEdit.fontMetrics().width(' ', 1) * 4)

    def updateTree(self):
        # обновления древа в случае удаления или добавления или
        # других действий с файлами проекта(если пользователь нажмет на кнопку)
        # очищение древа и последующее его заполнение, а также скрытие редактора,
        # чтобы пользователь открыл файл
        self.items.clear()
        self.treeWidget.clear()
        self.AlphaItem = Qt.QTreeWidgetItem([os.path.basename(self.project)])
        self.treeWidget.addTopLevelItem(self.AlphaItem)
        self.treeWidget.setHeaderHidden(True)
        self.CreateTree(self.project + '\\', self.AlphaItem)
        self.treeWidget.itemDoubleClicked.connect(self.getFile)
        self.label.show()
        self.plainTextEdit.clear()
        self.plainTextEdit.hide()
        self.autoOpenFile()

    def autoOpenFile(self):
        self.flag2 = False
        for i in self.items:  # открытие первого python файла, в противном случае,
            # программа ожидает ручного открытия
            if len(i) > 1:
                # проверка на python файл
                if 'py' in i[0].split('.')[-1] and 2 <= len(i[0].split('.')[-1]) <= 3:
                    self.text = i[2]
                    self.ok = True
                    self.plainTextEdit.setPlainText(open(i[2], encoding='utf8').read())
                    self.flag2 = True
                    # открытие редактора и скрытия текста (который говорит пользователю отркыть файл)
                    self.plainTextEdit.show()
                    self.label.hide()
                    break

    # создание меню вида
    def createViewAction(self):
        # меню вида
        self.viev = self.menuBar.addMenu('View')
        # дейстиве, изменяющее тему редактора на темную
        self.darkTheme = QtWidgets.QAction('Dark theme', self)
        # дейстиве, изменяющее тему редактора на светлую
        self.LightTheme = QtWidgets.QAction('Light theme', self)
        self.viev.addActions([self.darkTheme, self.LightTheme])
        # сигналы
        self.LightTheme.triggered.connect(self.setLight)
        self.darkTheme.triggered.connect(self.setDark)

    # метод меняющий тему на светлую
    def setLight(self):
        # фон каждого элемента по умолчанию.
        self.plainTextEdit.setStyleSheet(f'')
        self.console.setStyleSheet(f'')
        self.writeConsole.setStyleSheet(f'')
        self.pushButton.setStyleSheet(f'')
        self.treeWidget.setStyleSheet(f'')
        self.menuBar.setStyleSheet(f'')
        self.setStyleSheet(f'')

    # метод меняющий тему на темную
    def setDark(self):
        # фон каждого элемента серый
        self.plainTextEdit.setStyleSheet(f'background: rgb{DARK_GRAY};color: white;border: 1px solid #808080;')
        self.console.setStyleSheet(f'background: rgb{GRAY};color: white;border: 1px solid #808080;')
        self.writeConsole.setStyleSheet(f'background: rgb{GRAY};color: white;border: 1px solid #808080;')
        self.pushButton.setStyleSheet(f'background: rgb{GRAY};color: white;border: 1px solid #808080;')
        self.treeWidget.setStyleSheet(f'background: rgb{GRAY};color: white;')
        self.menuBar.setStyleSheet(f'background: rgb{GRAY};')
        self.setStyleSheet(f'background: rgb{GRAY};')

    # создание справочного меню
    def createReferenceAction(self):
        # меню справки
        self.Reference = self.menuBar.addMenu('Reference')
        # создание действия, вызывающее окно информации о проекте
        self.AboutProgramAction = QtWidgets.QAction('About Program', self)
        self.Reference.addAction(self.AboutProgramAction)
        self.AboutProgramAction.triggered.connect(self.getInfo)

    # отображение окна с информацией
    def getInfo(self):
        self.Info = About()
        self.Info.show()

    # добавление данных в поток stdin
    def write(self):
        # текст из консоли ввода данных
        text = self.writeConsole.toPlainText().split('\n')[-2] + '\n'
        self.p.write(text.encode())

    # вызов консоли
    def showConsole(self):
        if not self.flag:
            # консоль видна
            self.console.show()
            self.writeConsole.show()
            self.flag = True
        else:
            # консоли скрыта
            self.console.hide()
            self.writeConsole.hide()
            self.flag = False

    # выбор файла для редактирования
    def getFile(self, item):
        for i in self.items:
            if len(i) > 1:  # проверка является ли элемент файлом
                if i[1] == item:
                    # теперь self.text равен адресу нового файла
                    self.text = i[2]
                    self.ok = True  # эта переменная говорит нам о том, что файл открыт
                    self.plainTextEdit.setPlainText(open(i[2], encoding='utf8').read())
                    # теперь редактор виден, а текст, говорящий нам закрыть файл
                    self.plainTextEdit.show()
                    self.label.hide()

    # создание древа, рекурсивно открывая папки
    # file - изначальный файл, parent_item - родительская папка
    def CreateTree(self, file, parent_item):
        for i in os.listdir(file):
            new_item = Qt.QTreeWidgetItem([i])  # новый элемент
            # иконки файлов
            fileTypes = ['html', 'c', 'cpp', 'css', 'js', 'java', 'txt', 'dll', 'zip', 'mp3', 'png', 'jpg']
            if 'py' in i.split('.')[-1] and 2 <= len(i.split('.')[-1]) <= 3 or i.split('.') \
                    == 'pywz' or i.split('.') == 'py [cod]':
                new_item.setIcon(0, QtGui.QIcon('python.png'))
                parent_item.addChild(new_item)
            elif i.split('.')[-1] in fileTypes:
                # добавление иконки к файлу
                new_item.setIcon(0, QtGui.QIcon(f'{i.split(".")[-1]}.png'))
                parent_item.addChild(new_item)
            else:
                # добавления стандартной иконке в случае отсутствия расширения файла в fileTypes
                new_item.setIcon(0, QtGui.QIcon('text.png'))
                parent_item.addChild(new_item)
            if os.path.isdir(file + i):
                # если элемет папка. то рекурсивано открываем её
                new_item.setIcon(0, QtGui.QIcon('folder.png'))
                self.items.append((i))
                self.CreateTree(file + i + '\\', new_item)
            else:
                self.items.append((i, new_item, file + i))

    # создание меню папок
    def createFolderActions(self):
        # меню папок
        self.folder = self.menuBar.addMenu('Folder')
        # действие открытия
        self.openFolder = QtWidgets.QAction('Open folder')
        self.openFolder.triggered.connect(self.openFolder_)
        # действие создания
        self.createFolderAction = QtWidgets.QAction('Create folder')
        self.createFolderAction.triggered.connect(self.createFolder)
        # сигнал на каждое из действий
        self.folder.addAction(self.openFolder)
        self.folder.addAction(self.createFolderAction)

    # создание новой папки
    def createFolder(self):
        # диалог для получения название новой папки
        name, ok = QtWidgets.QInputDialog.getText(self, 'New Folder', 'Write folder and address')
        if ok:
            # с помощью os создаём папку
            if name not in os.listdir(self.project):
                os.mkdir(self.project + '\\' + name)
            else:
                # если проект уже существует
                msg = QtWidgets.QMessageBox()
                msg.setText('Program can`t create folder, because this file exists already in project')
                msg.setIcon(QtWidgets.QMessageBox.Question)
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                exec2 = msg.exec()
                if exec2 == QtWidgets.QMessageBox.Ok:
                    msg.hide()
            # обновление древа проекта
            self.treeWidget.clear()
            # создание нового главного элемента
            self.AlphaItem = Qt.QTreeWidgetItem([os.path.basename(self.project)])
            # добавление главного элемента
            self.treeWidget.addTopLevelItem(self.AlphaItem)
            # скрытие лишнего
            self.treeWidget.setHeaderHidden(True)
            # запись в древо файлов
            self.CreateTree(self.project + '\\', self.AlphaItem)
            # сигнал на каждый элемент
            self.treeWidget.itemDoubleClicked.connect(self.getFile)

    # открытие папки с обновлением древа на новое
    def openFolder_(self):
        # диалог для получения название папки
        project = QtWidgets.QFileDialog().getExistingDirectory(self, 'Choose folder', '')
        if project:
            # обновления древа
            self.items.clear()
            # присвоить переменной значение адреса нового проекта
            self.project = project
            # очищение древа
            self.treeWidget.clear()
            # создание нового главного элемента
            self.AlphaItem = Qt.QTreeWidgetItem([os.path.basename(self.project)])
            # добавление главного элемента
            self.treeWidget.addTopLevelItem(self.AlphaItem)
            # скрытие лишнего
            self.treeWidget.setHeaderHidden(True)
            # запись в древо файлов
            self.CreateTree(self.project + '\\', self.AlphaItem)
            # сигнал на каждый элемент
            self.treeWidget.itemDoubleClicked.connect(self.getFile)
            # текст label (просящйи открыть файл) будет виден до тех пор пока новый файл не будет открыт
            self.label.show()
            # очищение редактора
            self.plainTextEdit.clear()
            # скрытие редактора
            self.plainTextEdit.hide()
            # попытка открыть файл
            self.autoOpenFile()

    # создание меню файлов
    def createFilesActions(self):
        # меню файлов
        self.fileMenu = self.menuBar.addMenu('File')
        # действие создания нового файла
        self.createAction = QtWidgets.QAction('New', self)
        # действие открытия нового окна
        self.newAction = QtWidgets.QAction('New window', self)
        # действие открытия файла
        self.openAction = QtWidgets.QAction('Open', self)
        # действие сохранения файла
        self.saveAction = QtWidgets.QAction('Save', self)
        # действие сохранения файла по усмотрению пользователя
        self.saveAsAction = QtWidgets.QAction('Save as', self)
        # действие выхода из приложения
        self.exitAction = QtWidgets.QAction('Exit', self)
        self.fileMenu.addAction(self.createAction)
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.saveAsAction)
        self.fileMenu.addAction(self.exitAction)
        # сингналы действий
        self.exitAction.triggered.connect(self.exit_)
        self.createAction.triggered.connect(self.createFile_)
        self.openAction.triggered.connect(self.open_)
        self.newAction.triggered.connect(self.newWindow)
        self.saveAction.triggered.connect(self.saveFile)
        self.saveAsAction.triggered.connect(self.saveAsFile)

    # метод выхода
    def exit_(self):
        sys.exit(app.exec())

    # метод открытия файла
    def open_(self):
        # ссылка и переменная, подтверждающая открытие файла
        self.text, ok_pressed = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '', 'Файл (*.py)')
        if ok_pressed:
            # открытие и запись
            self.f = open(self.text, encoding='utf8')
            self.ok = True  # подтверждение того, что файл добавлен для последующих его изменений
            self.plainTextEdit.setPlainText(self.f.read())

    # метод создания нового файла
    def createFile_(self):
        # вызова диалога для получения названия нового файла
        name, ok = QtWidgets.QInputDialog.getText(self, 'New File', 'Write file name')
        if ok:
            # обновления древа
            open(f'{self.project}\\{name}', 'w', encoding='utf8')
            # очищение древа
            self.treeWidget.clear()
            # создание нового главного элемента
            self.AlphaItem = Qt.QTreeWidgetItem([os.path.basename(self.project)])
            # добавление главного элемента
            self.treeWidget.addTopLevelItem(self.AlphaItem)
            # скрытие лишнего
            self.treeWidget.setHeaderHidden(True)
            # запись в древо файлов
            self.CreateTree(self.project + '\\', self.AlphaItem)
            # сигнал на каждый элемент
            self.treeWidget.itemDoubleClicked.connect(self.getFile)

    # метод, открывающий новое окно
    def newWindow(self):
        self.newW = Adequate(self.project)
        self.newW.show()

    # метод сохранения файла
    def saveFile(self):
        if self.ok:
            # открытие файла и запись в него кода
            with open(self.text, 'w', encoding='utf8') as f:
                f.write(self.plainTextEdit.toPlainText())
        else:
            dialog = QtWidgets.QFileDialog.getSaveFileName(self, 'Save', '', 'Файл (*.py);; Все файлы (*)')
            # открытие файла и запись в него кода
            with open(dialog[0], 'w', encoding='utf8') as f:
                f.write(self.plainTextEdit.toPlainText())

    # метод сохранения по выбору пользователя
    def saveAsFile(self):
        # диалог открытия папок, при котором мы можем дать файлу новое имя и расширения
        dialog = QtWidgets.QFileDialog.getSaveFileName(self, 'Save', '', 'Файл (*.py);; Все файлы (*)')
        # открытие файла и запись в него кода
        with open(dialog[0], 'w', encoding='utf8') as f:
            f.write(self.plainTextEdit.toPlainText())

    # создание меню правки файла
    def createEditsActions(self):
        self.editMenu = self.menuBar.addMenu('Edit')
        self.undoAction = QtWidgets.QAction('Undo                 Ctrl+Z', self)
        self.cutOutAction = QtWidgets.QAction('Cut out             Ctrl+X', self)
        self.copyAction = QtWidgets.QAction('Copy                 Ctrl+C', self)
        self.insertAction_ = QtWidgets.QAction('Insert                 Ctrl+V')
        self.timeAction = QtWidgets.QAction('Date and time          F5')
        # действия возврата, вырезки, копирования, вставки, добавления времени
        self.editMenu.addAction(self.undoAction)
        self.editMenu.addAction(self.cutOutAction)
        self.editMenu.addAction(self.copyAction)
        self.editMenu.addAction(self.insertAction_)
        self.editMenu.addAction(self.timeAction)
        # сигналы действий
        self.undoAction.triggered.connect(self.undo)
        self.copyAction.triggered.connect(self.copy_)
        self.cutOutAction.triggered.connect(self.cutOut)
        self.insertAction_.triggered.connect(self.insert_)
        self.timeAction.triggered.connect(self.getDateTime)

    # метод возврата действия Ctrl+Z
    def undo(self):
        self.plainTextEdit.undo()

    # метод копирования Ctrl+C
    def copy_(self):
        self.plainTextEdit.copy()

    # метод вырезки действия Ctrl+X
    def cutOut(self):
        self.plainTextEdit.cut()

    # метод вcтавки Ctrl+V
    def insert_(self):
        self.plainTextEdit.insertPlainText(QtWidgets.QApplication.clipboard().text())

    # метод добавления времени Ctrl+X
    def getDateTime(self):
        # время
        time = ':'.join(str(datetime.datetime.now().time()).split(':')[:2])
        # дата
        date = '.'.join(reversed(str(datetime.datetime.now().date()).split('-')))
        # добавление даты и времени
        self.plainTextEdit.insertPlainText(f'{time} {date}')

    # создание меню команд
    def createExecuteActions(self):
        # меню команд
        self.executeMenu = self.menuBar.addMenu('Execute')
        # действие запуска
        self.RunAction = QtWidgets.QAction('Run', self)
        # действия остановки
        self.StopAction = QtWidgets.QAction('Stop', self)
        # добавление всех действий
        self.executeMenu.addAction(self.RunAction)
        self.executeMenu.addAction(self.StopAction)
        # добавление сигналов на действия
        self.RunAction.triggered.connect(self.Run)
        self.StopAction.triggered.connect(self.Stop)

    # запуск файла
    def Run(self):
        # очищение консоли
        self.console.clear()
        self.writeConsole.clear()
        # объект класса QProcess
        self.p = QtCore.QProcess()
        # сигнал readyReadStandardOutput, после которого все данные из вывода выводятся в консоль
        self.p.readyReadStandardOutput.connect(self.print_out)
        # сигнал readyReadStandardError, выводящий ошибки в консоль
        self.p.readyReadStandardError.connect(self.print_error)
        # запуск файла с помощью python
        self.p.start(f'python {self.text}')
        # открытие консоли
        self.console.show()
        self.writeConsole.show()
        self.flag = True
        # добавление названия открытого файла
        self.console.insertPlainText(f'-----{self.text}-----\n')
        # сигнал остановки
        self.p.finished.connect(self.finished)

    def print_out(self):
        # вывод данных
        out = self.p.readAllStandardOutput()  # получение вывода
        if out:
            self.console.insertPlainText(str(out, 'UTF-8') + '\n')

    def print_error(self):
        # вывод ошибок
        error = self.p.readAllStandardError()  # читание все ошибок
        if error:
            # добавление в консоль ошибки
            self.console.insertPlainText(str(error, 'UTF-8') + '\n')

    def finished(self):
        # добавление в консль статус выхода
        if len(self.console.toPlainText().split('\n')) == 2:
            # если выходных данныч нет
            self.console.insertPlainText(f'\nProcess finished with exit code {str(int(self.p.exitStatus()))}')
        else:
            self.console.insertPlainText(f'Process finished with exit code {str(int(self.p.exitStatus()))}')

    # метод остановки
    def Stop(self):
        # метод kill() удаляет процесс
        self.p.kill()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = ChooseProject(Adequate)
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec())
