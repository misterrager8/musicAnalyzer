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
    self.bgPanel = JPanel(mousePressed = self.bgPanelMousePressed,
                          mouseDragged = self.bgPanelMouseDragged)
    self.exitButton = JLabel(mouseClicked = self.exitButtonMouseClicked)
    self.jScrollPane1 = JScrollPane()
    self.albumTable = JTable()
    self.termField = JTextField(focusGained = self.termFieldFocusGained)
    self.filterBox = JComboBox()
    self.searchButton = JLabel(mouseEntered = self.searchButtonMouseEntered,
                               mouseExited = self.searchButtonMouseExited,
                               mouseClicked = self.searchButtonMouseClicked)
    self.delButton = JLabel(mouseEntered = self.delButtonMouseEntered,
                            mouseExited = self.delButtonMouseExited,
                            mouseClicked = self.delButtonMouseClicked)
    self.titleField = JTextField(focusGained = self.titleFieldFocusGained)
    self.artistField = JTextField(focusGained = self.artistFieldFocusGained)
    self.dateField = JTextField(focusGained = self.dateFieldFocusGained)
    self.ratingSpinner = JSpinner()
    self.genreBox = JComboBox()
    self.tagsField = JTextField(focusGained = self.tagsFieldFocusGained)
    self.titleLabel = JLabel()
    self.artistLabel = JLabel()
    self.dateLabel = JLabel()
    self.ratingLabel = JLabel()
    self.tagsLabel = JLabel()
    self.submitButton = JLabel(mouseEntered = self.submitButtonMouseEntered,
                               mouseExited = self.submitButtonMouseExited,
                               mouseClicked = self.submitButtonMouseClicked)

    self.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
    self.setUndecorated(True)

    self.bgPanel.setBackground(Color(102, 102, 255))

    self.exitButton.setText("X")
    self.exitButton.setCursor(Cursor(Cursor.HAND_CURSOR))

    self.albumTable.setAutoCreateRowSorter(True)
    self.albumTable.setModel(table.DefaultTableModel(
      [],
      ["ID", "Title", "Artist", "Genre", "Release Date", "Rating", "Tags"]))
    
    self.jScrollPane1.setViewportView(self.albumTable)

    self.termField.setOpaque(True)

    self.filterBox.setModel(DefaultComboBoxModel(["By Title", "By Artist", "By Tags", "By Date"]))

    self.searchButton.setBackground(self.bgPanel.getBackground().brighter())
    self.searchButton.setHorizontalAlignment(SwingConstants.CENTER)
    self.searchButton.setText("Search")
    self.searchButton.setCursor(Cursor(Cursor.HAND_CURSOR))
    self.searchButton.setOpaque(True)
    
    self.delButton.setBackground(Color(255, 51, 51))
    self.delButton.setHorizontalAlignment(SwingConstants.CENTER)
    self.delButton.setText("Delete")
    self.delButton.setCursor(Cursor(Cursor.HAND_CURSOR))
    self.delButton.setOpaque(True)

    self.ratingSpinner.setModel(SpinnerNumberModel(0.0, 0.0, 5.0, 0.5))

    self.genreBox.setModel(DefaultComboBoxModel(["Select Genre", "Hip-Hop", "Soul / R&B", "Alternative", "Rock", "Soundtrack"]))

    self.titleLabel.setText("Title")

    self.artistLabel.setText("Artist")

    self.dateLabel.setText("Date")

    self.ratingLabel.setText("Rating")

    self.tagsLabel.setText("Tags")

    self.submitButton.setBackground(Color(0, 204, 0))
    self.submitButton.setHorizontalAlignment(SwingConstants.CENTER)
    self.submitButton.setText("Add / Edit")
    self.submitButton.setCursor(Cursor(Cursor.HAND_CURSOR))
    self.submitButton.setOpaque(True)

    bgPanelLayout = GroupLayout(self.bgPanel)
    self.bgPanel.setLayout(bgPanelLayout)
    bgPanelLayout.setHorizontalGroup(
      bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
      .addGroup(bgPanelLayout.createSequentialGroup()
        .addContainerGap()
        .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
          .addComponent(self.jScrollPane1)
          .addGroup(GroupLayout.Alignment.TRAILING, bgPanelLayout.createSequentialGroup()
            .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.TRAILING, False)
              .addGroup(bgPanelLayout.createSequentialGroup()
                .addComponent(self.tagsLabel)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(self.tagsField, GroupLayout.PREFERRED_SIZE, 172, GroupLayout.PREFERRED_SIZE))
              .addGroup(bgPanelLayout.createSequentialGroup()
                .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.TRAILING)
                  .addComponent(self.titleLabel)
                  .addComponent(self.artistLabel)
                  .addComponent(self.dateLabel)
                  .addComponent(self.ratingLabel))
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.TRAILING, False)
                  .addComponent(self.dateField, GroupLayout.Alignment.LEADING)
                  .addComponent(self.genreBox, GroupLayout.Alignment.LEADING, 0, GroupLayout.DEFAULT_SIZE, sys.maxint)
                  .addComponent(self.artistField, GroupLayout.Alignment.LEADING)
                  .addComponent(self.titleField, GroupLayout.Alignment.LEADING)
                  .addComponent(self.ratingSpinner, GroupLayout.PREFERRED_SIZE, 172, GroupLayout.PREFERRED_SIZE))))
            .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED, GroupLayout.DEFAULT_SIZE, sys.maxint)
            .addComponent(self.exitButton))
          .addGroup(GroupLayout.Alignment.TRAILING, bgPanelLayout.createSequentialGroup()
            .addComponent(self.submitButton, GroupLayout.PREFERRED_SIZE, 234, GroupLayout.PREFERRED_SIZE)
            .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
            .addComponent(self.delButton, GroupLayout.PREFERRED_SIZE, 237, GroupLayout.PREFERRED_SIZE)
            .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
            .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
              .addComponent(self.filterBox, 0, GroupLayout.DEFAULT_SIZE, sys.maxint)
              .addGroup(GroupLayout.Alignment.TRAILING, bgPanelLayout.createSequentialGroup()
                .addGap(0, 0, sys.maxint)
                .addComponent(self.searchButton, GroupLayout.PREFERRED_SIZE, 222, GroupLayout.PREFERRED_SIZE))
              .addComponent(self.termField))))
        .addContainerGap()))

    bgPanelLayout.linkSize(SwingConstants.HORIZONTAL, [self.delButton, self.searchButton, self.submitButton])

    bgPanelLayout.setVerticalGroup(
      bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
      .addGroup(bgPanelLayout.createSequentialGroup()
        .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
          .addGroup(bgPanelLayout.createSequentialGroup()
            .addContainerGap()
            .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
              .addGroup(bgPanelLayout.createSequentialGroup()
                .addComponent(self.exitButton)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED, GroupLayout.DEFAULT_SIZE, sys.maxint)
                .addComponent(self.filterBox, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                .addGap(82, 82, 82))
              .addGroup(bgPanelLayout.createSequentialGroup()
                .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                  .addComponent(self.titleField, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                  .addComponent(self.titleLabel))
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                  .addComponent(self.artistField, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                  .addComponent(self.artistLabel))
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(self.genreBox, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                  .addComponent(self.dateField, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                  .addComponent(self.dateLabel))
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                  .addComponent(self.ratingSpinner, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                  .addComponent(self.ratingLabel))
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                  .addComponent(self.tagsField, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                  .addComponent(self.tagsLabel))
                .addGap(109, 109, 109))
              .addGroup(GroupLayout.Alignment.TRAILING, bgPanelLayout.createSequentialGroup()
                .addGap(0, 0, sys.maxint)
                .addComponent(self.termField, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(self.searchButton, GroupLayout.PREFERRED_SIZE, 42, GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED))))
          .addGroup(GroupLayout.Alignment.TRAILING, bgPanelLayout.createSequentialGroup()
            .addContainerGap(GroupLayout.DEFAULT_SIZE, sys.maxint)
            .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
              .addComponent(self.submitButton, GroupLayout.PREFERRED_SIZE, 42, GroupLayout.PREFERRED_SIZE)
              .addComponent(self.delButton, GroupLayout.PREFERRED_SIZE, 42, GroupLayout.PREFERRED_SIZE))
            .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)))
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
    
    print("Initializing...")
    subprocess.call("python ctrla.py", shell = True)
    print("Done!")
    self.viewTable()
    
  def exitButtonMouseClicked(self, evt):
    sys.exit()
    
  def termFieldFocusGained(self, evt):
    self.termField.selectAll()
    
  def titleFieldFocusGained(self, evt):
    self.titleField.selectAll()
    
  def artistFieldFocusGained(self, evt):
    self.artistField.selectAll()
    
  def dateFieldFocusGained(self, evt):
    self.dateField.selectAll()
    
  def tagsFieldFocusGained(self, evt):
    self.tagsField.selectAll()
    
  def searchButtonMouseEntered(self, evt):
    self.searchButton.setBorder(border.LineBorder(Color.black))
    
  def searchButtonMouseExited(self, evt):
    self.searchButton.setBorder(None)
    
  def searchButtonMouseClicked(self, evt):
    if self.termField.getText() == "":
      subprocess.call("python ctrla.py", shell = True)
      self.viewTable()
    else:
      params = self.termField.getText() + " " + str(self.filterBox.getSelectedIndex())
      subprocess.call("python ctrla.py search " + params, shell = True)
      self.viewTable()
    
  def delButtonMouseEntered(self, evt):
    self.delButton.setBorder(border.LineBorder(Color.black))
    
  def delButtonMouseExited(self, evt):
    self.delButton.setBorder(None)
    
  def delButtonMouseClicked(self, evt):
    selectedID = int(self.albumTable.getValueAt(self.albumTable.getSelectedRow(), 0))
    if JOptionPane.showConfirmDialog(None, "Delete?") == JOptionPane.YES_OPTION:
      subprocess.call("python ctrla.py del " + str(selectedID), shell = True)
      self.viewTable()
    
  def submitButtonMouseEntered(self, evt):
    self.submitButton.setBorder(border.LineBorder(Color.black))
    
  def submitButtonMouseExited(self, evt):
    self.submitButton.setBorder(None)
    
  def submitButtonMouseClicked(self, evt):
    x = album(None,
              self.titleField.getText(),
              self.artistField.getText(),
              str(self.genreBox.getSelectedItem()),
              self.dateField.getText(),
              self.ratingSpinner.getValue(),
              self.tagsField.getText())
    
    with open("temp.csv", "wb") as f:
      writer = csv.writer(f)
      writer.writerow([x.albumID,
                       x.title,
                       x.artist,
                       x.genre,
                       x.releaseDate,
                       x.rating,
                       x.tags])
      
    subprocess.call("python ctrla.py add", shell = True)
    self.viewTable()
    
  def bgPanelMousePressed(self, evt):
    del mouseLoc[:]
    mouseLoc.append(evt.getX())
    mouseLoc.append(evt.getY())
    
  def bgPanelMouseDragged(self, evt):
    x = evt.getXOnScreen()
    y = evt.getYOnScreen()

    self.setLocation(x - mouseLoc[0], y - mouseLoc[1])
    
  def viewTable(self):
    with open("albumsList.csv", "r") as f:
      reader = csv.reader(f)
      tempList = list(reader)

    del postList[:]

    for item in tempList:
      postList.append(album(item[0], item[1], item[2], item[3], item[4], item[5], item[6]))

    self.albumTable.getModel().setRowCount(0)

    for idx, item in enumerate(postList):
      self.albumTable.getModel().addRow([item.albumID, item.title, item.artist, item.genre, item.releaseDate, item.rating, item.tags])
    
if __name__ == "__main__":
  mainWindow().setVisible(True)