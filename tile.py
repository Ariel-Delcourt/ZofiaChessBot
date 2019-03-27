class Tile:
    def __init__(self, name, mailbox, piece):
        self.mailbox = mailbox  # Location on the board
        self.piece = piece
        self.watchedBy = {'white': [], 'black': []}            # The array contains pieces watching this square

    @staticmethod
    def mailboxToRank(mailbox):
        return (mailbox // 10 - 1)

    @staticmethod
    def mailboxToFile(mailbox):
        digit = mailbox % 10 - 1
        fileLetters = ['A','B','C','D','E','F','G','H']
        return (fileLetters[digit])

    @staticmethod
    def mailboxToCoordinate(mailbox):
        coordinate = str(Tile.mailboxToFile(mailbox)) + str(Tile.mailboxToRank(mailbox))
        return coordinate

    @staticmethod
    def rankToMailbox(rank):
        return ((int(rank) + 1) * 10)

    @staticmethod
    def fileToMailbox(file):
        i = 1
        fileLetters = ['A','B','C','D','E','F','G','H']
        for letter in fileLetters:
            if (letter == file):
                return i
            i += 1

    @staticmethod
    def coordinateToMailbox(coordinate):
        if isinstance(coordinate, int):
            return coordinate
        coordinate = str.capitalize(coordinate)
        return Tile.fileToMailbox(coordinate[0]) + Tile.rankToMailbox(coordinate[1])