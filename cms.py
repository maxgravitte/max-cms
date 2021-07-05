#Content Management System for my website
#Inspired by Luke Smith's lb: https://github.com/LukeSmithxyz/lb


#path to directory of html articles
#path to list of chronological entries (list.html)
#path to list of topics or tags (topics.html)

#maintain chronological list (date)
#maintain tags by article (n tags)
#store list of tags
#Article = (name, date, tag1,...tag n)


import sys
import argparse
from shutil import copyfile
from datetime import date
import csv

path2writing  = "/home/maxwell/Website2021/writing"
path2articles = "/home/maxwell/Website2021/writing/articles/"
path2list     = "/home/maxwell/Website2021/writing/list-template.html"
path2topics   = "/home/maxwell/Website2021/writing/topics-template.html"
path2store    = "/home/maxwell/Website2021/writing/.store.cvs"
path2template = "/home/maxwell/Website2021/writing/template0.html"

def main():
    parser = argparse.ArgumentParser(description='Simple HTML blogging system.')
    parser.add_argument("-new", help="Create new post", action="store_true")
    parser.add_argument("-delete", help="delete post", action="store_true")
    parser.add_argument("-init", help="init store", action="store_true")
    parser.add_argument("-publish", help="publish posts", action="store_true")
    args = parser.parse_args()
    if args.init:
        print("initializing data store")

    if args.new:
        title = input("Enter title: ") 
        path2new = path2articles+title+".html"
        copyfile(path2template,path2new)
        tags = input("Enter topic(s): ")
        tags = tags.split(' ')
        with open(path2new,'w') as new_file:
            with open(path2template) as oldfile:
                for line in oldfile:
                    if "Title" in line:
                        new_file.write("        <h1>"+title+"</h1>\n")
                    else:
                        new_file.write(line)
        day = date.today()
        csvfile=open(path2store, 'a', newline='')
        obj=csv.writer(csvfile)
        entry = [title,day] + tags
        obj.writerow(entry)
        csvfile.close()
    if args.delete:
        title = input("title to delete: ")
        lines = []
        csvfile=open(path2store,'r', newline='')
        obj=csv.reader(csvfile)
        for row in obj:
            if row[0] == title:
                print('found article to delete')
            else:
                lines.append(row)
        csvfile.close()
        csvfile=open(path2store, 'w', newline='')
        obj=csv.writer(csvfile)
        obj.writerows(lines)
        csvfile.close()
    if args.publish:
        posts = []
        tags  = []

        csvfile=open(path2store,'r',newline='')
        obj=csv.reader(csvfile)
        for row in obj:
            posts.append(row)
            for i in range(2,len(row)):
                if not row[i] in tags:
                    tags.append(row[i])
        csvfile.close()
        temp = open(path2writing+'/list.html','w')
        
        with open(path2list,'r') as f:
            for line in f:
                if "INSERT LIST HERE" in line:
                    for p in posts:
                        temp.write("<li>"+p[1]+"\t<a href="+path2articles+p[0]+".html>"+p[0]+"</a></li>\n")
                else:
                    temp.write(line)
        temp.close()

        temp = open(path2writing+'/topics.html','w')
        with open(path2topics,'r') as f:
            for line in f:
                if "INSERT TOPICS HERE" in line:
                    for t in tags:
                        temp.write("<h1>"+t+"</h1>\n")
                else:
                    temp.write(line)
        temp.close()

if __name__ == "__main__":
    # execute only if run as a script
    main()
