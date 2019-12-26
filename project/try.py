from configparser import ConfigParser

if __name__ == '__main__':
    parser = ConfigParser()
    parser.read('config.ini')
    data = parser.get('data', 'image_nums')
    print(data)
    parser.set('data', 'image_nums', str(int(data) + 1))
    print(parser.get('data', 'image_nums'))

    with open("config.ini", 'w') as f:
        parser.write(f)
