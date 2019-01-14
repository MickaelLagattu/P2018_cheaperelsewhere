
def read_test_file(file_name:str) -> str :
    file = open(file_name, "r", encoding='utf-8')
    line_liste = []
    i = 1
    for line in file :
        try:
            line_liste.append(line)
            print("xxxx")
            print(line)
        except :
            continue
    print(line_liste)
    return line_liste

file_name = 'test_sentences.txt'
read_test_file(file_name)
