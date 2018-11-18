pdf_text = ""
text_for_day = []


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
    pdf_file_object.close()
    # print(pdfText)


def extract_day_from_pdf_text(weekday: int):
    is_weekday = False
    for line in pdf_text.splitlines():
        if is_weekday:
            # is next day?
            if line.startswith(get_following_day_as_string(weekday)):
                is_weekday = False
            else:
                text_for_day.append(line)
        if line.startswith(get_weekday_as_string(weekday)):
            text_for_day.append(line)
            is_weekday = True


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


def get_following_day_as_string(weekday: int):
    weekday_as_string = decode_weekday((weekday + 1) % 7)
    return weekday_as_string


def get_weekday_as_string(weekday: int):
    weekday_as_string = decode_weekday(weekday)
    return weekday_as_string


def format_menu():
    formatted_text = []
    formatted_text.append(text_for_day[0])

    # for each dish
    rest = text_for_day[1:]
    for i in range(0, 3):
        single_dish_string = ''
        for line in rest:
            if line == "":
                rest = rest[1:]
                import re
                s = re.sub(" *(\d,)*\d?$", "", single_dish_string)
                s = re.sub("  \"OPTIMAHL\"", " (OPTIMAHL™)", s)
                s = re.sub("^", "• ", s)
                formatted_text.append(re.sub(" *(\d,)*\d?$", "", s))
                break
            else:
                single_dish_string += line
                rest = rest[1:]
    return '\n'.join(formatted_text)


def delete_pdf():
    import os
    os.remove('./wochenkarte.pdf')


def get_menu(weekday: int):
    if weekday == 5:
        return 'Am Samstag hat die Kantine leider geschlossen.'
    elif weekday == 6:
        return 'Am Sonntag hat die Kantine leider geschlossen.'

    global pdf_text
    pdf_text = ""
    global text_for_day
    text_for_day = []

    # TODO: This could more efficient if only downloaded once per day/week.
    download_pdf()
    extract_pdf_text_from_pdf()
    delete_pdf()
    extract_day_from_pdf_text(weekday)
    if not text_for_day:
        return 'Ich konnte für diesen Tag leider nichts auf der Speisekarte finden.'

    menu_text = format_menu()
    return menu_text


def main():
    print(get_menu(0))
    print('----------------------------------')
    print(get_menu(1))
    print('----------------------------------')
    print(get_menu(2))
    print('----------------------------------')
    print(get_menu(3))
    print('----------------------------------')
    print(get_menu(4))
    print('----------------------------------')
    print(get_menu(5))
    print('----------------------------------')
    print(get_menu(6))


if __name__ == "__main__": main()
