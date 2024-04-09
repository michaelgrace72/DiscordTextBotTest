import youtubesearchpython

search = input('Enter a song: ')

searchresult = youtubesearchpython.VideosSearch(search, limit=1)

print(searchresult.result()['result'][0]['link'])