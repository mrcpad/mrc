#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: v0.1
@author: xxf
@site: 
@software: PyCharm
@file: 算法工厂，生产解码算法类
@time: 2019-7-31
"""





class AlgorithmFactorytz():

    @staticmethod
    def create_algorithm(file):

        import lib.judgetype as jt
        from lib.judgetype import ModelDataType
        from module.algorithm.netcdf.netcdf import Nc
        from module.algorithm.netcdf.hdf import HDF
        from module.algorithm.micaps.pymicaps import M4
        import module.algorithm.grib.grib2_info as g2
        from module.algorithm.grib.grib2_info import GRIB2Info
        from module.algorithm.grib.grib1_info import GRIB1Info
        from module.mrc_core.gloalConfig import GloalConfig
        '''
        根据文件类型判断数据类型，输出解码类
        :param file:
        :return:
        '''
        data_type = None
        modelDataType = None
        try:
            modelDataType = jt.judge_model_data_type(file)

            if modelDataType == ModelDataType.NETCDF:  # nc类型
                data_type = Nc(file)

            elif modelDataType == ModelDataType.HDF:
                data_type = HDF(file)

            elif modelDataType == ModelDataType.MICAPS4:

                data_type = M4(file)

            elif modelDataType == ModelDataType.GRIB:
                # 增加判断是GRIB1还是2  xxf  20191210
                if (g2.judgeGribType(file) == "GRIB1"):
                    data_type = GRIB1Info(file)
                else:
                    data_type = GRIB2Info(file, GloalConfig.LibNetPath() + '/grib2Parameters.xml')
                pass


        except:
            return data_type, modelDataType
            # logger.error("AlgorithmFactory error  : ", exc_info=1)

        finally:
            return data_type, modelDataType
