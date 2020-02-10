from java.awt import *
from javax.swing import *
import sys

mouseLoc = []

class mainWindow(JFrame):
  
  def __init__(self):
    super(mainWindow, self).__init__()
    self.initComponents()
    
  def initComponents(self):
    self.bgPanel = JPanel()
    self.exitButton = JLabel(mouseClicked = self.exitButtonMouseClicked)

    self.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
    self.setUndecorated(True)

    self.bgPanel.setBackground(Color(153, 153, 255))

    self.exitButton.setText("X")
    self.exitButton.setCursor(Cursor(Cursor.HAND_CURSOR))

    bgPanelLayout = GroupLayout(self.bgPanel)
    self.bgPanel.setLayout(bgPanelLayout)
    bgPanelLayout.setHorizontalGroup(
      bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
      .addGroup(GroupLayout.Alignment.TRAILING, bgPanelLayout.createSequentialGroup()
        .addContainerGap(703, sys.maxint)
        .addComponent(self.exitButton)
        .addContainerGap()))
    bgPanelLayout.setVerticalGroup(
      bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
      .addGroup(bgPanelLayout.createSequentialGroup()
        .addContainerGap()
        .addComponent(self.exitButton)
        .addContainerGap(519, sys.maxint)))

    layout = GroupLayout(self.getContentPane())
    self.getContentPane().setLayout(layout)
    layout.setHorizontalGroup(
      layout.createParallelGroup(GroupLayout.Alignment.LEADING)
      .addComponent(self.bgPanel, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, sys.maxint))
    layout.setVerticalGroup(
      layout.createParallelGroup(GroupLayout.Alignment.LEADING)
      .addComponent(self.bgPanel, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, sys.maxint))

    self.pack()
    self.setLocationRelativeTo(None)
    
  def exitButtonMouseClicked(self, evt):
    sys.exit()
    
if __name__ == "__main__":
  mainWindow().setVisible(True)