# generate wordlist of password-extractor
def createfile(filepath: str):
    import json
    with open(filepath, 'r') as file, open('wordlist-c.txt') as wordlist:
        data: dict[dict[str, str]] = json.load(file)
        del data['From']
        password_list: list[str] = []
        
        for _, contents in data.items():
            for _, content in contents.items():
                passwd = content.get('decrypted_password', False)
                if passwd and passwd.strip() != '':
                    password_list.append(passwd)
        for password in set(password_list):
            wordlist.write(password + '\n')
def clearwordlist(filepath: str):
    with open(filepath, 'r+') as file:
        data = file.read()
        words = data.split('\n')
        file.seek(0)
        file.truncate()
        for word in words:
            if len(word) < 6:
                continue
            file.write(word + '\n')
if __name__ == '__main__':
    import sys
    clearwordlist('wordlist.txt')
    # try:
    #     createfile(sys.argv[1:][0])
    # except IndexError as e:
    #     print(str(e))
    #     exit(1)