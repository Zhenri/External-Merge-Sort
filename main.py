import math
import uuid
import tempfile
import sys
import os
import time


def merge(A, p, q, r):
    n1 = q - p + 1
    n2 = r - q 
    L = []
    R = []

    for i in range(n1):
        L.append(A[p + i])
    for j in range(n2):
        R.append(A[q + j + 1])

    L.append(uuid.UUID('ffffffff-ffff-ffff-ffff-ffffffffffff'))
    R.append(uuid.UUID('ffffffff-ffff-ffff-ffff-ffffffffffff'))

    i = 0
    j = 0
    for k in range (p, r + 1):
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
        else: 
            A[k] = R[j]
            j += 1


def merge_sort(A, p, r):
    if p < r:
        q = math.floor((p + r)/2)
        merge_sort(A, p, q)
        merge_sort(A, q + 1, r)
        merge(A, p, q, r)


def sort_and_write(file, A):
    merge_sort(A, 0, len(A) - 1)

    with open(file, 'w') as file:
        for _uuid in A:
            file.writelines(str(_uuid) + "\n")
        file.writelines('ffffffff-ffff-ffff-ffff-ffffffffffff')


print("Insira o limite de memória em MB:")
size = int(input()) * 500000

print("Programa iniciado.")
print("Criando e ordenando chunks...")
time1 = time.time()
with tempfile.TemporaryDirectory() as temp_dir:
#   1ª parte → criar os arquivos temporários:
    temp_files = []
    with open('input.txt', 'r') as file: 
        lines = []
        i = 0
        for line in file:
            lines.append(uuid.UUID(line.strip()))

            if sys.getsizeof(lines) >= size:
                temp_files.append(os.path.join(temp_dir, '{}.txt'.format(i)))
                sort_and_write(temp_files[i], lines)
                i += 1
                lines = []
        
        if len(lines) > 0:
            temp_files.append(os.path.join(temp_dir, '{}.txt'.format(i)))
            sort_and_write(temp_files[i], lines)
            lines = []
    
    time2 = time.time()
    print(len(temp_files), "Chunks criados e ordenados.")
    print("tempo: ", time2 - time1)
    print("Iniciando k-way merge...")

    n_files = len(temp_files)
    
#   2ª parte → k-way merge entre os arquivos temporários:
    with open('ordenado.txt', 'w') as file:
        done = False
        smallests_uuids = [_i for _i in range(n_files)]
        _temp_files = [open(_file, 'r') for _file in temp_files]
        for i in range(n_files):
            smallests_uuids[i] = uuid.UUID(_temp_files[i].readline().strip())

        while not done:
            smallest = min(smallests_uuids)
            
            if str(smallest) == 'ffffffff-ffff-ffff-ffff-ffffffffffff':
                break
              
            file.writelines(str(smallest)+ "\n")

            for i in range(n_files):
                if smallest == smallests_uuids[i]:
                    smallests_uuids[i] = uuid.UUID(_temp_files[i].readline().strip())
        
        for _temp_file in _temp_files:
            _temp_file.close()

    time3 = time.time()
print("K-way Merge finalizado.")
print("tempo: ", time3 - time2)
print("Programa finalizado.")
print("tempo total: ", time3 - time1)
            

