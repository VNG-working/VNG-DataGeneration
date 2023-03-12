import os

hint_test = 2000

raw_bank_names_path = os.getcwd() + "/content/raw_bank_names.txt"
raw_add_path = os.getcwd() + "/content/raw_foreign_address.txt"
raw_name_abbre_path = os.getcwd() + "/content/raw_foreign_company_names.txt"
raw_foreign_person_path = os.getcwd() + "/content/raw_foreign_person_names.txt"

raw_vn_unsign_add_path = os.getcwd() + "/content/raw_vietnamese_company_names.txt"
raw_vn_com_name_path = os.getcwd() + "/content/raw_vietnamese_company_foreign_form.txt"
raw_vn_per_name_path = os.getcwd() + "/content/raw_vietnamese_names.txt"

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

content = {
    "en_bank_name" : bank_names,
    "en_com_add" : com_add,
    "en_com_name_abrre" : com_name_abbre,
    "en_per_name" : per_name,
    "vn_unsign_add" : vn_unsign_add,
    "vn_com_name" : vn_com_name,
    "vn_per_name" : vn_per_name
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

    for key in content:
        # print(len(content[key]))

        f = open(os.getcwd() + f"/content/{key}.txt", "w")
        f.writelines(content[key])
        f.close()