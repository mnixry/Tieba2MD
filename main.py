from API import TiebaAPI
from argparse import ArgumentParser, Namespace
from logging import basicConfig
from concurrent.futures.thread import ThreadPoolExecutor

COPYRIGHT = r'''
 _____ _      _            _____ ___  ________ 
|_   _(_)    | |          / __  \|  \/  |  _  \
  | |  _  ___| |__   __ _ `' / /'| .  . | | | |
  | | | |/ _ \ '_ \ / _` |  / /  | |\/| | | | |
  | | | |  __/ |_) | (_| |./ /___| |  | | |/ / 
  \_/ |_|\___|_.__/ \__,_|\_____/\_|  |_/___/  

Copyright © 2018-2019 mnixry,All Rights Reserved
Project is publicly available under GPLv3
Github address:https://github.com/mnixry/Tieba2MD

'''

parser = ArgumentParser(description=COPYRIGHT)
parser.add_argument(
    'tid',
    type=int,
)
basicConfig(level=0)

if __name__ == "__main__":
    args = parser.parse_args().__dict__
    with open('test.json', 'wt', encoding='utf-8') as f:
        r = TiebaAPI.content(args['tid'])
        ridList = [i['id'] for i in r['post_list']]
        f.write(TiebaAPI.formatJson(r))
    with open('test2.json', 'wt', encoding='utf-8') as f:
        Pool = ThreadPoolExecutor(64)
        data = Pool.map(lambda x: TiebaAPI.replies(*x),
                        [(args['tid'], i) for i in ridList])
        data = list(data)
        f.write(
            TiebaAPI.formatJson(
                {str(ridList[i]): data[i]
                 for i in range(len(data))}))
