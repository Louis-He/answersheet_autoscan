mport matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import math
from PIL import Image

def convert_to_bw(im):
    print 'scan and auto grading for page1!'
    width = im.size[0]
    height = im.size[1]
    blacksignwidth = int(math.floor(width / 51.6))#51.6
    blacksignheight = int(math.floor(blacksignwidth * 21 / 24))

    print width, height
    print blacksignwidth, blacksignheight
    im = im.convert("L")
    im = im.point(lambda x: 255 if x > 150 else 0)
    #im = im.convert('1')
    im.save("/Users/hsw/Desktop/balckwhiteprocess.JPG")
    region = (900, 100, 3000, 2000)
    #cropImg = im.crop(region)
    #cropImg.save('/Users/hsw/Desktop/number/cut.png')

    pix = im.load()
    detect = False
    detectx = 0
    detecty = 0
    for x in range(int(0.08 * width * 0.2), int(width * 0.2)):
        for y in range(int(height * 0.05), int(height * 0.15)):
            qualityok = True
            for i in range(blacksignwidth):
                for j in range(blacksignheight):
                    if pix[x + i, y + j] == 255:
                        qualityok = False
            if qualityok and (not detect):
                detect = True
                detectx = x
                detecty = y
                break
        else:
            continue
        break
            #a = pix[x, y]
            #lists[x].append(a)

    print '#1 balck sign detect state:' + str(detect)
    print '#1 balck sign upper left conner (x-axis):' + str(detectx)
    print '#1 balck sign upper left conner (y-axis):' + str(detecty)

    detect2 = False
    detect2x = 0
    detect2y = 0
    for x in range(int(0.08 * width * 0.2), int(width * 0.2)):
        for y in range(int(height * 0.4),int(height * 0.55)):
            quality2ok = True
            for i in range(blacksignwidth):
                for j in range(blacksignheight):
                    if pix[x + i, y + j] == 255:
                        quality2ok = False
            if quality2ok and (not detect2):
                detect2 = True
                detect2x = x
                detect2y = y
            #a = pix[x, y]
            # lists[x].append(a)
                break
        else:
            continue
        break


    print '#2 balck sign detect state:' + str(detect2)
    print '#2 balck sign upper left conner (x-axis):' + str(detect2x)
    print '#2 balck sign upper left conner (y-axis):' + str(detect2y)

    #cut width for each question
    position = int((detectx+detect2x)/2.0 + width / 72.9)#72.9

    widthnode = [position]
    for i in range(0,5):
        position = position + width / 6.68
        widthnode.append(position)
    for i in range(0,6):
        widthnode[i] = int(widthnode[i])
    print 'sign for a new question in a row(for further analysis)'
    print widthnode

    # cut height for each question
    position = int(detecty +  height / 46.1)

    heightnode = [position]
    for i in range(0, 11):
        position = position + height / 29.75
        heightnode.append(position)
    for i in range(0, 12):
        heightnode[i] = int(heightnode[i])
    print 'sign for a new question in a col(for further analysis)'
    print heightnode

    #analyze for the location for each question
    selectionx = 0
    answerseq1 = [] #list for answers(section1)
    print 'answer for section1 part!'
    questionnumber = 0
    filledcondition = int(height / 192 / 2)
    for col in range(0,5):
        for row in range(0,11):
            if questionnumber < 52:
                select = ''
                selection = False
                selection2 = False
                questionnumber = questionnumber + 1
                ULx = widthnode[col]
                ULy = heightnode[row]
                LRx = int(widthnode[col]+ width / 6.7)
                LRy = int(heightnode[row]+ height / 29.75)
                for i in range(ULx+filledcondition,LRx-filledcondition):
                    for j in range(ULy+filledcondition,LRy-filledcondition):
                        filledcircle = True
                        for a in range(-filledcondition, filledcondition, 1):
                            for b in range(-filledcondition, filledcondition, 1):
                                if pix[i + a, j + b] == 255:
                                    filledcircle = False
                        if filledcircle and (not selection):
                            selection = True
                            selectionx = i + a
                            selectiony = j + b
                        elif filledcircle and (selection) and ((i+a) > (selectionx + width / 35.4)):
                            selection2 = True
                            selectionx2 = i + a
                            selectiony2 = j + b

                if selectionx > ULx + width / 34.42 and selectionx < ULx + width / 34.42 + width / 35.4 and selection and (not selection2):
                    select = 'A'
                elif selectionx > ULx + width / 34.42 + width / 35.4 and selectionx < ULx + width / 34.42 + 2 * width / 35.4 and selection and (not selection2):
                    select = 'B'
                elif selectionx > ULx + width / 34.42 + 2 * width / 35.4 and selectionx < ULx + width / 34.42 + 3 * width / 35.4 and selection and (not selection2):
                    select = 'C'
                elif selectionx > ULx + width / 34.42 + 3 * width / 35.4 and selectionx < ULx + width / 34.42 + 4 * width / 35.4 and selection and (not selection2):
                    select = 'D'
                elif selection2:
                    select = 'ERROR DETECTED. NEED TO CONFIRM AGAIN!'
                else:
                    select = 'NO ANSWER'
                answerseq1.append(select)
                print questionnumber, select


    '''
    Program for scan Grammer questions
    '''
    # cut height for each question
    position = int(detect2y + height / 46.1)

    heightnode = [position]
    for i in range(0, 9):
        position = position + height / 29.75
        heightnode.append(position)
    for i in range(0, 10):
        heightnode[i] = int(heightnode[i])
    print 'sign for a new question in a col(for further analysis)'
    print heightnode

    # analyze for the location for each question
    selectionx = 0
    answerseq2 = []  # list for answers(section1)
    print 'answer for section2 part!'
    questionnumber = 0
    filledcondition = int(height / 192 / 2)
    for col in range(0, 5):
        for row in range(0, 9):
            if questionnumber < 44:
                select = ''
                selection = False
                selection2 = False
                questionnumber = questionnumber + 1
                ULx = widthnode[col]
                ULy = heightnode[row]
                LRx = int(widthnode[col] + width / 6.7)
                LRy = int(heightnode[row] + height / 29.75)
                for i in range(ULx + filledcondition, LRx - filledcondition):
                    for j in range(ULy + filledcondition, LRy - filledcondition):
                        filledcircle = True
                        for a in range(-filledcondition, filledcondition, 1):
                            for b in range(-filledcondition, filledcondition, 1):
                                if pix[i + a, j + b] == 255:
                                    filledcircle = False
                        if filledcircle and (not selection):
                            selection = True
                            selectionx = i + a
                            selectiony = j + b
                        elif filledcircle and (selection) and ((i + a) > (selectionx + width / 35.4)):
                            selection2 = True
                            selectionx2 = i + a
                            selectiony2 = j + b

                if selectionx > ULx + width / 34.42 and selectionx < ULx + width / 34.42 + width / 35.4 and selection and (
                not selection2):
                    select = 'A'
                elif selectionx > ULx + width / 34.42 + width / 35.4 and selectionx < ULx + width / 34.42 + 2 * width / 35.4 and selection and (
                not selection2):
                    select = 'B'
                elif selectionx > ULx + width / 34.42 + 2 * width / 35.4 and selectionx < ULx + width / 34.42 + 3 * width / 35.4 and selection and (
                not selection2):
                    select = 'C'
                elif selectionx > ULx + width / 34.42 + 3 * width / 35.4 and selectionx < ULx + width / 34.42 + 4 * width / 35.4 and selection and (
                not selection2):
                    select = 'D'
                elif selection2:
                    select = 'ERROR DETECTED. NEED TO CONFIRM AGAIN!'
                else:
                    select = 'NO ANSWER'
                answerseq2.append(select)
                print questionnumber, select

    '''
    pix = im.load()
    for x in range(width):
        for y in range(height):
            a = pix[x, y]
            lists[x].append(a)
    '''
    return [answerseq1,answerseq2]

def convert_to_bw2(im):
    print 'scan and auto grading for page 2!'
    width = im.size[0]
    height = im.size[1]
    blacksignwidth = int(math.floor(width / 51.6))  # 51.6
    blacksignheight = int(math.floor(blacksignwidth * 21 / 24))

    print width, height
    print blacksignwidth, blacksignheight
    im = im.convert("L")
    im = im.point(lambda x: 255 if x > 150 else 0)
    # im = im.convert('1')
    im.save("/Users/hsw/Desktop/balckwhiteprocess.JPG")
    region = (900, 100, 3000, 2000)
    # cropImg = im.crop(region)
    # cropImg.save('/Users/hsw/Desktop/number/cut.png')

    pix = im.load()
    detect = False
    detectx = 0
    detecty = 0
    for x in range(int(0.08 * width * 0.2), int(width * 0.2)):
        for y in range(int(height * 0.05), int(height * 0.15)):
            qualityok = True
            for i in range(blacksignwidth):
                for j in range(blacksignheight):
                    if pix[x + i, y + j] == 255:
                        qualityok = False
            if qualityok and (not detect):
                detect = True
                detectx = x
                detecty = y
                break
        else:
            continue
        break
        # a = pix[x, y]
        # lists[x].append(a)

    print '#1 balck sign detect state:' + str(detect)
    print '#1 balck sign upper left conner (x-axis):' + str(detectx)
    print '#1 balck sign upper left conner (y-axis):' + str(detecty)

    detect2 = False
    detect2x = 0
    detect2y = 0
    for x in range(int(0.08 * width * 0.2), int(width * 0.2)):
        for y in range(int(height * 0.45), int(height * 0.6)):
            quality2ok = True
            for i in range(blacksignwidth):
                for j in range(blacksignheight):
                    if pix[x + i, y + j] == 255:
                        quality2ok = False
            if quality2ok and (not detect2):
                detect2 = True
                detect2x = x
                detect2y = y
                # a = pix[x, y]
                # lists[x].append(a)
                break
        else:
            continue
        break

    print '#2 balck sign detect state:' + str(detect2)
    print '#2 balck sign upper left conner (x-axis):' + str(detect2x)
    print '#2 balck sign upper left conner (y-axis):' + str(detect2y)

    # cut width for each question
    position = int((detectx + detect2x) / 2.0 + width / 72.9)

    widthnode = [position]
    for i in range(0, 5):
        position = position + width / 6.68
        widthnode.append(position)
    for i in range(0, 6):
        widthnode[i] = int(widthnode[i])
    print 'sign for a new question in a row(for further analysis)'
    print widthnode

    # cut height for each question
    position = int(detecty + height / 46.1)

    heightnode = [position]
    for i in range(0, 3):
        position = position + height / 29.75
        heightnode.append(position)
    for i in range(0, 4):
        heightnode[i] = int(heightnode[i])
    print 'sign for a new question in a col(for further analysis)'
    print heightnode

    # analyze for the location for each question
    selectionx = 0
    answerseq1 = []  # list for answers(section1)
    print 'answer for section3[selection] part!'
    questionnumber = 0
    filledcondition = int(height / 192 / 2)
    for col in range(0, 5):
        for row in range(0, 3):
            if questionnumber < 15:
                select = ''
                selection = False
                selection2 = False
                questionnumber = questionnumber + 1
                ULx = widthnode[col]
                ULy = heightnode[row]
                LRx = int(widthnode[col] + width / 6.7)
                LRy = int(heightnode[row] + height / 29.75)
                for i in range(ULx + filledcondition, LRx - filledcondition):
                    for j in range(ULy + filledcondition, LRy - filledcondition):
                        filledcircle = True
                        for a in range(-filledcondition, filledcondition, 1):
                            for b in range(-filledcondition, filledcondition, 1):
                                if pix[i + a, j + b] == 255:
                                    filledcircle = False
                        if filledcircle and (not selection):
                            selection = True
                            selectionx = i + a
                            selectiony = j + b
                        elif filledcircle and (selection) and ((i + a) > (selectionx + width / 35.4)):
                            selection2 = True
                            selectionx2 = i + a
                            selectiony2 = j + b

                if selectionx > ULx + width / 34.42 and selectionx < ULx + width / 34.42 + width / 35.4 and selection and (
                not selection2):
                    select = 'A'
                elif selectionx > ULx + width / 34.42 + width / 35.4 and selectionx < ULx + width / 34.42 + 2 * width / 35.4 and selection and (
                not selection2):
                    select = 'B'
                elif selectionx > ULx + width / 34.42 + 2 * width / 35.4 and selectionx < ULx + width / 34.42 + 3 * width / 35.4 and selection and (
                not selection2):
                    select = 'C'
                elif selectionx > ULx + width / 34.42 + 3 * width / 35.4 and selectionx < ULx + width / 34.42 + 4 * width / 35.4 and selection and (
                not selection2):
                    select = 'D'
                elif selection2:
                    select = 'ERROR DETECTED. NEED TO CONFIRM AGAIN!'
                else:
                    select = 'NO ANSWER'
                answerseq1.append(select)
                print questionnumber, select


    # cut height for each question
    position = int(detecty + height / 4.7097)

    heightnode = [position]
    for i in range(0, 12):
        position = position + height / 63.135
        heightnode.append(position)
    for i in range(0, 13):
        heightnode[i] = int(heightnode[i])
    print 'sign for a new question in a col(for further analysis)'
    print heightnode

    # analyze for the location for each question
    selectionx = 0
    answerseq1 = []  # list for answers(section3-1)
    answerseq2 = [] # list for answers(section3-2)
    print 'answer for section3(filling) part!'
    questionnumber = 0
    filledcondition = int(height / 192 / 2)
    for col in range(0, 5):
        questionnumber = questionnumber + 1
        tempanswer = ['','','','']
        for row in range(0, 12):
            if questionnumber < 6:
                selection = False
                selection2 = False
                selection3 = False
                selection4 = False
                ULx = widthnode[col]
                ULy = heightnode[row]
                LRx = int(widthnode[col] + width / 6.7)
                LRy = int(heightnode[row] + height / 29.75)
                for i in range(ULx + filledcondition, LRx - filledcondition):
                    for j in range(ULy + filledcondition, LRy - filledcondition):
                        filledcircle = True
                        for a in range(-filledcondition, filledcondition, 1):
                            for b in range(-filledcondition, filledcondition, 1):
                                if pix[i + a, j + b] == 255:
                                    filledcircle = False
                        if filledcircle == True and (i+a) > ULx + width / 25.28 and (i+a) < ULx + width / 25.28 + width / 39.3:
                            selection = True
                        if filledcircle == True and (i+a) > ULx + width / 25.28 + width / 39.3 and (i+a) < ULx + width / 25.28 + 2 * width / 39.3:
                            selection2 = True
                        if filledcircle == True and (i+a) > ULx + width / 25.28 + 2 * width / 39.3 and (i+a) < ULx + width / 25.28 + 3 * width / 39.3:
                            selection3 = True
                        if filledcircle == True and (i+a) > ULx + width / 25.28 + 3 * width / 39.3 and (i+a) < ULx + width / 25.28 + 4 * width / 39.3:
                            selection4 = True

                        symbol = ''
                        if row == 0:
                            symbol = '/'
                        if row == 1:
                            symbol = '.'
                        if row > 1 and row < 12:
                            symbol = str(row - 2)

                        if selection:
                            tempanswer[0] = symbol
                        if selection2:
                            tempanswer[1] = symbol
                        if selection3:
                            tempanswer[2] = symbol
                        if selection4:
                            tempanswer[3] = symbol

        if tempanswer[0] == '' and tempanswer[1] == '' and tempanswer[2] == '' and tempanswer[3] == '':
            print questionnumber, ': NO ANSWER'
            answerseq2.append('NO ANSWER')
        else:
            print questionnumber, ': ',tempanswer[0],tempanswer[1],tempanswer[2],tempanswer[3]
            answerseq2.append(str(tempanswer[0])+str(tempanswer[1])+str(tempanswer[2])+str(tempanswer[3]))

    '''
        Program for scan section4(selection) questions
        '''
    # cut height for each question
    position = int(detect2y + height / 46.1)

    heightnode = [position]
    for i in range(0, 6):
        position = position + height / 29.75
        heightnode.append(position)
    for i in range(0, 7):
        heightnode[i] = int(heightnode[i])
    print 'sign for a new question in a col(for further analysis)'
    print heightnode

    # analyze for the location for each question
    selectionx = 0
    answerseq3 = []  # list for answers(section1)
    print 'answer for section4(selection) part!'
    questionnumber = 0
    filledcondition = int(height / 192 / 2)
    for col in range(0, 5):
        for row in range(0, 6):
            if questionnumber < 44:
                select = ''
                selection = False
                selection2 = False
                questionnumber = questionnumber + 1
                ULx = widthnode[col]
                ULy = heightnode[row]
                LRx = int(widthnode[col] + width / 6.7)
                LRy = int(heightnode[row] + height / 29.75)
                for i in range(ULx + filledcondition, LRx - filledcondition):
                    for j in range(ULy + filledcondition, LRy - filledcondition):
                        filledcircle = True
                        for a in range(-filledcondition, filledcondition, 1):
                            for b in range(-filledcondition, filledcondition, 1):
                                if pix[i + a, j + b] == 255:
                                    filledcircle = False
                        if filledcircle and (not selection):
                            selection = True
                            selectionx = i + a
                            selectiony = j + b
                        elif filledcircle and (selection) and ((i + a) > (selectionx + width / 35.4)):
                            selection2 = True
                            selectionx2 = i + a
                            selectiony2 = j + b

                if selectionx > ULx + width / 34.42 and selectionx < ULx + width / 34.42 + width / 35.4 and selection and (
                        not selection2):
                    select = 'A'
                elif selectionx > ULx + width / 34.42 + width / 35.4 and selectionx < ULx + width / 34.42 + 2 * width / 35.4 and selection and (
                        not selection2):
                    select = 'B'
                elif selectionx > ULx + width / 34.42 + 2 * width / 35.4 and selectionx < ULx + width / 34.42 + 3 * width / 35.4 and selection and (
                        not selection2):
                    select = 'C'
                elif selectionx > ULx + width / 34.42 + 3 * width / 35.4 and selectionx < ULx + width / 34.42 + 4 * width / 35.4 and selection and (
                        not selection2):
                    select = 'D'
                elif selection2:
                    select = 'ERROR DETECTED. NEED TO CONFIRM AGAIN!'
                else:
                    select = 'NO ANSWER'
                answerseq3.append(select)
                print questionnumber, select


    return [answerseq1, answerseq2, answerseq3]

def convert_to_bw3(im):
    return

referenceans = [[['A', 'D', 'B', 'C', 'D', 'B', 'A', 'B', 'A', 'C', 'A', 'D', 'A', 'B', 'C', 'C', 'B', 'C', 'C', 'A', 'D', 'A', 'C', 'D', 'B', 'C', 'C', 'A', 'C', 'A', 'D', 'B', 'B', 'D', 'C', 'C', 'A', 'B', 'D', 'B', 'D', 'D', 'C', 'B', 'D', 'D', 'C', 'A', 'A', 'A', 'B', 'A'], ['C', 'D', 'A', 'C', 'D', 'C', 'B', 'A', 'A', 'B', 'A', 'A', 'B', 'D', 'B', 'C', 'A', 'B', 'B', 'A', 'D', 'D', 'D', 'B', 'C', 'A', 'A', 'B', 'C', 'D', 'C', 'A', 'C', 'B', 'A', 'B', 'C', 'D', 'A', 'C', 'B', 'C', 'D', 'A'],['C', 'C', 'D', 'A', 'A', 'D', 'D', 'D', 'C', 'C', 'A', 'D', 'B', 'A', 'C'],['B','A','B','D','C','D','A','B','C','A','B','D','D','B','C','A','B','C','D','B','D','D','C','A','B','A','B','A','D','B']]]
print 'select the number of test:'
test = input('number: ')
lists = [[] for i in range(3000)]
im = Image.open(" ")#place where the answer sheet page 1 is stored
scanresult = convert_to_bw(im)
print scanresult
im2 = Image.open(" ")#place where the answer sheet page 2 is stored
scanresult.append(convert_to_bw2(im2))

correct = 0
NA = []
null = []
mistakes = []
for i in range(0, len(scanresult[0])):
    if (scanresult[0][i]==referenceans[int(test)][0][i]):
        correct = correct + 1
    elif scanresult[0][i] == 'ERROR DETECTED. NEED TO CONFIRM AGAIN!':
        NA.append(i+1)
    elif scanresult[0][i] == 'NO ANSWER':
        null.append(i + 1)
    else:
        mistakes.append(i+1)

correct2 = 0
NA2 = []
null2 = []
mistakes2 = []
for i in range(0, len(scanresult[1])):
    if (scanresult[1][i]==referenceans[int(test)][1][i]):
        correct2 = correct2 + 1
    elif scanresult[1][i] == 'ERROR DETECTED. NEED TO CONFIRM AGAIN!':
        NA2.append(i + 1)
    elif scanresult[1][i] == 'NO ANSWER':
        null2.append(i + 1)
    else:
        mistakes2.append(i+1)

correct3 = 0
NA3 = []
null3 = []
mistakes3 = []
for i in range(0, len(scanresult[2][0])):
    if (scanresult[2][0][i]==referenceans[int(test)][2][i]):
        correct3 = correct3 + 1
    elif scanresult[2][0][i] == 'ERROR DETECTED. NEED TO CONFIRM AGAIN!':
        NA3.append(i + 1)
    elif scanresult[2][0][i] == 'NO ANSWER':
        null3.append(i + 1)
    else:
        mistakes3.append(i + 1)

correct4 = 0
NA4 = []
null4 = []
mistakes4 = []
for i in range(0, len(scanresult[2][2])):
    if (scanresult[2][2][i]==referenceans[int(test)][3][i]):
        correct4 = correct4 + 1
    elif scanresult[2][2][i] == 'ERROR DETECTED. NEED TO CONFIRM AGAIN!':
        NA4.append(i + 1)
    elif scanresult[2][2][i] == 'NO ANSWER':
        null4.append(i + 1)
    else:
        mistakes4.append(i + 1)

print 'Section1: correct:', correct, '; not sure:', NA, '; wrong answer:',mistakes, '; no answer:', null
print 'Section2: correct:', correct2, '; not sure:', NA2, '; wrong answer:', mistakes2, '; no answer:', null2
print 'Section3(selection): correct:', correct3, '; not sure:', NA3, '; wrong answer:', mistakes3, '; no answer:', null3
print 'Section3(filling): ', scanresult[2][1]
print 'Section4(selection): correct:', correct4, '; not sure:', NA4, '; wrong answer:', mistakes4, '; no answer:', null4
