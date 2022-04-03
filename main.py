# coding: utf-8
import Utils
import Class
import Option

if __name__ == "__main__":
    args = Option.BaseOptions().parse()
    author = Class.Author(args.author_name,args.school,args.department,args.city,args.country)
    m = Utils.get_author_url(author)
    if  isinstance(m,str):
        P = Class.Papers(m,author.name)
        P.parse()
        P.print_paper()


