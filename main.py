import hmac
import hashlib
import requests
from urllib.request import urlopen
import re
import csv
from PIL import Image
import urllib.request
import os
import shutil

tmdb_key = bytearray.fromhex(
    'F5DE66D2680E255B2DF79E74F890EBF349262F618BCAE2A9ACCDEE5156CE8DF2CDF2D48C71173CDC2594465B87405D197CF1AED3B7E9671EEB56CA6753C2E6B0')

# Notes:
# https://www.psdevwiki.com/ps3/TITLE_ID
# https://www.psdevwiki.com/ps4/Online_Connections
# images can be 400*400 inside Discord Presence with MINIMAL quality loss!


# Physical PS3
class PhysicalPS3:
    def __init__(self):
        self.media = 'B'
        self.rights = ['C', 'L']
        self.region = ['A', 'C', 'E', 'H', 'J', 'K', 'P', 'U']
        self.rType = ['M', 'S']     # 'M' is only used with region 'J'
        self.license_number = range(0, 100000)  # all 5 digit numbers (including leading 0s), use .zfill(5)

    def generate_titleID(self):
        for i in range(len(self.rights)):
            for j in range(len(self.region)):
                for k in range(len(self.rType)):
                    if self.region[j] == 'J':
                        for l in self.license_number:
                            titleID = self.media + self.rights[i] + self.region[j] + self.rType[k] + str(self.license_number[l]).zfill(5)
                            print(titleID)
                            generateXML(titleID)
                    else:
                        for l in self.license_number:
                            titleID = self.media + self.rights[i] + self.region[j] + self.rType[1] + str(self.license_number[l]).zfill(5)
                            print(titleID)
                            generateXML(titleID)
                        break


# Digital PS3
class DigitalPS3:
    def __init__(self):
        self.network_environment = 'NP'
        self.region = ['A', 'E', 'H', 'J', 'K', 'U', 'I', 'X']
        self.rType = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.license_number = range(0, 100000)  # all 5 digit numbers (including leading 0s), use .zfill(5)

    def generate_titleID(self):
        for i in range(len(self.region)):
            for j in range(len(self.rType)):
                for k in self.license_number:
                    titleID = self.network_environment + self.region[i] + self.rType[j] + str(self.license_number[k]).zfill(5)
                    print(titleID)
                    generateXML(titleID)


# All PS4
class PS4:
    def __init__(self):
        self.pos = 0
        self.media = 'CUSA'
        self.license_number = range(0, 100000-self.pos)  # all 5 digit numbers (including leading 0s), use .zfill(5)

    def generate_titleID(self):
        for i in self.license_number:
            titleID = self.media + str(i+self.pos).zfill(5)
            print(titleID)
            generateJSON(titleID)


def generateXML(titleID):
    titleID = titleID + '_00'
    titleID_hash = titleID.encode('utf-8')
    Hash = hmac.new(tmdb_key, titleID_hash, hashlib.sha1).hexdigest()
    Hash = Hash.upper()

    XML_url = "http://tmdb.np.dl.playstation.net/tmdb/" + titleID + "_" + Hash + "/" + titleID + ".xml"
    testURL(XML_url)


def generateJSON(titleID):
    titleID = titleID + '_00'
    titleID_hash = titleID.encode('utf-8')
    Hash = hmac.new(tmdb_key, titleID_hash, hashlib.sha1).hexdigest()
    Hash = Hash.upper()

    JSON_url = "http://tmdb.np.dl.playstation.net/tmdb2/" + titleID + "_" + Hash + "/" + titleID + ".json"
    testURL(JSON_url)


def testURL(url):
    r = requests.get(url)
    if r.status_code == 200:
        print(url)
        storeURL(url)


def storeURL(url):
    file = open("tmdb.txt", "a")
    file.write(url)


# pPS3 = PhysicalPS3()
# dPS3 = DigitalPS3()
# PS4 = PS4()
# pPS3.generate_titleID()
# dPS3.generate_titleID()
# PS4.generate_titleID()


class Modifytxt:
    def __init__(self):
        pass

    def getDoc(self):
        file = open("tmdb.txt", "r")
        lines = file.readlines()
        for i in range(len(lines)):
            self.getText(lines[i])

    def getText(self, row):
        print(row)
        response = urlopen(row)
        html = response.read()

        # Can't append "\n" while in bytes mode, so has to be opened twice
        file = open("tmdbEntries.txt", "ab")    # open file in append-bytes mode
        file.write(html)
        file.close()

        file = open("tmdbEntries.txt", "a")
        file.write("\n")
        file.close()


# mTXT = Modifytxt()
# mTXT.getDoc()


def convertToCSV():
    file = open("tmdbEntries.txt", "rb")    # read-bytes
    lines = file.readlines()
    file.close()

    for i in range(len(lines)):
        lines[i] = lines[i].decode('utf-8')           # convert to string(?)

        # PS3
        if lines[i][0] == '<':
            titleid = re.search('<id>(.*?)</id>', lines[i]).group(1)
            console = re.search('<console>(.*?)</console', lines[i]).group(1)
            mediatype = re.search('<media-type>(.*?)</media-type>', lines[i]).group(1)
            name = re.search('<name>(.*?)</name>', lines[i]).group(1)
            try:
                namelang = re.search('<name lang=\"(.)\">(.*)</name>', lines[i]).group(0)
            except AttributeError:
                namelang = None
            parentallevel = re.search('<parental-level>(.)</parental-level>', lines[i]).group(1)
            icon = re.search('<icon type=\".{7}\">(.*?)</icon>', lines[i]).group(1)
            try:
                iconlang = re.search('<icon lang=\"(.)\" type=\".{7}\">(.*)</icon>', lines[i]).group(0)
            except AttributeError:
                iconlang = None
            resolution = re.search('<resolution>(.*)</resolution>', lines[i]).group(1)
            soundformat = re.search('<sound-format>(.*)</sound-format>', lines[i]).group(1)

            with open('PS3tmdb.csv', 'a', newline='', encoding='utf-8') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([titleid, console, mediatype, name, namelang, parentallevel, icon, iconlang, resolution, soundformat])

        # PS4
        # revision			[REQUIRED] (22060)
        # patchRevision     4945
        # formatVersion		[REQUIRED]
        # npTitleId 		[REQUIRED]
        # console 			[REQUIRED]
        # names 			[REQUIRED] - array
        # icons 			[REQUIRED] - array
        # parentalLevel 	[REQUIRED]
        # pronunciation 	[REQUIRED]
        # contentId 		[REQUIRED]
        # backgroundImage	18899
        # bgm				4491
        # category			22055 		[CUSA00873, CUSA01436, CUSA01804, CUSA01805, CUSA02933]
        # playTogether      1958
        # psVr				22055 		[CUSA00873, CUSA01436, CUSA01804, CUSA01805, CUSA02933]
        # neoEnable			225		[CUSA00873, CUSA01436, CUSA01804, CUSA01805, CUSA02933]
        elif lines[i][0] == '{':
            # PS4
            revision = re.search('\"revision\":(.{1,2}),', lines[i]).group(1)
            try:
                patchRevision = re.search('\"patchRevision\":(.{1,2}),', lines[i]).group(1)
            except AttributeError:
                patchRevision = None
            formatVersion = re.search('\"formatVersion\":(.{1,2}),', lines[i]).group(1)
            npTitleId = re.search('\"npTitleId\":\"(.*?)\"', lines[i]).group(1)
            console = re.search('\"console\":\"(.*?)\"', lines[i]).group(1)
            names = re.search('\"names\":(\[.*?\]),', lines[i]).group(1)
            icons = re.search('\"icons\":(\[.*?\]),', lines[i]).group(1)
            parentalLevel = re.search('\"parentalLevel\":(.),', lines[i]).group(1)
            pronunciation = re.search('\"pronunciation\":\"(.*?)\",', lines[i]).group(1)
            contentId = re.search('\"contentId\":\"(.*?)\"', lines[i]).group(1)
            try:
                backgroundImage = re.search('\"backgroundImage\":\"(.*?)\"', lines[i]).group(1)
            except AttributeError:
                backgroundImage = None
            try:
                bgm = re.search('\"bgm\":\"(.*?)\"', lines[i]).group(1)
            except AttributeError:
                bgm = None
            try:
                category = re.search('\"category\":\"(.*?)\"', lines[i]).group(1)
                psVr = re.search('\"psVr\":(.)', lines[i]).group(1)
            except AttributeError:
                category = None
                psVr = None
            try:
                playTogether = re.search('\"playTogether\":(.)', lines[i]).group(1)
            except AttributeError:
                playTogether = None
            try:
                neoEnable = re.search('\"neoEnable\":(.)', lines[i]).group(1)
            except AttributeError:
                neoEnable = None
            with open('PS4tmdb.csv', 'a', newline='', encoding='utf-8') as csvfile:
                spamwriter = csv.writer(csvfile,delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([revision, patchRevision, formatVersion, npTitleId, console, names, icons, parentalLevel, pronunciation, contentId, backgroundImage, bgm, category, playTogether, psVr, neoEnable])




def DownloadPS3Images():
    file = open("new 4.txt", "r")  # read
    lines = file.readlines()
    file.close()

    os.chdir(r"F:\PSimg")
    #print(lines)
    for i in range(len(lines)):
    # check if image already exists
        titleID = re.search('tmdb/(.*)_', lines[i])
        titleID = titleID.group(1)
        if os.path.isfile('{titleID}.png'.format(titleID=titleID)):
            pass
        else:
            print(titleID)
        # save image
            urllib.request.urlretrieve(lines[i], "{name}.png".format(name=titleID))
        # resize image & overwrite original
            image = Image.open("{titleID}.png".format(titleID=titleID))
            newImg = image.resize((400, 400))
            newImg.save("{titleID}.png".format(titleID=titleID))


def removeTrailingZero():
    os.chdir(r"F:\PSimg")
    x = os.listdir()
    for i in range(len(x)):
        z = re.search('(.*)_', x[i])
        z = z.group(1)
        print(z)
        os.rename(x[i], "{z}.png".format(z=z))


def resizeImage():  # for testing
    image = Image.open('bces00510.png')
    new_image = image.resize((400,400))
    new_image.save('0_bces00510.png')


def findDupes():
    os.chdir(r"F:\PSimg")
    files = os.listdir()
    savedMD5 = []
    for i in range(len(files)):
        with open(files[i], 'rb') as f:
            data = f.read()
            md5 = hashlib.md5(data).hexdigest()
            savedMD5.append(md5)

    md5final = []
    namefinal = []
    for i in range(len(savedMD5)):
        if savedMD5[i] not in md5final:
            md5final.append(savedMD5[i])
            namefinal.append(files[i])
        else:   # savedMD5[i] is the same as *some* item of md5final
            for j in range(len(md5final)):
                if md5final[j] == savedMD5[i]:
                    # print(md5final[j], savedMD5[i])
                    print(namefinal[j], files[i])
                    # print('')


findDupes()
