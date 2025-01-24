import functools
import multiprocessing
import os
import time
import threading
import sys
from tqdm import tqdm
from Methods import subpath
from Methods import link_msps
from SingleExport import single_msp_export

def multiexport_inline_pool(folder_path = './Files_for_construction', include_path=2, export_path='./Exported_msp', fix_file=True, threads=4,
        merge_at_end=False, merge_wile_processing=True, delete_intermediate=False, merged_file_name='merge.msp'):
    # read method
    if merge_at_end and merge_wile_processing:
        print("please chose 1 or 0 merge method")
        sys.exit()
    pool = multiprocessing.Pool(processes=threads)
    t = time.time()

    if merge_wile_processing:
        print('merging while exporting')
    elif merge_at_end:
        print('merging after exported')

    # Create jobs
    paths = subpath(folder_path, include_path)
    tasks = []
    pbar = tqdm(total=len(paths))

    if threads < len(paths):  # Align jobs
        paths.sort(key=lambda x: os.path.getsize(os.path.join(folder_path, x)), reverse=True)
        paths = paths[int(-threads / 2):] + paths[:int(-threads / 2)]

    for i in range(0, len(paths)):
        tasks.append([folder_path, paths[i], export_path, 'process-' + str(i) + ' ' + os.path.basename(paths[i]) + '.msp', fix_file])

    if merge_wile_processing:
        merge_path = os.path.join(export_path, merged_file_name)
        if os.path.exists(merge_path):
            os.remove(merge_path)

    # Submit jobs
    results = []

    for i, task in enumerate(tasks):  
        start_time = time.time()
        if merge_wile_processing:
            callback_with_args = functools.partial(merge_while_export, epath=task[2], efilename=merged_file_name, pbar=pbar)
        else:
            callback_with_args = lambda _: pbar.update(1)
        result = pool.apply_async(single_msp_export, args=(*task,), callback=callback_with_args)
        results.append((result, start_time))  

    pool.close()
    pool.join()
    pbar.close()
    if merge_at_end:
        print("start merging at: " + str(round(time.time() - t, 2)) + "s")
        link_msps(export_path, export_path, merged_file_name, 2)

    if delete_intermediate:
        for file in os.listdir(export_path):
            if 'process-' in file:
                os.remove(os.path.join(export_path, file))
    print("All finished at: " + str(round(time.time() - t, 2)) + "s")


def merge_while_export(finished_file, epath, efilename, pbar):
    pbar.update(1)

    with lock:
        wfile = open(epath + '/' + efilename, 'a', encoding="utf-8")
        for line in open(epath + '/' + finished_file, errors='ignore'):
            wfile.writelines(line)
        if line != '\n':
            wfile.write('\n')

#change the dir of the source files
folder_path = './Files_for_construction'
export_path = './Exported_msp'

if __name__ == '__main__':
    multiprocessing.set_start_method("spawn")
    tt = time.time()
    lock = threading.Lock()
    #change the parameters
    multiexport_inline_pool(folder_path = folder_path, include_path=2, export_path=export_path, fix_file=True,
        merge_at_end=False, merge_wile_processing=True, delete_intermediate=False,threads=6)
    print("finished with " + str(round(time.time() - tt, 2)) + "s")
