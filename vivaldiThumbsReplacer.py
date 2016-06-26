#!/usr/bin/env python
import os
import shutil
import json
import sqlite3


# PATHs - edit only these!
# --------------------------------------------------------------------------- #
topSites_path = "Path to 'Top Sites' file"
bookmark_path = "Path to 'Bookmarks' file"

backup_path = "Path to Backup directory"
customThumbs_path = "Path to directory with thumbnails"
# --------------------------------------------------------------------------- #


def load_speeddial(file_path):
    """
    Load the bookmark entries from Vivaldi's speed dial and return as
    dictionary
    """
    # read bookmark file
    with open(file_path, encoding="UTF-8") as jfile:
        bookmarks = json.load(jfile)

    # access speed dial
    speeddial = bookmarks["roots"]["bookmark_bar"]["children"][0]["children"]
    return {x["id"]: x["name"] for x in speeddial if x["type"] == "url"}


def load_thumbs(dir_path):
    """
    Load custom thumbnails in specified directory and return as dictionary
    """
    thumbs = os.listdir(dir_path)
    return {x[0]: dir_path + "_".join(x)
            for x in [y.split("_") for y in thumbs]}


def update_thumbs(topSites_path, bookmarks, thumbnails):
    """
    Replace thumbnails where thumbnail id matches bookmark id and print results
    """
    updated = []
    not_found = []

    # open database
    conn = sqlite3.connect(topSites_path)
    cur = conn.cursor()

    # replace if match
    for key in bookmarks.keys():
        if key in thumbnails.keys():
            with open(thumbnails[key], "rb") as bfile:
                pic = bfile.read()
            sql = "UPDATE thumbnails SET thumbnail=? WHERE url=?"
            cur.execute(sql, (pic, "http://bookmark_thumbnail/" + str(key)))
            conn.commit()
            updated.append(key)
        else:
            not_found.append(key)

    conn.close()

    # print results
    if updated:
        print("\nUpdated:")
        for key in updated:
            print("{}: {}".format(key, bookmarks[key]))
    if not_found:
        print("\nNot updated (no custom thumbnails found):")
        for key in not_found:
            print("{}: {}".format(key, bookmarks[key]))


def main():
    print("Python Script for replacing thumbnails in Vivaldi Speedial")
    input("\nWARNING: Please make sure that Vivaldi isn't running. Press 'Enter' to continue.")

    # validate paths
    if not os.path.isfile(bookmark_path):
        print("\nERROR: Vivaldis bookmark file wasn't found under the path "
              "'{}'!".format(bookmark_path))
    elif not os.path.isfile(topSites_path):
        print("\nERROR: Vivaldis 'Top Sites' file wasn't found under the path "
              "'{}'!".format(topSites_path))
    elif not os.path.isdir(backup_path):
        print("\nERROR: '{}' is no valid directory!".format(backup_path))
    elif not os.path.isdir(customThumbs_path):
        print("\nERROR: '{}' is no valid directory!".format(customThumbs_path))

    # start script
    else:
        # load files
        bookmarks = load_speeddial(bookmark_path)
        custom_thumbnails = load_thumbs(customThumbs_path)

        # create backup
        shutil.copy(topSites_path, backup_path)
        print("\nCreated backup of 'Top Sites' in '{}'".format(backup_path))

        update_thumbs(topSites_path, bookmarks, custom_thumbnails)

    input("\nPress 'Enter' to exit.")
    exit()


if __name__ == "__main__":
    main()
