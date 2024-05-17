# main.py

from pyvmg import VMGReader, XMLWriter, CSVWriter, TextWriter

def main():
    # 設定輸入和輸出路徑
    input_dir = '.'  # 當前目錄
    output_xml = 'output.xml'
    output_csv = 'output.csv'
    output_txt = 'output.txt'

    # 初始化寫入器
    xml_writer = XMLWriter(output_xml)
    csv_writer = CSVWriter(output_csv)
    txt_writer = TextWriter(output_txt)

    # 處理目錄中的所有 .vmg 文件
    xml_writer.processdir(input_dir)
    csv_writer.processdir(input_dir)
    txt_writer.processdir(input_dir)

    # 寫入文件
    xml_writer.write()
    csv_writer.write()
    txt_writer.write()

    print(f"轉換完成！文件已保存為 {output_xml}, {output_csv}, 和 {output_txt}")

if __name__ == "__main__":
    main()

