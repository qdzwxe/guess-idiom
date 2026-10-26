import json

convert_table = {
    "ā": ["a", "1"],
    "á": ["a", "2"],
    "ǎ": ["a", "3"],
    "à": ["a", "4"],
    "ō": ["o", "1"],
    "ó": ["o", "2"],
    "ǒ": ["o", "3"],
    "ò": ["o", "4"],
    "ē": ["e", "1"],
    "é": ["e", "2"],
    "ě": ["e", "3"],
    "è": ["e", "4"],
    "ī": ["i", "1"],
    "í": ["i", "2"],
    "ǐ": ["i", "3"],
    "ì": ["i", "4"],
    "ū": ["u", "1"],
    "ú": ["u", "2"],
    "ǔ": ["u", "3"],
    "ù": ["u", "4"],
    "ǖ": ["v", "1"],
    "ǘ": ["v", "2"],
    "ǚ": ["v", "3"],
    "ǜ": ["v", "4"],
}


def convert_pinyin(pinyin):
    tone = ""
    res = ""
    for c in pinyin:
        if c in convert_table:
            tone = convert_table[c][1]
            res += convert_table[c][0]
        else:
            res += c
    return res + tone


def convert_word_pinyin(pinyins):
    pinyin_list = pinyins.split(" ")
    return " ".join([convert_pinyin(c) for c in pinyin_list])


def split_pinyin(pinyin):
    res = {"sheng": "", "yun": "", "diao": ""}
    if pinyin[-1] in {"1", "2", "3", "4"}:
        res["diao"] = pinyin[-1]
        pinyin = pinyin[:-1]

    if pinyin[0] not in {"a", "e", "u", "i", "o"}:
        if pinyin[0] in {"z", "c", "s"} and pinyin[1] == "h":
            res["sheng"] = pinyin[:2]
            pinyin = pinyin[2:]
        else:
            res["sheng"] = pinyin[0]
            pinyin = pinyin[1:]

    res["yun"] = pinyin
    return res


def game_match(gue, ans):

    gue = list(map(split_pinyin, gue.split(" ")))
    ans = list(map(split_pinyin, ans.split(" ")))

    res = {
        "sheng": [" ", " ", " ", " "],
        "yun": [" ", " ", " ", " "],
        "diao": [" ", " ", " ", " "],
        "under": ["", "", "", ""],
    }
    vis = {
        "sheng": [0, 0, 0, 0],
        "yun": [0, 0, 0, 0],
        "diao": [0, 0, 0, 0],
        "under": [0, 0, 0, 0],
    }

    for i in range(4):
        for type in {"sheng", "yun", "diao"}:
            if gue[i][type] != "":
                if gue[i][type] == ans[i][type]:
                    res[type][i] = "a"
                    vis[type][i] = 1
            else:
                res[type][i] = ""

        if gue[i]["sheng"] + gue[i]["yun"] == ans[i]["sheng"] + ans[i]["yun"]:
            res["under"][i] = "_"
            vis["under"][i] = 1

    for i in range(4):
        for j in range(4):
            if i == j:
                continue
            for type in {"sheng", "yun", "diao"}:
                if res[type][i] == " " and vis[type][j] == 0:
                    if gue[i][type] == ans[j][type]:
                        res[type][i] = "b"
                        vis[type][j] = 1

            if res["under"][i] == "" and vis["under"][j] == 0:
                if gue[i]["sheng"] + gue[i]["yun"] == ans[j]["sheng"] + ans[j]["yun"]:
                    res["under"][i] = "_"
                    vis["under"][j] = 1

    for i in range(4):
        for type in {"sheng", "yun", "diao"}:
            if res[type][i] == " ":
                res[type][i] = "x"

    return " ".join(
        [
            res["sheng"][i] + res["yun"][i] + res["diao"][i] + res["under"][i]
            for i in range(4)
        ]
    )


with open("idiom.json", "rb") as f:
    data = json.load(f)

words = {}
for c in data:
    if len(c["word"]) != 4:
        continue
    if c["pinyin"] not in words:
        words[convert_word_pinyin(c["pinyin"])] = [c["word"]]
    else:
        words[convert_word_pinyin(c["pinyin"])].append(c["word"])


# 先输入拼音，空格分隔，声调在每项的最后
# 再输入反馈，x是灰色 a是绿色 b是黄色，如果有下划线，最后需加「_」，每项之间空格分隔
# 程序不检查输入合法性，需要保证输入正确
while True:
    gue = input()
    res = input()
    tmp = {}
    for k in words:
        if game_match(gue, k) == res:
            tmp[k] = words[k]
    words = tmp
    if len(words) < 100:
        count = 0
        for w in words:
            for c in words[w]:
                print(c, end="  ")
                if count % 10 == 9:
                    print()
                count += 1
    print()
    print(len(words))
    print("Total: ", len(words))
