import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
from urllib.request import urlopen
import json
import requests


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

station_find = [['頂埔', '永寧', '土城', '海山', '亞東醫院', '府中', '板橋_BL', '新埔', '江子翠', '龍山寺', '西門_BL', '台北車站_BL', '善導寺', '忠孝新生_BL', '忠孝復興_BL', '忠孝敦化', '國父紀念館', '市政府', '永春', '後山埤', '昆陽', '南港', '南港展覽館_BL'], ['動物園', '木柵', '萬芳社區', '萬芳醫院', '辛亥', '麟光', '六張犁', '科技大樓', '大安_BR', '忠孝復興_BR', '南京復興_BR', '中山國中', '松山機場', '大直', '劍南路', '西湖', '港墘', '文德', '內湖', '大湖公園', '葫洲', '東湖', '南港軟體園區', '南港展覽館_BR'], ['象山', '台北101/世貿', '信義安和', '大安_R', '大安森林公園', '東門_R', '中正紀念堂_R', '台大醫院', '台北車站_R', '中山_R', '雙連', '民權西路_R', '圓山', '劍潭', '士林', '芝山', '明德', '石牌', '唭哩岸', '奇岩', '北投', '新北投', '復興崗', '忠義', '關渡', '竹圍', '紅樹林', '淡水'], ['新店', '新店區公所', '七張', '大坪林_G', '景美', '萬隆', '公館', '台電大樓', '古亭_G', '中正紀念堂_G', '小南門', '西門_G', '北門', '中山_G', '松江南京_G', '南京復興_G', '台北小巨蛋', '南京三民', '松山'], ['南勢角', '景安_O', '永安市場', '頂溪', '古亭_O', '東門_O', '忠孝新生_O', '松江南京_O', '行天宮', '中山國小', '民權西路_O', '大橋頭', '台北橋', '菜寮', '三重', '先嗇宮', '頭前庄_O', '新莊', '輔大', '丹鳳', '迴龍', '三重國小', '三和國小', '徐匯中學', '三民高中', '蘆洲', ' ', ' ', ' ', ' '], ['大坪林_Y', '十四張', '秀朗橋', '景平', '景安_Y', '中和', '橋和', '中原', '板新', '板橋_Y', '新埔民生', '頭前庄_Y', '幸福', '新北產業園區']]
station = [['頂埔', '永寧', '土城', '海山', '亞東醫院', '府中', '板橋', '新埔', '江子翠', '龍山寺', '西門', '台北車站', '善導寺', '忠孝新生', '忠孝復興', '忠孝敦化', '國父紀念館', '市政府', '永春', '後山埤', '昆陽', '南港', '南港展覽館'], ['動物園', '木柵', '萬芳社區', '萬芳醫院', '辛亥', '麟光', '六張犁', '科技大樓', '大安', '忠孝復興', '南京復興', '中山國中', '松山機場', '大直', '劍南路', '西湖', '港墘', '文德', '內湖', '大湖公園', '葫洲', '東湖', '南港軟體園區', '南港展覽館'], ['象山', '台北101/世貿', '信義安和', '大安', '大安森林公園', '東門', '中正紀念堂', '台大醫院', '台北車站', '中山', '雙連', '民權西路', '圓山', '劍潭', '士林', '芝山', '明德', '石牌', '唭哩岸', '奇岩', '北投', '新北投', '復興崗', '忠義', '關渡', '竹圍', '紅樹林', '淡水'], ['新店', '新店區公所', '七張', '大坪林', '景美', '萬隆', '公館', '台電大樓', '古亭', '中正紀念堂', '小南門', '西門', '北門', '中山', '松江南京', '南京復興', '台北小巨蛋', '南京三民', '松山'], ['南勢角', '景安', '永安市場', '頂溪', '古亭', '東門', '忠孝新生', '松江南京', '行天宮', '中山國小', '民權西路', '大橋頭', '台北橋', '菜寮', '三重', '先嗇宮', '頭前庄', '新莊', '輔大', '丹鳳', '迴龍', '三重國小', '三和國小', '徐匯中學', '三民高中', '蘆洲', ' ', ' ', ' ', ' '], ['大坪林', '十四張', '秀朗橋', '景平', '景安', '中和', '橋和', '中原', '板新', '板橋', '新埔民生', '頭前庄', '幸福', '新北產業園區']]
station_code = [["BL01", "BL02", "BL03", "BL04", "BL05", "BL06", "BL07", "BL08", "BL09", "BL10", "BL11", "BL12", "BL13", "BL14", "BL15", "BL16", "BL17", "BL18", "BL19", "BL20", "BL21", "BL22", "BL23"], ["BR01", "BR02", "BR03", "BR04", "BR05", "BR06", "BR07", "BR08", "BR09", "BR10", "BR11", "BR12", "BR13", "BR14", "BR15", "BR16", "BR17", "BR18", "BR19", "BR20", "BR21", "BR22", "BR23", "BR24"], ["R01", "R02", "R03", "R04", "R05", "R06", "R07", "R08", "R09", "R10", "R11", "R12", "R13", "R14", "R15", "R16", "R17", "R18", "R19", "R20", "R21", "R22", "R23", "R24", "R25", "R26", "R27", "R28"], ['G01', 'G02', 'G03', 'G04', 'G05', 'G06', 'G07', 'G08', 'G09', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16', 'G17', 'G18', 'G19'], ["O01", "O02", "O03", "O04", "O05", "O06", "O07", "O08", "O09", "O10", "O11", "O12", "O13", "O14", "O15", "O16", "O17", "O18", "O19", "O20", "O21", "O50", "O51", "O52", "O53", "O54", " ", " ", " ", " "], ["Y07", "Y08", "Y09", "Y10", "Y11", "Y12", "Y13", "Y14", "Y15", "Y16", "Y17", "Y18", "Y19", "Y20"]]
line = ['板南線', '文湖線', '淡水信義線', '松山新店線', '中和新蘆線', '環狀線']
line_color = ["#6486E3", "#945f1f", "#cf0e0e", "#176e17", "#e6a100", "#e6cb00"]
station_size = [23, 24, 28, 19, 26, 14]
往板南線 = ["南港展覽館_BR", "忠孝復興_BR", "忠孝新生_O", "台北車站_R", "西門_G", "板橋_Y"]
往文湖線 = ['南港展覽館_BL', '南京復興_G', '忠孝復興_BL', '大安_R']
往淡水信義線 = ['大安_BR', '東門_O', '中正紀念堂_G', '台北車站_BL', '中山_G', '民權西路_O']
往松山新店線 = ['大坪林_Y', '古亭_O', '中正紀念堂_R', '西門_BL', '中山_R', '松江南京_O', '南京復興_BR']
往中和新蘆線 = ['景安_Y', '古亭_G', '東門_R', '忠孝新生_BL', '松江南京_G', '民權西路_R', '頭前庄_Y']
往環狀線 = ["大坪林_G", "景安_O", "板橋_BL", "頭前庄_O"]

def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def get_double_box(index1, index2, index3):
    if index3 > 25:
        borderWidth = "none"
    else:
        borderWidth = "2px"
    box =   {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": station_code[index1][index2],
                    "size": "sm",
                    "align": "end",
                    "margin": "none",
                    "adjustMode": "shrink-to-fit",
                    "flex": 3
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "cornerRadius": "30px",
                        "width": "12px",
                        "height": "12px",
                        "borderColor": line_color[index1],
                        "borderWidth": "2px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "flex": 0,
                    "margin": "none",
                    "spacing": "none",
                    "paddingStart": "4px",
                    "paddingEnd": "4px"
                  },
                  {
                    "type": "text",
                    "text": station[index1][index2],
                    "flex": 4,
                    "size": "sm",
                    "align": "start",
                    "gravity": "center",
                    "margin": "none"
                  },
                  {
                    "type": "text",
                    "text": station[index1][index3],
                    "gravity": "center",
                    "flex": 4,
                    "size": "sm",
                    "align": "end",
                    "margin": "none"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "cornerRadius": "30px",
                        "width": "12px",
                        "height": "12px",
                        "borderColor": line_color[index1],
                        "borderWidth": borderWidth
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "flex": 0,
                    "margin": "none",
                    "paddingStart": "4px",
                    "paddingEnd": "4px"
                  },
                  {
                    "type": "text",
                    "text": station_code[index1][index3],
                    "size": "sm",
                    "margin": "none",
                    "adjustMode": "shrink-to-fit",
                    "flex": 3,
                    "align": "start",
                    "offsetStart": "1px"
                  }
                ],
                "spacing": "md",
                "cornerRadius": "30px"
            }
    return box

def get_double_line(index1, index2):
    if index2 > 25:
        width = "0px"
    else:
        width = "2px"
        
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "contents": [],
            "width": "56px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "width": "2px",
                    "backgroundColor": line_color[index1]
                  }
                ],
                "flex": 1
              }
            ],
            "width": "2px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [],
            "width": "144px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "width": width,
                    "backgroundColor": line_color[index1]
                  }
                ],
                "flex": 1
              }
            ],
            "width": "2px"
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": [],
            "width": "56px"
          }
        ],
        "spacing": "none",
        "height": "32px"
      }

def get_box(index1, index2):
    return {
              "type": "box",
              "layout": "horizontal",
              "contents": [
                {
                  "type": "text",
                  "text": station_code[index1][index2],
                  "size": "sm",
                  "align": "end",
                  "flex": 1
                },
                {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [
                    {
                      "type": "filler"
                    },
                    {
                      "type": "box",
                      "layout": "vertical",
                      "contents": [],
                      "cornerRadius": "30px",
                      "height": "12px",
                      "width": "12px",
                      "borderColor": line_color[index1],
                      "borderWidth": "2px"
                    },
                    {
                      "type": "filler"
                    }
                  ],
                  "flex": 0
                },
                {
                  "type": "text",
                  "text": station[index1][index2],
                  "gravity": "center",
                  "flex": 1,
                  "size": "sm"
                }
              ],
              "spacing": "lg",
              "cornerRadius": "sm",
              "margin": "none",
              "position": "relative"
            }
    
def get_horizontal_line(index1):
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "56px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": line_color[index1],
                "width": "148px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "56px"
              }
            ],
            "flex": 1
          }
        ],
        "width": "300px",
        "height": "2px"
      }
    
def get_line(index1):
    return {
              "type": "box",
              "layout": "horizontal",
              "contents": [
                {
                  "type": "box",
                  "layout": "baseline",
                  "contents": [
                    {
                      "type": "filler"
                    }
                  ],
                  "flex": 1
                },
                {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [
                    {
                      "type": "box",
                      "layout": "horizontal",
                      "contents": [
                        {
                          "type": "filler"
                        },
                        {
                          "type": "box",
                          "layout": "vertical",
                          "contents": [],
                          "width": "2px",
                          "backgroundColor": line_color[index1]
                        },
                        {
                          "type": "filler"
                        }
                      ],
                      "flex": 1
                    }
                  ],
                  "width": "12px"
                },
                {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [],
                  "flex": 1
                }
              ],
              "spacing": "lg",
              "height": "32px"
            }

def get_double_dotted_line(index1):
    return{
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [],
                "width": "56px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "0px",
                        "backgroundColor": line_color[index1]
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "2px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "144px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "0px",
                        "backgroundColor": line_color[index1]
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "2px"
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [],
                "width": "56px"
              }
            ],
            "spacing": "none",
            "height": "2px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [],
                "width": "56px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "2px",
                        "backgroundColor": line_color[index1]
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "2px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "144px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "2px",
                        "backgroundColor": line_color[index1]
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "2px"
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [],
                "width": "56px"
              }
            ],
            "spacing": "none",
            "height": "4px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [],
                "width": "56px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "0px",
                        "backgroundColor": line_color[index1]
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "2px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "144px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "0px",
                        "backgroundColor": line_color[index1]
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "2px"
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [],
                "width": "56px"
              }
            ],
            "spacing": "none",
            "height": "4px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [],
                "width": "56px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "2px",
                        "backgroundColor": line_color[index1]
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "2px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "144px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "2px",
                        "backgroundColor": line_color[index1]
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "2px"
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [],
                "width": "56px"
              }
            ],
            "spacing": "none",
            "height": "4px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [],
                "width": "56px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "0px",
                        "backgroundColor": line_color[index1]
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "2px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "144px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "0px",
                        "backgroundColor": line_color[index1]
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "2px"
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [],
                "width": "56px"
              }
            ],
            "spacing": "none",
            "height": "4px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [],
                "width": "56px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "2px",
                        "backgroundColor": line_color[index1]
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "2px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "144px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "2px",
                        "backgroundColor": line_color[index1]
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "2px"
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [],
                "width": "56px"
              }
            ],
            "spacing": "none",
            "height": "4px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [],
                "width": "56px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "0px",
                        "backgroundColor": line_color[index1]
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "2px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "144px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "0px",
                        "backgroundColor": line_color[index1]
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "2px"
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [],
                "width": "56px"
              }
            ],
            "spacing": "none",
            "height": "4px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [],
                "width": "56px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "2px",
                        "backgroundColor": line_color[index1]
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "2px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "144px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "2px",
                        "backgroundColor": line_color[index1]
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "2px"
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [],
                "width": "56px"
              }
            ],
            "spacing": "none",
            "height": "4px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [],
                "width": "56px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "0px",
                        "backgroundColor": line_color[index1]
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "2px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "144px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "0px",
                        "backgroundColor": line_color[index1]
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "2px"
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [],
                "width": "56px"
              }
            ],
            "spacing": "none",
            "height": "2px"
          }
        ]
      }
    
def get_dotted_line(index1):
    return{
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "filler"
                  }
                ],
                "flex": 1
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "backgroundColor": line_color[index1],
                        "width": "0px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "12px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "flex": 1
              }
            ],
            "spacing": "lg",
            "height": "2px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "filler"
                  }
                ],
                "flex": 1
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "2px",
                        "backgroundColor": line_color[index1]
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "12px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "flex": 1
              }
            ],
            "spacing": "lg",
            "height": "4px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "filler"
                  }
                ],
                "flex": 1
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "backgroundColor": line_color[index1],
                        "width": "0px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "12px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "flex": 1
              }
            ],
            "spacing": "lg",
            "height": "4px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "filler"
                  }
                ],
                "flex": 1
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "2px",
                        "backgroundColor": line_color[index1]
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "12px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "flex": 1
              }
            ],
            "spacing": "lg",
            "height": "4px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "filler"
                  }
                ],
                "flex": 1
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "backgroundColor": line_color[index1],
                        "width": "0px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "12px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "flex": 1
              }
            ],
            "spacing": "lg",
            "height": "4px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "filler"
                  }
                ],
                "flex": 1
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "2px",
                        "backgroundColor": line_color[index1]
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "12px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "flex": 1
              }
            ],
            "spacing": "lg",
            "height": "4px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "filler"
                  }
                ],
                "flex": 1
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "backgroundColor": line_color[index1],
                        "width": "0px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "12px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "flex": 1
              }
            ],
            "spacing": "lg",
            "height": "4px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "filler"
                  }
                ],
                "flex": 1
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "2px",
                        "backgroundColor": line_color[index1]
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "12px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "flex": 1
              }
            ],
            "spacing": "lg",
            "height": "4px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "filler"
                  }
                ],
                "flex": 1
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "backgroundColor": line_color[index1],
                        "width": "0px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "flex": 1
                  }
                ],
                "width": "12px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "flex": 1
              }
            ],
            "spacing": "lg",
            "height": "2px"
          }
        ]
      }
    
    
def get_horizontal_dotted_line(index1):
    horizontal_dotted_line = {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "56px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": line_color[index1],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": line_color[index1],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": line_color[index1],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": line_color[index1],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": line_color[index1],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": line_color[index1],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": line_color[index1],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": line_color[index1],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": line_color[index1],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": line_color[index1],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": line_color[index1],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": line_color[index1],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": line_color[index1],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": line_color[index1],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": line_color[index1],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": line_color[index1],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": line_color[index1],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": line_color[index1],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "4px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": "56px"
              }
            ],
            "flex": 1
          }
        ],
        "width": "300px",
        "height": "2px"
      }
        
    return horizontal_dotted_line
    
def get_button(text):
    if text == "home":
        label = "回首頁"
        data = "home"
    elif text == "toward":
        label = "下一站"
        data = "toward"
    elif text == "backward":
        label = "上一站"
        data = "backward"
    elif text == "往板南線":
        label = "往板南線"
        data = "往板南線"
    elif text == "往文湖線":
        label = "往文湖線"
        data = "往文湖線"
    elif text == "往淡水信義線":
        label = "往淡水信義線"
        data = "往淡水信義線"
    elif text == "往松山新店線":
        label = "往松山新店線"
        data = "往松山新店線"
    elif text == "往中和新蘆線":
        label = "往中和新蘆線"
        data = "往中和新蘆線"
    elif text == "往環狀線":
        label = "往環狀線"
        data = "往環狀線"
    elif text == "往台北橋":
        label = "往台北橋"
        data = "往台北橋"
    elif text == "往三重國小":
        label = "往三重國小"
        data = "往三重國小"
    return {
        "type": "button",
        "action": {
          "type": "postback",
          "label": label,
          "data": data
        },
        "height": "sm"
    }

def send_line_message(reply_token, text):
    if text == "板南線":
        index1 = 0
        index2 = 23
    elif text == "文湖線":
        index1 = 1
        index2 = 24
    elif text == "淡水信義線":
        index1 = 2
        index2 = 28
    elif text == "松山新店線":
        index1 = 3
        index2 = 19
    elif text == "中和新蘆線":
        index1 = 4
        index2 = 26
    elif text == "環狀線":
        index1 = 5
        index2 = 14
        
    line_bot_api = LineBotApi(channel_access_token)
    FlexMessage = {
        "type": "bubble",
        "size": "mega",
        "header": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": line[index1],
              "color": "#ffffff",
              "flex": 1,
              "weight": "bold",
              "align": "center",
              "contents": [],
              "size": "3xl",
              "margin": "md"
            }
          ],
          "backgroundColor": line_color[index1],
          "height": "100px"
        },
        "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
          ]
        }
    }
    if(not index1 == 4):
        FlexMessage["body"]["contents"].append(get_box(index1, 0))
        for i in range(1, index2):
            FlexMessage["body"]["contents"].append(get_line(index1))
            FlexMessage["body"]["contents"].append(get_box(index1, i))
    else:
        FlexMessage["body"]["contents"].append(get_box(index1, 0))
        for i in range(1, 12):
            FlexMessage["body"]["contents"].append(get_line(index1))
            FlexMessage["body"]["contents"].append(get_box(index1, i))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_horizontal_line(index1))
        for i in range(12, 21):
            FlexMessage["body"]["contents"].append(get_double_line(index1, i + 9))
            FlexMessage["body"]["contents"].append(get_double_box(index1, i, i + 9))
        
    
    FlexMessage["body"]["contents"].append(get_button("home"))    
    line_bot_api.reply_message(reply_token, FlexSendMessage(line[index1],FlexMessage))
            
    
    return "OK"


def send_station_message(reply_token, text):
    find = False
    index1 = 0
    index2 = 1
    for i in range(0, 6):
        for j in range(0, len(station_find[i])):
            if text == station_find[i][j]:
                index1 = i
                index2 = j
                find = True
                break
        if find:
            break
        index2 = 0
        
    url = "https://tdx.transportdata.tw/api/basic/v2/Rail/Metro/StationTimeTable/TRTC?%24top=30&%24format=JSON"
    res = requests.get(url)
    
    #data_json = json.decoder(res)
    
    print(res.status_code)
    
    FlexMessage = {
        "type": "bubble",
        "size": "mega",
        "header": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
                "type": "text",
                "text": station_code[index1][index2],
                "color": "#ffffff",
                "flex": 1,
                "weight": "bold",
                "align": "center",
                "contents": [],
                "size": "3xl",
                "margin": "none"
              },
              {
                "type": "text",
                "text": station[index1][index2],
                "flex": 1,
                "margin": "none",
                "size": "3xl",
                "color": "#ffffff",
                "align": "center",
                "weight": "bold"
              }
          ],
          "backgroundColor": line_color[index1],
          "height": "140px"
        },
        "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
          ]
        }
    }
    if index1 == 4 and index2 < 10 and index2 > 1:
        FlexMessage["body"]["contents"].append(get_box(index1, 0))
        FlexMessage["body"]["contents"].append(get_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2 - 1))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2 + 1))
        FlexMessage["body"]["contents"].append(get_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, 11))
        FlexMessage["body"]["contents"].append(get_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_horizontal_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_double_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_double_box(index1, 20, 25))
    elif index1 == 4 and index2 == 10:
        FlexMessage["body"]["contents"].append(get_box(index1, 0))
        FlexMessage["body"]["contents"].append(get_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2 - 1))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2 + 1))
        FlexMessage["body"]["contents"].append(get_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_horizontal_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_double_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_double_box(index1, 20, 25))
    elif index1 == 4 and index2 == 11:
        FlexMessage["body"]["contents"].append(get_box(index1, 0))
        FlexMessage["body"]["contents"].append(get_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2 - 1))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_horizontal_line(index1))
        FlexMessage["body"]["contents"].append(get_double_line(index1, index2 + 10))
        FlexMessage["body"]["contents"].append(get_double_box(index1, index2 + 1, index2 + 10))
        FlexMessage["body"]["contents"].append(get_double_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_double_box(index1, 20, 25))
    elif index1 == 4 and index2 == 21:
        FlexMessage["body"]["contents"].append(get_box(index1, 0))
        FlexMessage["body"]["contents"].append(get_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, 11))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2 + 1))
        FlexMessage["body"]["contents"].append(get_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, station_size[i] - 1))
    elif index1 == 4 and (index2 >= 12 and index2 < 19):
        FlexMessage["body"]["contents"].append(get_box(index1, 0))
        FlexMessage["body"]["contents"].append(get_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2 - 1))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2 + 1))
        FlexMessage["body"]["contents"].append(get_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, 20))
    elif index1 == 4 and (index2 == 19):
        FlexMessage["body"]["contents"].append(get_box(index1, 0))
        FlexMessage["body"]["contents"].append(get_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2 - 1))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2 + 1))
    elif index1 == 4 and (index2 == 20):
        FlexMessage["body"]["contents"].append(get_box(index1, 0))
        FlexMessage["body"]["contents"].append(get_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2 - 1))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2))
    elif index2 > 1 and index2 < station_size[index1] - 2:
        FlexMessage["body"]["contents"].append(get_box(index1, 0))
        FlexMessage["body"]["contents"].append(get_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2 - 1))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2 + 1))
        FlexMessage["body"]["contents"].append(get_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, station_size[i] - 1))
    elif index2 == 0:
        FlexMessage["body"]["contents"].append(get_box(index1, index2))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2 + 1))
        FlexMessage["body"]["contents"].append(get_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, station_size[i] - 1))
    elif index2 == station_size[index1] - 1:
        FlexMessage["body"]["contents"].append(get_box(index1, 0))
        FlexMessage["body"]["contents"].append(get_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2 - 1))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2))
    elif index2 == 1:
        FlexMessage["body"]["contents"].append(get_box(index1, index2 - 1))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2 + 1))
        FlexMessage["body"]["contents"].append(get_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, station_size[i] - 1))
    elif index2 == station_size[index1] - 2:
        FlexMessage["body"]["contents"].append(get_box(index1, 0))
        FlexMessage["body"]["contents"].append(get_dotted_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2 - 1))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2))
        FlexMessage["body"]["contents"].append(get_line(index1))
        FlexMessage["body"]["contents"].append(get_box(index1, index2 + 1))
        
    if index2 != 0:
        FlexMessage["body"]["contents"].append(get_button("backward"))
    if (index1 != 4 and index2 != station_size[index1] - 1) or (index1 == 4 and index2 != 11 and index2 != 20):
        FlexMessage["body"]["contents"].append(get_button("toward"))
    elif index2 == 11:
        print(index1)
        print(index2)
        FlexMessage["body"]["contents"].append(get_button("往台北橋"))
        FlexMessage["body"]["contents"].append(get_button("往三重國小"))
    if(index1 != 0 and text in 往板南線):
        FlexMessage["body"]["contents"].append(get_button("往板南線"))
    elif(index1 != 1 and text in 往文湖線):
        FlexMessage["body"]["contents"].append(get_button("往文湖線"))
    elif(index1 != 2 and text in 往淡水信義線):
        FlexMessage["body"]["contents"].append(get_button("往淡水信義線"))
    elif(index1 != 3 and text in 往松山新店線):
        FlexMessage["body"]["contents"].append(get_button("往松山新店線"))
    elif(index1 != 4 and text in 往中和新蘆線):
        FlexMessage["body"]["contents"].append(get_button("往中和新蘆線"))
    elif(index1 != 5 and text in 往環狀線):
        FlexMessage["body"]["contents"].append(get_button("往環狀線"))
    FlexMessage["body"]["contents"].append(get_button("home"))
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, FlexSendMessage(text, FlexMessage))

"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
