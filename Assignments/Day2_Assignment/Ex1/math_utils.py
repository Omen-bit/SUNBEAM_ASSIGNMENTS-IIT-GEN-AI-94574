

def circle(radius):
    return 3.14*(radius*radius)

def square(length):
    return length**2

def rectangle(length,breadth):
    return 2 * (length + breadth)

def triangle(base,height):
    return 0.5 * (base * height)

shape=input("Enter the name of shape you want to calculate area of [circle/square/rectangle/triangle]: ")
shape.lower()

if shape=='circle':
    radius=float(input("Enter radius of circle : "))
    circle_area=circle(radius)
    print("Area of Circle is : ", circle_area)

elif shape=='square':
    length=float(input("Enter length of side of square : "))
    sq_area=square(length)
    print("Area of Square is : ", sq_area)

elif shape=='rectangle':
    length=float(input("Enter length of rectangle : "))
    breadth=float(input("Enter breadth of rectangle : "))
    rec_area=rectangle(length,breadth)
    print("Area of Rectangle is : ", rec_area)

elif shape=='triangle':
    base=float(input("Enter base of equilateral triangle : "))
    height=float(input("Enter height of equilateral triangle : "))
    tri_area=rectangle(base,height)
    print("Area of Equilateral Triangle is : ",tri_area)

else:
    print("Invalid input !!")

