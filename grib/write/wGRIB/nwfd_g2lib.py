from __future__ import print_function
from ncepgrib2 import Grib2Encode
import datetime
import lib.gettime as gt
import os
import configparser
import json

class Data2Grib:

    def __init__(self, confPath):
        self.cfg = 0
        if os.path.exists(confPath):
            cf = configparser.ConfigParser()
            cf.read(confPath, encoding='gbk')
            self.category = int(cf.get('GRIB_smilped', 'category'))
            self.element = int(cf.get('GRIB_smilped', 'element'))
            self.statistical = int(cf.get('GRIB_smilped', 'statistical'))
            self.leveltype = int(cf.get('GRIB_smilped', 'leveltype'))
            self.generating_method = int(cf.get('GRIB_smilped', 'generating_method'))
            self.istimepoint = bool(cf.get('GRIB_smilped', 'istimepoint'))


            self.discipline = int(cf.get('Discipline', 'discipline'))
            self.status = int(cf.get('Discipline', 'status'))



            self.idsect = cf.get('IDsect', 'idsect')
            self.idsect = json.loads(self.idsect)

            self.drtnum = int(cf.get('Section5', 'drtnum'))
            self.drtmpl = cf.get('Section5', 'drtmpl')
            self.drtmpl = json.loads(self.drtmpl)
        else:
            self.cfg = 1
            print('The Configuration file does not exist!')

    def data2grib_info(self,start_lat,start_lon,end_lat,end_lon,len_lat,len_lon,lat_num,lon_num):

        '''网格定义段，
           @param gdsinfo: Sequence containing information needed for the grid definition section.
             - gdsinfo[0] = Source of grid definition  网格定义来源，默认0
             - gdsinfo[1] = Number of grid points in the defined grid. 格点数据个数
             - gdsinfo[2] = Number of octets needed for each additional grid points defn（定义的）.
               Used to define number of points in each row for non-reg grids (=0 for
               regular grid).   默认0，代表规则网格
             - gdsinfo[3] = Interp. of list for optional points defn，默认0，不使用插值
             - gdsinfo[4] = Grid Definition Template Number，格点定义模板，固定为0，等经纬度格点投影
           '''
        # 网格定义段信息
        # section3
        # lat_num = 170  # 纬向格点数
        # lon_num = 229  # 径向格点数
        # # 模板3.0 内容定义
        # start_lat = 26.0
        # start_lon = 97.25
        # end_lat = 34.45
        # end_lon = 108.65
        # len_lat = 0.05
        # len_lon = 0.05

        gdtmpl = [6, 0, 0, 0, 0, 0, 0, lon_num, lat_num, 1, 1000000, start_lat * 1000000, start_lon * 1000000, 48,
                  end_lat * 1000000, end_lon * 1000000, len_lon * 1000000, len_lat * 1000000, 64]

        self.gdtmpl = gdtmpl


    def data2grib_smiple(self,year,month,day,hour,minute,second,forecasttime,timerange,field,ngrdpts,level):

        date_time = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))#起报时间

        '''定义 section0-1
        @discipline:Discipline or GRIB Master Table Number (Code Table 0.0).
         (0 for meteorlogical, 1 for hydrological, 2 for land surface, 3 for space,
         10 for oceanographic products),学科，默认0
        @idsect：Sequence containing identification section (section 1)，section1内容
        Must have len >= 13.
                            listsec1[0]=Id of orginating centre (Common Code Table C-1)，中心点，固定值38，北京
                            listsec1[1]=Id of orginating sub-centre (local table)，子中心点，默认0
                            listsec1[2]=GRIB Master Tables Version Number (Code Table 1.0)，主表版本号，0：时间点产品，8：时间段产品
                            listsec1[3]=GRIB Local Tables Version Number (Code Table 1.1)，固定值0，没有本地表
                            listsec1[4]=Significance of Reference Time (Code Table 1.2)，固定值1，表示起报时间
                            listsec1[5]=Reference Time - Year (4 digits)
                            listsec1[6]=Reference Time - Month
                            listsec1[7]=Reference Time - Day
                            listsec1[8]=Reference Time - Hour
                            listsec1[9]=Reference Time - Minute
                            listsec1[10]=Reference Time - Second
                            listsec1[11]=Production status of data (Code Table 1.3)，产品状态
                                表：Status 产品状态定义
                            VALUE值	REMARKS描述
                            0	正式产品
                            1	测试产品
                            2	科研
                            3	再分析
                            4	TIGGE
                            5	TIGGE测试
    
                            listsec1[12]=Type of processed data (Code Table 1.4)，数据类型，固定值1：预报产品
    
    
    
    
        '''
        # section1
        #discipline = 0  # 学科
        #year = 2019
        #month = 11
        #day = 19
        #hour = 20
        #minute = 0
        #second = 0
        #status = 0  # 产品状态

        #idsect = [38, 0, 0, 0, 1, year, month, day, hour, minute, second, self.status, 1]
        idsects = self.idsect + [date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, self.status, 1]
        # 初始化Grib2Encode类
        ge = Grib2Encode(self.discipline, idsects)

        gdsinfo = [0, ngrdpts, 0, 0, 0]

        '''格点定义模板的内容值，默认使用Template3.0
        @param gdtmpl: Contains the data values for the specified Grid Definition
         Template ( NN=gdsinfo[4] ).  Each element of this integer
         array contains an entry (in the order specified) of Grid
         Definition Template 3.NN，
        
        按照顺序列出Template3.0的值
        
        字节范围	类型	描述	        内容
        15	CHAR	地球模型参数	固定值为6：地球半径为 6,371,229.0米
        16	CHAR	地球模型参数	固定值为0：
        17-20	INT	地球模型参数	固定值为0：
        21	CHAR	地球模型参数	固定值为0：
        22-25	INT	地球模型参数	固定值为0：
        26	CHAR	地球模型参数	固定值为0：
        27-30	INT	地球模型参数	固定值为0：
        31-34	INT	横向格点数	经度方向
        35-38	INT	纵向格点数	纬度方向
        39-42	INT	基本角度单位	固定值为1
        43-46	INT	基本角度份数	固定值为1000000
        47-50	INT	纬度起始点位置	值为：起始纬度* 1000000
        51-54	INT	经度起始点位置	值为：起始经度* 1000000
        55	CHAR	经度和纬度方向的增量信息	值为48
        56-59	INT	纬度终止点位置	值为：终止纬度* 1000000
        60-63	INT	经度终止点位置	值为：终止纬度* 1000000
        64-67	INT	经度方向的格距	值为：经度格距* 1000000
        68-71	INT	纬度方向的格距	值为：纬度格距* 1000000
        72	CHAR	数据的扫描方向	值64表示：经度方向为从小到大，纬度方向为从小到大
        
        '''

        ge.addgrid(gdsinfo, self.gdtmpl)

        '''写入section4-7
        @pdtnum:Product Definition Template Number    
         产品模板编号
         默认0：使用模板4.0（时间点产品[温度，相对湿度，能见度，风-U,风-V,雾，霾，雷暴等]）
         默认8：使用模板4.8（时间段产品[最大温度，最小相对湿度，累积降水等]）
        
        @pdtmpl：Sequence with the data values for the specified Product Definition
         Template (N=pdtnum)，对应产品模板的内容，按照顺序排
        ==================================================================
        产品模版4.0 时间点产品
        字节范围	类型	描述	        内容
        10	CHAR	产品的分类	*Note1
        11	CHAR	产品的编号	*Note2
        12	CHAR	生成方法	2: Forecast预报产品    8：Observation实况产品
        13	CHAR	后台生成进程标识	固定值为0
        14	CHAR	确定分析和预报生成过程	固定值为0
        15-16	SHORT	在起报时间后，需cut-off的数据时间小时部分	固定值为0
        17	CHAR	在起报时间后，需cut-off的数据时间分钟部分	固定值为0
        18	CHAR	时间范围的单位	固定值为1：1小时
        19-22	INT	相对于起报时间，预报时间的时间数	
        23	CHAR	第一层次类型	*Note3
        24	CHAR	第一层次因子	固定值为0
        25-28	INT	第一层次值	*Note4
        29	CHAR	第二层次类型	固定值为255
        30	CHAR	第二层次因子	固定值为0
        31-34	INT	第二层次值	固定值为0
        =====================================================================
        产品模版4.8 时间段产品
        字节范围	类型	描述	内容
        10	CHAR	产品的分类	*Note1
        11	CHAR	产品的编号	*Note2
        12	CHAR	生成方法	2: Forecast预报产品
        8：Observation实况产品
        13	CHAR	后台生成进程标识	固定值为0
        14	CHAR	确定分析和预报生成过程	固定值为0
        15-16	SHORT	在起报时间后，需cut-off的数据时间小时部分	固定值为0
        17	CHAR	在起报时间后，需cut-off的数据时间分钟部分	固定值为0
        18	CHAR	时间范围的单位	固定值为1：1小时
        19-22	INT	相对于起报时间，预报时间的时间数	*Note6
        23	CHAR	第一层次类型	*Note3
        24	CHAR	第一层次因子	固定值为0
        25-28	INT	第一层次值	*Note4
        29	CHAR	第二层次类型	固定值为255
        30	CHAR	第二层次因子	固定值为0
        31-34	INT	第二层次值	固定值为0
        35-36	SHORT	预报结束时间年	
        37	CHAR	预报结束时间月	
        38	CHAR	预报结束时间日	
        39	CHAR	预报结束时间时	
        40	CHAR	预报结束时间分	
        41	CHAR	预报结束时间秒	
        42	CHAR	时间范围的数量	固定为1
        43-46	INT	缺测数据总个数	
        47	CHAR	统计处理方式	*Note5
        48	CHAR	时间增量类型	固定值为2：对于同一起报时间的多个连续的预报，预报时间是递增的
        49	CHAR	预报时间范围单位	固定为1：小时
        50-53	INT	时间范围长度	以49字节为单位
        54	CHAR	递增时间单位	固定为1：小时
        55-58	INT	连续预报时间段的时间增量	
        
        
        @drtnum：Data Representation Template Number，数据表示段 模板编号
        @drtmpl：Sequence with the data values for the specified Data Representation
         Template,对应数据段模板的内容，按照顺序排
        字节范围	类型	    描述	                    内容
        12-15	FLOAT	参考值	                9999
        16-17	SHORT	二进制比例因子	            0
        18-19	SHORT	十进制比例因子	            0
        20	CHAR	Simple压码每个包的字节个数	    24
        21	CHAR	原数据值的类型	                固定为0：原始数据为浮点数
        默认：drtmpl=[9999,0,0,24,0]
        
        @field：numpy array of data points to pack.
         If field is a masked array, then a bitmap is created from
         the mask，格点场数据，按先经度后纬度，经向先西后东（从小到大），纬向先南后北（从小到大）顺序装填
        
        @coordlist：Sequence containing floating point values intended to document
         the vertical discretization with model data
         on hybrid coordinate vertical levels. Default None
        
        '''

        # section 4 产品模板定义
        #isTimePoint = True  # 是否是时间点产品，温度，风，相对湿度，云量等都是时间点的数据，而降水，最高温，最低温，最大相对湿度，最小相对湿度等都是时间段的数据
        pdtnum = 0 if self.istimepoint == True else 8  # 0：时间点产品；8：时间段产品
        # 测试平均温度   某时间点的2米温度，level type:103,level:2,产品模板4.0，unit:k,category:0,element:0,statistical:0,status:0
        #category = 0
        #element = 0

        product_type = self.generating_method  # 2:预报产品    8：实况产品   再分析产品=？
        #statistical = 0
        #time_range = 3  # 相对于起报时间，预报时间的时间数(该模版中的预报时效为每一段的起始预报时间的时间数，如3小时间隔的预报时间的时间数为0，3，6…)
        #level_type = 103
        #level = 2

        #连续预报时间段的时间增量
        #time_increment=0

        if self.istimepoint == True:
            pdtmpl = [self.category, self.element, product_type, 0, 0, 0, 0, 1, forecasttime, self.leveltype, 0, level, 255, 0, 0]
        else:
            # 缺测数据总个数，默认0
            miss_value_count = 0
            # 预报结束时间,根据起报时间+预报时效计算得出，是时间范围
            #forecast_time = gt.addtime_hour(date_time, forecasttime)
            forecast_time = date_time + datetime.timedelta(hours=forecasttime)
            forecast_year = forecast_time.year
            forecast_month = forecast_time.month
            forecast_day = forecast_time.day
            forecast_hour = forecast_time.hour
            forecast_minute = forecast_time.minute
            forecast_second = forecast_time.second

            pdtmpl = [self.category, self.element, product_type, 0, 0, 0, 0, 1, forecasttime, self.leveltype, 0, level, 255, 0, 0,
                      forecast_year, forecast_month, forecast_day, forecast_hour, forecast_hour, forecast_minute,
                      forecast_second, 1, miss_value_count, self.statistical, 2, 1, 49, 1,timerange]

        # section 5
        drtnum = 0
        # section5数据表示段，模板5.0，赋值
        drtmpl = [9999, 0, 0, 24, 0]
        #drtmpl = [1208536781, -3, 1, 24, 0]
        #field = None
        ge.addfield(pdtnum, pdtmpl, self.drtnum, self.drtmpl, field)

        # finalize the grib message.
        ge.end()


        self.message=ge

        # s = pygrib.Grib2Decode('test_masked.grb')
        # print(s)
        # print(s.values)



if __name__ == "__main__":
    gc = Data2Grib('grib_stb_config.conf')

