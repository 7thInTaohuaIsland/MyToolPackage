# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 11:10:35 2019

@author: 皮皮酥
"""
import numpy as np
import time
import os
import cv2
import pandas as pd
import pickle
import h5py


class file_writer:
    def numpy_to_excel(self,data: np.array, name: str, path: str):
        data_df = pd.DataFrame(data)
        # change the index and column name
        # data_df.columns = ['A','B','C','D','E','F','G','H','I','J']
        # data_df.index = ['a','b','c','d','e','f','g','h','i','j']
        # create and writer pd.DataFrame to excel
        filename = path + '/' + name + '.xlsx'
        writer = pd.ExcelWriter(filename)
        data_df.to_excel(writer, 'page_1', float_format='%.5f')  # float_format 控制精度
        writer.save()

    def dict_to_excel(self,data: dict, path: str, name: str):
        data_df = pd.DataFrame.from_dict(data, orient='index')
        filename = path + '/' + name + '.xlsx'
        if not os.path.exists(path):
            os.makedirs(path)
        writer = pd.ExcelWriter(filename)
        data_df.to_excel(writer, 'page_1', float_format='%.5f')  # float_format 控制精度
        writer.save()

    def mul_numpy_to_excel(self,data: dict, path: str,name='all'):
        data_df = []
        keys = []
        for key, value in data.items():
            #                print(key)
            keys.append(key)
            temp = pd.DataFrame(value)
            data_df.append(temp)
        data_df_all = pd.concat(data_df, keys=keys)
        filename = path + '/' + name+'.xlsx'
        writer = pd.ExcelWriter(filename)
        data_df_all.to_excel(writer, 'page_1', float_format='%.5f')  # float_format 控制精度
        writer.save()

    def array_data_save(self, data: np.array, name: str, path: str = r'save\arr_data'):
        date = time.strftime("%Y_%m_%d", time.localtime())
        dirs = '{0}_{1}'.format(path, date)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        filename = '{0}/{1}.npy'.format(dirs, name)
        np.save(filename, data)

    def pic_save(self, img, name: str, path: str = r'save\pic'):
        date = time.strftime("%Y_%m_%d", time.localtime())
        dirs = '{0}_{1}'.format(path, date)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        filename = '{0}/{1}.png'.format(dirs, name)
        cv2.imwrite(filename, img)

    def dict_writer(self,name,obj ):
        '''保存字典，name加后缀.pkl'''
        with open(name, 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    def arr_to_h5py(self,output_file, arr,dataset="data"):
        f = h5py.File(output_file, 'w')
        f.create_dataset(dataset, data=arr, dtype=arr.dtype, compression="gzip")  # data是一个numpy数组
        # 添加属性
        f[dataset].attrs['resolution'] = np.array(arr.shape)
        f.close()


class file_reader:
    def file_iterate_abs(self,path,sort:bool=False,filters:list=[])->list:
        abs_list = []
        for root,dirs,files in os.walk(path):
            if not files:
                continue
            else:
                for file in files:
                    if len(filters)>0:
                        for filter in filters:
                            if filter==os.path.splitext(file)[1]:
                                abs_list.append(root+'/'+file)
                                break
                    else:
                        abs_list.append(os.path.join(root,file))
        if sort:
            abs_list = sorted(abs_list,
                           key=lambda x: int(os.path.basename(x).split('.')[0]))
        return abs_list

    def dict_reader(self,name):
        '''读字典，name加后缀.pkl'''
        with open(name, 'rb') as f:
            return pickle.load(f)

    def hdf5_reader(self,infile):
        with h5py.File(infile, "r") as f:
            return f["image"][()]

def FNameSpilt(abs_file_name):
    '''
    :param abs_file_name: absolute path of the file
    :return: list->[path,name,suffix]
    '''
    path=os.path.split(abs_file_name)[0]
    fname=os.path.split(abs_file_name)[1]
    name=os.path.splitext(fname)[0]
    suffix=os.path.splitext(fname)[1]
    return [path,name,suffix]