import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackEvent, PostbackTemplateAction, ImageSendMessage

from fsm import TocMachine
from utils import send_text_message, send_line_message, send_station_message

load_dotenv()
in_station = False

states=['user', '文湖線', '淡水信義線', '松山新店線', '中和新蘆線', '板南線', '環狀線', '南港展覽館_BL', '南港', '昆陽', '後山埤', '永春', '市政府', '國父紀念館', '忠孝敦化', '忠孝復興_BL', '忠孝新生_BL', '善導寺', '台北車站_BL', '西門_BL', '龍山寺', '江子翠', '新埔', '板橋_BL', '府中', '亞東醫院', '海山', '土城', '永寧', '頂埔', '動物園', '木柵', '萬芳社區', '萬芳醫院', '辛亥', '麟光', '六張犁', '科技大樓', '大安_BR', '忠孝復興_BR', '南京復興_BR', '中山國中', '松山機場', '大直', '劍南路', '西湖', '港墘', '文德', '內湖', '大湖公園', '葫洲', '東湖', '南港軟體園區', '南港展覽館_BR', '象山', '台北101/世貿', '信義安和', '大安_R', '大安森林公園', '東門_R', '中正紀念堂_R', '台大醫院', '台北車站_R', '中山_R', '雙連', '民權西路_R', '圓山', '劍潭', '士林', '芝山', '明德', '石牌', '唭哩岸', '奇岩', '北投', '新北投', '復興崗', '忠義', '關渡', '竹圍', '紅樹林', '淡水', '新店', '新店區公所', '七張', '大坪林_G', '景美', '萬隆', '公館', '台電大樓', '古亭_G', '中正紀念堂_G', '小南門', '西門_G', '北門', '中山_G', '松江南京_G', '南京復興_G', '台北小巨蛋', '南京三民', '松山', '南勢角', '景安_O', '永安市場', '頂溪', '古亭_O', '東門_O', '忠孝新生_O', '松江南京_O', '行天宮', '中山國小', '民權西路_O', '大橋頭', '台北橋', '菜寮', '三重', '先嗇宮', '頭前庄_O', '新莊', '輔大', '丹鳳', '迴龍', '三重國小', '三和國小', '徐匯中學', '三民高中', '蘆洲', '大坪林_Y', '十四張', '秀朗橋', '景平', '景安_Y', '中和', '橋和', '中原', '板新', '板橋_Y', '新埔民生', '頭前庄_Y', '幸福', '新北產業園區']
板南線 = ['南港展覽館_BL', '南港', '昆陽', '後山埤', '永春', '市政府', '國父紀念館', '忠孝敦化', '忠孝復興_BL', '忠孝新生_BL', '善導寺', '台北車站_BL', '西門_BL', '龍山寺', '江子翠', '新埔', '板橋_BL', '府中', '亞東醫院', '海山', '土城', '永寧', '頂埔']
文湖線 = ['動物園', '木柵', '萬芳社區', '萬芳醫院', '辛亥', '麟光', '六張犁', '科技大樓', '大安_BR', '忠孝復興_BR', '南京復興_BR', '中山國中', '松山機場', '大直', '劍南路', '西湖', '港墘', '文德', '內湖', '大湖公園', '葫洲', '東湖', '南港軟體園區', '南港展覽館_BR']
淡水信義線 = ['象山', '台北101/世貿', '信義安和', '大安_R', '大安森林公園', '東門_R', '中正紀念堂_R', '台大醫院', '台北車站_R', '中山_R', '雙連', '民權西路_R', '圓山', '劍潭', '士林', '芝山', '明德', '石牌', '唭哩岸', '奇岩', '北投', '新北投', '復興崗', '忠義', '關渡', '竹圍', '紅樹林', '淡水']
松山新店線 = ['新店', '新店區公所', '七張', '大坪林_G', '景美', '萬隆', '公館', '台電大樓', '古亭_G', '中正紀念堂_G', '小南門', '西門_G', '北門', '中山_G', '松江南京_G', '南京復興_G', '台北小巨蛋', '南京三民', '松山']
中和新蘆線 = ['南勢角', '景安_O', '永安市場', '頂溪', '古亭_O', '東門_O', '忠孝新生_O', '松江南京_O', '行天宮', '中山國小', '民權西路_O', '大橋頭', '台北橋', '菜寮', '三重', '先嗇宮', '頭前庄_O', '新莊', '輔大', '丹鳳', '迴龍', '三重國小', '三和國小', '徐匯中學', '三民高中', '蘆洲']
環狀線 = ['大坪林_Y', '十四張', '秀朗橋', '景平', '景安_Y', '中和', '橋和', '中原', '板新', '板橋_Y', '新埔民生', '頭前庄_Y', '幸福', '新北產業園區']

machine = TocMachine(
    states = states,
    transitions=[
        {"trigger": "choose_line","source": "user","dest": "板南線","conditions": "go_to_板南線",},
        {"trigger": "choose_line","source": "user","dest": "文湖線","conditions": "go_to_文湖線",},
        {"trigger": "choose_line","source": "user","dest": "淡水信義線","conditions": "go_to_淡水信義線",},
        {"trigger": "choose_line","source": "user","dest": "松山新店線","conditions": "go_to_松山新店線",},
        {"trigger": "choose_line","source": "user","dest": "中和新蘆線","conditions": "go_to_中和新蘆線",},
        {"trigger": "choose_line","source": "user","dest": "環狀線","conditions": "go_to_環狀線",},
        #轉乘站
        {"trigger": "板南線","source": "南港展覽館_BR","dest": "南港展覽館_BL",},
        {"trigger": "板南線","source": "忠孝復興_BR","dest": "忠孝復興_BL",},
        {"trigger": "板南線","source": "忠孝新生_O","dest": "忠孝新生_BL",},
        {"trigger": "板南線","source": "台北車站_R","dest": "台北車站_BL",},
        {"trigger": "板南線","source": "西門_G","dest": "西門_BL",},
        {"trigger": "板南線","source": "板橋_Y","dest": "板橋_BL",},
        {"trigger": "文湖線","source": "南港展覽館_BL","dest": "南港展覽館_BR",},
        {"trigger": "文湖線","source": "南京復興_G","dest": "南京復興_BR",},
        {"trigger": "文湖線","source": "忠孝復興_BL","dest": "忠孝復興_BR",},
        {"trigger": "文湖線","source": "大安_R","dest": "大安_BR",},
        {"trigger": "淡水信義線","source": "大安_BR","dest": "大安_R",},
        {"trigger": "淡水信義線","source": "東門_O","dest": "東門_R",},
        {"trigger": "淡水信義線","source": "中正紀念堂_G","dest": "中正紀念堂_R",},
        {"trigger": "淡水信義線","source": "台北車站_BL","dest": "台北車站_R",},
        {"trigger": "淡水信義線","source": "中山_G","dest": "中山_R",},
        {"trigger": "淡水信義線","source": "民權西路_O","dest": "民權西路_R",},
        {"trigger": "松山新店線","source": "大坪林_Y","dest": "大坪林_G",},
        {"trigger": "松山新店線","source": "古亭_O","dest": "古亭_G",},
        {"trigger": "松山新店線","source": "中正紀念堂_R","dest": "中正紀念堂_G",},
        {"trigger": "松山新店線","source": "西門_BL","dest": "西門_G",},
        {"trigger": "松山新店線","source": "中山_R","dest": "中山_G",},
        {"trigger": "松山新店線","source": "松江南京_O","dest": "松江南京_G",},
        {"trigger": "松山新店線","source": "南京復興_BR","dest": "南京復興_G",},
        {"trigger": "中和新蘆線","source": "景安_Y","dest": "景安_O",},
        {"trigger": "中和新蘆線","source": "古亭_G","dest": "古亭_O",},
        {"trigger": "中和新蘆線","source": "東門_R","dest": "東門_O",},
        {"trigger": "中和新蘆線","source": "忠孝新生_BL","dest": "忠孝新生_O",},
        {"trigger": "中和新蘆線","source": "松江南京_G","dest": "松江南京_O",},
        {"trigger": "中和新蘆線","source": "民權西路_R","dest": "民權西路_O",},
        {"trigger": "中和新蘆線","source": "頭前庄_Y","dest": "頭前庄_O",},
        {"trigger": "環狀線","source": "大坪林_G","dest": "大坪林_Y",},
        {"trigger": "環狀線","source": "景安_O","dest": "景安_Y",},
        {"trigger": "環狀線","source": "板橋_BL","dest": "板橋_Y",},
        {"trigger": "環狀線","source": "頭前庄_O","dest": "頭前庄_Y",},
        {"trigger": "往三重國小","source": "大橋頭","dest": "三重國小",},
        {"trigger": "往台北橋","source": "大橋頭","dest": "台北橋",},
        
        #板南線
        {"trigger": "choose_station","source": "板南線","dest": "南港展覽館_BL","conditions": "南港展覽館_BL",},
        {"trigger": "choose_station","source": "板南線","dest": "南港","conditions": "南港",},
        {"trigger": "choose_station","source": "板南線","dest": "昆陽","conditions": "昆陽",},
        {"trigger": "choose_station","source": "板南線","dest": "後山埤","conditions": "後山埤",},
        {"trigger": "choose_station","source": "板南線","dest": "永春","conditions": "永春",},
        {"trigger": "choose_station","source": "板南線","dest": "市政府","conditions": "市政府",},
        {"trigger": "choose_station","source": "板南線","dest": "國父紀念館","conditions": "國父紀念館",},
        {"trigger": "choose_station","source": "板南線","dest": "忠孝敦化","conditions": "忠孝敦化",},
        {"trigger": "choose_station","source": "板南線","dest": "忠孝復興_BL","conditions": "忠孝復興_BL",},
        {"trigger": "choose_station","source": "板南線","dest": "忠孝新生_BL","conditions": "忠孝新生_BL",},
        {"trigger": "choose_station","source": "板南線","dest": "善導寺","conditions": "善導寺",},
        {"trigger": "choose_station","source": "板南線","dest": "台北車站_BL","conditions": "台北車站_BL",},
        {"trigger": "choose_station","source": "板南線","dest": "西門_BL","conditions": "西門_BL",},
        {"trigger": "choose_station","source": "板南線","dest": "龍山寺","conditions": "龍山寺",},
        {"trigger": "choose_station","source": "板南線","dest": "江子翠","conditions": "江子翠",},
        {"trigger": "choose_station","source": "板南線","dest": "新埔","conditions": "新埔",},
        {"trigger": "choose_station","source": "板南線","dest": "板橋_BL","conditions": "板橋_BL",},
        {"trigger": "choose_station","source": "板南線","dest": "府中","conditions": "府中",},
        {"trigger": "choose_station","source": "板南線","dest": "亞東醫院","conditions": "亞東醫院",},
        {"trigger": "choose_station","source": "板南線","dest": "海山","conditions": "海山",},
        {"trigger": "choose_station","source": "板南線","dest": "土城","conditions": "土城",},
        {"trigger": "choose_station","source": "板南線","dest": "永寧","conditions": "永寧",},
        {"trigger": "choose_station","source": "板南線","dest": "頂埔","conditions": "頂埔",},
        #板南線toward
        {"trigger": "toward","source": "南港","dest": "南港展覽館_BL",},
        {"trigger": "toward","source": "昆陽","dest": "南港",},
        {"trigger": "toward","source": "後山埤","dest": "昆陽",},
        {"trigger": "toward","source": "永春","dest": "後山埤",},
        {"trigger": "toward","source": "市政府","dest": "永春",},
        {"trigger": "toward","source": "國父紀念館","dest": "市政府",},
        {"trigger": "toward","source": "忠孝敦化","dest": "國父紀念館"},
        {"trigger": "toward","source": "忠孝復興_BL","dest": "忠孝敦化",},
        {"trigger": "toward","source": "忠孝新生_BL","dest": "忠孝復興_BL",},
        {"trigger": "toward","source": "善導寺","dest": "忠孝新生_BL",},
        {"trigger": "toward","source": "台北車站_BL","dest": "善導寺",},
        {"trigger": "toward","source": "西門_BL","dest": "台北車站_BL",},
        {"trigger": "toward","source": "龍山寺","dest": "西門_BL",},
        {"trigger": "toward","source": "江子翠","dest": "龍山寺",},
        {"trigger": "toward","source": "新埔","dest": "江子翠",},
        {"trigger": "toward","source": "板橋_BL","dest": "新埔",},
        {"trigger": "toward","source": "府中","dest": "板橋_BL",},
        {"trigger": "toward","source": "亞東醫院","dest": "府中",},
        {"trigger": "toward","source": "海山","dest": "亞東醫院",},
        {"trigger": "toward","source": "土城","dest": "海山",},
        {"trigger": "toward","source": "永寧","dest": "土城",},
        {"trigger": "toward","source": "頂埔","dest": "永寧",},
        #板南線backward
        {"trigger": "backward","source": "南港展覽館_BL","dest": "南港",},
        {"trigger": "backward","source": "南港","dest": "昆陽",},
        {"trigger": "backward","source": "昆陽","dest": "後山埤",},
        {"trigger": "backward","source": "後山埤","dest": "永春",},
        {"trigger": "backward","source": "永春","dest": "市政府",},
        {"trigger": "backward","source": "市政府","dest": "國父紀念館",},
        {"trigger": "backward","source": "國父紀念館","dest": "忠孝敦化",},
        {"trigger": "backward","source": "忠孝敦化","dest": "忠孝復興_BL"},
        {"trigger": "backward","source": "忠孝復興_BL","dest": "忠孝新生_BL",},
        {"trigger": "backward","source": "忠孝新生_BL","dest": "善導寺",},
        {"trigger": "backward","source": "善導寺","dest": "台北車站_BL",},
        {"trigger": "backward","source": "台北車站_BL","dest": "西門_BL",},
        {"trigger": "backward","source": "西門_BL","dest": "龍山寺",},
        {"trigger": "backward","source": "龍山寺","dest": "江子翠",},
        {"trigger": "backward","source": "江子翠","dest": "新埔",},
        {"trigger": "backward","source": "新埔","dest": "板橋_BL",},
        {"trigger": "backward","source": "板橋_BL","dest": "府中",},
        {"trigger": "backward","source": "府中","dest": "亞東醫院",},
        {"trigger": "backward","source": "亞東醫院","dest": "海山",},
        {"trigger": "backward","source": "海山","dest": "土城",},
        {"trigger": "backward","source": "土城","dest": "永寧",},
        {"trigger": "backward","source": "永寧","dest": "頂埔",},
        
        #文湖線
        {"trigger": "choose_station","source": "文湖線","dest": "動物園",             "conditions": "動物園",},
        {"trigger": "choose_station","source": "文湖線","dest": "木柵",               "conditions": "木柵",},
        {"trigger": "choose_station","source": "文湖線","dest": "萬芳社區",           "conditions": "萬芳社區",},
        {"trigger": "choose_station","source": "文湖線","dest": "萬芳醫院",           "conditions": "萬芳醫院",},
        {"trigger": "choose_station","source": "文湖線","dest": "辛亥",               "conditions": "辛亥",},
        {"trigger": "choose_station","source": "文湖線","dest": "麟光",               "conditions": "麟光",},
        {"trigger": "choose_station","source": "文湖線","dest": "六張犁",             "conditions": "六張犁",},
        {"trigger": "choose_station","source": "文湖線","dest": "科技大樓",           "conditions": "科技大樓",},
        {"trigger": "choose_station","source": "文湖線","dest": "大安_BR",            "conditions": "大安_BR",},
        {"trigger": "choose_station","source": "文湖線","dest": "忠孝復興_BR",        "conditions": "忠孝復興_BR",},
        {"trigger": "choose_station","source": "文湖線","dest": "南京復興_BR",        "conditions": "南京復興_BR",},
        {"trigger": "choose_station","source": "文湖線","dest": "中山國中",           "conditions": "中山國中",},
        {"trigger": "choose_station","source": "文湖線","dest": "松山機場",           "conditions": "松山機場",},
        {"trigger": "choose_station","source": "文湖線","dest": "大直",               "conditions": "大直",},
        {"trigger": "choose_station","source": "文湖線","dest": "劍南路",             "conditions": "劍南路",},
        {"trigger": "choose_station","source": "文湖線","dest": "西湖",               "conditions": "西湖",},
        {"trigger": "choose_station","source": "文湖線","dest": "港墘",               "conditions": "港墘",},
        {"trigger": "choose_station","source": "文湖線","dest": "文德",               "conditions": "文德",},
        {"trigger": "choose_station","source": "文湖線","dest": "內湖",               "conditions": "內湖",},
        {"trigger": "choose_station","source": "文湖線","dest": "大湖公園",           "conditions": "大湖公園",},
        {"trigger": "choose_station","source": "文湖線","dest": "葫洲",               "conditions": "葫洲",},
        {"trigger": "choose_station","source": "文湖線","dest": "東湖",               "conditions": "東湖",},
        {"trigger": "choose_station","source": "文湖線","dest": "南港軟體園區",        "conditions": "南港軟體園區",},
        {"trigger": "choose_station","source": "文湖線","dest": "南港展覽館_BR",       "conditions": "南港展覽館_BR",},
        #文湖線 toward
        {"trigger": "toward","source": "動物園",             "dest": "木柵",},
        {"trigger": "toward","source": "木柵",               "dest": "萬芳社區",},
        {"trigger": "toward","source": "萬芳社區",           "dest": "萬芳醫院",},
        {"trigger": "toward","source": "萬芳醫院",           "dest": "辛亥",},
        {"trigger": "toward","source": "辛亥",               "dest": "麟光",},
        {"trigger": "toward","source": "麟光",               "dest": "六張犁",},
        {"trigger": "toward","source": "六張犁",             "dest": "科技大樓"},
        {"trigger": "toward","source": "科技大樓",           "dest": "大安_BR",},
        {"trigger": "toward","source": "大安_BR",            "dest": "忠孝復興_BR",},
        {"trigger": "toward","source": "忠孝復興_BR",        "dest": "南京復興_BR",},
        {"trigger": "toward","source": "南京復興_BR",        "dest": "中山國中",},
        {"trigger": "toward","source": "中山國中",           "dest": "松山機場",},
        {"trigger": "toward","source": "松山機場",           "dest": "大直",},
        {"trigger": "toward","source": "大直",               "dest": "劍南路",},
        {"trigger": "toward","source": "劍南路",             "dest": "西湖",},
        {"trigger": "toward","source": "西湖",               "dest": "港墘",},
        {"trigger": "toward","source": "港墘",               "dest": "文德",},
        {"trigger": "toward","source": "文德",               "dest": "內湖",},
        {"trigger": "toward","source": "內湖",               "dest": "大湖公園",},
        {"trigger": "toward","source": "大湖公園",           "dest": "葫洲",},
        {"trigger": "toward","source": "葫洲",               "dest": "東湖",},
        {"trigger": "toward","source": "東湖",               "dest": "南港軟體園區",},
        {"trigger": "toward","source": "南港軟體園區",        "dest": "南港展覽館_BR",},
        #文湖線 backward
        {"trigger": "backward","source": "木柵",               "dest": "動物園",      },
        {"trigger": "backward","source": "萬芳社區",           "dest": "木柵",        },
        {"trigger": "backward","source": "萬芳醫院",           "dest": "萬芳社區",    },
        {"trigger": "backward","source": "辛亥",               "dest": "萬芳醫院",    },
        {"trigger": "backward","source": "麟光",               "dest": "辛亥",        },
        {"trigger": "backward","source": "六張犁",             "dest": "麟光",        },
        {"trigger": "backward","source": "科技大樓",           "dest": "六張犁",      },
        {"trigger": "backward","source": "大安_BR",            "dest": "科技大樓",    },
        {"trigger": "backward","source": "忠孝復興_BR",        "dest": "大安_BR",     },
        {"trigger": "backward","source": "南京復興_BR",        "dest": "忠孝復興_BR", },
        {"trigger": "backward","source": "中山國中",           "dest": "南京復興_BR", },
        {"trigger": "backward","source": "松山機場",           "dest": "中山國中",    },
        {"trigger": "backward","source": "大直",               "dest": "松山機場",    },
        {"trigger": "backward","source": "劍南路",             "dest": "大直",        },
        {"trigger": "backward","source": "西湖",               "dest": "劍南路",      },
        {"trigger": "backward","source": "港墘",               "dest": "西湖",        },
        {"trigger": "backward","source": "文德",               "dest": "港墘",        },
        {"trigger": "backward","source": "內湖",               "dest": "文德",        },
        {"trigger": "backward","source": "大湖公園",           "dest": "內湖",        },
        {"trigger": "backward","source": "葫洲",               "dest": "大湖公園",    },
        {"trigger": "backward","source": "東湖",               "dest": "葫洲",        },
        {"trigger": "backward","source": "南港軟體園區",        "dest":"東湖",        },
        {"trigger": "backward","source": "南港展覽館_BR",       "dest": "南港軟體園區",},
        
        #淡水信義線
        {"trigger": "choose_station","source": "淡水信義線","dest": "象山",         "conditions": "象山",         },
        {"trigger": "choose_station","source": "淡水信義線","dest": "台北101/世貿", "conditions": "台北101", },
        {"trigger": "choose_station","source": "淡水信義線","dest": "信義安和",     "conditions": "信義安和",     },
        {"trigger": "choose_station","source": "淡水信義線","dest": "大安_R",       "conditions": "大安_R",         },
        {"trigger": "choose_station","source": "淡水信義線","dest": "大安森林公園", "conditions": "大安森林公園", },
        {"trigger": "choose_station","source": "淡水信義線","dest": "東門_R",       "conditions": "東門_R",         },
        {"trigger": "choose_station","source": "淡水信義線","dest": "中正紀念堂_R", "conditions": "中正紀念堂_R", },
        {"trigger": "choose_station","source": "淡水信義線","dest": "台大醫院",     "conditions": "台大醫院",     },
        {"trigger": "choose_station","source": "淡水信義線","dest": "台北車站_R",   "conditions": "台北車站_R",   },
        {"trigger": "choose_station","source": "淡水信義線","dest": "中山_R",       "conditions": "中山_R",       },
        {"trigger": "choose_station","source": "淡水信義線","dest": "雙連",         "conditions": "雙連",         },
        {"trigger": "choose_station","source": "淡水信義線","dest": "民權西路_R",   "conditions": "民權西路_R",   },
        {"trigger": "choose_station","source": "淡水信義線","dest": "圓山",         "conditions": "圓山",         },
        {"trigger": "choose_station","source": "淡水信義線","dest": "劍潭",         "conditions": "劍潭",         },
        {"trigger": "choose_station","source": "淡水信義線","dest": "士林",         "conditions": "士林",         },
        {"trigger": "choose_station","source": "淡水信義線","dest": "芝山",         "conditions": "芝山",         },
        {"trigger": "choose_station","source": "淡水信義線","dest": "明德",         "conditions": "明德",         },
        {"trigger": "choose_station","source": "淡水信義線","dest": "石牌",         "conditions": "石牌",         },
        {"trigger": "choose_station","source": "淡水信義線","dest": "唭哩岸",       "conditions": "唭哩岸",       },
        {"trigger": "choose_station","source": "淡水信義線","dest": "奇岩",         "conditions": "奇岩",         },
        {"trigger": "choose_station","source": "淡水信義線","dest": "北投",         "conditions": "北投",         },
        {"trigger": "choose_station","source": "淡水信義線","dest": "新北投",       "conditions": "新北投",       },
        {"trigger": "choose_station","source": "淡水信義線","dest": "復興崗",       "conditions": "復興崗",       },
        {"trigger": "choose_station","source": "淡水信義線","dest": "忠義",         "conditions": "忠義",         },
        {"trigger": "choose_station","source": "淡水信義線","dest": "關渡",         "conditions": "關渡",         },
        {"trigger": "choose_station","source": "淡水信義線","dest": "竹圍",         "conditions": "竹圍",         },
        {"trigger": "choose_station","source": "淡水信義線","dest": "紅樹林",       "conditions": "紅樹林",       },
        {"trigger": "choose_station","source": "淡水信義線","dest": "淡水",         "conditions": "淡水",         },
        #淡水信義線 toward
        {"trigger": "toward","source": "象山",         "dest": "台北101/世貿", },
        {"trigger": "toward","source": "台北101/世貿", "dest": "信義安和",     },
        {"trigger": "toward","source": "信義安和",     "dest": "大安_R",       },
        {"trigger": "toward","source": "大安_R",       "dest": "大安森林公園", },
        {"trigger": "toward","source": "大安森林公園", "dest": "東門_R",       },
        {"trigger": "toward","source": "東門_R",       "dest": "中正紀念堂_R", },
        {"trigger": "toward","source": "中正紀念堂_R", "dest": "台大醫院",     },
        {"trigger": "toward","source": "台大醫院",     "dest": "台北車站_R",   },
        {"trigger": "toward","source": "台北車站_R",   "dest": "中山_R",       },
        {"trigger": "toward","source": "中山_R",       "dest": "雙連",         },
        {"trigger": "toward","source": "雙連",         "dest": "民權西路_R",   },
        {"trigger": "toward","source": "民權西路_R",   "dest": "圓山",         },
        {"trigger": "toward","source": "圓山",         "dest": "劍潭",         },
        {"trigger": "toward","source": "劍潭",         "dest": "士林",         },
        {"trigger": "toward","source": "士林",         "dest": "芝山",         },
        {"trigger": "toward","source": "芝山",         "dest": "明德",         },
        {"trigger": "toward","source": "明德",         "dest": "石牌",         },
        {"trigger": "toward","source": "石牌",         "dest": "唭哩岸",       },
        {"trigger": "toward","source": "唭哩岸",       "dest": "奇岩",         },
        {"trigger": "toward","source": "奇岩",         "dest": "北投",         },
        {"trigger": "toward","source": "北投",         "dest": "新北投",       },
        {"trigger": "toward","source": "新北投",       "dest": "復興崗",       },
        {"trigger": "toward","source": "復興崗",       "dest": "忠義",         },
        {"trigger": "toward","source": "忠義",         "dest": "關渡",         },
        {"trigger": "toward","source": "關渡",         "dest": "竹圍",         },
        {"trigger": "toward","source": "竹圍",         "dest": "紅樹林",       },
        {"trigger": "toward","source": "紅樹林",       "dest": "淡水",         },
        #淡水信義線 backward
        {"trigger": "backward","source": "台北101/世貿", "dest": "象山",         },
        {"trigger": "backward","source": "信義安和",     "dest": "台北101/世貿", },
        {"trigger": "backward","source": "大安_R",       "dest": "信義安和",     },
        {"trigger": "backward","source": "大安森林公園", "dest": "大安_R",       },
        {"trigger": "backward","source": "東門_R",       "dest": "大安森林公園", },
        {"trigger": "backward","source": "中正紀念堂_R", "dest": "東門_R",       },
        {"trigger": "backward","source": "台大醫院",     "dest": "中正紀念堂_R", },
        {"trigger": "backward","source": "台北車站_R",   "dest": "台大醫院",     },
        {"trigger": "backward","source": "中山_R",       "dest": "台北車站_R",   },
        {"trigger": "backward","source": "雙連",         "dest": "中山_R",       },
        {"trigger": "backward","source": "民權西路_R",   "dest": "雙連",         },
        {"trigger": "backward","source": "圓山",         "dest": "民權西路_R",   },
        {"trigger": "backward","source": "劍潭",         "dest": "圓山",         },
        {"trigger": "backward","source": "士林",         "dest": "劍潭",         },
        {"trigger": "backward","source": "芝山",         "dest": "士林",         },
        {"trigger": "backward","source": "明德",         "dest": "芝山",         },
        {"trigger": "backward","source": "石牌",         "dest": "明德",         },
        {"trigger": "backward","source": "唭哩岸",       "dest": "石牌",         },
        {"trigger": "backward","source": "奇岩",         "dest": "唭哩岸",       },
        {"trigger": "backward","source": "北投",         "dest": "奇岩",         },
        {"trigger": "backward","source": "新北投",       "dest": "北投",         },
        {"trigger": "backward","source": "復興崗",       "dest": "新北投",       },
        {"trigger": "backward","source": "忠義",         "dest": "復興崗",       },
        {"trigger": "backward","source": "關渡",         "dest": "忠義",         },
        {"trigger": "backward","source": "竹圍",         "dest": "關渡",         },
        {"trigger": "backward","source": "紅樹林",       "dest": "竹圍",         },
        {"trigger": "backward","source": "淡水",         "dest": "紅樹林",       },
        
        #松山新店線
        {"trigger": "choose_station","source": "松山新店線","dest": "新店",             "conditions": "新店",             },
        {"trigger": "choose_station","source": "松山新店線","dest": "新店區公所",       "conditions": "新店區公所",       },
        {"trigger": "choose_station","source": "松山新店線","dest": "七張",             "conditions": "七張",             },
        {"trigger": "choose_station","source": "松山新店線","dest": "大坪林_G",         "conditions": "大坪林_G",         },
        {"trigger": "choose_station","source": "松山新店線","dest": "景美",             "conditions": "景美",             },
        {"trigger": "choose_station","source": "松山新店線","dest": "萬隆",             "conditions": "萬隆",             },
        {"trigger": "choose_station","source": "松山新店線","dest": "公館",             "conditions": "公館",             },
        {"trigger": "choose_station","source": "松山新店線","dest": "台電大樓",         "conditions": "台電大樓",         },
        {"trigger": "choose_station","source": "松山新店線","dest": "古亭_G",           "conditions": "古亭_G",           },
        {"trigger": "choose_station","source": "松山新店線","dest": "中正紀念堂_G",     "conditions": "中正紀念堂_G",     },
        {"trigger": "choose_station","source": "松山新店線","dest": "小南門",           "conditions": "小南門",           },
        {"trigger": "choose_station","source": "松山新店線","dest": "西門_G",           "conditions": "西門_G",           },
        {"trigger": "choose_station","source": "松山新店線","dest": "北門",             "conditions": "北門",             },
        {"trigger": "choose_station","source": "松山新店線","dest": "中山_G",           "conditions": "中山_G",           },
        {"trigger": "choose_station","source": "松山新店線","dest": "松江南京_G",       "conditions": "松江南京_G",       },
        {"trigger": "choose_station","source": "松山新店線","dest": "南京復興_G",       "conditions": "南京復興_G",       },
        {"trigger": "choose_station","source": "松山新店線","dest": "台北小巨蛋",       "conditions": "台北小巨蛋",       },
        {"trigger": "choose_station","source": "松山新店線","dest": "南京三民",         "conditions": "南京三民",         },
        {"trigger": "choose_station","source": "松山新店線","dest": "松山",             "conditions": "松山",             },
        #松山新店線 toward
        {"trigger": "toward","source": "新店",             "dest": "新店區公所",       },
        {"trigger": "toward","source": "新店區公所",       "dest": "七張",             },
        {"trigger": "toward","source": "七張",             "dest": "大坪林_G",         },
        {"trigger": "toward","source": "大坪林_G",         "dest": "景美",             },
        {"trigger": "toward","source": "景美",             "dest": "萬隆",             },
        {"trigger": "toward","source": "萬隆",             "dest": "公館",             },
        {"trigger": "toward","source": "公館",             "dest": "台電大樓",         },
        {"trigger": "toward","source": "台電大樓",         "dest": "古亭_G",           },
        {"trigger": "toward","source": "古亭_G",           "dest": "中正紀念堂_G",     },
        {"trigger": "toward","source": "中正紀念堂_G",     "dest": "小南門",           },
        {"trigger": "toward","source": "小南門",           "dest": "西門_G",           },
        {"trigger": "toward","source": "西門_G",           "dest": "北門",             },
        {"trigger": "toward","source": "北門",             "dest": "中山_G",           },
        {"trigger": "toward","source": "中山_G",           "dest": "松江南京_G",       },
        {"trigger": "toward","source": "松江南京_G",       "dest": "南京復興_G",       },
        {"trigger": "toward","source": "南京復興_G",       "dest": "台北小巨蛋",       },
        {"trigger": "toward","source": "台北小巨蛋",       "dest": "南京三民",         },
        {"trigger": "toward","source": "南京三民",         "dest": "松山",             },
        #松山新店線 backward
        {"trigger": "backward","source": "新店區公所",       "dest": "新店",             },
        {"trigger": "backward","source": "七張",             "dest": "新店區公所",       },
        {"trigger": "backward","source": "大坪林_G",         "dest": "七張",             },
        {"trigger": "backward","source": "景美",             "dest": "大坪林_G",         },
        {"trigger": "backward","source": "萬隆",             "dest": "景美",             },
        {"trigger": "backward","source": "公館",             "dest": "萬隆",             },
        {"trigger": "backward","source": "台電大樓",         "dest": "公館",             },
        {"trigger": "backward","source": "古亭_G",           "dest": "台電大樓",         },
        {"trigger": "backward","source": "中正紀念堂_G",     "dest": "古亭_G",           },
        {"trigger": "backward","source": "小南門",           "dest": "中正紀念堂_G",     },
        {"trigger": "backward","source": "西門_G",           "dest": "小南門",           },
        {"trigger": "backward","source": "北門",             "dest": "西門_G",           },
        {"trigger": "backward","source": "中山_G",           "dest": "北門",             },
        {"trigger": "backward","source": "松江南京_G",       "dest": "中山_G",           },
        {"trigger": "backward","source": "南京復興_G",       "dest": "松江南京_G",       },
        {"trigger": "backward","source": "台北小巨蛋",       "dest": "南京復興_G",       },
        {"trigger": "backward","source": "南京三民",         "dest": "台北小巨蛋",       },
        {"trigger": "backward","source": "松山",             "dest": "南京三民",         },
        
        #中和新蘆線
        {"trigger": "choose_station","source": "中和新蘆線","dest": "南勢角",             "conditions": "南勢角",             },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "景安_O",             "conditions": "景安_O",             },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "永安市場",           "conditions": "永安市場",           },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "頂溪",               "conditions": "頂溪",               },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "古亭_O",             "conditions": "古亭_O",             },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "東門_O",             "conditions": "東門_O",             },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "忠孝新生_O",         "conditions": "忠孝新生_O",         },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "松江南京_O",         "conditions": "松江南京_O",         },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "行天宮",             "conditions": "行天宮",             },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "中山國小",           "conditions": "中山國小",           },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "民權西路_O",         "conditions": "民權西路_O",         },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "大橋頭",             "conditions": "大橋頭",             },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "台北橋",             "conditions": "台北橋",             },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "菜寮",               "conditions": "菜寮",               },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "三重",               "conditions": "三重",               },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "先嗇宮",             "conditions": "先嗇宮",             },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "頭前庄_O",           "conditions": "頭前庄_O",           },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "新莊",               "conditions": "新莊",               },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "輔大",               "conditions": "輔大",               },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "丹鳳",               "conditions": "丹鳳",               },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "迴龍",               "conditions": "迴龍",               },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "三重國小",           "conditions": "三重國小",           },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "三和國小",           "conditions": "三和國小",           },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "徐匯中學",           "conditions": "徐匯中學",           },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "三民高中",           "conditions": "三民高中",           },
        {"trigger": "choose_station","source": "中和新蘆線","dest": "蘆洲",               "conditions": "蘆洲",               },
        #中和新蘆線 toward
        {"trigger": "toward","source": "南勢角",             "dest": "景安_O",             },
        {"trigger": "toward","source": "景安_O",             "dest": "永安市場",           },
        {"trigger": "toward","source": "永安市場",           "dest": "頂溪",               },
        {"trigger": "toward","source": "頂溪",               "dest": "古亭_O",             },
        {"trigger": "toward","source": "古亭_O",             "dest": "東門_O",             },
        {"trigger": "toward","source": "東門_O",             "dest": "忠孝新生_O",         },
        {"trigger": "toward","source": "忠孝新生_O",         "dest": "松江南京_O",         },
        {"trigger": "toward","source": "松江南京_O",         "dest": "行天宮",             },
        {"trigger": "toward","source": "行天宮",             "dest": "中山國小",           },
        {"trigger": "toward","source": "中山國小",           "dest": "民權西路_O",         },
        {"trigger": "toward","source": "民權西路_O",         "dest": "大橋頭",             },#
        {"trigger": "toward","source": "台北橋",             "dest": "菜寮",               },
        {"trigger": "toward","source": "菜寮",               "dest": "三重",               },
        {"trigger": "toward","source": "三重",               "dest": "先嗇宮",             },
        {"trigger": "toward","source": "先嗇宮",             "dest": "頭前庄_O",           },
        {"trigger": "toward","source": "頭前庄_O",           "dest": "新莊",               },
        {"trigger": "toward","source": "新莊",               "dest": "輔大",               },
        {"trigger": "toward","source": "輔大",               "dest": "丹鳳",               },
        {"trigger": "toward","source": "丹鳳",               "dest": "迴龍",               },#
        {"trigger": "toward","source": "三重國小",           "dest": "三和國小",           },
        {"trigger": "toward","source": "三和國小",           "dest": "徐匯中學",           },
        {"trigger": "toward","source": "徐匯中學",           "dest": "三民高中",           },
        {"trigger": "toward","source": "三民高中",           "dest": "蘆洲",               },
        #中和新蘆線 backward
        {"trigger": "backward","source": "景安_O",             "dest": "南勢角",             },
        {"trigger": "backward","source": "永安市場",           "dest": "景安_O",             },
        {"trigger": "backward","source": "頂溪",               "dest": "永安市場",           },
        {"trigger": "backward","source": "古亭_O",             "dest": "頂溪",               },
        {"trigger": "backward","source": "東門_O",             "dest": "古亭_O",             },
        {"trigger": "backward","source": "忠孝新生_O",         "dest": "東門_O",             },
        {"trigger": "backward","source": "松江南京_O",         "dest": "忠孝新生_O",         },
        {"trigger": "backward","source": "行天宮",             "dest": "松江南京_O",         },
        {"trigger": "backward","source": "中山國小",           "dest": "行天宮",             },
        {"trigger": "backward","source": "民權西路_O",         "dest": "中山國小",           },
        {"trigger": "backward","source": "大橋頭",             "dest": "民權西路_O",         },
        {"trigger": "backward","source": "台北橋",             "dest": "大橋頭",             },
        {"trigger": "backward","source": "菜寮",               "dest": "台北橋",             },
        {"trigger": "backward","source": "三重",               "dest": "菜寮",               },
        {"trigger": "backward","source": "先嗇宮",             "dest": "三重",               },
        {"trigger": "backward","source": "頭前庄_O",           "dest": "先嗇宮",             },
        {"trigger": "backward","source": "新莊",               "dest": "頭前庄_O",           },
        {"trigger": "backward","source": "輔大",               "dest": "新莊",               },
        {"trigger": "backward","source": "丹鳳",               "dest": "輔大",               },
        {"trigger": "backward","source": "迴龍",               "dest": "丹鳳",               },
        {"trigger": "backward","source": "三重國小",           "dest": "大橋頭",               },
        {"trigger": "backward","source": "三和國小",           "dest": "三重國小",           },
        {"trigger": "backward","source": "徐匯中學",           "dest": "三和國小",           },
        {"trigger": "backward","source": "三民高中",           "dest": "徐匯中學",           },
        {"trigger": "backward","source": "蘆洲",               "dest": "三民高中",           },
        
        #環狀線
        {"trigger": "choose_station","source": "環狀線","dest": "大坪林_Y",         "conditions": "大坪林_Y",        },
        {"trigger": "choose_station","source": "環狀線","dest": "十四張",           "conditions": "十四張",          },
        {"trigger": "choose_station","source": "環狀線","dest": "秀朗橋",           "conditions": "秀朗橋",          },
        {"trigger": "choose_station","source": "環狀線","dest": "景平",             "conditions": "景平",            },
        {"trigger": "choose_station","source": "環狀線","dest": "景安_Y",           "conditions": "景安_Y",          },
        {"trigger": "choose_station","source": "環狀線","dest": "中和",             "conditions": "中和",            },
        {"trigger": "choose_station","source": "環狀線","dest": "橋和",             "conditions": "橋和",            },
        {"trigger": "choose_station","source": "環狀線","dest": "中原",             "conditions": "中原",            },
        {"trigger": "choose_station","source": "環狀線","dest": "板新",             "conditions": "板新",            },
        {"trigger": "choose_station","source": "環狀線","dest": "板橋_Y",           "conditions": "板橋_Y",          },
        {"trigger": "choose_station","source": "環狀線","dest": "新埔民生",         "conditions": "新埔民生",        },
        {"trigger": "choose_station","source": "環狀線","dest": "頭前庄_Y",         "conditions": "頭前庄_Y",        },
        {"trigger": "choose_station","source": "環狀線","dest": "幸福",             "conditions": "幸福",            },
        {"trigger": "choose_station","source": "環狀線","dest": "新北產業園區",     "conditions": "新北產業園區",    },
        #環狀線 toward
        {"trigger": "toward","source": "大坪林_Y",         "dest": "十四張",           },
        {"trigger": "toward","source": "十四張",           "dest": "秀朗橋",           },
        {"trigger": "toward","source": "秀朗橋",           "dest": "景平",             },
        {"trigger": "toward","source": "景平",             "dest": "景安_Y",           },
        {"trigger": "toward","source": "景安_Y",           "dest": "中和",             },
        {"trigger": "toward","source": "中和",             "dest": "橋和",             },
        {"trigger": "toward","source": "橋和",             "dest": "中原",             },
        {"trigger": "toward","source": "中原",             "dest": "板新",             },
        {"trigger": "toward","source": "板新",             "dest": "板橋_Y",           },
        {"trigger": "toward","source": "板橋_Y",           "dest": "新埔民生",         },
        {"trigger": "toward","source": "新埔民生",         "dest": "頭前庄_Y",         },
        {"trigger": "toward","source": "頭前庄_Y",         "dest": "幸福",             },
        {"trigger": "toward","source": "幸福",             "dest": "新北產業園區",     },
        #環狀線 backward
        {"trigger": "backward","source": "十四張",           "dest": "大坪林_Y",         },
        {"trigger": "backward","source": "秀朗橋",           "dest": "十四張",           },
        {"trigger": "backward","source": "景平",             "dest": "秀朗橋",           },
        {"trigger": "backward","source": "景安_Y",           "dest": "景平",             },
        {"trigger": "backward","source": "中和",             "dest": "景安_Y",           },
        {"trigger": "backward","source": "橋和",             "dest": "中和",             },
        {"trigger": "backward","source": "中原",             "dest": "橋和",             },
        {"trigger": "backward","source": "板新",             "dest": "中原",             },
        {"trigger": "backward","source": "板橋_Y",           "dest": "板新",             },
        {"trigger": "backward","source": "新埔民生",         "dest": "板橋_Y",           },
        {"trigger": "backward","source": "頭前庄_Y",         "dest": "新埔民生",         },
        {"trigger": "backward","source": "幸福",             "dest": "頭前庄_Y",         },
        {"trigger": "backward","source": "新北產業園區",     "dest": "幸福",             },
        
        {   
            "trigger": "home", 
            "source": ["南港展覽館_BL", '文湖線', '淡水信義線', '松山新店線', '中和新蘆線', '板南線', '環狀線', '南港', '昆陽', '後山埤', '永春', '市政府', '國父紀念館', '忠孝敦化', '忠孝復興_BL', '忠孝新生_BL', '善導寺', '台北車站_BL', '西門_BL', '龍山寺', '江子翠', '新埔', '板橋_BL', '府中', '亞東醫院', '海山', '土城', '永寧', '頂埔', '動物園', '木柵', '萬芳社區', '萬芳醫院', '辛亥', '麟光', '六張犁', '科技大樓', '大安_BR', '忠孝復興_BR', '南京復興_BR', '中山國中', '松山機場', '大直', '劍南路', '西湖', '港墘', '文德', '內湖', '大湖公園', '葫洲', '東湖', '南港軟體園區', '南港展覽館_BR', '象山', '台北101/世貿', '信義安和', '大安_R', '大安森林公園', '東門_R', '中正紀念堂_R', '台大醫院', '台北車站_R', '中山_R', '雙連', '民權西路_R', '圓山', '劍潭', '士林', '芝山', '明德', '石牌', '唭哩岸', '奇岩', '北投', '新北投', '復興崗', '忠義', '關渡', '竹圍', '紅樹林', '淡水', '新店', '新店區公所', '七張', '大坪林_G', '景美', '萬隆', '公館', '台電大樓', '古亭_G', '中正紀念堂_G', '小南門', '西門_G', '北門', '中山_G', '松江南京_G', '南京復興_G', '台北小巨蛋', '南京三民', '松山', '南勢角', '景安_O', '永安市場', '頂溪', '古亭_O', '東門_O', '忠孝新生_O', '松江南京_O', '行天宮', '中山國小', '民權西路_O', '大橋頭', '台北橋', '菜寮', '三重', '先嗇宮', '頭前庄_O', '新莊', '輔大', '丹鳳', '迴龍', '三重國小', '三和國小', '徐匯中學', '三民高中', '蘆洲', '大坪林_Y', '十四張', '秀朗橋', '景平', '景安_Y', '中和', '橋和', '中原', '板新', '板橋_Y', '新埔民生', '頭前庄_Y', '幸福', '新北產業園區'], 
            "dest": "user",
            "conditions": "back_to_user",
        },
        {   
            "trigger": "home_postback", 
            "source": ["南港展覽館_BL", '文湖線', '淡水信義線', '松山新店線', '中和新蘆線', '板南線', '環狀線', '南港', '昆陽', '後山埤', '永春', '市政府', '國父紀念館', '忠孝敦化', '忠孝復興_BL', '忠孝新生_BL', '善導寺', '台北車站_BL', '西門_BL', '龍山寺', '江子翠', '新埔', '板橋_BL', '府中', '亞東醫院', '海山', '土城', '永寧', '頂埔', '動物園', '木柵', '萬芳社區', '萬芳醫院', '辛亥', '麟光', '六張犁', '科技大樓', '大安_BR', '忠孝復興_BR', '南京復興_BR', '中山國中', '松山機場', '大直', '劍南路', '西湖', '港墘', '文德', '內湖', '大湖公園', '葫洲', '東湖', '南港軟體園區', '南港展覽館_BR', '象山', '台北101/世貿', '信義安和', '大安_R', '大安森林公園', '東門_R', '中正紀念堂_R', '台大醫院', '台北車站_R', '中山_R', '雙連', '民權西路_R', '圓山', '劍潭', '士林', '芝山', '明德', '石牌', '唭哩岸', '奇岩', '北投', '新北投', '復興崗', '忠義', '關渡', '竹圍', '紅樹林', '淡水', '新店', '新店區公所', '七張', '大坪林_G', '景美', '萬隆', '公館', '台電大樓', '古亭_G', '中正紀念堂_G', '小南門', '西門_G', '北門', '中山_G', '松江南京_G', '南京復興_G', '台北小巨蛋', '南京三民', '松山', '南勢角', '景安_O', '永安市場', '頂溪', '古亭_O', '東門_O', '忠孝新生_O', '松江南京_O', '行天宮', '中山國小', '民權西路_O', '大橋頭', '台北橋', '菜寮', '三重', '先嗇宮', '頭前庄_O', '新莊', '輔大', '丹鳳', '迴龍', '三重國小', '三和國小', '徐匯中學', '三民高中', '蘆洲', '大坪林_Y', '十四張', '秀朗橋', '景平', '景安_Y', '中和', '橋和', '中原', '板新', '板橋_Y', '新埔民生', '頭前庄_Y', '幸福', '新北產業園區'], 
            "dest": "user",
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")



# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/", methods=["POST"])
def de():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
        
    global in_station

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
            text = event.message.text
        elif isinstance(event, PostbackEvent): 
            text = event.postback.data
        else:
            continue
        if text == "fsm":
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url="https://i.imgur.com/9INfHsn.png", preview_image_url="https://i.imgur.com/ulXo57j.jpeg"))
            continue
        if text == "help":
            send_text_message(event.reply_token, "請先從以下六條線選擇一條線輸入:\n板南線 、 文湖線 、 淡水信義線 、 松山新店線 、 中和新蘆線 、 環狀線\n再從選擇的線裡選擇一站輸入")
            print(machine.state)
            continue
        if text == "home":
            send_text_message(event.reply_token, "請先從以下六條線選擇一條線輸入:\n板南線 、 文湖線 、 淡水信義線 、 松山新店線 、 中和新蘆線 、 環狀線")
            print("123")
            machine.home_postback()
            in_station = False
            continue
        if machine.is_user():
            machine.choose_line(event)
            print(machine.state)
        elif in_station:
            print("2")
            if text == "上一站" or text == "backward":
                machine.backward()
                send_station_message(event.reply_token, machine.state)
                continue
            elif text == "下一站" or text == "toward":
                machine.toward()
                send_station_message(event.reply_token, machine.state)
                continue
            elif (machine.state == "南港展覽館_BL" or machine.state == "南京復興_G" or machine.state == "忠孝復興_BL" or machine.state == "大安_R") and text == "往文湖線":
                machine.文湖線()
                send_station_message(event.reply_token, machine.state)
                continue
            elif (machine.state == "南港展覽館_BR" or machine.state == "忠孝復興_BR" or machine.state == "忠孝新生_O" or machine.state == "台北車站_R" or machine.state == "西門_G" or machine.state == "板橋_Y") and text == "往板南線":
                machine.板南線()
                send_station_message(event.reply_token, machine.state)
                continue
            elif (machine.state == "大安_BR" or machine.state == "東門_O" or machine.state == "中正紀念堂_G" or machine.state == "台北車站_BL" or machine.state == "中山_G" or machine.state == "民權西路_O") and text == "往淡水信義線":
                machine.淡水信義線()
                send_station_message(event.reply_token, machine.state)
                continue
            elif (machine.state == "大坪林_Y" or machine.state == "古亭_O" or machine.state == "中正紀念堂_R" or machine.state == "西門_BL" or machine.state == "中山_R" or machine.state == "松江南京_O" or machine.state == "南京復興_BR") and text == "往松山新店線":
                machine.松山新店線()
                send_station_message(event.reply_token, machine.state)
                continue
            elif (machine.state == "景安_Y" or machine.state == "古亭_G" or machine.state == "東門_R" or machine.state == "忠孝新生_BL" or machine.state == "松江南京_G" or machine.state == "民權西路_R" or machine.state == "頭前庄_Y") and text == "往中和新蘆線":
                machine.中和新蘆線()
                send_station_message(event.reply_token, machine.state)
                continue
            elif (machine.state == "大坪林_G" or machine.state == "景安_O" or machine.state == "板橋_BL" or machine.state == "頭前庄_O") and text == "往環狀線":
                machine.環狀線()
                send_station_message(event.reply_token, machine.state)
                continue
            elif text == "往三重國小":
                machine.往三重國小()
                send_station_message(event.reply_token, machine.state)
                continue
            elif text == "往台北橋":
                machine.往台北橋()
                send_station_message(event.reply_token, machine.state)
                continue
                
        elif machine.is_文湖線 or machine.is_淡水信義線 or machine.is_松山新店線 or machine.is_板南線 or machine.is_中和新蘆線 or machine.is_環狀線:
            print("1")
            response = machine.choose_station(event)
            if response == True:
                in_station = True
                print(machine.state)
                send_station_message(event.reply_token, machine.state)
                continue
        #if response == False:
        #    send_text_message(event.reply_token, "Not Entering any State")
        #
        #line_bot_api.reply_message(
        #    event.reply_token, TextSendMessage(text='123')
        #)

    return "OK"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        
        
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    #machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
