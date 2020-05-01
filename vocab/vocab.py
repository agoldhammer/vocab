import docx
import click
import sqlite3

myfname = "/Users/agold/Google Drive/Vocabulary/German.docx"

def get_doc(fname):
    return docx.Document(fname)

def get_vitems(doc):
    return [p.text.split(':') for p in doc.paragraphs]

def validate_vitem(vitem):
    "return status, vitem where status is t/f and vitem is of len 3 with blank string added to supp field if nec"
    l = len(vitem)
    if l == 2:
        vitem.append('')
        return True, vitem
    elif l == 3:
        return True, vitem
    else:
        return False, vitem

""" def print_vitems(vitems):
    for vitem in vitems:
        print([text.strip() for text in vitem])

def print_bad(vitems):
    for vitem in vitems:
        l = len(vitem)
        if l != 2 and l != 3:
            print(f'Bad vitem {vitem}') """

if __name__ == "__main__":
    doc = get_doc(myfname)
    vitems = get_vitems(doc)
    valid_vitems = []
    invalid_vitems = []
    for vitem in vitems:
        status, v = validate_vitem(vitem)
        print(status, v)
        if status:
            valid_vitems.append([v[0].strip(), v[1].strip(), v[2].strip(), 0, 0])
        else:
            invalid_vitems.append(v)
    for vitem in valid_vitems:
        print(vitem)
    for vitem in invalid_vitems:
        print(f'Bad vitem: {vitem}')
    print(f'Total vitems: {len(vitems)}')
