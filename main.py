import requests 
import os                       # well its OS my greatest enemy and allows to comm to OS
import discord                  # pip installed it to get the discord lib for bots                # this is for sending request to OSM server
from discord.ext import commands# this is for creating my commands YAY i used "/" as command starter
from dotenv import load_dotenv #to protect my keys i guess to hide it

# load my keys first
load_dotenv('key.env')            # to get to env file
#constant
TOKEN = os.getenv('DISCORD_TOKEN') # to get mi tokens! so that i dont have to type it



#config the dbot intent like to read the msg kapag nag type ng commands
#so these are like the configs for the bot as well
msgIntents = discord.Intents.default() 
msgIntents.message_content = True #so what this does is like when peopel are messaging on discord it will be able to read it
msgIntents.members = True
bot = commands.Bot(command_prefix="!", intents=msgIntents)
#this signals the commands for when messaging start the bot is how i understant it
#basically the command prompt to call it in chat


#run the api OSM (open street map api since its free and im broke)
#make function
def query_food_from_osm(place, cuisine):
    # gonna make a var that for the url of query engine ng api 
    OSM_query_url = "https://overpass-api.de/api/interpreter" #this is found sa website mismo ng API but its also in their wiki

    headers = {
        'User-Agent': 'FoodRecoBot/1.0 (Contact: mythomight@gmail.com)',
    }

    try:
        # read the file
        with open('OSMdirect.txt', 'r') as f:
            query_temps = f.read()
    except FileNotFoundError:
        print("Error: OSMdirect.txt not found!")
        return []

    # replace user inputs
    #the strips are so that walang whitespaces
    put_query = query_temps.replace("{{CITY}}", place.strip())
    put_query = put_query.replace("{{CUISINE}}", cuisine.strip())

    print(f"---- SENDING request to OSM -----") #debugging 101 but now it stays here so i can see if its raeading the rest of the lines

    try:
        # this will be sent sa OSM server
        response_server = requests.post(
            OSM_query_url, 
            data={'data': put_query}, 
            headers=headers,
            timeout=30 
        )

        # Check status inside the try block
        if response_server.status_code != 200:
            print(f"Error from server: {response_server.status_code}")
            print(f"details: {response_server.text}")
            return []

        data = response_server.json()
        return data.get('elements', [])
        
    except Exception as e:
        print(f"error during request: {e}")
        return []
#this is when you run the py and will output the following:
@bot.event
async def on_ready():
    print(f' Logged in as {bot.user.name}')
    print('---------')

#then the actual logic for when typing the command "!"
@bot.command()            #this is to call for the bot command
async def find(ctx, city: str, *, food: str):
        # so tto explain, the ctx is like who sends it and stuff
        #the '*' to get everything as the food name
    await ctx.send(f" Searching for {food} in {city}...")

    food_result = query_food_from_osm(city, food) #to run the server of osm to get the searches

    if not food_result: #if it doesnt find anything base on the useri nput
        await ctx.send("No Places / Restaurant Found :(")
        return
        
    get_first_place = food_result[0]             #get the first result from the result 

    store_info = get_first_place.get('tags', {}) # osm stores info like the name and cuisine using tags
    name = store_info.get('name', 'Unknown')
    
    lat = get_first_place.get('lat')
    lon = get_first_place.get('lon')

    # If it's a building (way), coordinates are inside 'center'
    if not lat or not lon:
        center = get_first_place.get('center', {})
        lat = center.get('lat')
        lon = center.get('lon')
        
#longitude
#latitude

    #gmaps Search Link
    if lat and lon:
        # We use a search query with the name + coordinates for accuracy
        clean_name = name.replace(" ", "+")
        map_link = f"https://www.google.com/maps/search/?api=1&query={clean_name}@{lat},{lon}"
        
        await ctx.send(f"I found **{name}** in {city}!! GO BIG BACKS!\n📍 View on Map: {map_link}")
    else:
        await ctx.send(f"I found **{name}** in {city}!! GO BIG BACKS! (Could not pinpoint location)")
        # so basiclly this will send msg to the discord once it finds a place

#keeps the script running and listenign to commands in disc
bot.run(TOKEN) 

#my notes:

#async and wait is like the python will do or send a task and wont pause and freeze the bot. the python will pause until its done
#request get is the bot searching and browsing the web to get from the OSM API



