import csv 
import pymysql
QUERY_INSERT = """INSERT INTO transactions (id,transaction_date,id_customers,id_products,quantity,value) VALUES(%s,%s,%s,%s,%s,%s)"""



if __name__ == '__main__':

    connect = pymysql.connect( host = 'localhost',
        user = 'root',db = 'tonqq', passwd='Cesar20022007#')

    box = []
    with open('/home/cesarppz/Documents/jobs/tonqq/data.csv', 'r') as f:
        csv_data = csv.reader(f)

        for idx, row in enumerate(csv_data):
            if idx == 0:
                pass
            else:
                box.append(tuple(row))

    with connect.cursor() as cursor:
        for row in box:
            try:
                row = (row[0], row[1], row[2], row[3], row[4], row[-1].replace(r'ONE\x','').replace(r'\x','') )
                cursor.execute(QUERY_INSERT,row)
                connect.commit()
            except Exception as ex:
                print(row)
                print(ex)





            
    #cursor.execute('INSERT INTO product_relationship(id, products_id, solution_area_id, environment_id, external_id, development_group_id) VALUES(%s, %s,%s, %s,%s, %s)',row)

#db.commit()
#cursor.close()
