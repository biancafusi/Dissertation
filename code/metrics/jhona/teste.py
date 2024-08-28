import Parameters as Pa
import logging
import threading
import time
import f_metrix as f
import numpy as np


def call_funtion(part):

    logging.info("Thread %s: starting", part)
    #part = int(part)
    f.indices_varying_rmax(Pa.data_era5, part, Pa.out_era5+'/%s'%part[0], prefix='ERA5')
    #time.sleep(10+part[0])
    logging.info("Thread %s: finishing", part)

    return

if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    rmin    =0 #tempo
    rmax    =744
    nrange  =4
    rdef    = np.linspace(rmin,rmax,nrange,endpoint=True)
    rdef[0] = 0.01

    nthreads= nrange-1

    threads = list()
    for i in range(0,nthreads):

       part=[rdef[i],rdef[i+1]]  
       logging.info("Main    : create and start thread %d.", i)
       x = threading.Thread(target=call_funtion, args=(part,))
       threads.append(x)
       x.start()


    ##for index, thread in enumerate(threads):
    ##    logging.info("Main    : before joining thread %d.", index)
    ##    thread.join()
    ##    logging.info("Main    : thread %d done", index)


