import os

hint_test = -1

raw_bank_names_path = os.getcwd() + "/content/en_bank_name.txt"
raw_add_path = os.getcwd() + "/content/en_com_add.txt"
raw_name_abbre_path = os.getcwd() + "/content/en_com_name_abrre.txt"
raw_foreign_person_path = os.getcwd() + "/content/en_per_name.txt"

raw_vn_unsign_add_path = os.getcwd() + "/content/vn_unsign_add.txt"
raw_vn_com_name_path = os.getcwd() + "/content/vn_com_name.txt"
raw_vn_per_name_path = os.getcwd() + "/content/vn_per_name.txt"

position_path = os.getcwd() + "/content/all_position.txt"

with open(raw_bank_names_path, "r", encoding="utf-8") as f:
    bank_names = [x[:-1] for x in f.readlines(hint_test)]

with open(raw_add_path, "r", encoding="utf-8") as f:
    com_add = [x[3:-1] for x in f.readlines(hint_test)]

with open(raw_name_abbre_path, "r", encoding="utf-8") as f:
    com_name_abbre = [x[:-1] for x in f.readlines(hint_test)]

with open(raw_foreign_person_path, "r", encoding="utf-8") as f:
    per_name = [x[:-1] for x in f.readlines(hint_test)]

with open(raw_vn_unsign_add_path, "r", encoding="utf-8") as f:
    vn_unsign_add = [x[:-1] for x in f.readlines(hint_test)]

with open(raw_vn_com_name_path, "r", encoding="utf-8") as f:
    vn_com_name = [x[:-1] for x in f.readlines(hint_test)]

with open(raw_vn_per_name_path, "r", encoding="utf-8") as f:
    vn_per_name = [x[:-1] for x in f.readlines(hint_test)]

with open(position_path, "r", encoding="utf-8") as f:
    pos = [x[:-1] for x in f.readlines(hint_test) if len(x.split(" ")) < 3]

content = {
    "en_bank_name" : bank_names,
    "en_com_add" : com_add,
    "en_com_name_abrre" : com_name_abbre,
    "en_per_name" : per_name,
    "vn_unsign_add" : vn_unsign_add,
    "vn_com_name" : vn_com_name,
    "vn_per_name" : vn_per_name,
    "pos" : pos
}

if __name__ == "__main__":
    from numpy.random import choice
    print(choice(content["en_bank_name"]))
    print(choice(content["en_com_add"]))
    print(choice(content["en_com_name_abrre"]))
    print(choice(content["en_per_name"]))
    print(choice(content["vn_unsign_add"]))
    print(choice(content["vn_com_name"]))
    print(choice(content["vn_per_name"]))
    print(choice(content["pos"]))