#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from .. import utils
from .ui.ui_wblower import Ui_WBlower


class WBlower(QtWidgets.QDialog, Ui_WBlower):
    sigClosed = QtCore.pyqtSignal()
    sigConnect = QtCore.pyqtSignal(str, str, str, str, str)
    sigDisconnect = QtCore.pyqtSignal()
    sigRun = QtCore.pyqtSignal(float, float)
    sigShowSeqAction = QtCore.pyqtSignal(dict, object)
    sigCreateSeqAction = QtCore.pyqtSignal(dict, object, bool)

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.signalOnHold = None
        self.holdTemp = 0.
        self.temps = []
        self.runPlot = False
        self.paused = False
        self.setupUi(self)
        self.loadSettings()
        self.sigShowSeqAction.connect(self.showSeqAction)
        self.buttonDisconnect.hide()
        self.editError.setValidator(QtGui.QDoubleValidator())
        self.editComTimout.setValidator(QtGui.QIntValidator())

    def pause(self):
        pass

    def resume(self):
        pass

    def closeEvent(self, event):
        self.on_buttonDisconnect_clicked()
        self.saveSettings()
        self.sigClosed.emit()

    def saveSettings(self):
        s = QtCore.QSettings()
        s.setValue('WBlower/Geometry', self.saveGeometry())
        s.setValue('WBlower/target', self.spinTarget.value())
        s.setValue('WBlower/ramp', self.spinRamp.value())
        s.setValue('WBlower/host', self.editHost.text())
        s.setValue('WBlower/session', self.editSession.text())
        s.setValue('WBlower/counter', self.editCounter.text())
        s.setValue('WBlower/rampcmd', self.editRamp.text())
        s.setValue('WBlower/error', self.editError.text())
        s.setValue('WBlower/timeout', self.editComTimout.text())
        s.setValue('WBlower/tempcmd', self.editTemp.text())

    def loadSettings(self):
        s = QtCore.QSettings()
        self.restoreGeometry(s.value('WBlower/Geometry', QtCore.QByteArray()))
        self.spinTarget.setValue(float(s.value('WBlower/target', 25)))
        self.spinRamp.setValue(float(s.value('WBlower/ramp', 1)))
        self.editHost.setText(s.value('WBlower/host', 'snbla1.esrf.fr'))
        self.editSession.setText(s.value('WBlower/session', 'rheuro'))
        self.editCounter.setText(s.value('WBlower/counter', 'ceuro'))
        self.editRamp.setText(s.value('WBlower/rampcmd', 'euro2400parameters unit=0 RampRate={:.2f}'))
        self.editError.setText(s.value('WBlower/error', str(utils.DEFAULT_ERROR)))
        self.editComTimout.setText(s.value('WBlower/timeout', str(utils.DEFAULT_TIMEOUT)))
        self.editTemp.setText(s.value('WBlower/tempcmd', 'umv meuro {:.2f}'))

    @QtCore.pyqtSlot()
    def on_buttonClose_clicked(self):
        self.resume()
        self.close()

    def updateTemperature(self, value):
        if self.runPlot:
            self.temps.append(value)
            self.plotView.plot(y=self.temps, pen='g', clear=True)
        self.labelTemp.setText(f'<html><head/><body><p>{value:.1f} &deg;C</p></body></html>')
        try:
            error = float(self.editError.text())
        except ValueError:
            error = utils.DEFAULT_ERROR
        if self.signalOnHold and abs(value - self.holdTemp) < error:
            signal = self.signalOnHold
            self.signalOnHold = None
            signal.emit()

    @QtCore.pyqtSlot()
    def on_buttonRun_clicked(self):
        self.runBlower(self.spinTarget.value(), self.spinRamp.value())

    def runBlower(self, target, ramp):
        self.resume()
        self.labelCurrent.setText(f'<html><head/><body><p>{target:.1f} &deg;C | {ramp}&deg;C/min</p></body></html>')
        self.sigRun.emit(target, ramp)

    @QtCore.pyqtSlot()
    def on_buttonToSeq_clicked(self):
        target = self.spinTarget.value()
        ramp = self.spinRamp.value()
        self.createAction(target, ramp, False)

    def createAction(self, target, ramp, now):
        d = {
            f'Eurotherm: to {target:.1f} C with the rate {ramp:.1f} deg/min':
                {
                    f'Target temperature: {target:.1f} C': f'spinTarget={target:.1f}',
                    f'Ramp rate: {ramp:.1f} deg/min': f'spinRamp={ramp:.1f}'
                }
        }
        self.spinTarget.setValue(target)
        self.spinRamp.setValue(ramp)
        self.sigCreateSeqAction.emit(d, self.sigShowSeqAction, now)

    def showSeqAction(self, action, signal):
        for v in list(action.values())[0].values():
            name, val = v.split('=')
            self.__dict__[name].setValue(float(val))
        if signal:
            self.holdTemp = self.spinTarget.value()
            self.on_buttonRun_clicked()
            signal.emit()

    def setSignalOnHold(self, action, signal):
        if signal:
            self.resume()
            self.euroAction = action
            try:
                timeout = int(self.editComTimout.text())
            except ValueError:
                timeout = utils.DEFAULT_TIMEOUT
            QtCore.QTimer.singleShot(timeout, lambda: setattr(self, 'signalOnHold', signal))

    @QtCore.pyqtSlot()
    def on_buttonStartPlot_clicked(self):
        if self.runPlot:
            self.runPlot = False
            self.buttonStartPlot.setText('Start')
            self.buttonStartPlot.setIcon(QtGui.QIcon(':/run'))
        else:
            self.runPlot = True
            self.buttonStartPlot.setText('Stop')
            self.buttonStartPlot.setIcon(QtGui.QIcon(':/stop'))

    @QtCore.pyqtSlot()
    def on_buttonClearPlot_clicked(self):
        self.temps = []
        self.plotView.clear()

    @QtCore.pyqtSlot()
    def on_buttonConnect_clicked(self):
        self.resume()
        host = self.editHost.text()
        session = self.editSession.text()
        counter = self.editCounter.text()
        cramp = self.editRamp.text()
        ctarget = self.editTemp.text()
        if host and session and cramp and counter and ctarget:
            self.sigConnect.emit(host, session, counter, cramp, ctarget)

    @QtCore.pyqtSlot()
    def on_buttonDisconnect_clicked(self):
        self.sigDisconnect.emit()
        self.connectionFailed()

    def connectionSucceed(self):
        self.buttonConnect.hide()
        self.buttonDisconnect.show()

    def connectionFailed(self):
        self.buttonConnect.show()
        self.buttonDisconnect.hide()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            pass
        else:
            super().keyPressEvent(event)
