import time
import pymysql
import json

route_list =[]
def routee(path):
    def func_out(fn):
        route_list.append((path,fn))
        print('记录日志:有人访问啦' + time.ctime())
        def func_in(*args,**kwargs):
            # print('记录日志:有人访问啦in'+time.ctime())
            result = fn(*args,**kwargs)
            return result
        return func_in
    return func_out

@routee('/index.html')

def index():
    status = '200 OK'
    headers = [("Server","YUMI/2.0")]
    with open('template/index.html','r')as r:
        html_data = r.read()
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='mysql', database='stock_db',
                           charset='utf8')
    cs = conn.cursor()
    sql = 'select * from info;'
    cs.execute(sql)
    info_list = cs.fetchall()
    cs.close()
    conn.close()
    # print(info_list)  # ================================
    mysql_data = ''
    for row in info_list:
        mysql_data += '''<tr>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td><input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="000007"></td>
                </tr>''' % row


    data = html_data.replace('{%content%}',time.ctime()+mysql_data)

    return status,headers,data

@routee('/center_data.html')
def center_data():#=====================center_data==================================
    status = '200 OK'
    headers = [("Server","YUMI/2.0"),('Content-Type','text/html;charset=utf-8')]

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='mysql', database='stock_db',
                           charset='utf8')
    cs = conn.cursor()
    sql = 'select i.code,i.short,i.chg,i.turnover,i.price,i.highs,f.note_info from focus as f inner join info as i on f.info_id=i.id;'
    cs.execute(sql)
    info_list  = cs.fetchall()
    cs.close()
    conn.close()
    info_dict_list=[]
    for row in info_list:

        dict_info = {}
        dict_info["code"] = row[0]
        dict_info["short"] = row[1]
        dict_info["chg"] = str(row[2])
        dict_info["turnover"] = str(row[3])
        dict_info["price"] = str(row[4])
        dict_info["highs"] = str(row[5])
        dict_info["note_info"] = row[6]
        info_dict_list.append(dict_info)

    json_str = json.dumps(info_dict_list,ensure_ascii=False)
    return status,headers,json_str

def no_found():
    status = '404 Not Found'
    headers = [('Server', 'YUMI/2.0')]
    data = 'not found'
    return status, headers, data

@routee('/center.html')
def center():#=======================================================
    status = '200 OK'
    headers = [("Server","YUMI/2.0")]
    with open('template/center.html','r')as r:
        html_data = r.read()
    data = html_data.replace('{%content%}','')
    return status,headers,data

def no_found():
    status = '404 Not Found'
    headers = [('Server', 'YUMI/2.0')]
    data = 'not found'
    return status, headers, data



def handle_request(env):
    request_path = env['request_path']
    for path, funcc in route_list:
        if request_path == path:
            result = funcc()
            return result
    else:
        result = no_found()
        return result



    # if request_path == '/index.html':
    #     result = index()
    #     return result
    #
    # elif request_path == '/center.html':
    #     result = center()
    #     return result
    # else:
    #     result = no_found()
    #     return result

