"""This is just a exercise, I am a python beginner."""

def print_lol(a_list,indent=False,level=0,fn=sys.stdout):
    for each in a_list:
        if isinstance(each,list):
            print_lol(each,indent,level+1,fn)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",end='',file=fn)
            print(each,file=fn)

