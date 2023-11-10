from fake_useragent import UserAgent
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QGroupBox, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QIcon
from pySmartDL import SmartDL
import subprocess
import sys

class DownloaderThread(QThread):
    finished = pyqtSignal()
    progress_updated = pyqtSignal(int, int)
    started_download = pyqtSignal(str)
    
    def __init__(self, urlListFile, destinationFolder):
        super().__init__()
        self.urlListFile = urlListFile
        self.destinationFolder = destinationFolder
        self.stopFlag = False

    def run(self):
        with open(self.urlListFile, "r", encoding='utf-8') as f:
            urls = f.readlines()
            headers = {
                "User-Agent": f"{ua.random}"
            }
            for url in urls:
                if self.stopFlag:
                    break
                url = url
                downloadLink = url.split(";")[0]
                fileName = url.split(";")[1]
                finalDest = self.destinationFolder + '/' + fileName.replace('\n', '') + '.mp4'
                obj = SmartDL(downloadLink, dest=finalDest, progress_bar=False, request_args={'headers': headers})
                obj.start(blocking=False)
                self.started_download.emit(fileName)
                while not obj.get_status() == "finished":
                    if obj.filesize:
                        total = obj.filesize
                        downloaded = obj.get_dl_size()
                        self.progress_updated.emit(downloaded, total)
                    self.sleep(1)
                    
                obj.wait()
        self.finished.emit()

    def stop(self):
        self.stopFlag = True

class NodeAppRunner(QWidget):
    finished = pyqtSignal()

    def run_node_app(self, script_path):
        process = subprocess.Popen(['node', script_path])
        process.wait()

        self.finished.emit()

class ExternalScriptRunner(QWidget):
    finished = pyqtSignal()

    def run_script(self, url, totalEps):
        subprocess.run(['python', '-c', f'import getEpis; getEpis.create_input_file("{url}", {totalEps})'], shell=True)

class DownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setupThreadSignals()

    def initUI(self):
        mainLayout = QVBoxLayout()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateWindowTitle)
        self.timer.start(3000)
        
        # GroupBox Arası Boşluk

        anotherBlankSpace = QLabel("")
        anotherBlankSpace.setFixedHeight(10)
        mainLayout.addWidget(anotherBlankSpace)
        
        # Durum Etiketi
        
        self.statusLabel = QLabel('HAZIR')
        mainLayout.addWidget(self.statusLabel)
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.statusLabel.setStyleSheet('font-size: 15px; font-weight: bold;')

        # GroupBox Arası Boşluk

        anotherBlankSpace = QLabel("")
        anotherBlankSpace.setFixedHeight(10)
        mainLayout.addWidget(anotherBlankSpace)

        # Bölüm Linki Oluşturma

        fetchSectionsGroupBox = QGroupBox("Oluştur")
        fetchSectionsLayout = QVBoxLayout()
        
        urlLabel = QLabel('URL:')
        self.urlInput = QLineEdit(self)
        fetchSectionsLayout.addWidget(urlLabel)
        fetchSectionsLayout.addWidget(self.urlInput)

        totalEpsLabel = QLabel('Toplam Bölüm:')
        self.totalEpsInput = QLineEdit(self)
        fetchSectionsLayout.addWidget(totalEpsLabel)
        fetchSectionsLayout.addWidget(self.totalEpsInput)

        self.fetchSectionsButton = QPushButton('Bölüm Linklerini Oluştur', self)
        self.fetchSectionsButton.clicked.connect(self.runExternalScript)
        fetchSectionsLayout.addWidget(self.fetchSectionsButton)

        fetchSectionsGroupBox.setLayout(fetchSectionsLayout)
        mainLayout.addWidget(fetchSectionsGroupBox)

        # GroupBox Arası Boşluk

        anotherBlankSpace = QLabel("")
        anotherBlankSpace.setFixedHeight(10)
        mainLayout.addWidget(anotherBlankSpace)

        # İndirme Linklerini Üret

        runNodeAppGroupBox = QGroupBox("Çek")
        runNodeAppLayout = QVBoxLayout()

        self.runNodeAppButton = QPushButton('Linkleri Çek', self)
        self.runNodeAppButton.clicked.connect(self.runNodeApp)
        runNodeAppLayout.addWidget(self.runNodeAppButton)

        runNodeAppGroupBox.setLayout(runNodeAppLayout)
        mainLayout.addWidget(runNodeAppGroupBox)

        # GroupBox Arası Boşluk

        anotherBlankSpace = QLabel("")
        anotherBlankSpace.setFixedHeight(10)
        mainLayout.addWidget(anotherBlankSpace)

        # Dosyaları İndirme

        downloadGroupBox = QGroupBox("İndir")
        downloadLayout = QVBoxLayout()

        self.selectURLButton = QPushButton('Bölüm Listesini Seç', self)
        self.selectURLButton.clicked.connect(self.selectURLList)
        downloadLayout.addWidget(self.selectURLButton)

        self.selectDestButton = QPushButton('Kayıt Yerini Seç', self)
        self.selectDestButton.clicked.connect(self.selectDestinationFolder)
        downloadLayout.addWidget(self.selectDestButton)
        
        self.startStopButton = QPushButton('Başlat', self)
        self.startStopButton.clicked.connect(self.startStopDownload)
        downloadLayout.addWidget(self.startStopButton)

        downloadGroupBox.setLayout(downloadLayout)
        mainLayout.addWidget(downloadGroupBox)

        self.setLayout(mainLayout)
        self.setWindowTitle('SibnetDL')
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(100, 100, 500, 300)
        self.show()

        self.thread = None
        
    def setupThreadSignals(self):
        if self.thread:
            self.thread.started_download.connect(self.updateStatusLabel)
        
    def updateStatusLabel(self, file_name):
        self.statusLabel.setText(f"İndirilen dosya: {file_name}")
    
    def updateWindowTitle(self):
        if self.thread and self.thread.isRunning():
            total, current = getattr(self.thread, 'total_sections', 0), getattr(self.thread, 'downloaded_sections', 0)
            try:
                percentage = round(current / total * 100, 2)
            except ZeroDivisionError:
                percentage = 0
            self.setWindowTitle(f'İndirilen: %{percentage}')
        else:
            self.setWindowTitle('SibnetDL')

    def selectURLList(self):
        options = QFileDialog.Options()
        urlListFile, _ = QFileDialog.getOpenFileName(self, "Metin Belgesini Seç", "", "Text Files (*.txt)", options=options)
        if urlListFile:
            self.urlListFile = urlListFile
            self.statusLabel.setText(f'Seçilen Dosya: {urlListFile}')

    def selectDestinationFolder(self):
        options = QFileDialog.Options()
        destinationFolder = QFileDialog.getExistingDirectory(self, "Nereye Kaydedileceğini Seç", options=options)
        if destinationFolder:
            self.destinationFolder = destinationFolder
            self.statusLabel.setText(f'Kayıt Yeri: {destinationFolder}')

    def startStopDownload(self):
        if not hasattr(self, 'urlListFile') or not hasattr(self, 'destinationFolder'):
            self.statusLabel.setText('Lütfen Metin Belgesini ve Kayıt Yerini Seçin.')
            return
        
        if not self.thread or not self.thread.isRunning():
            self.runNodeAppButton.setEnabled(False)
            self.fetchSectionsButton.setEnabled(False)
            self.selectDestButton.setEnabled(False)
            self.selectURLButton.setEnabled(False)
            
            self.thread = DownloaderThread(self.urlListFile, self.destinationFolder)
            self.thread.finished.connect(self.downloadFinished)
            self.thread.progress_updated.connect(self.onProgressUpdate)
            self.thread.started_download.connect(self.statusLabelUpdate)
            self.thread.start()
            self.startStopButton.setText('Durdur')
        else:
            self.thread.stop()
            self.startStopButton.setEnabled(False)
    
    def statusLabelUpdate(self, fileName):
        self.statusLabel.setText(f'İndirilen Dosya: \n{fileName}')
    
    def onProgressUpdate(self, downloaded, total):
        self.thread.downloaded_sections = downloaded
        self.thread.total_sections = total

    def runExternalScript(self):
        self.script_runner = ExternalScriptRunner()
        self.script_runner.finished.connect(self.onScriptFinished)
        script_path = './getEpis.py'
        url = self.urlInput.text()
        totalEps = self.totalEpsInput.text()
        self.script_runner.run_script(script_path, url, totalEps)

    def runNodeApp(self):
        self.node_runner = NodeAppRunner()
        self.node_runner.finished.connect(self.onScriptFinished)
        self.node_runner.run_node_app('app.js')

    def downloadFinished(self):
        self.startStopButton.setEnabled(True)
        self.startStopButton.setText('Başlat')
        self.statusLabel.setText('İndirme Tamamlandı.')

    def onScriptFinished(self):
        self.statusLabel.setText('Script Başarıyla Çalıştırıldı.')

    def closeEvent(self, event):
        if self.thread and self.thread.isRunning():
            self.thread.stop()
            self.thread.wait()
        event.accept()

def run_app():
    app = QApplication(sys.argv)
    downloader = DownloaderApp()  # noqa: F841
    sys.exit(app.exec_())

if __name__ == '__main__':
    ua = UserAgent()
    run_app()
