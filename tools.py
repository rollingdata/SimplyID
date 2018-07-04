# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 15:49:25 2018

@author: januszhou
"""

import numpy as np
from datetime import datetime



# ok, let's try to build up some tools first
# maybe we should make things as a class



def get_birthday(pid):
    
    # assume that we have defensive code 
    
    birthday_raw = pid[6:14]
    
    # if we want to parse the IDs
    birthday = datetime.strptime(birthday_raw, '%Y%m%d')
    
    # return with python datetime type
    return(birthday)
    
    
def get_age(pid):
    # TODO
    pass
    

    
def get_zodiac(birth_date):    
    # assuming the input is python date type
    day = birth_date.day
    month = birth_date.month
    if month == 12:
    	astro_sign = 'Sagittarius' if (day < 22) else 'Capricorn'
    elif month == 1:
    	astro_sign = 'Capricorn' if (day < 20) else 'Aquarius'
    elif month == 2:
    	astro_sign = 'Aquarius' if (day < 19) else 'Pisces'
    elif month == 3:
    	astro_sign = 'Pisces' if (day < 21) else 'Aries'
    elif month == 4:
    	astro_sign = 'Aries' if (day < 20) else 'Taurus'
    elif month == 5:
    	astro_sign = 'Taurus' if (day < 21) else 'Gemini'
    elif month == 6:
    	astro_sign = 'Gemini' if (day < 21) else 'Cancer'
    elif month == 7:
    	astro_sign = 'Cancer' if (day < 23) else 'Leo'
    elif month == 8:
    	astro_sign = 'Leo' if (day < 23) else 'Virgo'
    elif month == 9:
    	astro_sign = 'Virgo' if (day < 23) else 'Libra'
    elif month == 10:
    	astro_sign = 'Libra' if (day < 23) else 'Scorpio'
    elif month == 11:
    	astro_sign = 'Scorpio' if (day < 22) else 'Sagittarius'
    return(astro_sign)
    

def get_animal_zodiac(year):
    zodiacYear = year % 12 
    if zodiacYear == 0:
        return("Monkey")
    elif zodiacYear == 1:
        return("Rooster")
    elif zodiacYear == 2:
        return("Dog")
    elif zodiacYear == 3:
        return("Pig")
    elif zodiacYear == 4: 
        return("Rat")
    elif zodiacYear == 5: 
        return("Ox")
    elif zodiacYear == 6:
        return("Tiger")
    elif zodiacYear == 7:
        return("Rabbit")
    elif zodiacYear == 8:
        return("Dragon")
    elif zodiacYear == 9:
        return("Snake")
    elif zodiacYear == 10:
        return("Horse")
    else: 
        return("Sheep")
    

    
    
def get_gender(pid):
    
    # assuming pid is a string with 18 digits
    
    if len(pid) != 18:
        raise ValueError('The input pid does not have 18 digits!')
    
    gender_code = int(pid[16]) % 2 
    
    if gender_code:
        return('Male')
    else:
        return('Female')
    
    
def id_upgrade(old_pid):
    # input has to be the old 15 digits pid
    if len(old_pid) != 15:
        raise ValueError('The input old pid does not have 15 digits!')
    
    temp_pid = old_pid[:6] + '19' + old_pid[6:]
    
    last_digit = get_last_digit(temp_pid)
    
    new_pid = temp_pid + last_digit
    
    return(new_pid)
    
    
def is_valid_id(pid):
    
    status = False
    
    if pid[-1] == get_last_digit(pid[:-1]):
        status = True        
    
    return(status)
    
    
    
def get_last_digit(pid_without_tail):
    multiplier = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    
    base_numbers = [int(i) for i in pid_without_tail]
    
    product = np.dot(np.asarray(multiplier), np.asarray(base_numbers))
    
    remainder = product % 12
    
    verification_code = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    
    return(verification_code[remainder])
    

# need to wrap the area name lookup

def get_place_of_birth(pid):
    # first 6 digits
    area_code = pid[:6]
    
    area_name = get_area_name(area_code)


    
if __name__ = '__main__':
    continue