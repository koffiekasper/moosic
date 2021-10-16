# FIFO queue
# Implemenets Song
# Functions to add song, remove song, skip song
# Also function UserSongCount() that returns a dict with users and the amount of songs they got queued up
# Also function Clear() which clears the entire queue
# Also function GetQueue() which returns the entire queue
# Also function RenderFirstSong() which simply renders the first song

from song import Song

class SongQueue:
    def __init__(self, limit=-1):
        self.queue = []
        self.limit = limit
    
    def addSong(self, user, arg):
        if user in self.UserSongCount() and self.UserSongCount()[user] >= self.limit:
            return False
        songObject = Song(user, arg)
        self.queue.append(songObject)
        return True

    def removeSong(self, index):
        self.queue.pop(index)
        return True
    
    def skipSong(self):
        self.queue.pop(0)
        self.RenderFirstSong()
        return True

    def UserSongCount(self):
        returnDict = {}
        for song in self.queue:
            if song.user not in returnDict:
                returnDict[song.user] = 1
            else:
                returnDict[song.user] += 1
        return returnDict

    def ClearQueue(self):
        self.queue = []
        return True

    def GetQueue(self):
        return self.queue

    def RenderFirstSong(self):
        if len(self.queue) > 0:
            self.queue[0].renderAudio()
