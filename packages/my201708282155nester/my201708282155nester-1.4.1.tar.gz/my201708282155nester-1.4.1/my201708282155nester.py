"""这是一个打印嵌套列表的函数，可以

把列表做为参数传递进去，然后挨项打印

出来。"""
import sys
def print_lol(the_list,indent=False,level=0,whereout=sys.stdout):
    """the_list是要打印项目的列表,indent是否缩进，level是缩进的程度
whereout是输出的目标"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1,whereout)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",end='',file=whereout)
            print(each_item,file=whereout)
