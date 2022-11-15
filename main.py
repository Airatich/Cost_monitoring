from prod1 import main_prod_1
from prod2 import main_prod_2
from prod3 import main_prod_3
from prod4 import main_prod_4

import time
def start():
    start_time=time.time()
    try:
        print('Выгружаю Лист_рулон_гк')
        main_prod_1()
    except Exception:
        print("Выскочила капча, зайди на сайт, пройди ее и запусти код по новой")

    try:
        print('Выгружаю Лист_рулон_хк')
        main_prod_2()
    except Exception:
        print("Выскочила капча, зайди на сайт, пройди ее и запусти код ,начиная с выгрузки Лист_рулон_хк")

    try:
        print('Выгружаю Лист_рулон_оцинк')
        main_prod_3()
    except Exception:
        print("Выскочила капча, зайди на сайт, пройди ее и запусти код ,начиная с выгрузки Лист_рулон_оцинк")

    try:
        print('Выгружаю Лист_рулон_окраш')
        main_prod_4()
    except Exception:
        print("Выскочила капча, зайди на сайт, пройди ее и запусти код ,начиная с выгрузки Лист_рулон_окраш")

    print(f"TOTAL TIME: {time.time() - start_time}")


start()