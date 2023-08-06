'''
Created on 2017年7月12日

@author: WYQ
'''
def get_desktop():
    '''
    Get Desktop path
    '''
    import winreg
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]



def get_home():
    '''
    Get home path
    '''
    import os
    return os.getenv('USERPROFILE', '')



def get_home_desktop():
    '''
    Get Desktop path
    '''
    import os
    return os.getenv('USERPROFILE', '') + '\Desktop'