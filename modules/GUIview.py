# TODO: KeyListener for faster editing on JTable(?)

import csv
import subprocess
import sys
import webbrowser

from java.awt import *
from java.lang import *
from javax.swing import *
from javax.swing.table import *

from model import *

mouse_loc = []
album_list = []


class Tablemodelwrapper(DefaultTableModel):
    """Wrapper class for TableModel. Makes it easier to modify table properties"""

    def __init__(self):
        head = "ID,Title,Artist,Genre,Release Date,Rating,Tags,Genius URL".split(",")
        self.data = []
        DefaultTableModel.__init__(self, self.data, head)

    @classmethod
    def getColumnClass(cls, col):
        types = [int, str, str, str, str, Object, str, str]
        return types[col]

    @classmethod
    def isCellEditable(cls, row, col):
        canEdit = [False, True, True, True, True, True, True, True]
        return canEdit[col]


class Mainwindow(JFrame):
    """Class for main JFrame components/actions"""

    def __init__(self):
        super(Mainwindow, self).__init__()
        self.bgPanel = JPanel(mousePressed=self.bgPanelMousePressed,
                              mouseDragged=self.bgPanelMouseDragged)
        self.exitButton = JLabel(mouseClicked=self.exitButtonMouseClicked)
        self.contentPanel = JPanel()
        self.jScrollPane1 = JScrollPane()
        self.albumTable = JTable(mouseClicked=self.albumTableMouseClicked)
        self.countLabel = JLabel()
        self.statusLabel = JLabel()
        self.buttonPanel = JPanel()
        self.addButton = JLabel(mouseEntered=self.addButtonMouseEntered,
                                mouseExited=self.addButtonMouseExited,
                                mouseClicked=self.addButtonMouseClicked)
        self.exportButton = JLabel(mouseEntered=self.exportButtonMouseEntered,
                                   mouseExited=self.exportButtonMouseExited,
                                   mouseClicked=self.exportButtonMouseClicked)
        self.editButton = JLabel(mouseEntered=self.editButtonMouseEntered,
                                 mouseExited=self.editButtonMouseExited,
                                 mouseClicked=self.editButtonMouseClicked)
        self.geniusButton = JLabel(mouseEntered=self.geniusButtonMouseEntered,
                                   mouseExited=self.geniusButtonMouseExited,
                                   mouseClicked=self.geniusButtonMouseClicked)
        self.delButton = JLabel(mouseEntered=self.delButtonMouseEntered,
                                mouseExited=self.delButtonMouseExited,
                                mouseClicked=self.delButtonMouseClicked)
        self.importButton = JLabel(mouseEntered=self.importButtonMouseEntered,
                                   mouseExited=self.importButtonMouseExited,
                                   mouseClicked=self.importButtonMouseClicked)
        self.lyricsButton = JLabel(mouseEntered=self.lyricsButtonMouseEntered,
                                   mouseExited=self.lyricsButtonMouseExited,
                                   mouseClicked=self.lyricsButtonMouseClicked)
        self.formPanel = JPanel()
        self.titleLabel = JLabel()
        self.titleField = JTextField(focusGained=self.titleFieldFocusGained)
        self.artistLabel = JLabel()
        self.artistField = JTextField(focusGained=self.artistFieldFocusGained)
        self.dateLabel = JLabel()
        self.dateField = JTextField(focusGained=self.dateFieldFocusGained)
        self.ratingLabel = JLabel()
        self.ratingSpinner = JSpinner()
        self.genreBox = JComboBox()
        self.tagsLabel = JLabel()
        self.tagsField = JTextField(focusGained=self.tagsFieldFocusGained)
        self.filterBox = JComboBox()
        self.searchButton = JLabel(mouseEntered=self.searchButtonMouseEntered,
                                   mouseExited=self.searchButtonMouseExited,
                                   mouseClicked=self.searchButtonMouseClicked)
        self.termField = JTextField(focusGained=self.termFieldFocusGained)
        self.mainButtonPanel = JPanel()
        self.mainButton1 = JLabel(mouseEntered=self.mainButton1MouseEntered,
                                mouseExited=self.mainButton1MouseExited,
                                mouseClicked=self.mainButton1MouseClicked)
        self.mainButton2 = JLabel(mouseEntered=self.mainButton2MouseEntered,
                                mouseExited=self.mainButton2MouseExited,
                                mouseClicked=self.mainButton2MouseClicked)
        self.mainButton3 = JLabel(mouseEntered=self.mainButton3MouseEntered,
                                mouseExited=self.mainButton3MouseExited,
                                mouseClicked=self.mainButton3MouseClicked)
        self.mainButton4 = JLabel(mouseEntered=self.mainButton4MouseEntered,
                                  mouseExited=self.mainButton4MouseExited,
                                  mouseClicked=self.mainButton4MouseClicked)

        self.init_components()
        self.setVisible(True)

    def init_components(self):

        self.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
        self.setUndecorated(True)
        self.setPreferredSize(Dimension(1000, 570))
        self.getContentPane().setLayout(None)

        self.bgPanel.setBackground(Color(51, 153, 255))
        self.bgPanel.setLayout(None)

        self.exitButton.setHorizontalAlignment(SwingConstants.CENTER)
        self.exitButton.setText("X")
        self.exitButton.setCursor(Cursor(Cursor.HAND_CURSOR))
        self.bgPanel.add(self.exitButton)
        self.exitButton.setBounds(960, 10, 30, 30)

        self.contentPanel.setBorder(BorderFactory.createLineBorder(Color(0, 0, 0)))
        self.contentPanel.setOpaque(False)
        self.contentPanel.setLayout(None)
        self.contentPanel.add(self.termField)
        self.termField.setBounds(622, 208, 190, 26)

        self.formPanel.setOpaque(False)
        self.formPanel.setLayout(GridLayout(11, 1, 5, 5))

        self.titleLabel.setText("Title")
        self.formPanel.add(self.titleLabel)
        self.formPanel.add(self.titleField)

        self.artistLabel.setText("Artist")
        self.formPanel.add(self.artistLabel)
        self.formPanel.add(self.artistField)

        self.dateLabel.setText("Date")
        self.formPanel.add(self.dateLabel)
        self.formPanel.add(self.dateField)

        self.ratingLabel.setText("Rating")
        self.formPanel.add(self.ratingLabel)

        self.ratingSpinner.setModel(SpinnerNumberModel(0.0, 0.0, 5.0, 0.5))
        self.formPanel.add(self.ratingSpinner)

        self.genreBox.setModel(
            DefaultComboBoxModel(["Select Genre", "Hip-Hop/Rap", "R&B/Soul", "Alternative", "Rock", "Soundtrack"]))
        self.formPanel.add(self.genreBox)

        self.tagsLabel.setText("Tags")
        self.formPanel.add(self.tagsLabel)
        self.formPanel.add(self.tagsField)

        self.contentPanel.add(self.formPanel)
        self.formPanel.setBounds(6, 6, 221, 263)

        self.albumTable.setModel(Tablemodelwrapper())
        self.jScrollPane1.setViewportView(self.albumTable)

        self.albumTable.getColumnModel().getColumn(0).setPreferredWidth(3)
        self.albumTable.getColumnModel().getColumn(1).setPreferredWidth(175)
        self.albumTable.getColumnModel().getColumn(5).setPreferredWidth(6)

        self.contentPanel.add(self.jScrollPane1)
        self.jScrollPane1.setBounds(6, 275, 810, 200)

        self.filterBox.setModel(DefaultComboBoxModel(["Search Filter", "By Title", "By Artist", "By Date", "By Tags"]))
        self.contentPanel.add(self.filterBox)
        self.filterBox.setBounds(622, 175, 190, 27)

        self.buttonPanel.setOpaque(False)
        self.buttonPanel.setLayout(GridLayout(3, 3, 5, 5))

        self.addButton.setBackground(self.bgPanel.getBackground().darker())
        self.addButton.setHorizontalAlignment(SwingConstants.CENTER)
        self.addButton.setText("Add")
        self.addButton.setCursor(Cursor(Cursor.HAND_CURSOR))
        self.addButton.setOpaque(True)
        self.buttonPanel.add(self.addButton)

        self.exportButton.setBackground(self.bgPanel.getBackground().darker())
        self.exportButton.setHorizontalAlignment(SwingConstants.CENTER)
        self.exportButton.setText("Export All")
        self.exportButton.setCursor(Cursor(Cursor.HAND_CURSOR))
        self.exportButton.setOpaque(True)
        self.buttonPanel.add(self.exportButton)

        self.editButton.setBackground(self.bgPanel.getBackground().darker())
        self.editButton.setHorizontalAlignment(SwingConstants.CENTER)
        self.editButton.setText("Edit")
        self.editButton.setCursor(Cursor(Cursor.HAND_CURSOR))
        self.editButton.setOpaque(True)
        self.buttonPanel.add(self.editButton)

        self.geniusButton.setBackground(self.bgPanel.getBackground().darker())
        self.geniusButton.setHorizontalAlignment(SwingConstants.CENTER)
        self.geniusButton.setText("Genius")
        self.geniusButton.setCursor(Cursor(Cursor.HAND_CURSOR))
        self.geniusButton.setOpaque(True)
        self.buttonPanel.add(self.geniusButton)

        self.delButton.setBackground(self.bgPanel.getBackground().darker())
        self.delButton.setHorizontalAlignment(SwingConstants.CENTER)
        self.delButton.setText("Delete")
        self.delButton.setCursor(Cursor(Cursor.HAND_CURSOR))
        self.delButton.setOpaque(True)
        self.buttonPanel.add(self.delButton)

        self.importButton.setBackground(self.bgPanel.getBackground().darker())
        self.importButton.setHorizontalAlignment(SwingConstants.CENTER)
        self.importButton.setText("Import")
        self.importButton.setCursor(Cursor(Cursor.HAND_CURSOR))
        self.importButton.setOpaque(True)
        self.buttonPanel.add(self.importButton)

        self.lyricsButton.setBackground(self.bgPanel.getBackground().darker())
        self.lyricsButton.setHorizontalAlignment(SwingConstants.CENTER)
        self.lyricsButton.setText("Lyrics")
        self.lyricsButton.setCursor(Cursor(Cursor.HAND_CURSOR))
        self.lyricsButton.setOpaque(True)
        self.buttonPanel.add(self.lyricsButton)

        self.contentPanel.add(self.buttonPanel)
        self.buttonPanel.setBounds(233, 172, 280, 97)

        self.searchButton.setBackground(self.bgPanel.getBackground().darker())
        self.searchButton.setHorizontalAlignment(SwingConstants.CENTER)
        self.searchButton.setText("Search")
        self.searchButton.setCursor(Cursor(Cursor.HAND_CURSOR))
        self.searchButton.setOpaque(True)
        self.contentPanel.add(self.searchButton)
        self.searchButton.setBounds(622, 240, 190, 29)
        self.contentPanel.add(self.countLabel)
        self.countLabel.setBounds(10, 480, 230, 20)

        self.statusLabel.setHorizontalAlignment(SwingConstants.TRAILING)
        self.contentPanel.add(self.statusLabel)
        self.statusLabel.setBounds(550, 480, 260, 20)

        self.bgPanel.add(self.contentPanel)
        self.contentPanel.setBounds(170, 50, 820, 510)

        self.mainButtonPanel.setOpaque(False)
        self.mainButtonPanel.setLayout(GridLayout(10, 1, 5, 5))

        self.mainButton1.setBackground(self.bgPanel.getBackground().darker())
        self.mainButton1.setHorizontalAlignment(SwingConstants.CENTER)
        self.mainButton1.setText("Button 1")
        self.mainButton1.setCursor(Cursor(Cursor.HAND_CURSOR))
        self.mainButton1.setOpaque(True)
        self.mainButtonPanel.add(self.mainButton1)

        self.mainButton2.setBackground(self.bgPanel.getBackground().darker())
        self.mainButton2.setHorizontalAlignment(SwingConstants.CENTER)
        self.mainButton2.setText("Button 2")
        self.mainButton2.setCursor(Cursor(Cursor.HAND_CURSOR))
        self.mainButton2.setOpaque(True)
        self.mainButtonPanel.add(self.mainButton2)

        self.mainButton3.setBackground(self.bgPanel.getBackground().darker())
        self.mainButton3.setHorizontalAlignment(SwingConstants.CENTER)
        self.mainButton3.setText("Button 3")
        self.mainButton3.setCursor(Cursor(Cursor.HAND_CURSOR))
        self.mainButton3.setOpaque(True)
        self.mainButtonPanel.add(self.mainButton3)

        self.mainButton4.setBackground(self.bgPanel.getBackground().darker())
        self.mainButton4.setHorizontalAlignment(SwingConstants.CENTER)
        self.mainButton4.setText("Button 4")
        self.mainButton4.setCursor(Cursor(Cursor.HAND_CURSOR))
        self.mainButton4.setOpaque(True)
        self.mainButtonPanel.add(self.mainButton4)

        self.bgPanel.add(self.mainButtonPanel)
        self.mainButtonPanel.setBounds(10, 50, 150, 510)

        self.getContentPane().add(self.bgPanel)
        self.bgPanel.setBounds(0, 0, 1000, 570)

        self.pack()
        self.setLocationRelativeTo(None)

        print("Initializing...")
        subprocess.call("python Ctrla.py", shell=True)
        print("Done!")
        self.view_table()

    @classmethod
    def exitButtonMouseClicked(cls, evt):
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
            subprocess.call("python Ctrla.py", shell=True)
            self.view_table()
        else:
            params = self.termField.getText() + " " + str(self.filterBox.getSelectedIndex())
            subprocess.call("python Ctrla.py search " + params, shell=True)
            self.view_table()

    def delButtonMouseEntered(self, evt):
        self.delButton.setBorder(border.LineBorder(Color.black))

    def delButtonMouseExited(self, evt):
        self.delButton.setBorder(None)

    def delButtonMouseClicked(self, evt):
        selected_id = int(self.albumTable.getValueAt(self.albumTable.getSelectedRow(), 0))
        if JOptionPane.showConfirmDialog(None, "Delete?") == JOptionPane.YES_OPTION:
            subprocess.call("python Ctrla.py del " + str(selected_id), shell=True)
            self.view_table()
            self.statusLabel.setText(str(selected_id) + " deleted.")

    def addButtonMouseEntered(self, evt):
        self.addButton.setBorder(border.LineBorder(Color.black))

    def addButtonMouseExited(self, evt):
        self.addButton.setBorder(None)

    def addButtonMouseClicked(self, evt):
        x = Album(None,
                  self.titleField.getText(),
                  self.artistField.getText(),
                  str(self.genreBox.getSelectedItem()),
                  self.dateField.getText(),
                  self.ratingSpinner.getValue(),
                  self.tagsField.getText(),
                  None)

        with open("temp.csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerow([x.album_id, x.title, x.artist, x.genre, x.release_date, x.rating, x.tags])

        subprocess.call("python Ctrla.py add", shell=True)
        self.view_table()
        self.clear_all_fields()
        self.statusLabel.setText(x.title + " added.")

    def editButtonMouseEntered(self, evt):
        self.editButton.setBorder(border.LineBorder(Color.black))

    def editButtonMouseExited(self, evt):
        self.editButton.setBorder(None)

    def editButtonMouseClicked(self, evt):
        selected = self.albumTable.getSelectedRow()
        row_data = [self.albumTable.getValueAt(selected, 0),
                    self.albumTable.getValueAt(selected, 1),
                    self.albumTable.getValueAt(selected, 2),
                    self.albumTable.getValueAt(selected, 3),
                    self.albumTable.getValueAt(selected, 4),
                    self.albumTable.getValueAt(selected, 5),
                    self.albumTable.getValueAt(selected, 6),
                    self.albumTable.getValueAt(selected, 7)]

        with open("temp.csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerow(row_data)

        subprocess.call("python Ctrla.py edit", shell=True)
        self.statusLabel.setText(str(self.albumTable.getValueAt(selected, 1)) + " edited.")

    @classmethod
    def bgPanelMousePressed(cls, evt):
        del mouse_loc[:]
        mouse_loc.append(evt.getX())
        mouse_loc.append(evt.getY())

    def bgPanelMouseDragged(self, evt):
        x = evt.getXOnScreen()
        y = evt.getYOnScreen()

        self.setLocation(x - mouse_loc[0], y - mouse_loc[1])

    def albumTableMouseClicked(self, evt):
        if evt.getClickCount() == 3:
            album_id = str(self.albumTable.getValueAt(self.albumTable.getSelectedRow(), 0))
            subprocess.call("python Ctrla.py genius " + album_id, shell=True)

    def exportButtonMouseEntered(self, evt):
        self.exportButton.setBorder(border.LineBorder(Color.black))

    def exportButtonMouseExited(self, evt):
        self.exportButton.setBorder(None)

    def exportButtonMouseClicked(self, evt):
        subprocess.call("python Ctrla.py export", shell=True)
        self.statusLabel.setText("Albums exported.")

    def importButtonMouseEntered(self, evt):
        self.importButton.setBorder(border.LineBorder(Color.black))

    def importButtonMouseExited(self, evt):
        self.importButton.setBorder(None)

    def importButtonMouseClicked(self, evt):
        if JOptionPane.showConfirmDialog(None, "Import?") == JOptionPane.YES_OPTION:
            subprocess.call("python Ctrla.py import", shell=True)
            self.view_table()
            self.statusLabel.setText("Albums imported.")

    def geniusButtonMouseEntered(self, evt):
        self.geniusButton.setBorder(border.LineBorder(Color.black))

    def geniusButtonMouseExited(self, evt):
        self.geniusButton.setBorder(None)

    def geniusButtonMouseClicked(self, evt):
        genius_url = str(self.albumTable.getValueAt(self.albumTable.getSelectedRow(), 7))
        if genius_url == "":
            JOptionPane.showMessageDialog(None, "No Genius URL found.")
        else:
            webbrowser.open(genius_url)

    def lyricsButtonMouseEntered(self, evt):
        self.lyricsButton.setBorder(border.LineBorder(Color.black))

    def lyricsButtonMouseExited(self, evt):
        self.lyricsButton.setBorder(None)

    def lyricsButtonMouseClicked(self, evt):
        genius_url = str(self.albumTable.getValueAt(self.albumTable.getSelectedRow(), 7))
        subprocess.call("python Ctrla.py lyrics " + genius_url, shell=True)

    def mainButton1MouseEntered(self, evt):
        self.mainButton1.setBorder(border.LineBorder(Color.black))

    def mainButton1MouseExited(self, evt):
        self.mainButton1.setBorder(None)

    def mainButton1MouseClicked(self, evt):
        print("None")

    def mainButton2MouseEntered(self, evt):
        self.mainButton2.setBorder(border.LineBorder(Color.black))

    def mainButton2MouseExited(self, evt):
        self.mainButton2.setBorder(None)

    def mainButton2MouseClicked(self, evt):
        print("None")

    def mainButton3MouseEntered(self, evt):
        self.mainButton3.setBorder(border.LineBorder(Color.black))

    def mainButton3MouseExited(self, evt):
        self.mainButton3.setBorder(None)

    def mainButton3MouseClicked(self, evt):
        print("None")

    def mainButton4MouseEntered(self, evt):
        self.mainButton4.setBorder(border.LineBorder(Color.black))

    def mainButton4MouseExited(self, evt):
        self.mainButton4.setBorder(None)

    def mainButton4MouseClicked(self, evt):
        print("None")

    def view_table(self):
        """Takes Album data from DB for display on JTable"""
        with open("albumsList.csv", "r") as f:
            reader = csv.reader(f)
            temp_list = list(reader)

        del album_list[:]

        for item in temp_list:
            album_list.append(Album(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]))

        self.albumTable.getModel().setRowCount(0)

        for idx, item in enumerate(album_list):
            self.albumTable.getModel().addRow(
                [item.album_id, item.title, item.artist, item.genre, item.release_date, item.rating, item.tags,
                 item.get_genius_url()])

        self.countLabel.setText(str(len(album_list)) + " album(s) found.")

    def clear_all_fields(self):
        self.titleField.setText(None)
        self.artistField.setText(None)
        self.genreBox.setSelectedIndex(0)
        self.dateField.setText(None)
        self.ratingSpinner.setValue(0.0)
        self.tagsField.setText(None)


if __name__ == "__main__":
    Mainwindow()
