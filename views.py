from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .forms import GameForm
from .models import Game
import requests
from bs4 import BeautifulSoup
import json
from .forms import WishListForm
from .models import WishList

## ADMIN---------------------------------------------------------------------------------------------------------------
def admin_console(request):                                 #The general naming convention is that methods start with lower case letters
    tableContents = Game.GameModel.all()                    # Declare a variable to hold the model.modelManager.all(), which returns all records in the db
    wishListContents = WishList.WishListModelMgr.all()      # The general naming convention is that Models start with upper case letters.
    contents = {
        'tableContents':tableContents,
        'wishListContents':wishListContents
    }
    return render(request, 'GameHoard/GH_index.html', contents)   #render is the keyword to display the browser Syntax: {request object, the file, {context}

def include_templates(request):
    #Django docs recommended way to create/load a template...So when GH_index is loaded, included templates are loaded too.
    template = loader.get_template('GameHoard/GH_index.html')
    return HttpResponse(template.render())
## ADMIN --------------------------------------------------------------------------------------------------------------

## GH_index.html (CREAT, READ, RENDER BEAUTIFUL SOUP, RENDER API)------------------------------------------------------
# Notes: The index (home) page is where users can create a database record for a game in their collection, access a link to another page to edit it, view records in the WishList DB, view rendered beautifulsoup content, and view rendered API content.
#   CREATE function is accessed via an included modal from GH_create.html (see modal instructions in gameHoard.js). The function must be included as part of this view, since here is where the CREATE function is actually performed (the modal is part of this page)..
#   READ function in this view accesses the model manager and returns all records. The html content is included from GH_read.html, where it is parsed as as_p and as as_table.
#   Beautifulsoup web scraping is rendered by calling the create_soup function and passing its content in via a variable.
#   API info is passed in from the api and apiQuery functions.
def GH_index(request):
    #CREATE a RECORD IN THE DB
    form = GameForm(data=request.POST or None)  # Declare a variable 'form' and equate it to the existing Account form (as defined in forms.py); request.Post or None is the default syntax to take any input from the form and put it into this form.
    if request.method == 'POST':
        if form.is_valid():
            form.save()                         # Apply save(), a built-in model Manager method to save an object back to the db
            return redirect('GameHoard')        # Redirect to the 'shortcut' (as defined in urls.py)
        else:
            print(form.errors)                  # If the form cannot meet the if statement, print the built-in method .errors
            form = GameForm()                   # Create an empty version of the form as the variable 'form'.

    ## To include content from other templates,
    ## create a variable to call the relevant function(s) to then render as 'content'

    #READ all RECORDs via the model Manager
    tableContents = Game.GameModel.all()
    wishListContents = WishList.WishListModelMgr.all()

    #READ BEAUTIFULSOUP results
    # Use the dictionary key to call a specific result
    soupList = create_soupList()['soupList']

    #READ API CALLs
    # Use the dictionary key to call a specific result
    queryList = apiQuery(request)["responseList"]
    responseList = api()["responseList"]

    content = {                                 # Declare a variable to then pass via return render
        'form': form,                           # Pass in the 'form' variable back as a dictionary.
        'tableContents': tableContents,         # Pass in all records in the Game DB
        'wishListContents':wishListContents,    # Pass in all records in the WishList DB
        'soupList':soupList,                    # Pass in results from beautifulsoup web scrape
        'queryList':queryList,                  # Pass in results from API user search
        'responseList':responseList,            # Pass in results from API
    }
    return render(request, "GameHoard/GH_index.html", content)
## GH_index.html (CREAT, READ, RENDER BEAUTIFUL SOUP, RENDER API)------------------------------------------------------


## GH_update.html (UPDATE and DELETE A RECORD IN THE DB) --------------------------------------------------------------
# Notes: When a request is called by the user, by clicking on an anchor tag (i.e a 'Game Card' on the index page) it goes to the url 'switchboard', which points to this method.

def update(request, pk):
    #GET FORM OBJECT VIA THE MODEL MANAGER
    item = get_object_or_404(Game, pk=pk)       # Assigns a variable to represent this built-in function from the django.shortcuts module. Query the responseListbase for the Product (using this built-in function) and it's value at that primary key (which is now converted to an integer).
    form = GameForm(data=request.POST or None, instance=item)    #Invoke the ProductForm, get the information from the form that was sent via the post method (or provide a none value), then use that information to create an instance called item. The instance 'item' then passes back all of its values from its various fields
    #UPDATE A RECORD
    if request.method == 'POST':
        if form.is_valid():                     # If the request method is possed, check the form
            form.save()                         # save() is a built-in model Manager method to save an object back to the db
            return redirect('GameHoard')        # Redirect to the 'shortcut' (as defined in urls.py)
        else:
            print(form.errors)
    else:
        content = {
            'form': form,                   #pass in the form as a dictionary
            'item':item,
        }
        return render(request, 'GameHoard/GH_update.html', content)  #Render the page that the user sees. This actually happens first, because nothing prior has had a chance to happen yet.
    #DELETE A RECORD
    if request.method == 'POST':
        item.delete()                       #delete() is a built-in model Manager method
        return redirect('GameHoard')
    return render(request, "GameHoard/GH_index.html")
## GH_update.html (UPDATE and DELETE A RECORD IN THE DB) --------------------------------------------------------------


## GH_beautifulsoup.html ----------------------------------------------------------------------------------------------
def beautifulsoup(request):
    soupList = create_soupList()["soupList"]            #Call create_soupList function[dictionary's key] to pass along content so the included page (GH_read_soup.html) can render on this page
    soupChildren = create_soupList()["soupChildren"]    #Use a different dictionary key to get a different result set
    content = {
        'soupList':soupList,
        'soupChildren':soupChildren,
    }
    return render(request, "GameHoard/GH_beautifulsoup.html", content)  #Render the page, passsing in the content so the included pages can load
## GH_beautifulsoup.html ----------------------------------------------------------------------------------------------


## GH_bsoup.html (BEAUTIFL SOUP web scraping)--------------------------------------------------------------------------
def create_soupList():
    page = requests.get("https://www.boardgamequest.com/category/game-reviews/")  # request the page to scrpate using the .get method
    soup = BeautifulSoup(page.content,'html.parser')            #define a variable to hold the BeautifulSoup page.content or page.text using 'html.parser' (there are others available)
    #Notes:
    #soupPretty = soup.prettify()                               #use the prettify() method to make the scraped html code more readable by adding tabulation
    #soupType = [type(item) for item in list(soup.children)]    #for every list object, display it's type

    soupChildren = list(soup.children)[8]                       #list the children elements at a specific index in 'soup' variable, this is the html content that is to be scraped.

    soupList = []
    n = 0       #the index number
    while n < 7:
        #Use various soup methods to select the desired content.
        href = soup.find_all('h3')[n].find('a').get('href')
        thumb = soup.find(class_='td-main-content').find_all('img')[n].get('src')
        title = soup.find_all('h3')[n].get_text()
        author = soup.find_all('span', class_='td-post-author-name')[n].get_text()
        date = soup.find_all('span', class_='td-post-date')[n].get_text()
        excerpt = soup.find_all('div', class_='td-excerpt')[n].get_text()
        soupList.append({'href':href, 'thumb':thumb, 'title':title, 'author':author, 'date':date, 'excerpt':excerpt})
        n += 1

    content = {
        'soupList':soupList,
        'soupChildren':soupChildren,
    }
    return content
## GH_bsoup.html (BEAUTIFL SOUP web scraping)--------------------------------------------------------------------------


## GH_api_template.html------------------------------------------------------------------------------------------------
def api_template(request):
    #variable = functionName()["keyName"]
    queryList = apiQuery(request)["responseList"]   #Call apiQuery function[dictionary's key] to pass along content so the include tags can render on this page
    responseList = api()["responseList"]            #Call api function[dictionary's key]
    response = api()["response"]                    #Call api function[different dictionary key]

    content = {
        'responseList':responseList,
        'response':response,
        'queryList': queryList,
    }
    return render(request, "GameHoard/GH_api_template.html", content)
## GH_api_template.html------------------------------------------------------------------------------------------------


## GH_api.html (API CALL functions)------------------------------------------------------------------------------------
#Search the API based on user input (via a form and the .get method)
def apiQuery(request):
    query = request.POST.get('inputquery', None)    #Use a variable to hold the game's name when it's called by the get request
    if query != None:
        title = query.replace(' ','%')              #replace any empty spaces with '%'.
    else:
        title = ""

    parameters = {
        'title': title,
        'limit':1,
    }
    response = requests.get("https://www.cheapshark.com/api/1.0/games?", params=parameters)
    response = json.loads(response.text)

    responseList = []
    for i in response:
        id = i["steamAppID"]
        thumb = i["thumb"]
        title = i["external"]
        salePrice = i["cheapest"]
        query = title.replace(' ', '%20')
        responseList.append({'id': id, 'thumb': thumb, 'title': title,'salePrice': salePrice, 'query':query})

    content = {
        'responseList':responseList,
    }
    return content

##Search the api
def api():
    parameters = {
        'storeID': 1,
        'upperPrice': 50,
    }
    response = requests.get("https://www.cheapshark.com/api/1.0/deals?", params=parameters)
    response = json.loads(response.text)

    responseList = []
    for i in response:
        id = i["dealID"]
        thumb = i["thumb"]
        title = i["title"]
        rating = i["steamRatingPercent"]
        salePrice = i["salePrice"]
        fullPrice = i["normalPrice"]
        responseList.append({'id': id, 'thumb': thumb, 'title': title, 'rating': rating, 'salePrice': salePrice,'fullPrice': fullPrice})

    content = {
        'response':response,
        'responseList':responseList,
    }
    return content
## GH_api.html (API CALL functions)------------------------------------------------------------------------------------


## GH_create_wishlist.html (CREATE a record from API results via a form in the api.html--------------------------------
def create_wishlist(request):
    #Gather (beautifulsoup/API) info from the input form by using the .get method
    Name = request.POST.get('Name', None)
    Thumb = request.POST.get('Thumb', None)
    Price = request.POST.get('Price', None)
    if Price == "":         #Because Price is a decimal field in the model, it can only accept numbers - it will error if "" or None get passed to it. This ensures "00.00" is the 'default'.
        Price = 00.00;
    duplicate = WishList.WishListModelMgr.all().filter(Name=Name)
    #CREATE A RECORD IN THE DB
    if duplicate:
        delete_wishlist(request)
    else:
        WishList.WishListModelMgr.create(Name=Name, Thumb=Thumb, Price=Price)
    return redirect('GameHoard')  # Redirect to the 'shortcut' (as defined in urls.py)
## GH_create_wishlist.html---------------------------------------------------------------------------------------------

## GH_delete_wishlist.html--------------------------------------------------------------------------------------------
def delete_wishlist(request): # When a request is called by the user, it goes to the url 'switchboard', which directs it to a certain method
    Name = request.POST.get('Name', None)
    record = WishList.WishListModelMgr.get(Name=Name)
    record.delete()
    #WishList.WishListModelMgr.delete(Name)
    return redirect('GameHoard')  # Redirect to the 'shortcut' (as defined in urls.py)
## GH_delete_wishlist.html--------------------------------------------------------------------------------------------
