import os
import eyed3
import Tkinter, tkFileDialog

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def customSplit(tekst, separator, mesto):
    mesto_int = int(mesto)
    artist = ""
    title = ""
    if tekst.count(separator) == 1:
        return map(str.strip, tekst.split(separator))
    else:
        splitted = tekst.split(separator)
        
        counter=0
        for t in splitted:
            if counter<mesto_int:
                if counter+1==mesto_int:
                    artist=artist+t
                else:
                    artist=artist+t+separator
            else:
                if counter+1==len(splitted):
                    title=title+t
                else:
                    title=title+t+separator
            counter=counter+1
        
        return [artist.strip(), title.strip()]

def SpremeniTage(path, filename, separator, album_name, artist_album, mesto_separiranja):
    filename_notype = os.path.splitext(filename)[0]
    if not separator:
        song = eyed3.load(path+"/"+filename)
        song.tag.title = unicode(filename_notype.strip(), "utf-8")
        song.tag.album=unicode(album_name, "utf-8")
        song.tag.album_artist=unicode(artist_album, "utf-8")
        return song
    else:
        if not mesto_separiranja:
            #artist_title = customSplit(filename_notype,separator,mesto_separiranja)
            artist = customSplit(filename_notype,separator,1)[0]
            title = customSplit(filename_notype,separator,1)[1]
            song = eyed3.load(file_path+"/"+filename)
            song.tag.artist = unicode(artist, "utf-8")
            song.tag.title = unicode(title, "utf-8")
            song.tag.album=unicode(album_name, "utf-8")
            song.tag.album_artist=unicode(artist_album, "utf-8")
            return song
        else:
            artist = customSplit(filename_notype,separator,mesto_separiranja)[0]
            title = customSplit(filename_notype,separator,mesto_separiranja)[1]
            song = eyed3.load(file_path+"/"+filename)
            song.tag.artist = unicode(artist, "utf-8")
            song.tag.title = unicode(title, "utf-8")
            song.tag.album=unicode(album_name, "utf-8")
            song.tag.album_artist=unicode(artist_album, "utf-8")
            return song


a = raw_input("\033[92mWelcome to id3 folder tag editor. Press enter to continue.")
#odpre okno za izbiro mape
root = Tkinter.Tk()
root.withdraw()
file_path = tkFileDialog.askdirectory()
#naredi seznam vseh datotek v mapi
songs = os.listdir(file_path)
#vprasa za naslov albuma in izvajalca labuma. ce izvajalca albuma nebi bilo potem itunes vrze vsako pesem za sebe
album = raw_input("\033[92mEnter an album name: ").strip()
album_artist = raw_input("\033[92mEnter an album artist: ").strip()

while True:
    individualno = raw_input("\033[92mDo you want to edit [a]one ate a time or [b]all at once?: ")
    if individualno!="p" and individualno!="n":
        print("\033[91mError: Enter a or b")
        continue
    else:
        break

if individualno=="b":
    separator = ""
    mesto = ""
    while True:
        separator = raw_input("\033[92mEnter a separator (empty -> filename is track artist): ")
        if not separator:
            break
        while True:
            mesto = raw_input("\033[92mEnter on which occurence the separator separates the filename (default 1.): ")
            if not mesto:
                break
            else:
                if RepresentsInt(mesto):
                    break
                else:
                    print("\033[91mError: Must be a number")
                    continue
        break
    counter=0
    for s in songs:
        print("\033[92mCurrent file: \033[94m"+s)
        
        song=SpremeniTage(path=file_path,filename=s,separator=separator,album_name=album,artist_album=album_artist, mesto_separiranja=mesto)
        try:
            print("\033[92mArtist: \033[91m"+song.tag.artist)
            print("\033[92mTitle: \033[91m"+song.tag.title)
            print("\033[92mAlbum: \033[91m"+song.tag.album)
            print("\033[92mAlbum artist: \033[91m"+song.tag.album_artist)
            song.tag.save()
        except:
            print("\033[91mError saving")
        
        counter=counter+1
    print("\033[94m"+str(counter)+" files were changed.")
if individualno=="a":
    counter = 0
    for s in songs:
        print("\033[92mCurrent file: \033[94m"+s)
        separator = ""
        mesto = ""
        while True:
            separator = raw_input("\033[92mEnter a separator (empty -> filename is track artist): ")
            if not separator:
                break
            while True:
                mesto = raw_input("\033[92mEnter on which occurence the separator separates the filename (default 1.): ")
                if not mesto:
                    break
                else:
                    if RepresentsInt(mesto):
                        break
                    else:
                        print("\033[91mError: Must be a number")
                        continue
            break
        
        song=SpremeniTage(path=file_path,filename=s,separator=separator,album_name=album,artist_album=album_artist, mesto_separiranja=mesto)
        try:
            print("\033[92mArtist: \033[91m"+song.tag.artist)
            print("\033[92mTitle: \033[91m"+song.tag.title)
            print("\033[92mAlbum: \033[91m"+song.tag.album)
            print("\033[92mAlbum artist: \033[91m"+song.tag.album_artist)
            song.tag.save()
        except:
            print("\033[91mError saving")
        
        counter=counter+1

    print("\033[94m"+str(counter)+" files were changed.")