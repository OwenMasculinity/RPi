import pygame  # pip install pygame


def playMusic(filename, loops=0, start=0.0, value=0.5):
  
    flag = False 
    pygame.mixer.init()  
    while 1:
        if flag == 0:
            pygame.mixer.music.load(filename)
            # pygame.mixer.music.play(loops=0, start=0.0) loopsºÍstart·ֱð´ú±íÖظ´µĴÎÊýºͿªʼ²¥·ŵÄλÖá£
            pygame.mixer.music.play(loops=loops, start=start)
            pygame.mixer.music.set_volume(value)  
        if pygame.mixer.music.get_busy() == True:
            flag = True
        else:
            if flag:
                pygame.mixer.music.stop()  
                break


playMusic('lisinan.mp3')
#playMusic('out.wav')
