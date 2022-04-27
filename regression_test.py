import yaml
from utils.regression_tool import test





if __name__ == '__main__':
    with open('api.yaml') as f:
        content = yaml.load(f,Loader=yaml.FullLoader)
        f.close()
        type = 'btc'
        # for code in os.listdir(line_5_path)[0:10]:
        #     test(normal_5_path, code,content)
        test(type, content)