from java.awt import *
from javax.swing import *
from java.lang import *
import sys
import csv
import subprocess
from model import *
from javax.swing.table import *

mouseLoc = []
albumList = []

class tableModelWrapper(DefaultTableModel):
  """Wrapper class for TableModel. Makes it easier to modify table properties"""
  def __init__(self):
    head = "ID,Title,Artist,Genre,Release Date,Rating,Tags".split(",")
    self.data = []
    DefaultTableModel.__init__(self, self.data, head)
    
  def getColumnClass(self, col):
    types = [int, str, str, str, str, Object, str]
    return types[col]
    
  def isCellEditable(self, row, col):
    canEdit = [False, True, True, True, True, True, True]
    return canEdit[col]

class mainWindow(JFrame):
  """Class for main JFrame components/actions"""
  def __init__(self):
    super(mainWindow, self).__init__()
    self.initComponents()
    self.setVisible(True)
    
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
    self.editButton = JLabel(mouseEntered = self.editButtonMouseEntered,
                             mouseExited = self.editButtonMouseExited,
                             mouseClicked = self.editButtonMouseClicked)
    self.addButton = JLabel(mouseEntered = self.addButtonMouseEntered,
                            mouseExited = self.addButtonMouseExited,
                            mouseClicked = self.addButtonMouseClicked)
    self.countLabel = JLabel()
    self.statusLabel = JLabel()

    self.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
    self.setUndecorated(True)

    self.bgPanel.setBackground(Color(102, 102, 255))

    self.exitButton.setText("X")
    self.exitButton.setCursor(Cursor(Cursor.HAND_CURSOR))

    self.albumTable.setModel(tableModelWrapper())
    
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

    self.genreBox.setModel(DefaultComboBoxModel(["Select Genre", "Hip-Hop/Rap", "R&B/Soul", "Alternative", "Rock", "Soundtrack"]))

    self.titleLabel.setText("Title")

    self.artistLabel.setText("Artist")

    self.dateLabel.setText("Date")

    self.ratingLabel.setText("Rating")

    self.tagsLabel.setText("Tags")

    self.editButton.setBackground(Color(255, 153, 51))
    self.editButton.setHorizontalAlignment(SwingConstants.CENTER)
    self.editButton.setText("Edit")
    self.editButton.setCursor(Cursor(Cursor.HAND_CURSOR))
    self.editButton.setOpaque(True)

    self.addButton.setBackground(Color(0, 204, 0))
    self.addButton.setHorizontalAlignment(SwingConstants.CENTER)
    self.addButton.setText("Add")
    self.addButton.setCursor(Cursor(Cursor.HAND_CURSOR))
    self.addButton.setOpaque(True)
    
    self.countLabel.setText(" ")
    
    self.statusLabel.setHorizontalAlignment(SwingConstants.TRAILING);
    self.statusLabel.setText(" ");

    bgPanelLayout = GroupLayout(self.bgPanel)
    self.bgPanel.setLayout(bgPanelLayout)
    bgPanelLayout.setHorizontalGroup(
      bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
      .addGroup(bgPanelLayout.createSequentialGroup()
        .addContainerGap()
        .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
          .addComponent(self.jScrollPane1, GroupLayout.DEFAULT_SIZE, 723, sys.maxint)
          .addGroup(GroupLayout.Alignment.TRAILING, bgPanelLayout.createSequentialGroup()
            .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.TRAILING, False)
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
                  .addComponent(self.ratingSpinner, GroupLayout.PREFERRED_SIZE, 172, GroupLayout.PREFERRED_SIZE)))
              .addGroup(bgPanelLayout.createSequentialGroup()
                .addComponent(self.tagsLabel)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                  .addComponent(self.addButton, GroupLayout.PREFERRED_SIZE, 113, GroupLayout.PREFERRED_SIZE)
                  .addComponent(self.editButton, GroupLayout.PREFERRED_SIZE, 113, GroupLayout.PREFERRED_SIZE)
                  .addComponent(self.delButton, GroupLayout.PREFERRED_SIZE, 113, GroupLayout.PREFERRED_SIZE)
                  .addComponent(self.tagsField, GroupLayout.PREFERRED_SIZE, 172, GroupLayout.PREFERRED_SIZE))))
            .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED, 286, sys.maxint)
            .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING, False)
              .addComponent(self.exitButton, GroupLayout.Alignment.TRAILING)
              .addComponent(self.searchButton, GroupLayout.Alignment.TRAILING, GroupLayout.PREFERRED_SIZE, 113, GroupLayout.PREFERRED_SIZE)
              .addComponent(self.termField)
              .addComponent(self.filterBox, 0, 219, sys.maxint)))
          .addGroup(bgPanelLayout.createSequentialGroup()
            .addComponent(self.countLabel, GroupLayout.PREFERRED_SIZE, 207, GroupLayout.PREFERRED_SIZE)
            .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED, GroupLayout.DEFAULT_SIZE, sys.maxint)
            .addComponent(self.statusLabel, GroupLayout.PREFERRED_SIZE, 207, GroupLayout.PREFERRED_SIZE)))
        .addContainerGap()))
    
    bgPanelLayout.setVerticalGroup(
      bgPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
      .addGroup(bgPanelLayout.createSequentialGroup()
        .addContainerGap()
        .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.TRAILING)
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
            .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
            .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.TRAILING)
              .addGroup(bgPanelLayout.createSequentialGroup()
                .addComponent(self.addButton, GroupLayout.PREFERRED_SIZE, 30, GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(self.editButton, GroupLayout.PREFERRED_SIZE, 30, GroupLayout.PREFERRED_SIZE)
                .addGap(36, 36, 36))
              .addGroup(bgPanelLayout.createSequentialGroup()
                .addGap(72, 72, 72)
                .addComponent(self.delButton, GroupLayout.PREFERRED_SIZE, 30, GroupLayout.PREFERRED_SIZE))))
          .addGroup(bgPanelLayout.createSequentialGroup()
            .addComponent(self.exitButton)
            .addGap(188, 188, 188)
            .addComponent(self.filterBox, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
            .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
            .addComponent(self.termField, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
            .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
            .addComponent(self.searchButton, GroupLayout.PREFERRED_SIZE, 30, GroupLayout.PREFERRED_SIZE)))
        .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED, 23, sys.maxint)
        .addComponent(self.jScrollPane1, GroupLayout.PREFERRED_SIZE, 221, GroupLayout.PREFERRED_SIZE)
        .addGap(3, 3, 3)
        .addGroup(bgPanelLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
          .addComponent(self.countLabel)
          .addComponent(self.statusLabel))
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
      self.statusLabel.setText(str(selectedID) + " deleted.")
    
  def addButtonMouseEntered(self, evt):
    self.addButton.setBorder(border.LineBorder(Color.black))
    
  def addButtonMouseExited(self, evt):
    self.addButton.setBorder(None)
    
  def addButtonMouseClicked(self, evt):
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
    self.clearAllFields()
    self.statusLabel.setText(x.title + " added.")
    
  def editButtonMouseEntered(self, evt):
    self.editButton.setBorder(border.LineBorder(Color.black))
    
  def editButtonMouseExited(self, evt):
    self.editButton.setBorder(None)
    
  def editButtonMouseClicked(self, evt):
    selected = self.albumTable.getSelectedRow()
    rowData = [self.albumTable.getValueAt(selected, 0),
               self.albumTable.getValueAt(selected, 1),
               self.albumTable.getValueAt(selected, 2),
               self.albumTable.getValueAt(selected, 3),
               self.albumTable.getValueAt(selected, 4),
               self.albumTable.getValueAt(selected, 5),
               self.albumTable.getValueAt(selected, 6)]
    
    with open("temp.csv", "wb") as f:
      writer = csv.writer(f)
      writer.writerow(rowData)
      
    subprocess.call("python ctrla.py edit", shell = True)
    self.statusLabel.setText(str(self.albumTable.getValueAt(selected, 1)) + " edited.")
    
  def bgPanelMousePressed(self, evt):
    del mouseLoc[:]
    mouseLoc.append(evt.getX())
    mouseLoc.append(evt.getY())
    
  def bgPanelMouseDragged(self, evt):
    x = evt.getXOnScreen()
    y = evt.getYOnScreen()

    self.setLocation(x - mouseLoc[0], y - mouseLoc[1])
    
  def viewTable(self):
    """Takes album data from DB for display on JTable"""
    with open("albumsList.csv", "r") as f:
      reader = csv.reader(f)
      tempList = list(reader)

    del albumList[:]

    for item in tempList:
      albumList.append(album(item[0], item[1], item[2], item[3], item[4], item[5], item[6]))

    self.albumTable.getModel().setRowCount(0)

    for idx, item in enumerate(albumList):
      self.albumTable.getModel().addRow([item.albumID, item.title, item.artist, item.genre, item.releaseDate, item.rating, item.tags])
      
    self.countLabel.setText(str(len(albumList)) + " album(s) found.")
      
  def clearAllFields(self):
    self.titleField.setText(None)
    self.artistField.setText(None)
    self.genreBox.setSelectedIndex(0)
    self.dateField.setText(None)
    self.ratingSpinner.setValue(0.0)
    self.tagsField.setText(None)
    
if __name__ == "__main__":
  mainWindow().setVisible(True)