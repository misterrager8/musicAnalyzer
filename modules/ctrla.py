import csv
import os
import sys
import webbrowser

import MySQLdb
import bs4
import requests

from model import *


class Ctrla:
    def __init__(self):
        pass

    @classmethod
    def run_query(cls, query):
        """Executes general SQL command"""
        db = MySQLdb.connect("localhost", "root", "bre9ase4", "TESTDB")
        cursor = db.cursor()

        try:
            cursor.execute(query)
            db.commit()
        except MySQLdb.Error, e:
            print(e)

        db.close()

    @classmethod
    def run_read_query(cls, query):
        """Executes SQL SELECT command"""
        db = MySQLdb.connect("localhost", "root", "bre9ase4", "TESTDB")
        cursor = db.cursor()

        try:
            cursor.execute(query)
            return cursor.fetchall()
        except MySQLdb.Error, e:
            print(e)

    @classmethod
    def run_search_query(cls, query, term):
        """Executes SQL WHERE/LIKE command"""
        db = MySQLdb.connect("localhost", "root", "bre9ase4", "TESTDB")
        cursor = db.cursor()

        try:
            cursor.execute(query, ("%" + term + "%",))
            return cursor.fetchall()
        except MySQLdb.Error, e:
            print(e)

    @classmethod
    def get_album_by_id(cls, album_id):
        """Returns album with given Album ID"""
        sql = "SELECT * FROM albums WHERE albumID = '%d'" % album_id
        db = MySQLdb.connect("localhost", "root", "bre9ase4", "TESTDB")
        cursor = db.cursor()

        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            x = Album(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
            return x
        except MySQLdb.Error, e:
            print(e)

    def add_album(self, new_album):
        """Adds Album to DB"""
        sql = "INSERT INTO albums (title, artist, genre, releaseDate, rating, tags) VALUES ('%s', '%s', '%s', '%s', " \
              "'%d', '%s')" % (
                  new_album.title, new_album.artist, new_album.genre, new_album.release_date, new_album.rating,
                  new_album.tags)
        self.run_query(sql)

    def delete_album(self, album_id):
        """Deletes Album from DB"""
        sql = "DELETE FROM albums WHERE albumID = '%d'" % album_id
        self.run_query(sql)

    def edit_album(self, album_id, search_type, change):
        """Edits info of selected Album according to user's choice"""
        sql0 = "UPDATE albums SET title = '%s' WHERE albumID = '%d'" % (change, album_id)
        sql1 = "UPDATE albums SET artist = '%s' WHERE albumID = '%d'" % (change, album_id)
        sql2 = "UPDATE albums SET releaseDate = '%s' WHERE albumID = '%d'" % (change, album_id)
        sql3 = "UPDATE albums SET rating = '%s' WHERE albumID = '%d'" % (change, album_id)
        sql4 = "UPDATE albums SET tags = '%s' WHERE albumID = '%d'" % (change, album_id)

        if search_type == 0:
            self.run_query(sql0)
        elif search_type == 1:
            self.run_query(sql1)
        elif search_type == 2:
            self.run_query(sql2)
        elif search_type == 3:
            self.run_query(sql3)
        elif search_type == 4:
            self.run_query(sql4)

        print("Album edited.")

    def delete_all_albums(self):
        """Deletes all albums in the DB, and also resets albumID's to 0"""
        sql = "TRUNCATE TABLE albums"
        self.run_query(sql)

    def view_albums(self):
        """Gets all albums in DB, and stores them in a list"""
        albums_list = []
        sql = "SELECT * FROM albums"

        for row in self.run_read_query(sql):
            x = Album(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            albums_list.append(x)

        return albums_list

    def search_albums(self, term, search_type):
        """Search albums by specified column"""
        albums_list = []
        b = {}
        sql0 = "SELECT * FROM albums WHERE title LIKE %s"
        sql1 = "SELECT * FROM albums WHERE artist LIKE %s"
        sql2 = "SELECT * FROM albums WHERE releaseDate LIKE %s"
        sql3 = "SELECT * FROM albums WHERE tags LIKE %s"

        if int(search_type) == 0:
            b = self.run_search_query(sql0, term)
        elif int(search_type) == 1:
            b = self.run_search_query(sql1, term)
        elif int(search_type) == 2:
            b = self.run_search_query(sql2, term)
        elif int(search_type) == 3:
            b = self.run_search_query(sql3, term)

        for row in b:
            x = Album(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            albums_list.append(x)

        return albums_list

    def export_albums(self):
        """Exports all albums to csv file"""
        sql = "SELECT * FROM albums"
        results = self.run_read_query(sql)

        with open("output.csv", "w") as f:
            a = csv.writer(f, delimiter=",")
            a.writerow(["Album ID", "Title", "Artist", "Genre", "Release Date", "Rating", "Tags"])
            a.writerows(results)

        print("Exported.")

    def import_albums(self):
        """Takes all info from CSV, stores in DB"""
        imported = []
        csv_data = csv.reader(file("input.csv"))
        for row in csv_data:
            q_album = Album(None, row[0], row[1], row[2], row[3], float(row[4]), row[5], row[6])
            imported.append(q_album)

        print(str(len(imported)) + " Album(s) found.")
        for item in imported:
            item.to_string()

        answer = raw_input("Add these albums? ")
        if answer == "Y" or answer == "y":
            for item in imported:
                self.add_album(item)

    def gui_view_albums(self):
        """Gets all albums in DB, writes to CSV for display on a JTable"""
        results = []
        for submission in self.view_albums():
            results.append([submission.album_id,
                            submission.title,
                            submission.artist,
                            submission.genre,
                            submission.release_date,
                            submission.rating,
                            submission.tags,
                            submission.genius_url])

        with open("albumsList.csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerows(results)

    def gui_search_albums(self, term, search_type):
        """Search albums by specified column, writes to CSV for display on a JTable"""
        results = []
        for submission in self.search_albums(term, search_type):
            results.append([submission.album_id,
                            submission.title,
                            submission.artist,
                            submission.genre,
                            submission.release_date,
                            submission.rating,
                            submission.tags,
                            submission.genius_url])

        with open("albumsList.csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerows(results)

    def gui_delete_album(self, album_id):
        """Deletes Album in DB straight from JTable"""
        self.delete_album(album_id)
        self.gui_view_albums()

    def gui_add_album(self):
        """Adds Album to DB from Desktop GUI"""
        csv_data = csv.reader(file("temp.csv"))
        for row in csv_data:
            sql = "INSERT INTO albums (title, artist, genre, releaseDate, rating, tags, genius_url) VALUES ('%s', '%s', '%s', " \
                  "'%s', '%s', '%s', '%s')" % (
                      row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            self.run_query(sql)

        os.remove("temp.csv")
        self.gui_view_albums()

    def gui_edit_album(self):
        """Edits info of selected Album according to user's choice, straight from JTable"""
        csv_data = csv.reader(file("temp.csv"))
        for row in csv_data:
            sql = "UPDATE albums SET title = '%s', artist = '%s', genre = '%s', releaseDate = '%s', rating = '%s', " \
                  "tags = '%s', genius_url = '%s' WHERE albumID = '%d'" % (
                      row[1], row[2], row[3], row[4], row[5], row[6], row[7], int(row[0]))
            self.run_query(sql)

        os.remove("temp.csv")
        self.gui_view_albums()

    def search_in_genius(self, album_id):
        """Allows user to search Genius.com for selected album"""
        the_album = self.get_album_by_id(album_id)
        webbrowser.open("https://genius.com/search?q=" + the_album.title)

    def gui_import_albums(self):
        """Imports multiple Albums to DB from Desktop GUI"""
        csv_data = csv.reader(file("input.csv"))
        for row in csv_data:
            sql = "INSERT INTO albums (title, artist, genre, releaseDate, rating, tags, genius_url) VALUES ('%s', '%s', '%s', " \
                  "'%s', '%s', '%s', '%s')" % (
                      row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            self.run_query(sql)

        self.gui_view_albums()

    @classmethod
    def get_lyrics(cls, genius_url):
        global res
        album_name = genius_url.split('/')[5]

        res_a = requests.get(genius_url)
        os.makedirs('./' + album_name, 0o777)

        soup_a = bs4.BeautifulSoup(res_a.text, features='html.parser')
        type(soup_a)

        elems_a = soup_a.findAll('a', {'class': 'u-display_block', 'href': True})

        for i, item in enumerate(elems_a):
            song_name = item['href'][19:]
            txt_name = str(i + 1) + '-' + song_name + '.txt'

            try:
                res = requests.get(item['href'])
            except requests.ConnectionError as e:
                print(e)

            soup = bs4.BeautifulSoup(res.text, features='html.parser')
            type(soup)

            elems2 = soup.select(".lyrics")[0].getText()

            file2 = open(album_name + '/' + txt_name, 'wb')
            file2.write(elems2.encode('utf8'))
            file2.close()

            print(song_name + ' lyrics saved to folder')


if __name__ == "__main__":
    albumCtrla = Ctrla()
    if len(sys.argv) == 1:
        albumCtrla.gui_view_albums()
    elif sys.argv[1] == "search":
        albumCtrla.gui_search_albums(sys.argv[2], int(sys.argv[3]))
    elif sys.argv[1] == "del":
        albumCtrla.gui_delete_album(int(sys.argv[2]))
    elif sys.argv[1] == "add":
        albumCtrla.gui_add_album()
    elif sys.argv[1] == "edit":
        albumCtrla.gui_edit_album()
    elif sys.argv[1] == "genius":
        albumCtrla.search_in_genius(int(sys.argv[2]))
    elif sys.argv[1] == "export":
        albumCtrla.export_albums()
    elif sys.argv[1] == "import":
        albumCtrla.gui_import_albums()
    elif sys.argv[1] == "lyrics":
        albumCtrla.get_lyrics(str(sys.argv[2]))
