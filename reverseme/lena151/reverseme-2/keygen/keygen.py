username = 'patrik'
magic_number = ((len(username)*5.0/17.0 + ((len(username)-2.0)*45789.0))//1 / (len(username)*17.0/6.0))
float_key = (
(
    ord(username[0].lower())  * ord(username[0])  + 
    ord(username[0])          * ord(username[0])  +
    ord(username[-1].upper()) * ord(username[-2]) +
    ord(username[-3])         * ord(username[-4])
) * ord(username[0].lower())
  * ord(username[0])
  * ord(username[0])
  * magic_number)
rounded_float_key = round(float_key)
print(int(rounded_float_key))

