
def write_log(msg):
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(msg + '\n')