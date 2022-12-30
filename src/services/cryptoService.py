from cryptography.fernet import Fernet


class cryptoService:
    
    def __init__(self):
        
        self.cryptor = None
    
    def __backgroundCrypto(self, data: str | bytes, key: str | bytes):
        
        if type(data) == str:
            
            data = data.encode('utf8')
        
        if type(key) == str:
            
            key = key.encode('utf8')    
            
        
        cryptor = Fernet(key)
        
        self.cryptor = cryptor
        
        return cryptor.encrypt(data)    
    
    def crypt(self, data, key):
        
        rst = self.__backgroundCrypto(data, key)
        
        
        if rst:
            return rst
        else:
            return None
    
    def decrypt(self,data: str | bytes):  
        
        if type(data) == str:
            
            data = data.encode('utf8')   
            
        if self.cryptor is None:
            return None       
            
        return self.cryptor.decrypt(data)
    
    @staticmethod
    def decrypt(crypted: str | bytes, key: str | bytes):
        
        if type(key) == str:
            
            key = key.encode('utf8') 
            
        if type(crypted) == str:
            
            crypted = crypted.encode('utf8')   
            
        return Fernet(key).decrypt(crypted)          
        