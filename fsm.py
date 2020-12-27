from transitions import Machine
from flask import Flask, jsonify, request, abort, send_file
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, MessageTemplateAction
from utils import send_text_message, send_button_message, send_image_message
import time, random

enough_time = 30
start_exercise_time = 0

def MyMachine():    

    machine = TocMachine(
        states = ["user", "menu", "exercise","thigh","core","arm","exercise_ing","check_finish",
                "finish_exercise","not_finish_exercise","wait_conti","show_record",
                "health_food","east","north","south","random_food"],
        transitions=[
            {   "trigger": "advance",
                "source": "user",
                "dest": "menu",
                "conditions": "is_going_menu"   },

            {   "trigger": "advance",
                "source": "menu",
                "dest": "exercise",
                "conditions": "is_going_exercise"   },

            {   "trigger": "advance",
                "source": "menu",
                "dest": "show_record",
                "conditions": "is_going_show_record"   },            

            {   "trigger": "advance",
                "source": "exercise",
                "dest": "thigh",
                "conditions": "is_going_thigh"  },

            {   "trigger": "advance",
                "source": "exercise",
                "dest": "core",
                "conditions": "is_going_core"   },

            {   "trigger": "advance",
                "source": "exercise",
                "dest": "arm",
                "conditions": "is_going_arm"  },

            {   "trigger": "advance",
                "source": ["thigh","core","arm"],
                "dest": "exercise_ing",
                "conditions": "is_going_exercise_ing"    },

            {   "trigger": "goto_check_finish",
                "source": "exercise_ing",
                "dest": "check_finish"    },

            {   "trigger": "advance",
                "source": "check_finish",
                "dest": "finish_exercise",
                "conditions": "is_past_15minute"   },

            {   "trigger": "advance",
                "source": "check_finish",
                "dest": "not_finish_exercise",
                "conditions": "is_not_past_15minute"   },

            {   "trigger": "goto_check_finish",
                "source": "not_finish_exercise",
                "dest": "check_finish"  },

            {   "trigger": "goto_wait_conti",
                "source": "finish_exercise",
                "dest": "wait_conti"  },

            {   "trigger": "advance",
                "source": "wait_conti",
                "dest": "menu",
                "conditions": "is_conti_exercise"   },

            {   "trigger": "advance",
                "source": "menu",
                "dest": "health_food",
                "conditions": "is_going_health_food"   },

            {   "trigger": "advance",
                "source": "health_food",
                "dest": "east",
                "conditions": "is_going_east"   },

            {   "trigger": "advance",
                "source": "health_food",
                "dest": "north",
                "conditions": "is_going_north"   },

            {   "trigger": "advance",
                "source": "health_food",
                "dest": "south",
                "conditions": "is_going_south"   },

            {   "trigger": "advance",
                "source": "health_food",
                "dest": "random_food",
                "conditions": "is_going_random_food"   },

            {   "trigger": "advance",
                "source": ["east","north","south"],
                "dest": "random_food",
                "conditions": "is_going_random_food"   },

            {   "trigger": "advance",
                "source": ["east","north","south"],
                "dest": "health_food",
                "conditions": "is_other_food"   },

            {   "trigger": "advance",
                "source": ["exercise","thigh","core","arm","exercise_ing","check_finish",
                "finish_exercise","not_finish_exercise","wait_conti","show_record",
                "health_food","east","north","south","random_food"],
                "dest": "menu",
                "conditions": "is_go_back"}

        ],
        initial="user",
        auto_transitions=False
    )
    return machine


class TocMachine(Machine):
    def __init__(self, **machine_configs):
        self.machine = Machine(model=self, **machine_configs)
        self.food = ["https://goo.gl/maps/TtDyWTmLPqthFf8z8",
            "https://g.page/boiledfood?share",
            "https://goo.gl/maps/witZSExN6sJgHma18",
            "https://goo.gl/maps/q1sGpZo3GeJ2W5V99",
            "https://goo.gl/maps/7dzuBBm2dTVPB7wx8",
            "https://g.page/graingarden?share",
            "https://goo.gl/maps/nEDZT41P7eqbNjoo6",
            "https://g.page/ShaLaLaBento?share",
            "https://goo.gl/maps/KDPESG2syG4D7Kqs7"   ]

    def is_going_menu(self, event):
        text = event.message.text
        return text == "開始"

    def is_go_back(self, event):
        text = event.message.text
        return text == "go back"

    def is_going_exercise(self, event):
        text = event.message.text
        return text == "開始健身"

    def is_going_thigh(self, event):
        text = event.message.text
        return text == "瘦大腿"

    def is_going_core(self, event):
        text = event.message.text
        return text == "練核心"

    def is_going_arm(self, event):
        text = event.message.text
        return text == "練手臂"

    def is_going_exercise_ing(self, event):
        text = event.message.text
        return text == "開始健身15分"

    def is_conti_exercise(self, event):
        text = event.message.text
        return text == "我下次會繼續健身"

    def is_past_15minute(self, event):
        global start_exercise_time, enough_time
        past_time = time.time() - start_exercise_time
        text = event.message.text
        return past_time >= enough_time and text == "完成健身"

    def is_not_past_15minute(self, event):
        global start_exercise_time, enough_time
        past_time = time.time() - start_exercise_time
        text = event.message.text
        return past_time < enough_time and text == "完成健身"

    def is_going_show_record(self, event):
        text = event.message.text
        return text == "查看健身紀錄"

    def is_going_health_food(self, event):
        text = event.message.text
        return text == "健康飲食"

    def is_going_east(self, event):
        text = event.message.text
        return text == "東安路附近"

    def is_going_north(self, event):
        text = event.message.text
        return text == "東豐路附近以北"

    def is_going_south(self, event):
        text = event.message.text
        return text == "東門路附近"

    def is_going_random_food(self, event):
        text = event.message.text
        return text == "幫我random"

    def is_other_food(self, event):
        text = event.message.text
        return text == "其他健康餐"

    def on_enter_menu(self, event):
        print("I'm entering menu")
        title = '選擇功能'
        text = '點擊「開始健身」選擇健身項目\n點擊「健康飲食」查看推薦健康餐點\n點擊「查看健身紀錄」查看使用小助手健身的紀錄'
        btn = [MessageTemplateAction(label = '開始健身',text ='開始健身'),
            MessageTemplateAction(label = '健康飲食',text ='健康飲食'),
            MessageTemplateAction(label = '查看健身紀錄',text ='查看健身紀錄')]
        url = 'https://i.imgur.com/dclblAW.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_exercise(self, event):
        title = '選擇健身項目'
        text = '選擇項目以獲取健身影片'
        btn = [MessageTemplateAction(label = '瘦大腿',text ='瘦大腿'),
            MessageTemplateAction(label = '練核心',text ='練核心'),
            MessageTemplateAction(label = '練手臂',text ='練手臂')]
        url = 'https://st2.depositphotos.com/1734074/7477/v/600/depositphotos_74779619-stock-illustration-fitness-logo-set-elegant-women.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_health_food(self, event):
        title = '選擇地段'
        text = '成大附近有不少健康餐點呢！請選擇方便的地段\n如果太多選擇不知道要吃什麼，也可以幫忙random一家店！'
        btn = [MessageTemplateAction(label = '東安路附近',text ='東安路附近'),
            MessageTemplateAction(label = '東門路附近',text ='東門路附近'),
            MessageTemplateAction(label = '東豐路附近以北',text ='東豐路附近以北'),
            MessageTemplateAction(label = '幫我random',text ='幫我random')]
        url = 'https://content.shopback.com/tw/wp-content/uploads/2020/06/16230019/benefit-beef.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_east(self, event):
        msg = "推薦三間健康餐點給您！\n" + self.food[0] + "\n" + self.food[1] + "\n" + self.food[2] + \
        "\n輸入「其他健康餐」，可重新回到選擇地段頁面\n輸入「幫我random」，可幫您隨機選一間店"
        send_text_message(event.reply_token, msg)  

    def on_enter_north(self, event):
        msg = "推薦三間健康餐點給您！\n" + self.food[3] + "\n" + self.food[4] + "\n" + self.food[5] + \
        "\n輸入「其他健康餐」，可重新回到選擇地段頁面\n輸入「幫我random」，可幫您隨機選一間店"
        send_text_message(event.reply_token, msg) 

    def on_enter_south(self, event):
        msg = "推薦三間健康餐點給您！\n" + self.food[6] + "\n" + self.food[7] + "\n" + self.food[8] + \
        "\n輸入「其他健康餐」，可重新回到選擇地段頁面\n輸入「幫我random」，可幫您隨機選一間店"
        send_text_message(event.reply_token, msg)    

    def on_enter_random_food(self, event):
        r = random.randrange(9)
        msg = "以下為幫您隨機選擇的店家！\n" + self.food[r] + "\n祝您用餐愉快！\n輸入「go back」可回到主菜單"
        send_text_message(event.reply_token, msg)

    def on_enter_thigh(self, event):
        msg = "推薦兩個瘦大腿的影片給您！\n\
        https://www.youtube.com/watch?v=Rr8CEyQ3-5k&t=620s\n\
        https://www.youtube.com/watch?v=q-gNpBsh1ds\n\
        輸入「開始健身15分」，即可開始計時"
        send_text_message(event.reply_token, msg)       

    def on_enter_core(self, event):
        msg = "推薦兩個練核心的影片給您！\n\
        https://www.youtube.com/watch?v=oHEob_UmtQk\n\
        https://www.youtube.com/watch?v=xYFUWfJf9hs\n\
        輸入「開始健身15分」，即可開始計時"       
        send_text_message(event.reply_token, msg)

    def on_enter_arm(self, event):
        msg = "推薦兩個練手臂的影片給您！\n\
        https://www.youtube.com/watch?v=YXCjEtDKIpA\n\
        https://www.youtube.com/watch?v=G1z8errGHZQ\n\
        輸入「開始健身15分」，即可開始計時"       
        send_text_message(event.reply_token, msg)

    def on_enter_exercise_ing(self, event):
        msg = "完成15分鐘的健身後，請輸入「完成健身」！"
        global start_exercise_time
        start_exercise_time = time.time();
        send_text_message(event.reply_token, msg)
        self.goto_check_finish();        

    def on_enter_finish_exercise(self, event):        
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        t += "\n"
        with open('exercise_record.txt','a') as f:
            f.write(t)
        msg = '完成健身！\n輸入「我下次會繼續健身」返回主菜單'
        send_text_message(event.reply_token, msg)
        self.goto_wait_conti()

    def on_enter_not_finish_exercise(self, event):
        msg = '尚未運動15分鐘，請繼續努力！'
        send_text_message(event.reply_token, msg)
        self.goto_check_finish()

    def on_enter_show_record(self, event):        
        with open('exercise_record.txt','r') as f:
            all_txt = f.readlines()
        use_time = len(all_txt)
        time_record = ""
        for i in range(use_time):
            time_record += all_txt[i]
        msg = f'您已經使用小助手運動{use_time}次了！使用的日期及時間為：\n{time_record}\n輸入「go back」回到主選單'
        send_text_message(event.reply_token, msg)
