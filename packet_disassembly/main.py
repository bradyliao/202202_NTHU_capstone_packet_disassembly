import re
import codecs
#test github 20220504
#test 20220508
# test again
#test on windows

def pack_bcd(code):
    return int(code)

def hex_to_string(hex):
    if hex[:2] == '0x':
        hex = hex[2:]
    string_value = bytes.fromhex(hex).decode('utf-8')
    return string_value


# 4 hex digit
def message_type(code):
    switcher = {#         TM code
        # 每個 Multicast Group
        "3031": "I001", # 01 心跳訊息
        "3032": "I002", # 02 序號重置訊息

        # 期貨
        # "3131": "I010", # 11 商品漲跌幅及基本資料訊息
        # "3132": "I030", # 12 商品委託量累計訊息
        # "3133": "I011", # 13 契約基本資料
        # "3134": "I050", # 14 公告訊息
        # "3135": "I060", # 15 現貨標的資訊揭示
        # "3136": "I120", # 16 股票*期貨*與現貨標的對照表
        # "3137": "I130", # 17 契約調整檔
        # "3138": "I064", # 18 現貨標的試撮與狀態資訊
        #
        # "3233": "I140", # 23 系統訊息
        # "3234": "I100", # 24 詢價揭示訊息
        "3241": "I081", # 2A 委託簿揭示訊息
        "3242": "I083", # 2B 委託簿快照訊息
        # "3243": "I084", # 2C 快照更新訊息
        "3244": "I024", # 2D 成交價量揭示訊息
        # "3245": "I025", # 2E 盤中最高低價揭示訊息
        #
        # "3331": "I070", # 31 收盤行情資料訊息
        # "3332": "I071", # 32 收盤行情訊息含結算價
        # "3333": "I072", # 33 行情訊息含結算價及未平倉合約數
        # "3334": "I073", # 34 複式商品收盤行情資料訊息
        #
        # # 選擇權
        # "3431": "I010", # 41 商品漲跌幅及基本資料訊息
        # "3432": "I030", # 42 商品委託量累計訊息
        # "3433": "I011", # 43 契約基本資料
        # "3434": "I050", # 44 公告訊息
        # "3435": "I060", # 45 現貨標的資訊揭示
        # "3436": "I120", # 46 股票*選擇權*與現貨標的對照表
        # "3437": "I130", # 47 契約調整檔
        # "3438": "I064", # 48 現貨標的試撮與狀態資訊
        #
        # "3533": "I140", # 53 系統訊息
        # "3534": "I100", # 54 詢價揭示訊息
        "3541": "I081", # 5A 委託簿揭示訊息
        "3542": "I083", # 5B 委託簿快照訊息
        # "3543": "I084", # 5C 快照更新訊息
        "3544": "I024", # 5D 成交價量揭示訊息
        # "3545": "I025", # 5E 盤中最高低價揭示訊息
        #
        # "3631": "I070", # 61 收盤行情資料訊息
        # "3632": "I071", # 62 收盤行情訊息含結算價
        # "3633": "I072", # 63 行情訊息含結算價及未平倉合約數
        # "3634": "x   ", # 64 x
    }
    return switcher.get(code, "x   ")


# 12 hex digit
def information_time(code):
    return (pack_bcd(code[0:2]), pack_bcd(code[2:4]), pack_bcd(code[4:6]), pack_bcd(code[6:9]), pack_bcd(code[9:12]))

# 4 hex digit
def channel_id(code):
    return pack_bcd(code)

# 10 hex digit
def channel_seq(code):
    return pack_bcd(code)

# 2 hex digit
def version_no(code):
    return pack_bcd(code)

# 4 hex digit
def body_length(code):
    return pack_bcd(code)


def prod_id(code):
    return hex_to_string(code)

def prod_msg_seq(code):
    return pack_bcd(code)

def calculated_flag(code):
    return hex_to_string(code)

# 12 hex digit
def match_time(code):
    return (pack_bcd(code[0:2]), pack_bcd(code[2:4]), pack_bcd(code[4:6]), pack_bcd(code[6:9]), pack_bcd(code[9:12]))

def sign(code):
    if hex_to_string(code) == "1" :
        return "-"
    elif hex_to_string(code) == "0" :
        return "+"

# 10 hex digit
def first_match_price(code):
    return pack_bcd(code)

# 8 hex digit
def first_match_qty(code):
    return pack_bcd(code)


#def check_check_sum(content, check_sum):

# I024 process
def I024(data):
    #                                                                         info
    #                                                                         in
    #                                                                         packet counted
    #                                                                         byte   byte
    #       id   T M     MT   小時   分鐘   秒    ms    us   c-id  c_seq  v_no  len_c  len_d prod_id prod_msg_seq  calculated_flag 小時   分鐘   秒    ms    us    sign  1st m $  1st m #
    print("{:>8} {:>4} {:>4} {:>2} {:>2} {:>2} {:>3} {:>3} {:>4} {:>10} {:>2} {:>3}  {:>5}  {:>20}   {:>10}      {:>1}           {:>2} {:>2} {:>2} {:>3} {:>3} {:>1} {:>10}   {:>8} "
            .format(
            id, data[2:6], message_type(data[2:6]) ,
            information_time(data[6:18])[0], information_time(data[6:18])[1], information_time(data[6:18])[2], information_time(data[6:18])[3], information_time(data[6:18])[4],
            channel_id(data[18:22]), channel_seq(data[22:32]), version_no(data[32:34]), body_length(data[34:38]), len(data[38:-6])/2,
            # I024
            prod_id(data[38:78]), prod_msg_seq(data[78:88]), calculated_flag(data[88:90]),
            match_time(data[90:102])[0], match_time(data[90:102])[1], match_time(data[90:102])[2], match_time(data[90:102])[3], match_time(data[90:102])[4],
            sign(data[102:104]), first_match_price(data[104:114]), first_match_qty(data[114:122])
            ) #.format)
            ) #print)
    return


def I083(data):







file_read = open("MarketDataLog_20220215_23615.log", "rb")
#file_read = open("udp_Sniffer_20220216.log", "rb")
byte_form = file_read.read(100000)
file_read.close()



hex_form = byte_form.hex()
extract_result = re.findall(r'1b.*?0d0a', hex_form)

# split with "1b", "0d0a"
#extract_result = re.split('(1b|0d0a)', hex_form)


x_count = 0



file_write = open("export_py.txt","w")



for id, data in enumerate(extract_result) :


    file_write.write(str(id) + " " + message_type(data[2:6]) + '\n')




    if message_type(data[2:6]) == "x   " :
        print()
        x_count += 1
        continue

    if message_type(data[2:6]) == "I024":
        I024(data)
        continue

    if message_type(data[2:6]) == "I083":
        I083(data)
        continue






file_write.close()
