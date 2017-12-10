'''
Created on 30 ene. 2017

@author: diego
'''
import os
import unittest

from Player import Player


sPathAudioFilesTest=os.path.join(os.path.dirname(os.path.abspath(__file__)),'files')

class Test_Player(unittest.TestCase):
    
    
    
    def setUp(self):
        self.sPathAudio1=os.path.join(sPathAudioFilesTest,'audio.webm')
        
        self.sPathAudio2=os.path.join(sPathAudioFilesTest,'audio.mp3')
        self.player=Player()
        
        


    def tearDown(self):
        pass


    def testIsPlayableAdded(self):
        self.player.addPlayable(self.sPathAudio1)
        self.player.addPlayable(self.sPathAudio2)
        
        
        self.assertEqual(self.player.getListAudios(), [self.sPathAudio1,self.sPathAudio2], "Audios weren't added correctly to the player")
        
    def testChangeSong(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()