import time 

from background_task import background

@background(schedule=60)
def run_model():
    try:
        for i in range(10):
            time.sleep(1)
            print(i)
    except Exception as e:
        print(e)