'''
每執行這個程式一次, 就會清除logfile.log的前 
'''

def clear_log_file(file_path, lines_to_remove):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if len(lines) <= lines_to_remove:
        # 如果要刪除的行數超過或等於文件中的行數，那麼整個文件都會被清除
        open(file_path, 'w').close()
    else:
        # 刪除前 lines_to_remove 行，並將剩餘行寫回文件
        with open(file_path, 'w') as file:
            file.writelines(lines[lines_to_remove:])


file_path = '/home/ken/pttCrawler/logfile.log'
lines_to_remove = 300
clear_log_file(file_path, lines_to_remove)
