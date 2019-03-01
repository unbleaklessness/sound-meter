import serial
import tkinter
import threading

class GUI:
  def __init__(self, master):
    self.master = master

    self.label_text = tkinter.StringVar()
    self.label = tkinter.Label(master, textvariable = self.label_text)
    self.label.pack()

class GUIThread(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)

  def run(self):
    print('GUI thread started.')

    self.root = tkinter.Tk()
    self.gui = GUI(self.root)
    self.root.mainloop()

    print('TEST')
  
  def set_gui_label(self, text):
    self.gui.label_text.set(text)
  
class SerialThread(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  
  def run(self):
    print('Serial thread started.')

    with serial.Serial('/dev/ttyUSB0') as s:
      line = s.readline()
      self.callback(line)
  
  def set_serial_callback(self, callback):
    self.callback = callback

def main():
  gui_thread = GUIThread()
  serial_thread = SerialThread()

  serial_thread.set_serial_callback(gui_thread.set_gui_label)

  gui_thread.start()
  serial_thread.start()

  gui_thread.join()
  serial_thread.join()

if __name__ == '__main__':
  main()