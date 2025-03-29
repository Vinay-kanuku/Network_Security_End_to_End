from logger.logger import logging 
class NetworkException(Exception):
    def __init__(self, message):
        self.message = message
        logging.info("NetworkCustomException: " + self.message)
        super().__init__(self.message)
        
    def __str__(self):
        return f"NetworkCustomException:  {self.message}"
    

if __name__ == "__main__":
    try:
        raise NetworkException("This is a custom exception")
    except NetworkException as e:
        logging.error("Exception raised: " + str(e))
        print(e)
