import os

import utils.io as io


class Constants(io.JsonSerializableClass):
    def __init__(self):
        pass


class ExpConstants(Constants):
    def __init__(
            self,
            exp_name='default_exp',
            out_base_dir='/home/tanmay/Data/weakly_supervised_hoi_exp'):
        self.exp_name = exp_name
        self.out_base_dir = out_base_dir
        self.exp_dir = os.path.join(self.out_base_dir,self.exp_name)