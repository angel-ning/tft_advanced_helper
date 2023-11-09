import time
import random
import threading
from utils import *
from logger import *
from constants import *

global WaitStageFlag

def check_for_end_cond():
    round_img = capture_screen(bbox=(740, 0, 820, 30))

    osd = read_digit_from_image(round_img)

    end_condition = ["5-1", "5-2", "5-3", "5-4", "5-5", "5-6", "5-7",
                     "6-1"]

    if any(item in osd for item in end_condition):
        return True
    else :
        return False
    
def stray():
    # 在棋盘小范围内随机游荡，防止鼠标指针挡住关卡图片导致检测不到3-2关卡
    x = random.randint(400, 1500)
    y = random.randint(200, 500)

    left_slow_click((x, y), button='right', move_time=0.5)

    return True

def buy_single_champ(index):
    global champ_box

    if index > 4:
        index = 4
    if index < 0:
        index = 0

    box = champ_box[index]
    center = get_box_center(box)
    left_slow_click(center, move_time=0.3)

    return True

def upgrade_champ():
    pg.press('f')
    return True

def refresh_shop():
    pg.press('d')  # Using pyautogui to press the key
    return True

def show_emoji():
    pg.press('t')  # Using pyautogui to press the key
    return True

def move_to_empty_area():
    global box_empty_area

    center = (1000, 580)
    pg.moveTo(center[0], center[1], duration=0.1)

    return True

def surrender():
    global box_settings, box_surrender, box_confirm

    slow_key_press('esc')

    center = get_box_center(box_surrender)
    # 发起投降
    left_slow_click(center, move_time=0.5)

    center = get_box_center(box_confirm)
    # 确定离开
    left_slow_click(center, move_time=0.5)

    return True

def click_find_match():

    p = (840, 870)
    left_slow_click(p)
    move_to_empty_area()
    return True

def stop_and_start_a_new_match():
    left_slow_click(722,873)
    move_to_empty_area()

    time.sleep(1)
    return click_find_match()

def game_start():
    im = capture_screen(bbox=(444, 290, 688, 308))  # X1,Y1,X2,Y2
    # save image file
    # im.save("box.png")

    title = pytesseract.image_to_string(im, lang='eng')

    if "TEAMFIGHT" in title:
        return True
    else:
        return False
    
def close_award_interface():
    left_slow_click((860, 830))
    move_to_empty_area()

    return True
    
def accept_match(logger):
    # 5分钟未进入游戏，直接重新匹配
    timeout = 5 * 60
    start_time = time.time()

    accept_point = (986, 750)

    while time.time() - start_time < timeout * 10:
        while time.time() - start_time < timeout:
            left_slow_click(accept_point)
            # move_to_empty_area()
            # 客户端已最小化，正在启动游戏
            if not if_check_word(444, 290, 688, 308, "TEAMFIGHT"):
                return True
            time.sleep(2)
        # 等待太久，重新匹配
        if not stop_and_start_a_new_match():
            return False

    logger.write_log("10次超时未找到对局！")
    return False

def pg_find_match(logger):
    click_find_match()
    return accept_match(logger)

def pg_wait_loading():
    while True:
        # pyautogui 模块检测关卡
        # loading_test_img = ImageGrab.grab(bbox=(275, 1005, 460, 1070))
        # loading_test_img.save("loading_test.png")
        # print("test" + pytesseract.image_to_string(loading_test_img, lang='eng'))
        result = if_check_word(275, 1005, 460, 1070, "Refresh")
        if result:
            return True
        time.sleep(2)
    return True


def change_wait_flag_callback(logger):
    global WaitStageFlag
    logger.write_log("17分钟未检测到3-2回合，直接进行下一步操作")
    WaitStageFlag = False
    return True

WaitStageFlag = True

def pg_wait_stage_3_2(logger):
    global WaitStageFlag

    WaitStageFlag = True

    # 启动一个Timer，17分钟未检测到3-2回合，直接进行下一步
    t = threading.Timer(17 * 60, change_wait_flag_callback)
    t.start()

    while WaitStageFlag:


        result = check_for_end_cond()
        if result:
            # 检测到3-2，停止Timer
            t.cancel()
            return True

        case = random.randint(1, 100)
        # %40 概率游荡
        if case <= 40:
            stray()
        case = random.randint(1, 100)
        # %25 概率买1个英雄
        if case >= 25 and case < 50:
            buy_single_champ(random.randint(0, 4))

        case = random.randint(1, 100)
        # %0 概率刷新商店
        if case == 0:
            refresh_shop()

        case = random.randint(1, 100)
        # %30 概率发表情
        if case <= 30:
            show_emoji()

        case = random.randint(1, 100)
        # %5 概率升级
        if case >= 85 and case < 90:
            upgrade_champ()

        time.sleep(random.uniform(2, 10))

    return True

def pg_wait_surrender_finish():
    # client_title = 'League of Legends (TM) Client'
    times = 0
    # 检测结算界面是否打开
    while True:
        time.sleep(1)
        times += 1
        

        if if_check_word(780, 860, 930, 888, "PLAY AGAIN"):
            break
        if times % 10 == 0:
            print("pg_wait_surrender_finish %d sec, still wait client over!" % times)   
            
        left_slow_click((965, 580))
        time.sleep(2)     
        close_award_interface()

        time.sleep(8)

    return True

def pg_play_again():
    global box_play_again, box_empty_area

    pg.click(850, 877, duration=0.3)  # 点击再玩一次

    time.sleep(1)

    result_find = if_check_word(800, 860, 900, 880, "FIND MATCH")
    result_queue = if_check_word(800, 860, 900, 880, "QUEUE")
    result = result_find or result_queue
    while not result:
        pg.click(850, 877, duration=0.3)  # 点击再玩一次


        time.sleep(5)
        result_find = if_check_word(800, 860, 900, 880, "FIND MATCH")
        result_queue = if_check_word(800, 860, 900, 880, "QUEUE")
        result = result_find or result_queue

    return True