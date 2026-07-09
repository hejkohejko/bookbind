from PIL import Image
import math
import os
import array

# May god forgive me for this, this is the first time I actually wrote a useful
# script in python

# join two images into one, with an optional middle margin
def joiner(returnname, imgl, imgr, width, height, marginmiddle, flip):
    img = Image.open(imgl)
    img1 = Image.open(imgr)

    widthofone = math.ceil((width - marginmiddle)/2)
    img_size = img.resize((widthofone, height))
    img1_size = img1.resize((widthofone, height))

    img2 = Image.new("RGB", (width, height), "white")
    img2.paste(img_size, (0, 0))
    img2.paste(img1_size, (widthofone+marginmiddle, 0))
    if flip == 'y':
        img2 = img2.transpose(Image.ROTATE_180)

    print("saving " + imgl + " and " + imgr + " as " + returnname)
    img2.save(returnname)

# okay, so basically you need a goddamn text file with all your file names
# for now it only works on linux lolll I am so not suffering on windows. I am discriminating

# load in image names from a .txt file, return their names
def load_in_files(filename):
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file]

    if len(lines) % 4 != 0:
        for i in range(4 - (len(lines) % 4)):
            lines.append("empty.png")

    return lines

# calculating that
def pages_per_signature(pagenum, persignature):
    if persignature > 13:
        print("The upper limit of pages per signature is 13! (my apolocheese, the way i name these is fully based on the english alphabet)")
        return

    kartki = math.ceil(pagenum/4)
    signaturenum = math.ceil(kartki/persignature)

    kartken = []
    for i in range(signaturenum):
        kartken.append(persignature)

    extra = persignature*signaturenum - kartki
    for i in range(extra):
        kartken[i] = kartken[i] - 1

    return kartken

# like, generate the damned png files for it
# only rlly works when you have less than 26 pngs per signature
def splice_one_signature(filenames, startindex, endindex, width, height, marginmiddle, signum, flip, outputfolder):
    if endindex - startindex > 52:
        os._exit("Oops! the signature got too thick... aka my naming conventions have failed. Delete whatever images got created and restart with a higher amount of signatures")
        return

    sigletter = chr(97 + signum)
    pom = 0

    while startindex < endindex:
        name = outputfolder + "/" + sigletter + '-' + chr(pom + 97) + ".png"
        joiner(name, filenames[endindex], filenames[startindex], width, height, marginmiddle, 'n')

        startindex = startindex + 1
        endindex = endindex - 1
        pom = pom + 1

        name = outputfolder + "/" + sigletter + '-' + chr(pom + 97) + ".png"
        joiner(name, filenames[startindex], filenames[endindex], width, height, marginmiddle, flip)
        startindex = startindex + 1
        endindex = endindex - 1
        pom = pom + 1

# currently only works on linux
def generate_file_list(ordering, path):
    cmd = "ls -1d" + ordering + " " + path + "/* > ./files.txt"
    os.system(cmd)


# generate image files for everything ever!!!
def splice_entire_thing(filenames, width, height, marginmiddle, signum, flip, outputfolder):
    files = load_in_files(filenames)
    kartken = pages_per_signature(len(files), signum)

    print("Sheets per each signature:")
    print(kartken)

    startindex = 0
    for i in range(len(kartken)):
        endindex = startindex + kartken[i]*4 - 1

        print("pages ", startindex + 1, "-", endindex + 1)
        splice_one_signature(files, startindex, endindex, width, height, marginmiddle, i, flip, outputfolder)

        startindex = endindex + 1

# anddd the actual running of the boy!!!!!
print("Welcome to bookbind aid: a simple terminal based tool to turn your image files into something you can print and bookbind!\n")

# all the parameters
folderpath = input("Path to the folder with the images :")
ordering = input("Order of the pages: \n  1) alphabetical\n  2) alphabetical reversed\n  3) last edit time\n  4) last edit time reversed")

if ordering == 2:
    ordering = "r"
elif ordering == 3:
    ordering = "t"
elif ordering == 4:
    ordering = "tr"
else:
    ordering = ""

width = int(input("Width of one signature (px): "))
height = int(input("Height of one signature (px): "))
marginmiddle = int(input("Width of the margin inbetween images: "))
signum = int(input("Max. amount of paper sheets per signature (max 13): "))
flip = input("Do you want every other page flipped 180 degrees? (might be needed for some printers) [y/n]: ")

generate_file_list(ordering, folderpath)
splice_entire_thing("files.txt", width, height, marginmiddle, signum, flip, "printable")

print("\nAll spliced and put into the 'printable' folder. Happy bookbinding!")
