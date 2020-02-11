from java.awt import *
from javax.swing import *
import sys
import csv
import subprocess
from model import *

mouseLoc = []
postList = []

class mainWindow(JFrame):
  
  def __init__(self):
    super(mainWindow, self).__init__()
    self.initComponents()
    
  def initComponents(self):
    self.bgPanel = JPanel()
    self.exitButton = JLabel(mouseClicked = self.exitButtonMouseClicked)
    self.jScrollPane1 = JScrollPane()
    self.albumTable = JTable()
    self.termField = JTextField()
#    self.filterBox = JComboBox<>()
    self.searchButton = JLabel()

    self.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
    self.setUndecorated(True)

    self.bgPanel.setBackground(Color(102, 102, 255))

    self.exitButton.setText("X")
    self.exitButton.setCursor(Cursor(Cursor.HAND_CURSOR))

    self.albumTable.setModel(table.DefaultTableModel(
      [],
      ["ID", "Title", "Artist", "Genre", "Release Date", "Rating", "Tags"]))
    
    self.jScrollPane1.setViewportView(self.albumTable)

    self.termField.setOpaque(True)

#    self.filterBox.setModel(DefaultComboBoxModel<>(["Search Filter", "By Title", "By Artist", "By Date", "By Tags"]))

    self.searchButton.setBackground(Color(255, 255, 255))
    self.searchButton.setHorizontalAlignment(SwingConstants.CENTER)
    self.searchButton.setText("Search")
    self.searchButton.setCursor(Cursor(Cursor.HAND_CURSOR))
    self.searchButton.setOpaque(True)

    bgPanelLayout = GroupLayout(self.bgPanel)
    self.bgPanel.setLayout(bgPanelLayout)
    bgPanelLayout.setHorizontalGroup(
      bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
      .addGroup(bgPanelLayout.createSequentialGroup()
        .addContainerGap()
        .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
          .addComponent(self.jScrollPane1, GroupLayout.DEFAULT_SIZE, 705, sys.maxint)
          .addGroup(GroupLayout.Alignment.TRAILING, bgPanelLayout.createSequentialGroup()
            .addGap(0, 0, sys.maxint)
            .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
              .addComponent(self.exitButton, GroupLayout.Alignment.TRAILING)
              .addGroup(GroupLayout.Alignment.TRAILING, bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING, False)
                .addComponent(self.searchButton, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, sys.maxint)
#                .addComponent(self.filterBox, 0, GroupLayout.DEFAULT_SIZE, sys.maxint)
                .addComponent(self.termField, GroupLayout.PREFERRED_SIZE, 199, GroupLayout.PREFERRED_SIZE)))))
        .addContainerGap()))
    bgPanelLayout.setVerticalGroup(
      bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
      .addGroup(bgPanelLayout.createSequentialGroup()
        .addContainerGap()
        .addComponent(self.exitButton)
        .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED, 164, sys.maxint)
#        .addComponent(self.filterBox, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
        .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
        .addComponent(self.termField, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
        .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
        .addComponent(self.searchButton, GroupLayout.PREFERRED_SIZE, 42, GroupLayout.PREFERRED_SIZE)
        .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
        .addComponent(self.jScrollPane1, GroupLayout.PREFERRED_SIZE, 240, GroupLayout.PREFERRED_SIZE)
        .addContainerGap()))

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
    self.viewTable()
    
  def exitButtonMouseClicked(self, evt):
    sys.exit()
    
  def viewTable(self):
    print("Collecting albums...")
    subprocess.call("python getAlbums.py", shell = True)
    print("Done!")

    with open("albumsList.csv", "r") as f:
      reader = csv.reader(f)
      tempList = list(reader)

    del postList[:]

    for item in tempList:
      postList.append(album(item[0],
                            item[1],
                            item[2],
                            item[3],
                            item[4],
                            item[5],
                            item[6]))

    self.albumTable.getModel().setRowCount(0)

    for idx, item in enumerate(postList):
      self.albumTable.getModel().addRow([item.albumID,
                                        item.title,
                                        item.artist,
                                        item.genre,
                                        item.releaseDate,
                                        item.rating,
                                        item.tags])
    
if __name__ == "__main__":
  mainWindow().setVisible(True)