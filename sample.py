def asd(a,b,c):
	name = input ( )
	y = int ( input ( ) )
	print ("Values inputted:" )
	print ( name , y )
	print ("Loop" )
	x = 10
	while x < 15 and x >= 10 and x != 20:
		if x == 12:
			y = 100
			while y < 200:
				if y > 110 and y <= 190:
					print ( y )
				y+=10
		else:
			print ( x )
		x+=1
	return 0
print ("Calling function" )
ret = asd ( 1 , asd , False )
print ("Function returned" , ret )

