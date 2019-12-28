from argparse import ArgumentParser

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
parser.add_argument('tid',metavar='N',type=int)
parser.add_argument('--debug','-d',action='store_true',default=False)
parser.add_argument('--without-image','-NI',action='store_false',default=True)