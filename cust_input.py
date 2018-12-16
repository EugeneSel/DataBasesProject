def float_input(low_border, high_border, msg):
    while 1:
        try:
            var = float(input(msg))
            if var < low_border or var > high_border:
                print("You entered wrong data\n")
            else:
                break
        except ValueError:
            print("You entered wrong data\n")
    return var

def int_input(low_border, high_border, msg):
    while 1:
        try:
            var = int(input(msg))
            if var < low_border or var > high_border:
                print("You entered wrong data\n")
            else:
                break
        except ValueError:
            print("You entered wrong data\n")
    return var
