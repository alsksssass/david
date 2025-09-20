import os


def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    password_txt_path = os.path.join(base_path, "password.txt")
    dic_txt_path = os.path.join(base_path, "dic.txt")
    dic = []
    with open(dic_txt_path, "r", encoding="utf-8") as f:
        for line in f:
            dic.append(line.strip())
    word = ""
    with open(password_txt_path, "r", encoding="utf-8") as f:
        word = f.read().strip()
    caesar_cipher_decode(word, dic)


def get_next_ascii(char):
    if char == " ":
        return char
    next_number = ord(char)
    if next_number == ord("z"):
        next_number = ord("a")
    else:
        next_number += 1
    return chr(next_number)


def get_next_word(word):
    return "".join([get_next_ascii(w) for w in word])


def caesar_cipher_decode(target_text, dic):
    for i in range(26):
        target_text = get_next_word(target_text)
        for word in dic:
            if word.strip() in target_text:
                print(f" No.{i+1}  :  {target_text} - Found match: {word.strip()}")
                return
        print(f" No.{i+1}  :  {target_text}")


if __name__ == "__main__":
    main()
