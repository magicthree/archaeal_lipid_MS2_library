import argparse
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
        merge_at_end=False, merge_wile_processing=True, delete_intermediate=False, merged_file_name='merge.msp',max_peak=1000,min_peak=0.1):
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
        tasks.append([folder_path, paths[i], export_path, 'process-' + str(i) + ' ' + os.path.basename(paths[i]) + '.msp', fix_file,max_peak,min_peak])

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

folder_path = './Files_for_construction'
export_path = './Exported_msp'

if __name__ == '__main__':
    multiprocessing.set_start_method("spawn")
    tt = time.time()
    lock = threading.Lock()

    parser = argparse.ArgumentParser(description="Run multiexport_inline_pool with configurable parameters.")

    parser.add_argument('--folder_path', type=str, default=folder_path, help='Path to the folder to process')
    parser.add_argument('--export_path', type=str,default=export_path, help='Path to export results')
    parser.add_argument('--include_path', type=int, default=2, help='Include path level (default: 2)')
    parser.add_argument('--standardization', type=bool, default=True, help='Whether to standardize peaks(default: True)')
    parser.add_argument('--merge_at_end', type=bool, default=False, help='Merge at end (default: False)')
    parser.add_argument('--merge_while_processing', type=bool, default=True, help='Merge while processing (default: True)')
    parser.add_argument('--delete_intermediate', type=bool, default=False, help='Delete intermediate files (default: False)')
    parser.add_argument('--threads', type=int, default=0, help='Number of threads to use (default: 0)')
    parser.add_argument('--max_peak', type=float, default=1000, help='Maximum peak height after standardization (default: 1000)')
    parser.add_argument('--min_peak', type=float, default=0.1, help='Peak height below will be filtered (default: 0.1)')

    args = parser.parse_args()

    threads_to_use = os.cpu_count() if args.threads == 0 else args.threads
    # 调用主函数
    multiexport_inline_pool(
        folder_path=args.folder_path,
        include_path=args.include_path,
        export_path=args.export_path,
        fix_file=args.standardization,
        merge_at_end=args.merge_at_end,
        merge_wile_processing=args.merge_while_processing,
        delete_intermediate=args.delete_intermediate,
        max_peak=args.max_peak,
        min_peak=args.min_peak,
        threads=threads_to_use
    )

    print("finished with " + str(round(time.time() - tt, 2)) + "s")
