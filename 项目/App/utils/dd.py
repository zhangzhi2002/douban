
actorsList = ['Tom Hanks', 'Meryl Streep', 'Tom Hanks', 'Leonardo DiCaprio', 'Meryl Streep']
maxActor = max(actorsList, key=lambda x: actorsList.count(x))
print(maxActor)