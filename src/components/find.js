import Idioms from '../assets/idiom.json';

const convert_table = {
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
};

function convertPinyin(pinyin) { // ā to a1
    let tone = "",
        res = "";
    for (let c of pinyin) {
        if (c in convert_table) {
            tone = convert_table[c][1];
            res += convert_table[c][0];
        }
        else {
            res += c;
        }
    }
    return res + tone;
}

function convertWordPinyin(pinyins) { // ā á to [a1, a2]
    const pinyinList = pinyins.split(" ");
    return pinyinList.map(p => convertPinyin(p));
}

function splitPinyin(pinyin) {
    const res = { "sheng": "", "yun": "", "diao": "" };
    if (["1", "2", "3", "4"].includes(pinyin.slice(-1))) {
        res["diao"] = pinyin.slice(-1);
        pinyin = pinyin.slice(0, -1);
    }
    if (!["a", "e", "u", "i", "o"].includes(pinyin[0])) {
        if (["zh", "ch", "sh"].includes(pinyin.slice(0, 2))) {
            res["sheng"] = pinyin.slice(0, 2);
            pinyin = pinyin.slice(2);
        }
        else {
            res["sheng"] = pinyin[0];
            pinyin = pinyin.slice(1);
        }
    }
    res["yun"] = pinyin;
    return res;
}

export default function find(check = Array(4).fill(Array(4).fill('')), ban = Array(4).fill()) {
    const idioms = Idioms;
    const [checkChar, checkSheng, checkYun, checkDiao] = check;
    const res = [];
    const [banChar, banSheng, banYun, banDiao] = ban.map(b => b.split(' '));
    // console.log(banChar)
    idioms.forEach(idiom => {
        let match = true;
        if (idiom.word.length !== 4) match = false;
        const syds = convertWordPinyin(idiom.pinyin).map(p => splitPinyin(p));
        for (let i = 0; match && (i < 4); i++) {
            const [char, sheng, yun, diao] = [idiom.word[i], syds[i].sheng, syds[i].yun, syds[i].diao];
            if (banChar) match &&= !banChar.includes(char);
            if (banSheng) match &&= !banSheng.includes(sheng);
            if (banYun) match &&= !banYun.includes(yun);
            if (banDiao) match &&= !banDiao.includes(diao);
            if (match) {
                if (checkChar[i]) match &&= char === checkChar[i];
                if (checkSheng[i]) match &&= sheng === checkSheng[i];
                if (checkYun[i]) match &&= yun === checkYun[i];
                if (checkDiao[i]) match &&= diao === checkDiao[i];
            }
        }
        if (match) res.push(idiom.word);
    });
    return res.slice(0, 20);
}