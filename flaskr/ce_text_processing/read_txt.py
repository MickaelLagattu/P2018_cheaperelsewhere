
def read_test_file(file_name:str) -> list :
    file = open(file_name, "r", encoding='utf-8')
    line_liste = []
    i = 1
    for line in file :
        try:
            line_liste.append(line)
        except :
            continue
    # print(line_liste)
    return line_liste

def read_sentences_file(file_name:str) -> list :
    file = open(file_name, "r", encoding='utf-8')
    line_liste = []
    i = 1
    for line in file :
        try:
            line_liste.append(line)
        except :
            continue
    # print(line_liste)
    return line_liste
