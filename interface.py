import subprocess
import sys

def install_dependencies():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Установка зависимостей прошла успешно.")
    except subprocess.CalledProcessError:
        print("Ошибка при установке зависимостей.")

def check_dependencies():
    try:
        import pyperclip # Замени "required_module" на фактический импортируемый модуль
        from PyQt6.QtGui import QAction, QIcon
        from PyQt6.QtWidgets import QToolBar, QComboBox, QDialog, QStatusBar, QApplication, QMainWindow, QLabel, \
            QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QWidget, QTextBrowser
        print("Все необходимые зависимости установлены.")
    except ImportError:
        print("Не все зависимости установлены.")
        install_dependencies()

import pyperclip
import model_add as gpt

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QToolBar, QComboBox, QDialog, QStatusBar, QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QWidget, QTextBrowser

chat = []

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("ChatBot")

        self.setWindowIcon(QIcon("icons/gpt4free_icon.png"))

        self.setGeometry(800, 350, 400, 500)

        menu = self.menuBar()
        settings_menu = menu.addMenu("&Settings")

        lang = settings_menu.addMenu("&Language")
        eng_lang = QAction("&English", self)
        rus_lang = QAction("&Русский", self)
        ger_lang = QAction("&Deutch", self)
        lang.addAction(eng_lang)
        lang.addAction(rus_lang)
        lang.addAction(ger_lang)
        lang.setStatusTip("Change language")

        context = QAction("&Maintains context", self)
        context.setStatusTip("Maintains context/does not maintains context")
        context.setCheckable(True)
        context.setChecked(True)
        context.triggered.connect(self.contextChanged)

        version = QAction("GPT version", self)
        version.setStatusTip("Choose GPT version")

        #settings_menu.addAction(lang)
        settings_menu.addAction(context)

        self.toolbar = QToolBar("Toolbar")

        self.addToolBar(self.toolbar)

        copy_action = QAction(QIcon("icons/copyIcon.png"), "Copy", self)
        copy_action.setStatusTip("Copy last ChatGPT's message")
        copy_action.triggered.connect(self.copyClick)

        clear_action = QAction(QIcon("icons/clear.png"), "Clear", self)
        clear_action.setStatusTip("Clear chat history")
        clear_action.triggered.connect(self.clearClick)

        aboutDialog = QAction(QIcon("icons/infoIcon.png"), "About", self)
        aboutDialog.setStatusTip("About program")
        aboutDialog.triggered.connect(self.aboutClick)

        self.versComboBox = QComboBox()

        self.versComboBox.addItems(gpt.ver_list)

        self.versComboBox.currentIndexChanged.connect(self.idxChanged)

        self.toolbar.addAction(copy_action)
        self.toolbar.addAction(clear_action)
        self.toolbar.addAction(aboutDialog)

        self.toolbar.addWidget(QLabel("GPT Ver.:"))
        self.toolbar.addWidget(self.versComboBox)

        self.toolbar.setContentsMargins(1, 1, 1, 1)

        self.toolbar.setStyleSheet("QToolBar{spacing:10px;}")

        self.setStatusBar(QStatusBar(self))

        self.input = QLineEdit(text="Ask a question")
        self.output = QTextBrowser()
        self.sendButton = QPushButton()
        self.sendButton.setMinimumSize(70, 20)
        self.sendButton.setIcon(QIcon("icons/sendIcon.png"))
        self.sendButton.clicked.connect(self.sendClicked)

        self.hello_message = ("<b>ChatGPT:</b><br />" + gpt.get_responce("Hello"))

        chat.append(self.hello_message)

        self.output.setHtml('<br />'.join(chat))

        self.responceLayout = QVBoxLayout()
        self.responceLayout.addWidget(self.output)
        self.promptLayout = QHBoxLayout()
        self.promptLayout.addWidget(self.input)
        self.promptLayout.addWidget(self.sendButton)

        self.commonLayout = QVBoxLayout()
        self.commonLayout.addLayout(self.responceLayout)
        self.commonLayout.addLayout(self.promptLayout)

        self.setMinimumSize(200, 250)
        self.setMaximumSize(1200, 800)

        widget = QWidget()

        widget.setLayout(self.commonLayout)

        self.setCentralWidget(widget)

    def copyClick(self, s):
        for message in gpt.messages:
            if message["role"] == "assistant":
                pyperclip.copy(message["content"])

    def clearClick(self):
        gpt.messages.clear()
        chat.clear()
        chat.append(self.hello_message)
        self.output.setText('<br />'.join(chat))

    def contextChanged(self, s):
        gpt.maintain_context = s

    def aboutClick(self):
        about_dlg = QDialog(self)
        about_dlg.setWindowTitle("About")
        about_dlg.setWindowIcon(QIcon("icons/infoIcon.png"))
        lt = QVBoxLayout()
        lbl = QLabel()
        lbl.setText("GPT-Version: " + str(gpt.chosen_model))
        lt.addWidget(lbl)
        about_dlg.setLayout(lt)
        about_dlg.exec()

    def sendClicked(self):
        prompt = self.input.text()

        resp = gpt.get_responce(prompt)

        resp_formatted = format_string(resp)

        output_text = ("<br /><b>You:</b><br />" + prompt +
                       "<br /><br /><b>ChatGPT:</b><br />" + resp_formatted)

        chat.append(output_text)

        self.output.setHtml('<br />'.join(chat))
        self.input.setText("Ask a question")

    #def keyPressEvent(self, event):
     #   print('Enter pressed')
      #  print(event.key())
       # if (event.key() == 16777220) or (event.key() == 43):
        #    self.sendClicked()
       # else:
        #    super().keyPressEvent(event)

    def idxChanged(self):
        gpt.set_model(self.versComboBox.currentIndex())
        self.clearClick()

def format_string(input_string: str) -> str:
    split_string = input_string.split('\n')

    formatted_lines = []

    for line in split_string:
        if line == "```":
            formatted_lines.append('</b>')
        elif line.startswith('```'):
            formatted_lines.append(f'<b>{line.split("```")[1]}')
        else:
            formatted_lines.append(line)
    return '<br />'.join(formatted_lines)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()