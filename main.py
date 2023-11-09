import time
import pyautogui as pg
import keyboard
import os

# import pygetwindow as gw
# from pytesseract.pytesseract import Output
from constants import *
from utils import *
from game_control import *
from logger import *

AutoPlayFlag = True

# Define the path for the subfolder and log file
log_subfolder = 'log'
log_filename = '%s.log' % time.strftime('%Y_%m_%d_%H_%M_%S')
log_path = os.path.join(log_subfolder, log_filename)

# Create the subfolder if it doesn't exist
os.makedirs(log_subfolder, exist_ok=True)

# Create the logger object with the path
logger = Logger(log_path)

# def location_check(x1, y1, x2, y2, target):
#     im = ImageGrab.grab(bbox=(x1, y1, x2, y2))  # X1,Y1,X2,Y2

#     title = pytesseract.image_to_string(
#         im, lang='eng')

#     if "TEAMFIGHT" in title:
#         print("Found")
#     else:
#         print("Not found")




def get_time_fmt_str(t=None):
    if not t:
        t = time.localtime()
    return time.strftime("%Y/%m/%d %H:%M:%S", t)


def pg_stop_play():
    global AutoPlayFlag
    AutoPlayFlag = False
    print("Hotkey detected, Game Stopped")
    return True

# 手动结束脚本命令，按Ctrl+Alt+q即可设置停止运行标志
keyboard.add_hotkey('q', pg_stop_play)

# wait for keyboard events
# keyboard.wait()
# pg.add_hotkey('ctrl+alt+a', pg_game_start)
# pg.hotkey


def pg_main():
    global AutoPlayFlag, log_file

    # w = get_lol_hwnd()

    play_times = 0
    start_time = time.localtime()
    game_time_list = []

    time.sleep(5)
    # keyboard.wait()

    try:
        while AutoPlayFlag:
            # 游戏开始时间
            game_start = time.time()
            logger.write_log("[%s] pg_find_match" % get_time_fmt_str())
            pg_find_match(logger)
            logger.write_log("[%s] pg_wait_loading" % get_time_fmt_str())
            pg_wait_loading()
            logger.write_log("[%s] pg_wait_stage_3_2" % get_time_fmt_str())
            pg_wait_stage_3_2(logger)
            logger.write_log("[%s] surrender" % get_time_fmt_str())
            surrender()
            logger.write_log(
                "[%s] pg_wait_surrender_finish" % get_time_fmt_str())
            pg_wait_surrender_finish()
            play_times += 1
            logger.write_log("[%s] pg_play_again" % get_time_fmt_str())

            # 游戏结束时间
            game_end = time.time()
            game_time = int(game_end - game_start)
            game_time_list.append(game_time)

            if not AutoPlayFlag:
                break
            pg_play_again()
    except pg.FailSafeException:
        logger.write_log("Fail-safe triggered. Moving to the statistics section.")

    # 统计每局时间，写入到文件
    for i in range(len(game_time_list)):
        seconds = game_time_list[i] % 60
        minutes = int(game_time_list[i] / 60)
        info = "第%d局用时[%d]分[%d]秒" % (i + 1, minutes, seconds)
        logger.write_log(info)

    # 输出统计信息
    end_time = time.localtime()

    logger.write_log("[%s] 开始挂机" % get_time_fmt_str(start_time))
    logger.write_log("[%s] 结束挂机" % get_time_fmt_str(end_time))

    diff_time_sec = time.mktime(end_time) - time.mktime(start_time)
    t_s = int(diff_time_sec) % 60
    diff_time_sec /= 60
    # 总共所用分钟数
    total_minutes = diff_time_sec
    t_m = int(diff_time_sec) % 60
    diff_time_sec /= 60
    t_h = int(diff_time_sec)

    average_minutes = total_minutes / play_times
    t_ave_m = int(average_minutes)
    t_ave_s = int((average_minutes - t_ave_m) * 60)
    logger.write_log("共挂机[%d]小时[%d]分钟[%d]秒，挂机[%d]局，平均[%d]分钟[%d]秒一局" % (
        t_h, t_m, t_s, play_times, t_ave_m, t_ave_s))

    logger.close_log()

    return True


if __name__ == '__main__':
    pg_main()
    # os.system("pause")
    input("Press Enter to continue...")
