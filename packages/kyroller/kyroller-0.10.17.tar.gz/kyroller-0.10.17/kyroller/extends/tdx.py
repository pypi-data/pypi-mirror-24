import comtypes.client as cc
import time
from enum import Enum
from datetime import datetime
from ..types import *
import random
import json


class AccountType(Enum):
    LOGINIACCOUNTTYPE_SZA = 0
    LOGINIACCOUNTTYPE_SHA = 1
    LOGINIACCOUNTTYPE_SZB = 2
    LOGINIACCOUNTTYPE_SHB = 3
    LOGINIACCOUNTTYPE_CAPITAL = 8
    LOGINIACCOUNTTYPE_CUSTOMER = 9
    LOGINIACCOUNTTYPE_THREEBOARD = 12
    LOGINIACCOUNTTYPE_MNCS = 50


class BrokerType(Enum):
    BROKERTYPE_UNKNOWN = 0
    BROKERTYPE_CJZQ = 1
    BROKERTYPE_DYCY = 2
    BROKERTYPE_DGZQ = 3
    BROKERTYPE_GXZQ = 4
    BROKERTYPE_LHZQ = 6
    BROKERTYPE_PAZQ = 7
    BROKERTYPE_GFZQ = 12
    BROKERTYPE_DTZQ = 13
    BROKERTYPE_HXZQ = 14
    BROKERTYPE_XYZQ = 15
    BROKERTYPE_ZSZQ = 16
    BROKERTYPE_JYDT = 17
    BROKERTYPE_ZXJT = 18
    BROKERTYPE_YNHT = 19
    BROKERTYPE_CCZQ = 20
    BROKERTYPE_HYZQ = 21
    BROKERTYPE_GTJA = 22
    BROKERTYPE_SJZQ = 23
    BROKERTYPE_AXZQ = 24
    BROKERTYPE_CFZQ = 25
    BROKERTYPE_DXZQ = 26
    BROKERTYPE_YHZQ = 27
    BROKERTYPE_GDZQ = 28
    BROKERTYPE_YDZQ = 29
    BROKERTYPE_DBZQ = 30
    BROKERTYPE_NJZQ = 31
    BROKERTYPE_ZXZQ = 32
    BROKERTYPE_SHZQ = 33
    BROKERTYPE_HBZQ = 34
    BROKERTYPE_AJZQ = 35
    BROKERTYPE_QLZQ = 36
    BROKERTYPE_ZYGJ = 37
    BROKERTYPE_MZZQ = 38
    BROKERTYPE_XCZQ = 39
    BROKERTYPE_GJZQ = 40
    BROKERTYPE_SCZQ = 41
    BROKERTYPE_GLZQ = 42
    BROKERTYPE_HLZQ = 43
    BROKERTYPE_HFZQ = 44
    BROKERTYPE_GYZQ = 45
    BROKERTYPE_GZZQ = 46
    BROKERTYPE_FZZQ = 47
    BROKERTYPE_BHZQ = 48
    BROKERTYPE_XNZQ = 49
    BROKERTYPE_XSDZQ = 50
    BROKERTYPE_ZTZQ = 51
    BROKERTYPE_HRZQ = 52
    BROKERTYPE_SYWG = 53
    BROKERTYPE_SHXZQ = 54
    BROKERTYPE_JLDB = 56
    BROKERTYPE_MSZQ = 57
    BROKERTYPE_SXDT = 58
    BROKERTYPE_ZCZQ = 59
    BROKERTYPE_XMZQ = 60
    BROKERTYPE_DFZQ = 61
    BROKERTYPE_YTZQ = 62
    BROKERTYPE_JLDT = 67
    BROKERTYPE_WHZQ = 68
    BROKERTYPE_GKZQ = 69
    BROKERTYPE_ZXWT = 70
    BROKERTYPE_XDZQ = 71
    BROKERTYPE_WKZQ = 72
    BROKERTYPE_JHZQ = 73
    BROKERTYPE_HCZQ = 74
    BROKERTYPE_TPYZQ = 75
    BROKERTYPE_GHZQ = 76
    BROKERTYPE_DHZQ = 77
    BROKERTYPE_XBZQ = 78
    BROKERTYPE_SXZQ = 79
    BROKERTYPE_KYZQ = 80
    BROKERTYPE_HAHX = 81
    BROKERTYPE_GSZQ = 83
    BROKERTYPE_ZJZXJT = 84
    BROKERTYPE_SCHX = 85
    BROKERTYPE_WLZQ = 89
    BROKERTYPE_LNZT = 90
    BROKERTYPE_NMHT = 92
    BROKERTYPE_TFZQ = 93
    BROKERTYPE_GSHL = 94
    BROKERTYPE_RXZQ = 95
    BROKERTYPE_ZHZQ = 96
    BROKERTYPE_CTZQ = 98
    BROKERTYPE_HTZQ = 102
    BROKERTYPE_DWZQ = 103
    BROKERTYPE_ZJZS = 104
    BROKERTYPE_LXZQ = 106
    BROKERTYPE_SHHX = 107
    BROKERTYPE_XZTX = 109
    BROKERTYPE_ZYZQ = 110
    BROKERTYPE_BJGD = 111
    BROKERTYPE_ZJZQ = 114
    BROKERTYPE_SXZY = 116
    BROKERTYPE_MNCS = 117
    BROKERTYPE_MNCP = 118
    BROKERTYPE_KT = 996
    BROKERTYPE_DZH = 997
    BROKERTYPE_THS = 998
    BROKERTYPE_TDX = 999


class TdxAccount(Account):
    def __init__(self, serverIp: str, serverPort: int, loginId: str, tradePassword: str, brokerType: BrokerType, accountType=AccountType.LOGINIACCOUNTTYPE_CAPITAL, departmentID=0, isCreditAccount=False, enableLog=True):
        Account.__init__(self, 0)
        self._com_obj = cc.CreateObject('ZMStockCom.StockTrade')
        self._com_obj.AutoReportSuccess = True
        self._com_obj.CreditAccount = isCreditAccount
        self._com_obj.AutoReportSuccess = True
        self._com_obj.AutoKeepConn = False
        self._com_obj.Init("8.03", 1)
        self._com_obj.EnableLog = enableLog
        self._com_obj.BrokerType = brokerType.value  # ZMStockCom.BROKERTYPE_HLZQ
        self._com_obj.AccountType = accountType.value
        self._com_obj.CurServerHost = serverIp
        self._com_obj.CurServerPort = serverPort
        self._com_obj.LoginID = loginId
        self._com_obj.TradeAccount = '051600000090'
        self._com_obj.DepartmentID = departmentID  # 营业部id
        self._com_obj.TradePassword = tradePassword
        if not self._com_obj.Login(False):
            raise Exception(self._com_obj.LastErrDesc)
        print('登录成功，开始更新资产信息')
        self.sync_assets()

    @staticmethod
    def gen_ex_id():
        return datetime.now().strftime('tdx%Y%m%d%H%M%S') + str(random.randrange(1000000, 9999999))

    def sync_assets(self):
        # 获取资金信息
        queryRecord = self._com_obj.queryTradeData(
            self._com_obj.CurTradeId, 1)   # ZMStockCom.STOCKQUERYTYPE_CAPITAL
        dic = json.loads(queryRecord.GetJsonString())
        assert(len(dic) == 1)
        assetsDic = dic[0]
        self._balance = assetsDic['可用资金']
        self._frozen_balance = assetsDic['冻结资金']
        # 获取持仓信息

        print(assetsDic)
