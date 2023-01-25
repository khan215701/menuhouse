import datetime

def order_number_generator(pk):
    dateCombination = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    order_number = dateCombination + str(pk)
    return order_number