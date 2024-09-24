import logging
logger=logging.getLogger()

logging.basicConfig(
    format='[%(asctime)s][%(levelname)s] %(message)s',
    level=logging.DEBUG,
    filename='limit.log'
)

def calculate_limit(a, b, c, d):
    try:
        if d==0:
           #Crittical log-message
            logging.critical("Division by zero detected! 'd' cannot be 0.")
            return None
        
        limit = a * (b + c / d) - 33  # Calculete max_100
        logging.debug(f"limit: {limit}")
        
         # Log-level based on the max_100
        if 0 < limit < 95:
            logging.info(f"INFO: limit value is in normal range: {limit}")
        elif 95 <= limit <= 100:
            logging.warning(f"WARNING: limit is in the warning range: {limit}")
        elif limit > 100:
            logging.error(f"ERROR: limit value exceeds the limit: {limit}")
        elif limit <= 0:
            logging.error (f"ERROR: max_100 value less than the limit 0: {limit}")

        return limit
    except Exception as e:
       # Log an error if anything else goes wrong
        logging.error(f"An error occurred during calculation: {e}")
        return None
    
#Test 
calculate_limit(2, 50, 10, 5)  # Normal range
calculate_limit(2, 55, 10, 1)  # Warning
calculate_limit(2, 100, 50, 1)  # Error
calculate_limit(2, 50, 10, 0)  # Critical (d=0)
calculate_limit(2, -50, 10, 1) # Error