'''
Description: It is used to generate web files for convenient visual comparison.
version: 1.0
Author: ThreeStones1029 221620010039@hhu.edu.cn
Date: 2024-02-27 10:16:27
LastEditors: ShuaiLei
LastEditTime: 2024-04-22 12:35:37
'''
from dominate import document
from dominate.tags import div, img, h3, span
import os
import pandas as pd


def gen_images_visualize_data(folder_path2name):
    """
    folder_path2name params(dict):
    """
    # 将图片路径加入到列表
    images_data = []
    exts = ["png", "bmp", "jpg", "jpeg"]
    for file in sorted(os.listdir(list(folder_path2name.keys())[0])):
        if file.split(".")[1] in exts:
            single_image_data = {}
            for folder_path in folder_path2name.keys():
                folder_name = os.path.basename(folder_path2name[folder_path])
                image_path = os.path.join(folder_path, file)
                single_image_data[folder_name] = image_path
            images_data.append(single_image_data)
    return images_data


def gen_visualize_html(images_data, html_save_path):
    doc = document(title="Gt and Result")
    with doc:
        with div(style="display: flex"):
            for folder_name in images_data[0].keys():
                with div(style="flex: 1; text-align:center"):
                    h3(folder_name)
                    for i, data in enumerate(images_data, start=1):
                        img(src=data[folder_name], style="max-width: 90%")
                        with h3():
                            span(f"Image {i}", ":", style="color: red")
                            span(os.path.basename(data[folder_name]))
 
    with open(html_save_path, "w") as f:
        f.write(doc.render())
    print("visualize html generate successfully!")


def from_xlsx2html(results_xlsx_path2title, html_save_path):
    """
    通过xlsx保存的评估数据生成网页
    """
    # 定义文件路径列表
      # 替换为你的文件路径
    html_file = "merged_tables.html"  # 输出的 HTML 文件

    # 初始化 HTML 内容
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Multiple Tables</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h2 { text-align: center; }
            table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
            th { background-color: #f4f4f4; }
        </style>
    </head>
    <body>
    """

    # 遍历每个 Excel 文件，将表格添加到 HTML 内容
    for i, file_path in enumerate(results_xlsx_path2title.keys(), start=1):
        # 读取 Excel 文件
        df = pd.read_excel(file_path)
        
        # 添加标题
        html_content += f"<h2>Table {i} - {results_xlsx_path2title[file_path]}</h2>\n"
        
        # 转换为 HTML 表格
        html_content += df.to_html(index=False, border=1, justify="center")
        html_content += "<br>\n"  # 添加表格之间的间隔

    # 结束 HTML 文件
    html_content += """
    </body>
    </html>
    """
    # 将内容写入到 HTML 文件
    with open(html_save_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"all table save to {html_save_path}")


if __name__ == "__main__":
    images_data = gen_images_visualize_data({"dataset/BUU/test/rotate_gt":"GT",
                                            "runs/detect/rotate": "Predict Rotated Box",
                                            "runs/detect/rotate_point2": "Predict Rotated Box + Point"})
    gen_visualize_html(images_data, "visualize.html")

    results_xlsx_path2title = {"runs/val/rotate_test/eval_results.xlsx": "Test:Rotate (根据0.1 * map50 + 0.9 * map50:95指标训练)", 
                              "runs/val/rotate_point1_test/eval_results.xlsx": "Test:Rotate + point (根据0.1 * map50 + 0.9 * map50:95指标训练)",
                              "runs/val/rotate_point2_test/eval_results.xlsx": "Test:Rotate + point (根据0.1 * map50 + 0.8 * map50:95 + 0.1 * pdmap10:50指标训练)",
                              "runs/val/rotate_val/eval_results.xlsx": "Val:Rotate (根据0.1 * map50 + 0.9 * map50:95指标训练)", 
                              "runs/val/rotate_point1_val/eval_results.xlsx": "Val:Rotate + point (根据0.1 * map50 + 0.9 * map50:95指标训练)",
                              "runs/val/rotate_point2_val/eval_results.xlsx": "Val:Rotate + point (根据0.1 * map50 + 0.8 * map50:95 + 0.1 * pdmap10:50指标训练)"}
    from_xlsx2html(results_xlsx_path2title, "results.html")
