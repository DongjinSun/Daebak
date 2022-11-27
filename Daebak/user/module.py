def listToString(listMenu):            #[1,2,3,4] -> 1234
    str_list = list(map(str, listMenu))#int list -> str list ["1", "2", "3", "4"]
    result = ""
    for s in str_list:
        result += s
    return result

def stringToList(intMenu):           #1234 -> [1,2,3,4]
    strMenu = str(intMenu)           #int -> str
    str_list = list(strMenu)         # ["1", "2", "3", "4"]
    return list(map(int, str_list))  # [1, 2, 3, 4]


