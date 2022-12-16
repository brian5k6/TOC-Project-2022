from transitions.extensions import GraphMachine

from utils import send_text_message, send_line_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        
    #line
    def go_to_文湖線(self, event):
        text = event.message.text
        return text.lower() in "文湖線"
    
    def go_to_板南線(self, event):
        text = event.message.text
        return text.lower() in "板南線"
    
    def go_to_淡水信義線(self, event):
        text = event.message.text
        return text.lower() in "淡水信義線"
    
    def go_to_松山新店線(self, event):
        text = event.message.text
        return text.lower() in "松山新店線"
    
    def go_to_中和新蘆線(self, event):
        text = event.message.text
        return text.lower() in "中和新蘆線"
    
    def go_to_環狀線(self, event):
        text = event.message.text
        return text.lower() in "環狀線"
    
    def on_enter_文湖線(self, event):
        send_line_message(event.reply_token, "文湖線")
    
    def on_enter_板南線(self, event):
        send_line_message(event.reply_token, "板南線")
    
    def on_enter_淡水信義線(self, event):
        send_line_message(event.reply_token, "淡水信義線")
    
    def on_enter_松山新店線(self, event):
        send_line_message(event.reply_token, "松山新店線")
    
    def on_enter_中和新蘆線(self, event):
        send_line_message(event.reply_token, "中和新蘆線")
    
    def on_enter_環狀線(self, event):
        send_line_message(event.reply_token, "環狀線")
    
    
    #toward or backward    
    def go_to_上一站(self, event):
        text = event.message.text
        return text.lower() == "上一站"
        
    def go_to_下一站(self, event):
        text = event.message.text
        return text.lower() == "下一站"
    
    #板南線    
    def 南港展覽館_BL(self, event):
        text = event.message.text
        return text.lower() == "南港展覽館"
        
    def 南港(self, event):
        text = event.message.text
        return text.lower() == "南港"
        
    def 昆陽(self, event):
        text = event.message.text
        return text.lower() == "昆陽"
        
    def 後山埤(self, event):
        text = event.message.text
        return text.lower() == "後山埤"
        
    def 永春(self, event):
        text = event.message.text
        return text.lower() == "永春"
        
    def 市政府(self, event):
        text = event.message.text
        return text.lower() == "市政府"
        
    def 國父紀念館(self, event):
        text = event.message.text
        return text.lower() == "國父紀念館"
        
    def 忠孝敦化(self, event):
        text = event.message.text
        return text.lower() == "忠孝敦化"
        
    def 忠孝復興_BL(self, event):
        text = event.message.text
        return text.lower() == "忠孝復興"
        
    def 忠孝新生_BL(self, event):
        text = event.message.text
        return text.lower() == "忠孝新生"
        
    def 善導寺(self, event):
        text = event.message.text
        return text.lower() == "善導寺"
        
    def 台北車站_BL(self, event):
        text = event.message.text
        return text.lower() == "台北車站"
        
    def 西門_BL(self, event):
        text = event.message.text
        return text.lower() == "西門"
        
    def 龍山寺(self, event):
        text = event.message.text
        return text.lower() == "龍山寺"
        
    def 江子翠(self, event):
        text = event.message.text
        return text.lower() == "江子翠"
        
    def 新埔(self, event):
        text = event.message.text
        return text.lower() == "新埔"
        
    def 板橋_BL(self, event):
        text = event.message.text
        return text.lower() == "板橋"
        
    def 府中(self, event):
        text = event.message.text
        return text.lower() == "府中"
        
    def 亞東醫院(self, event):
        text = event.message.text
        return text.lower() == "亞東醫院"
        
    def 海山(self, event):
        text = event.message.text
        return text.lower() == "海山"
        
    def 土城(self, event):
        text = event.message.text
        return text.lower() == "土城"
        
    def 永寧(self, event):
        text = event.message.text
        return text.lower() == "永寧"
        
    def 頂埔(self, event):
        text = event.message.text
        return text.lower() == "頂埔"
    
    #文湖線    
    def 動物園(self, event):
        text = event.message.text
        return text.lower() == "動物園"
        
    def 木柵(self, event):
        text = event.message.text
        return text.lower() == "木柵"
        
    def 萬芳社區(self, event):
        text = event.message.text
        return text.lower() == "萬芳社區"
        
    def 萬芳醫院(self, event):
        text = event.message.text
        return text.lower() == "萬芳醫院"
        
    def 辛亥(self, event):
        text = event.message.text
        return text.lower() == "辛亥"
        
    def 麟光(self, event):
        text = event.message.text
        return text.lower() == "麟光"
        
    def 六張犁(self, event):
        text = event.message.text
        return text.lower() == "六張犁"
        
    def 科技大樓(self, event):
        text = event.message.text
        return text.lower() == "科技大樓"
        
    def 大安_BR(self, event):
        text = event.message.text
        return text.lower() == "大安"
        
    def 忠孝復興_BR(self, event):
        text = event.message.text
        return text.lower() == "忠孝復興"
        
    def 南京復興_BR(self, event):
        text = event.message.text
        return text.lower() == "南京復興"
        
    def 中山國中(self, event):
        text = event.message.text
        return text.lower() == "中山國中"
        
    def 松山機場(self, event):
        text = event.message.text
        return text.lower() == "松山機場"
        
    def 大直(self, event):
        text = event.message.text
        return text.lower() == "大直"
        
    def 劍南路(self, event):
        text = event.message.text
        return text.lower() == "劍南路"
        
    def 西湖(self, event):
        text = event.message.text
        return text.lower() == "西湖"
        
    def 港墘(self, event):
        text = event.message.text
        return text.lower() == "港墘"
        
    def 文德(self, event):
        text = event.message.text
        return text.lower() == "文德"
        
    def 內湖(self, event):
        text = event.message.text
        return text.lower() == "內湖"
        
    def 大湖公園(self, event):
        text = event.message.text
        return text.lower() == "大湖公園"
        
    def 葫洲(self, event):
        text = event.message.text
        return text.lower() == "葫洲"
        
    def 東湖(self, event):
        text = event.message.text
        return text.lower() == "東湖"
        
    def 南港軟體園區(self, event):
        text = event.message.text
        return text.lower() == "南港軟體園區"
        
    def 南港展覽館_BR(self, event):
        text = event.message.text
        return text.lower() == "南港展覽館"
    
    #淡水信義線    
    def 象山(self, event):
        text = event.message.text
        return text.lower() == "象山"
        
    def 台北101(self, event):
        text = event.message.text
        return text.lower() == "台北101/世貿"
        
    def 信義安和(self, event):
        text = event.message.text
        return text.lower() == "信義安和"
        
    def 大安_R(self, event):
        text = event.message.text
        return text.lower() == "大安"
        
    def 大安森林公園(self, event):
        text = event.message.text
        return text.lower() == "大安森林公園"
        
    def 東門_R(self, event):
        text = event.message.text
        return text.lower() == "東門"
        
    def 中正紀念堂_R(self, event):
        text = event.message.text
        return text.lower() == "中正紀念堂"
        
    def 台大醫院(self, event):
        text = event.message.text
        return text.lower() == "台大醫院"
        
    def 台北車站_R(self, event):
        text = event.message.text
        return text.lower() == "台北車站"
        
    def 中山_R(self, event):
        text = event.message.text
        return text.lower() == "中山"
        
    def 雙連(self, event):
        text = event.message.text
        return text.lower() == "雙連"
        
    def 民權西路_R(self, event):
        text = event.message.text
        return text.lower() == "民權西路"
        
    def 圓山(self, event):
        text = event.message.text
        return text.lower() == "圓山"
        
    def 劍潭(self, event):
        text = event.message.text
        return text.lower() == "劍潭"
        
    def 士林(self, event):
        text = event.message.text
        return text.lower() == "士林"
        
    def 芝山(self, event):
        text = event.message.text
        return text.lower() == "芝山"
        
    def 明德(self, event):
        text = event.message.text
        return text.lower() == "明德"
        
    def 石牌(self, event):
        text = event.message.text
        return text.lower() == "石牌"
        
    def 唭哩岸(self, event):
        text = event.message.text
        return text.lower() == "唭哩岸"
        
    def 奇岩(self, event):
        text = event.message.text
        return text.lower() == "奇岩"
        
    def 北投(self, event):
        text = event.message.text
        return text.lower() == "北投"
        
    def 新北投(self, event):
        text = event.message.text
        return text.lower() == "新北投"
        
    def 復興崗(self, event):
        text = event.message.text
        return text.lower() == "復興崗"
        
    def 忠義(self, event):
        text = event.message.text
        return text.lower() == "忠義"
        
    def 關渡(self, event):
        text = event.message.text
        return text.lower() == "關渡"
        
    def 竹圍(self, event):
        text = event.message.text
        return text.lower() == "竹圍"
        
    def 紅樹林(self, event):
        text = event.message.text
        return text.lower() == "紅樹林"
        
    def 淡水(self, event):
        text = event.message.text
        return text.lower() == "淡水"
    
    #松山新店線    
    def 新店(self, event):
        text = event.message.text
        return text.lower() == "新店"
        
    def 新店區公所(self, event):
        text = event.message.text
        return text.lower() == "新店區公所"
        
    def 七張(self, event):
        text = event.message.text
        return text.lower() == "七張"
        
    def 大坪林_G(self, event):
        text = event.message.text
        return text.lower() == "大坪林"
        
    def 景美(self, event):
        text = event.message.text
        return text.lower() == "景美"
        
    def 萬隆(self, event):
        text = event.message.text
        return text.lower() == "萬隆"
        
    def 公館(self, event):
        text = event.message.text
        return text.lower() == "公館"
        
    def 台電大樓(self, event):
        text = event.message.text
        return text.lower() == "台電大樓"
        
    def 古亭_G(self, event):
        text = event.message.text
        return text.lower() == "古亭"
        
    def 中正紀念堂_G(self, event):
        text = event.message.text
        return text.lower() == "中正紀念堂"
        
    def 小南門(self, event):
        text = event.message.text
        return text.lower() == "小南門"
        
    def 西門_G(self, event):
        text = event.message.text
        return text.lower() == "西門"
        
    def 北門(self, event):
        text = event.message.text
        return text.lower() == "北門"
        
    def 中山_G(self, event):
        text = event.message.text
        return text.lower() == "中山"
        
    def 松江南京_G(self, event):
        text = event.message.text
        return text.lower() == "松江南京"
        
    def 南京復興_G(self, event):
        text = event.message.text
        return text.lower() == "南京復興"
        
    def 台北小巨蛋(self, event):
        text = event.message.text
        return text.lower() == "台北小巨蛋"
        
    def 南京三民(self, event):
        text = event.message.text
        return text.lower() == "南京三民"
        
    def 松山(self, event):
        text = event.message.text
        return text.lower() == "松山"
    
    #中和新蘆線    
    def 南勢角(self, event):
        text = event.message.text
        return text.lower() == "南勢角"
        
    def 景安_O(self, event):
        text = event.message.text
        return text.lower() == "景安"
        
    def 永安市場(self, event):
        text = event.message.text
        return text.lower() == "永安市場"
        
    def 頂溪(self, event):
        text = event.message.text
        return text.lower() == "頂溪"
        
    def 古亭_O(self, event):
        text = event.message.text
        return text.lower() == "古亭"
        
    def 東門_O(self, event):
        text = event.message.text
        return text.lower() == "東門"
        
    def 忠孝新生_O(self, event):
        text = event.message.text
        return text.lower() == "忠孝新生"
        
    def 松江南京_O(self, event):
        text = event.message.text
        return text.lower() == "松江南京"
        
    def 行天宮(self, event):
        text = event.message.text
        return text.lower() == "行天宮"
        
    def 中山國小(self, event):
        text = event.message.text
        return text.lower() == "中山國小"
        
    def 民權西路_O(self, event):
        text = event.message.text
        return text.lower() == "民權西路"
        
    def 大橋頭(self, event):
        text = event.message.text
        return text.lower() == "大橋頭"
        
    def 台北橋(self, event):
        text = event.message.text
        return text.lower() == "台北橋"
        
    def 菜寮(self, event):
        text = event.message.text
        return text.lower() == "菜寮"
        
    def 三重(self, event):
        text = event.message.text
        return text.lower() == "三重"
        
    def 先嗇宮(self, event):
        text = event.message.text
        return text.lower() == "先嗇宮"
        
    def 頭前庄_O(self, event):
        text = event.message.text
        return text.lower() == "頭前庄"
        
    def 新莊(self, event):
        text = event.message.text
        return text.lower() == "新莊"
        
    def 輔大(self, event):
        text = event.message.text
        return text.lower() == "輔大"
        
    def 丹鳳(self, event):
        text = event.message.text
        return text.lower() == "丹鳳"
        
    def 迴龍(self, event):
        text = event.message.text
        return text.lower() == "迴龍"
        
    def 三重國小(self, event):
        text = event.message.text
        return text.lower() == "三重國小"
        
    def 三和國小(self, event):
        text = event.message.text
        return text.lower() == "三和國小"
        
    def 徐匯中學(self, event):
        text = event.message.text
        return text.lower() == "徐匯中學"
        
    def 三民高中(self, event):
        text = event.message.text
        return text.lower() == "三民高中"
        
    def 蘆洲(self, event):
        text = event.message.text
        return text.lower() == "蘆洲"
    
    #環狀線    
    def 大坪林_Y(self, event):
        text = event.message.text
        return text.lower() == "大坪林"
        
    def 十四張(self, event):
        text = event.message.text
        return text.lower() == "十四張"
        
    def 秀朗橋(self, event):
        text = event.message.text
        return text.lower() == "秀朗橋"
        
    def 景平(self, event):
        text = event.message.text
        return text.lower() == "景平"
        
    def 景安_Y(self, event):
        text = event.message.text
        return text.lower() == "景安"
        
    def 中和(self, event):
        text = event.message.text
        return text.lower() == "中和"
        
    def 橋和(self, event):
        text = event.message.text
        return text.lower() == "橋和"
        
    def 中原(self, event):
        text = event.message.text
        return text.lower() == "中原"
        
    def 板新(self, event):
        text = event.message.text
        return text.lower() == "板新"
        
    def 板橋_Y(self, event):
        text = event.message.text
        return text.lower() == "板橋"
        
    def 新埔民生(self, event):
        text = event.message.text
        return text.lower() == "新埔民生"
        
    def 頭前庄_Y(self, event):
        text = event.message.text
        return text.lower() == "頭前庄"
        
    def 幸福(self, event):
        text = event.message.text
        return text.lower() == "幸福"
        
    def 新北產業園區(self, event):
        text = event.message.text
        return text.lower() == "新北產業園區"
    
    def back_to_user(self, event):
        text = event.message.text
        return text.lower() == "go back"

    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "go to state1"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to state2"

    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state1")
        #self.go_back()

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state2")
        #self.go_back()

