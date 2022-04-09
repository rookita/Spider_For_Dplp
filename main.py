# coding: utf-8
from utils import *
from myclass import *
from option import *

if __name__ == "__main__":
    args = BaseOptions().parse()
    author = Author(args.author_name,args.school,args.department,args.city,args.country)
    cmp_info,url = get_author_url(author)
    if args.print_cmp_info:
        cmp_info.print_cmp_info()
    if  isinstance(url,str):
        P = Papers(author)
        P.parse()
        P.print_paper()


