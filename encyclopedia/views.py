from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import markdown2
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def content(request,title):
    return render(request,"encyclopedia/content.html",{
        "contents":markdown2.markdown(util.get_entry(title)),
        "contento":util.get_entry(title),
        "titlein":title
    })

def search(request):
    if request.method=="POST":
        search_query=request.POST.get('search_bar')
        querylist=util.list_entries()
        querymatch=[]
        for i in querylist :
            if search_query.lower()==i.lower():
                return HttpResponseRedirect(reverse('content',args=[search_query]))
            elif search_query.lower() in i.lower():
                querymatch.append(i)

        return render(request,"encyclopedia/search.html",{
                    "search_n":querymatch,
                    "search_query":search_query
                })
        
def new_page(request):
    if request.method=="POST":
        title=request.POST.get('title_content')
        new_content=request.POST.get('text_content')
        querylist=util.list_entries()
        for i in querylist:
            if title.lower()==i.lower():
                return render(request,"encyclopedia/new_page.html",{
                    "notice":"This content is already exist"
                }) 
        util.save_entry(title,new_content)
        return HttpResponseRedirect(reverse('index'))
    return render(request,"encyclopedia/new_page.html")  



def edit_page(request):
    if request.method=="POST":
        action=request.POST.get('action')
        if action=="edit":
            edit_title=request.POST.get('edit_title')
            edit_content=request.POST.get('edit_content')       
            return render(request,"encyclopedia/edit_page.html",{
                    "edit_title":edit_title,
                    "edit_content":edit_content
                })
        elif action=="safe":
            edit_title=request.POST.get('title_content')
            edit_content=request.POST.get('text_content')
            util.save_entry(edit_title,edit_content)
            return HttpResponseRedirect(reverse('content',args=[edit_title]))
    else:
        return render(request,"encyclopedia/edit_page.html")


def random_page(request):
    allcontent=util.list_entries()
    random_item=random.choice(allcontent)
    return HttpResponseRedirect(reverse('content',args=[random_item]))
    





       

