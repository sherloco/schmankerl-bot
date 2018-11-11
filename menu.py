test_mode = False
test_day = 4
pdf_text = ""
text_today = []
menu_text = []


def download_pdf():
    import requests
    import codecs
    url_file = codecs.open('./url.dat', encoding='utf-8')
    url = url_file.read()
    r = requests.get(url, stream=True)

    with open('./wochenkarte.pdf', 'wb') as f:
        f.write(r.content)


def extract_pdf_text_from_pdf():
    import PyPDF2
    pdf_file_object = open('./wochenkarte.pdf', 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_object)
    global pdf_text
    pdf_text = pdf_reader.getPage(0).extractText()
    # print(pdfText)


def extract_today_from_pdf_text():
    current_day = False
    for line in pdf_text.splitlines():
        if current_day:
            if line.startswith(get_next_day_of_the_week()):
                current_day = False
            else:
                text_today.append(line)
        if line.startswith(get_day_of_the_week()):
            text_today.append(line)
            current_day = True


def decode_weekday(weekday: int):
    switcher = {
        0: "Montag",
        1: "Dienstag",
        2: "Mittwoch",
        3: "Donnerstag",
        4: "Freitag",
        5: "Samstag",
        6: "Sonntag"
    }
    return switcher.get(weekday, "Invalid day")


def get_next_day_of_the_week():
    import datetime
    weekday_as_int = (datetime.datetime.today().weekday() + 1) % 7
    if test_mode:
        weekday_as_int = (test_day + 1) % 7
    weekday_as_string = decode_weekday(weekday_as_int)
    return weekday_as_string


def get_day_of_the_week():
    import datetime
    weekday_as_int = datetime.datetime.today().weekday()
    if test_mode:
        weekday_as_int = test_day
    weekday_as_string = decode_weekday(weekday_as_int)
    return weekday_as_string


def format_menu():
    formated_text = []
    formated_text.append(text_today[0])

    # for each dish
    rest = text_today[1:]
    for i in range(0, 3):
        single_dish_string = ''
        for line in rest:
            if line == "":
                rest = rest[1:]
                formated_text.append(single_dish_string)
                break
            else:
                single_dish_string += line
                rest = rest[1:]
    return '\n'.join(formated_text)


def get_menu():
    if (not test_mode) or (test_day == 5) or (test_day == 6):
        import datetime
        if not test_mode:
            weekday_as_int = datetime.datetime.today().weekday()
        else:
            weekday_as_int = test_day
        if weekday_as_int == 5:
            return 'Am Samstag hat die Kantine leider geschlossen.'
        elif weekday_as_int == 6:
            return 'Am Sonntag hat die Kantine leider geschlossen.'

    # TODO: This could more efficient if only downloaded once per day/week.
    download_pdf()
    extract_pdf_text_from_pdf()
    extract_today_from_pdf_text()
    if not text_today:
        return 'Ich konnte für heute leider nichts auf der Speisekarte finden.'
    global menu_text
    menu_text = format_menu()
    print(menu_text)
    return menu_text


def get_test_mode():
    return test_mode


def main():
    get_menu()


if __name__ == "__main__": main()
