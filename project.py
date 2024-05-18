import graphs
import digraphs
import csv


def gamesOK(games):
    E = symmetrise(games)
    V = getVertices(games)
    if (len({graphs.degree(V, E, v) for v in V}) != 1):
        return False
    return all(len(graphs.N(V, E, u).intersection(graphs.N(V, E, v))) > 1 for u in V for v in V if (u, v) not in E)


def referees(games, refereecsvfilename):
    conflicts = []
    with (open(refereecsvfilename, newline='')) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        conflicts = {row[0]: set(row[1:]) for row in reader}

    referees = {(game, referee)
                for referee in conflicts
                for game in games
                if not conflicts[referee].intersection(game) and referee not in game
                }
    print(referees)
    matching = digraphs.maxMatching(games, conflicts.keys(), referees)
    assignedReferees = {game: referee for game,
                        referee in matching if game in games and referee in conflicts.keys()}
    if len(assignedReferees) != len(games):
        assignedReferees = None
    return assignedReferees


def gameGroups(assignedReferees):
    V = {
        (game[0], game[1], referee) for game, referee in assignedReferees.items()}
    E = {
        (v, u) for v in V for u in V if set(v).intersection(set(u)) and v != u}
    minColourings = graphs.minColouring(V, E)
    # data = graphs.colourClassesFromColouring(minColourings[1])

    # group minColourings[1] by color where key is game, value is color
    # TODO: check if use colour
    return([
        {
            # convert (player1, player2, referee)back into just players
            game[:2]
            for game, color in minColourings[1].items() if color == c
        } for c in range(0, minColourings[0])
    ])

def gameSchedule(assignedReferees, gameGroups):
    pass


def scores(p, s, c, games):
    pass


def getVertices(E):
    return {v for e in E for v in e}


def symmetrise(E) -> set:
    return E | {(v, u) for (u, v) in E}
