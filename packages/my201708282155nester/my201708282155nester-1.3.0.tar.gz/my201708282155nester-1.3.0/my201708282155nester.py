"""本函数定义了列表的打印，子列表

可以选择是否缩进"""
def print_lol(the_list,indent=False,level=0):
    """参数１是必须的，传递待打印的列表给函数
       参数２是可选的，默认为０"""
    for    each_item    in    the_list:
        if    isinstance(each_item,list):
            print_lol(each_item,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print('\t',end='')
            print(each_item)	
