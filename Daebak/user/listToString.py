def listToString(listMenu):            #[1,2,3,4] -> 1234
    str_list = list(map(str, listMenu))#int list -> str list ["1", "2", "3", "4"]
    result = ""
    for s in str_list:
        result += s
        #int형으로 반환
    return result

def stringToList(intMenu):           #1234 -> [1,2,3,4]
    strMenu = str(intMenu)           #int -> str
    str_list = list(strMenu)         # ["1", "2", "3", "4"]
    return list(map(int, str_list))  # [1, 2, 3, 4]


### TEST ###
dinner_selected = [1,2,3,4,5,6,7,8]
print("변환 전 리스트", dinner_selected)
dinner_int = listToString(dinner_selected)
print("list to int: ", dinner_int)
dinner_list = stringToList(dinner_int)
print("int to list: ", dinner_list)
