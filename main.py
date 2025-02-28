from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import time
from core.analysis_manager import global_analysis_manager

mapping = {
  0: [1, 2, 3],
  1: [2, 5],
  2: [1, 4],
  14:[7],
}

#global_analysis_manager.analyze(mapping)
thread = Thread(target = global_analysis_manager.analyze, args = (mapping, ))
thread.start()


time.sleep(5)
while global_analysis_manager.analysis_in_progress == True:
  print(global_analysis_manager.get_state())
  time.sleep(5)

thread.join()