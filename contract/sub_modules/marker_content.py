import os

source_txt = os.getcwd() + "/content/ds_cty.txt"
with open(source_txt, "r", encoding="utf-8") as f:
    lines = f.readlines()
    cty_lst = [x[:-1] for x in lines if "CÔNG TY" in x and "Mã số thuế" not in x]
    dc_lst = [" ".join(x[:-1].split(":")[-1].replace(",", " ").split(" ")) for x in lines if "Địa chỉ" in x]


content = {
    "company_add" : dc_lst,
    "company_name" : cty_lst
}

if __name__ == "__main__":
    pass
    # print(content["company_name"])