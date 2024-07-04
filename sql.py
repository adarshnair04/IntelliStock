import sqlite3

## Connectt to SQlite
connection=sqlite3.connect("Tshirt.db")

# Create a cursor object to insert record,create table

cursor=connection.cursor()

## create the table
table_info="""
Create table TSHIRT(BRAND VARCHAR(25),COLOUR VARCHAR(25),
SIZE VARCHAR(4),PRICE INT,STOCK_QUANTITY INT);

"""
cursor.execute(table_info)

## Insert Some more records

cursor.execute("INSERT INTO TSHIRT VALUES ('Nike', 'Blue', 'M', 200, 190)")
cursor.execute("INSERT INTO TSHIRT VALUES ('Adidas', 'Red', 'L', 215, 205)")
cursor.execute("INSERT INTO TSHIRT VALUES ('Puma', 'Green', 'XL', 190, 180)")
cursor.execute("INSERT INTO TSHIRT VALUES ('Reebok', 'Yellow', 'S', 225, 210)")
cursor.execute("INSERT INTO TSHIRT VALUES ('Under Armour', 'Black', 'XXL', 180, 170)")
cursor.execute("INSERT INTO TSHIRT VALUES ('New Balance', 'Orange', 'M', 210, 200)")
cursor.execute("INSERT INTO TSHIRT VALUES ('Converse', 'Purple', 'L', 220, 210)")
cursor.execute("INSERT INTO TSHIRT VALUES ('Vans', 'Gray', 'S', 230, 220)")
cursor.execute("INSERT INTO TSHIRT VALUES ('Adidas', 'Blue', 'S', 195, 289)")
cursor.execute("INSERT INTO TSHIRT VALUES ('Fila', 'Pink', 'XS', 240, 230)")
cursor.execute("INSERT INTO TSHIRT VALUES ('ASICS', 'Brown', 'XL', 195, 185)")
cursor.execute("INSERT INTO TSHIRT VALUES ('Tommy Hilfiger', 'White', 'M', 220, 210)")
cursor.execute("INSERT INTO TSHIRT VALUES ('Calvin Klein', 'Black', 'L', 230, 220)")
cursor.execute("INSERT INTO TSHIRT VALUES ('H&M', 'Gray', 'S', 210, 200)")
cursor.execute("INSERT INTO TSHIRT VALUES ('Adidas', 'White', 'XXL', 350, 150)")
cursor.execute("INSERT INTO TSHIRT VALUES ('Zara', 'Blue', 'XL', 205, 195)")
cursor.execute("INSERT INTO TSHIRT VALUES ('Ralph Lauren', 'Red', 'XXL', 190, 180)")
cursor.execute("INSERT INTO TSHIRT VALUES ('Guess', 'Pink', 'XS', 240, 230)")
cursor.execute("INSERT INTO TSHIRT VALUES ('American Eagle', 'Green', 'L', 215, 205)")
cursor.execute("INSERT INTO TSHIRT VALUES ('Forever 21', 'Yellow', 'M', 225, 215)")
cursor.execute("INSERT INTO TSHIRT VALUES ('Gap', 'Purple', 'S', 235, 225)")
cursor.execute("INSERT INTO TSHIRT VALUES ('Uniqlo', 'Orange', 'XL', 200, 190)")

## Disspaly ALl the records

print("The inserted records are")
data=cursor.execute('''Select * from TSHIRT''')
for row in data:
    print(row)

## Commit your changes int he databse
connection.commit()
connection.close()