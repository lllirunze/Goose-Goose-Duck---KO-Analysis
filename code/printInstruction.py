def write_to_markdown(input_file):
    try:
        # 读取输入文件内容
        with open(input_file, 'r', encoding='utf-8') as infile:
            content = infile.read()

        print(content)

    except FileNotFoundError:
        print(f"错误: 无法找到文件 {input_file}")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    # 输入文件路径
    input_file = "code/instruction.md"  # 请根据需要修改文件名

    # 调用函数
    write_to_markdown(input_file)