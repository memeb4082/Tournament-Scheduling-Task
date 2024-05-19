import graphs
import digraphs
import csv


def gamesOK(games):
    E = symmetrise(games)
    V = vertices(games)
    return False if (len({graphs.degree(V, E, v) for v in V}) != 1) else all(len(graphs.N(V, E, u).intersection(graphs.N(V, E, v))) > 1 for u in V for v in V if (u, v) not in E)


def referees(games, refereecsvfilename):
    conflicts = []
    with (open(refereecsvfilename, newline='')) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        conflicts = {row[0]: set(row[1:]) for row in reader}
    assignedReferees = {game: referee for game, referee in digraphs.maxMatching(games, conflicts.keys(), {(
        game, referee) for referee in conflicts for game in games if not conflicts[referee].intersection(game) and referee not in game}) if game in games and referee in conflicts.keys()}
    return assignedReferees if (len(assignedReferees) != len(games)) else None


def gameGroups(assignedReferees):
    V = {(game[0], game[1], referee)
         for game, referee in assignedReferees.items()}
    E = {(v, u) for v in V for u in V if set(
        v).intersection(set(u)) and v != u}
    return ([{game[:2] for game, color in graphs.minColouring(V, E)[1].items() if color == c} for c in range(0, graphs.minColouring(V, E)[0])])


def gameSchedule(assignedReferees, gameGroups):
    V = {frozenset(gameGroup) for gameGroup in gameGroups}
    E = {(u, v) for u in V for v in V for game in u for player in game for game2 in v if u !=
         v and player in assignedReferees[game2]}
    return digraphs.topOrdering(V, E)


def scores(p, s, c, games):
    # # calculate weightings remaining for primary and secondary after accounting for capacity
    # w = [(c-p) % c, (c-s) % c]
    # players = {player for game in games for player in game}
    # scores = {player : 0 for player in players}
    # primary_neighbours = {
    #     print(digraphs.N_out(players, games, player))
    #     for player in players
    # }
    # print(primary_neighbours)
    # [
    #     # print("win for", player)
    #     print(player, "primary wins",  "secondary wins", digraphs.NS_out(players, games, game))
    #     for game in games
    #     for player in players
    #     if game[0] == player
    # ]
    pass

    print("\n")
    # print(f"Players: {players}\nGames: {games}\nPrimary: {p}\nSecondary: {s}\nC: {c}")
    # steps for scoring
    # get primary neighbors per player, assign them p points each
    # get secondary neighbors per player, assign them s points each
    # move n points from secondary player till primary player points is c or secondary player points is 0
    # point for player is the sum of points on the neighbours now
    # do for all players
    pass


def vertices(E) -> set:
    return {v for e in E for v in e}


def symmetrise(E) -> set:
    return E | {(v, u) for (u, v) in E}
