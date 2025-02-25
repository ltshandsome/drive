import os
from collections import defaultdict

# 定義分割大小：25MB（以位元組為單位）
CHUNK_SIZE = 25 * 1024 * 1024

def split_files(source_folder, output_folder):
    """
    將 source_folder 中的每個檔案分割成不超過 25MB 的小檔案，
    並將分割後的檔案命名為 original_name_1, original_name_2, ...，
    儲存到 output_folder 中。
    
    Args:
        source_folder (str): 包含原始檔案的來源資料夾路徑
        output_folder (str): 分割後檔案的儲存資料夾路徑
    """
    # 確保輸出資料夾存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 遍歷來源資料夾中的所有檔案
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)
        if os.path.isfile(file_path):  # 確認是檔案而非子資料夾
            with open(file_path, 'rb') as f:
                part_num = 1
                while True:
                    # 每次讀取 25MB 大小的資料
                    chunk = f.read(CHUNK_SIZE)
                    if not chunk:  # 資料讀完則退出
                        break
                    # 將資料寫入新的分割檔案
                    output_file = os.path.join(output_folder, f"{filename}_{part_num}")
                    with open(output_file, 'wb') as out_f:
                        out_f.write(chunk)
                    part_num += 1

def merge_files(source_folder, output_folder):
    """
    將 source_folder 中的分割檔案（例如 x.pdf_1, x.pdf_2, ...）
    合併回原始檔案（例如 x.pdf），並儲存到 output_folder 中。
    
    Args:
        source_folder (str): 包含分割檔案的來源資料夾路徑
        output_folder (str): 合併後檔案的儲存資料夾路徑
    """
    # 確保輸出資料夾存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 使用字典來分組分割檔案
    groups = defaultdict(list)
    
    # 遍歷來源資料夾中的所有檔案
    for filename in os.listdir(source_folder):
        # 以最後一個底線分割檔案名稱
        parts = filename.rsplit('_', 1)
        if len(parts) == 2 and parts[1].isdigit():  # 確認符合分割檔案的命名格式
            base_name = parts[0]  # 基礎名稱，例如 "x.pdf"
            part_num = int(parts[1])  # 分割編號，例如 1, 2, ...
            groups[base_name].append((part_num, filename))
    
    # 對每個基礎名稱進行合併
    for base_name, file_list in groups.items():
        # 按分割編號排序
        sorted_files = sorted(file_list)
        output_file = os.path.join(output_folder, base_name)
        with open(output_file, 'wb') as out_f:
            for _, filename in sorted_files:  # 依序讀取每個分割檔案
                part_file = os.path.join(source_folder, filename)
                with open(part_file, 'rb') as in_f:
                    out_f.write(in_f.read())
                    
#split_files("Computer organization note", "Computer organization note (splitted)")
merge_files("Computer organization note (splitted)", "Computer organization note (merge test)")