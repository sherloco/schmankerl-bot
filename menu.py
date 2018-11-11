testMode = False
testDay = 4
pdfText = ""
textToday = []
menuText = []


def downloadPdf():
    import requests
    url = 'http://justika.de/Speisekarten/Justika_Wochenkarte_aktuell.pdf'
    r = requests.get(url, stream=True)

    with open('./wochenkarte.pdf', 'wb') as f:
        f.write(r.content)


def extractPdfTextFromPdf():
    import PyPDF2
    pdfFileObject = open('./wochenkarte.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
    global pdfText
    pdfText = pdfReader.getPage(0).extractText()
    # print(pdfText)


def extractTodayFromPdfText():
    currentDay = False
    for line in pdfText.splitlines():
        if currentDay:
            if line.startswith(getNextDayOfTheWeek()):
                currentDay = False
            else:
                textToday.append(line)
                #print(line)
        if line.startswith(getDayOfTheWeek()):
            textToday.append(line)
            currentDay = True
            #print(line)


def decodeWeekday(weekdayAsInt: int):
    switcher = {
        0: "Montag",
        1: "Dienstag",
        2: "Mittwoch",
        3: "Donnerstag",
        4: "Freitag",
        5: "Samstag",
        6: "Sonntag"
    }
    return switcher.get(weekdayAsInt, "Invalid day")


def getNextDayOfTheWeek():
    import datetime
    weekdayAsInt = (datetime.datetime.today().weekday() + 1) % 7
    if (testMode):
        weekdayAsInt = (testDay + 1) % 7
    weekdayAsString = decodeWeekday(weekdayAsInt)
    return weekdayAsString


def getDayOfTheWeek():
    import datetime
    weekdayAsInt = datetime.datetime.today().weekday()
    if (testMode):
        weekdayAsInt = testDay
    weekdayAsString = decodeWeekday(weekdayAsInt)
    return weekdayAsString


def formatMenu(textToday):
    formatedText = []
    formatedText.append(textToday[0])

    # for each dish
    rest = textToday[1:]
    for i in range(0, 3):
        singleDishString = ''
        for line in rest:
            if line == "":
                rest = rest[1:]
                formatedText.append(singleDishString)
                break
            else:
                singleDishString += line
                rest = rest[1:]
    return '\n'.join(formatedText)
    #print(formatedText)


def getMenu():
    if (not testMode) or (testDay == 5) or (testDay == 6):
        import datetime
        if not testMode:
            weekdayAsInt = datetime.datetime.today().weekday()
        else:
            weekdayAsInt = testDay
        if weekdayAsInt == 5:
            return 'Am Samstag hat die Kantine leider geschlossen.'
        elif weekdayAsInt == 6:
            return 'Am Sonntag hat die Kantine leider geschlossen.'

    downloadPdf()
    extractPdfTextFromPdf()
    extractTodayFromPdfText()
    if not textToday:
        return 'Ich konnte für heute leider nichts auf der Speisekarte finden.'
    global menuText
    menuText = formatMenu(textToday)
    print(menuText)
    return menuText

def getTestMode():
    return testMode


def main():
    getMenu()


if __name__ == "__main__": main()
