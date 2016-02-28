from direct.gui.DirectGui import DirectButton, DirectFrame, DGG
from direct.task.Task import Task
from otp.otpbase import OTPLocalizer
from toontown.toonbase import ToontownGlobals, TTLocalizer, ToontownTimer
import SosShopGlobals

#TODO: Add Text For The Gui.

class SosShopGui(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(self, parent=aspect2d, relief=None, geom=DGG.getDefaultDialogGeom(), geom_color=ToontownGlobals.GlobalDialogColor, geom_scale=(1.33, 1, 1.3), pos=(0, 0, 0), text='', text_scale=0.07, text_pos=(0, 0.475))
        self.initialiseoptions(SosShopGui)
        
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.reparentTo(aspect2d)
        self.timer.posInTopRightCorner()
        self.timer.countdown(SosShopGlobals.TIMER_SECONDS, self.__cancel, [SosShopGlobals.TIMER_END])
        self.setupButtons()

    def setupButtons(self):
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        
        self.cancelButton = DirectButton(parent=self, relief=None, image=(buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr')), pos=(-0.2, 0, -0.5), text=OTPLocalizer.lCancel, text_scale=0.06, text_pos=(0, -0.1), command=self.__cancel, extraArgs=[SosShopGlobals.USER_CANCEL])
        self.okButton = DirectButton(parent=self, relief=None, image=(buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr')), pos=(0.2, 0, -0.5), text=OTPLocalizer.lOK, text_scale=0.06, text_pos=(0, -0.1), command=self.__roll)
        buttons.removeNode()


    def destroy(self):
        self.ignoreAll()

        if self.timer:
            self.timer.destroy()

        DirectFrame.destroy(self)

    def __cancel(self, state):
        self.destroy()
        messenger.send('sosShopDone', [state])

    def __roll(self):
        self.destroy()
        messenger.send('sosShopDone', [SosShopGlobals.ROLL])


    def __runTask(self, task):
        if task.time - task.prevTime < task.delayTime:
            return Task.cont
        else:
            task.delayTime = max(0.05, task.delayTime * 0.75)
            task.prevTime = task.time

            return Task.done  