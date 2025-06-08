import csv
from rdkit import Chem
from rdkit.Chem import Draw
import concurrent.futures
import os

def smiles_to_image(smiles, output_file):
    mol = Chem.MolFromSmiles(smiles)
    if mol is not None:
        img = Draw.MolsToImage([mol])
        img.save(output_file)
        return True
    else:
        print(f"Invalid SMILES string: {smiles}")
        return False

if __name__ == "__main__":
    csv_file = r'.\data\metabolites\metabolites-2025-04-19.csv'  # 替换为你的CSV文件路径
    tasks = []
    output_dir = r'.\Fig\smiles'
    # 检查文件夹是否存在，不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    valid_count = 0
    line = 248137
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # 跳过表头
        for row in reader:
            smiles = row[2]
            hmdb_id = row[0]
            output_file = os.path.join(output_dir, f"{hmdb_id}.png")
            # 检查 SMILES 字符串是否有效
            mol = Chem.MolFromSmiles(smiles)
            if mol is not None:
                tasks.append((smiles, output_file))
                valid_count += 1
                if valid_count == 10000:
                    break

    success_count = 0
    # 使用线程池执行任务
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(smiles_to_image, smiles, output_file) for smiles, output_file in tasks]
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                success_count += 1
                print(f"已成功生成 {success_count} 个图像。")