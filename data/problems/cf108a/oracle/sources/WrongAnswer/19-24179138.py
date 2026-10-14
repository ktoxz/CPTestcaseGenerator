def find_soonest_palindromic():
    time_input = input()
    time_input = time_input.split(':')
    minutes_palindromic = int( time_input[0][1] + time_input[0][0] )
    hour_palindromic = int( time_input[0] )

    #same hour
    if  minutes_palindromic > int( time_input[1] ) and minutes_palindromic < 60:
        palindrome = str( time_input[0] ) + ':' + str( minutes_palindromic ) 
    #one hour more
    else:   
        while True:
            if hour_palindromic == 23:
                hour_palindromic = str('00')
            else:
                hour_palindromic += 1
            temporary = str( hour_palindromic )
            minutes_palindromic = temporary[1] + temporary[0]

            if int(minutes_palindromic) < 60:
                palindrome = str( hour_palindromic) + ':' + str( minutes_palindromic ) 
                break

    #print(palindrome)
    return palindrome