def createDic(name, text, tooltip):
    dic = {}
    dic[name] = {}
    dic[name]['text'] = text
    dic[name]["tool_tip_text"] = str(tooltip)
    return dic


print(createDic('load_button', 'Load',
                "loads the saved board or (l : key)"))
