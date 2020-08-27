from datetime import datetime
import tkinter as tk
import configparser
import os

root = tk.Tk()
root.wm_attributes("-alpha", 0.95)
root.wm_attributes("-toolwindow", True)
root.wm_attributes("-topmost", False)
root.overrideredirect(True)
root.configure(background="SeaGreen")

base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/conf.ini"
config = configparser.ConfigParser()
config.read(file_path)

if("pos" in config.sections()):
  frame = '382x269+%s+%s' % (config.get("pos", "pos_x"),config.get("pos", "pos_y") )
  root.geometry(frame)
else:
  config.add_section("pos")

w = tk.Label(root, font=("宋体", 20), fg="WhiteSmoke",background="SeaGreen")
w.pack()
w2 = tk.Label(root, font=("宋体", 20), fg="WhiteSmoke",background="SeaGreen")
w2.pack()
click_x,click_y = 0,0


def drag(event):
  global click_x, click_y
  frame = '382x269+%s+%s'  % (root.winfo_x()-click_x+event.x,root.winfo_y()+event.y-click_y)
  root.geometry(frame)
  config.set('pos', 'pos_x', str(root.winfo_x()))
  config.set('pos', 'pos_y', str(root.winfo_y()))

  with open(file_path, 'w')as conf:
    config.write(conf)

def click(event):
  global click_x, click_y
  click_x, click_y = event.x,event.y


def getTipsString(target_name,target_time):
  now_datetime = datetime.now()
  time_struct = datetime.strptime(target_time, "%Y-%m-%d %H:%M:%S")
  total_seconds = (time_struct-now_datetime).total_seconds()
  m, s = divmod(abs(total_seconds), 60)
  h, m = divmod(m, 60)
  d, h = divmod(h, 24)
  return "%s到现在\n %s%d天%d小时%d分%d秒" %\
              (target_name,"已过" if total_seconds<0 else"还有" , abs(d), h,m,s)

def updateTime():
  target_time = '2017-10-18 09:00:00'
  target_time2 = '2020-10-03 00:00:00'
  w["text"] = getTipsString("十九大",target_time)
  w2["text"] = getTipsString("萌萌生日",target_time2)
  root.after(1000, updateTime)

root.after(1000, updateTime)
root.bind("<B1-Motion>",drag)
root.bind("<Button-1>", click)

root.mainloop()
