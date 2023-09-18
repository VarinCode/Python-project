from random import *
from math import *
from datetime import datetime as dt
import sys

sys.path.append('./libs/prettytable') # ถ้าไม่ได้ติดตั้ง libraries ผ่าน pip ให้ใช้จาก folder
from prettytable import PrettyTable # pip install prettytable

# ? สร้างตาราง
table = PrettyTable() # ตารางอาหาร
commands = PrettyTable() # ตารางคำสั่ง

# ? วันที่
days = ("จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์" , "อาทิตย์")
months = ("มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม")
# ? วันเวลาปัจจุบัน
now = dt.now()
time = now.time()
today = now.date().strftime('%d/%m/%Y')

# ? function สวัสดีในแต่ละช่วงเวลา
def greeting(h):
    hi = ''
    if 12 > h >= 0: hi = 'สวัสดีตอนเช้า'
    elif 18 >= h >= 12: hi = 'สวัสดีตอนบ่าย'
    elif 23 >= h >= 19: hi = 'สวัสดีตอนเย็น'
    return hi
print(f'''
{greeting(time.hour)} วัน{days[now.date().weekday()]} ที่ {now.date().day} เดือน {months[now.date().month - 1]} ปี พ.ศ. {now.year + 543} ({today})
เวลา {time.hour}:{f'0{time.minute}' if time.minute < 10 else time.minute}:{f'0{time.second}' if time.second < 10 else time.second}
โปรแกรมพร้อมให้บริการ 🙂''')

# ? function สร้างเลข id
def createID(length=5):
    idLi = []  # * เก็บตัวเลขที่สุ่มมาได้
    randomNum = lambda: str(floor(id({}) * randint(1, 10)))  # * สุ่มเลข
    for i in range(length):
        idLi.append(randomNum()[i])  # * เก็บตัวเลขเข้าใน list
    _id = "".join(idLi)  # * รวม element ใน list ให้เป็นข้อความ
    _id = int(_id)
    return _id

# ? เมนูอาหาร
menu = [
    {
        "name": "ข้าวผัดกะเพราหมู",
        "price": 50,
        "id": 1776475
    },
    {
        "name": "ผัดไทยกุ้งสด",
        "price": 60,
        "id": 1444716
    },
    {
        "name": "ต้มยำกุ้ง",
        "price": 80,
        "id": 1601015
    },
    {
        "name": "ส้มตำ",
        "price": 40,
        "id": 3849731
    },
    {
        "name": "ปาตองโก",
        "price": 30,
        "id": 1324088
    },
    {
        "name": "ข้าวมันไก่",
        "price": 45,
        "id": 1407018
    },
    {
        "name": "ผัดซีอิ๊ว",
        "price": 55,
        "id": 1586753
    },
    {
        "name": "หมูสะเต๊ะ",
        "price": 35,
        "id": 1372995
    },
    {
        "name": "ก๋วยเตี๋ยวเรือ",
        "price": 40,
        "id": 1741773
    },
    {
        "name": "ข้าวหมูแดง",
        "price": 50,
        "id": 1485024
    },
    {
        "name": "แกงเขียวหวานไก่",
        "price": 70,
        "id": 3446324
    },
    {
        "name": "ไข่เจียว",
        "price": 25,
        "id": 1361098
    },
    {
        "name": "ก๋วยจั๊บ",
        "price": 45,
        "id": 1879055
    },
    {
        "name": "ข้าวต้ม",
        "price": 30,
        "id": 1601455
    },
    {
        "name": "แกงมัสมั่นหมู",
        "price": 65,
        "id": 1749811
    },
    {
        "name": "ปลาทอดกระเทียม",
        "price": 75,
        "id": 8162257
    },
    {
        "name": "ขนมจีนนำยา",
        "price": 50,
        "id": 5707388
    },
    {
        "name": "ผัดผักบุ้งไฟแดง",
        "price": 45,
        "id": 1634298
    },
    {
        "name": "ลาบหมู",
        "price": 60,
        "id": 6722376
    },
    {
        "name": "สปาเก็ตตี้พริกสด",
        "price": 70,
        "id": 1722728
    },
    {
        "name": "ข้าวไก่ทอด",
        "price": 55,
        "id": 8084716
    },
    {
        "name": "ไก่ป่า",
        "price": 75,
        "id": 1847755
    },
    {
        "name": "หมูผัดน้ำพริกเผา",
        "price": 60,
        "id": 1765013
    },
    {
        "name": "ข้าวเหนียวหมูย่าง",
        "price": 40,
        "id": 6279737
    },
    {
        "name": "แกงเผ็ดหมู",
        "price": 65,
        "id": 8189093
    },
    {
        "name": "ผัดพริกแกงหมูกรอบ",
        "price": 55,
        "id": 1532025
    },
    {
        "name": "ก๋วยเตี๋ยวต้มยำกุง",
        "price": 70,
        "id": 1627753
    },
    {
        "name": "ข้าวผัดปู",
        "price": 80,
        "id": 1684313
    },
    {
        "name": "ผัดเห็ดรวมหมู",
        "price": 60,
        "id": 1236281
    },
    {
        "name": "ปลากะพงทอดน้ำปลา",
        "price": 75,
        "id": 1022275
    },
    {
        "name": "ยำกุนเชียง",
        "price": 40,
        "id": 5189711
    },
    {
        "name": "ข้าวหน้าเป็ด",
        "price": 50,
        "id": 1821821
    },
    {
        "name": "ส้มตำไก่ย่าง",
        "price": 65,
        "id": 1107083
    },
    {
        "name": "ไก่ทอด",
        "price": 35,
        "id": 5389358
    },
    {
        "name": "แกงกะหรี่",
        "price": 45,
        "id": 1534751
    },
    {
        "name": "ข้าวหมูทอดกระเทียม",
        "price": 50,
        "id": 1862287
    },
    {
        "name": "แกงมัสมั่นไก่",
        "price": 70,
        "id": 1541738
    },
    {
        "name": "หอยนางรมทอด",
        "price": 60,
        "id": 6221378
    },
    {
        "name": "น้ำพริกปลาทู",
        "price": 25,
        "id": 1127878
    },
    {
        "name": "ไข่เจียวมะระ",
        "price": 45,
        "id": 1672715
    },
    {
        "name": "ผัดกระเพราหมูกรอบ",
        "price": 65,
        "id": 1471016
    },
    {
        "name": "บะหมี่เส้นใหญ่",
        "price": 40,
        "id": 1765257
    },
    {
        "name": "ข้าวขาหมู",
        "price": 55,
        "id": 3162015
    },
    {
        "name": "แกงเขียวหวานหมูสับ",
        "price": 70,
        "id": 1742756
    },
    {
        "name": "ปลาเป้า",
        "price": 75,
        "id": 8101874
    },
    {
        "name": "ยำสาหร่าย",
        "price": 60,
        "id": 1542918
    },
    {
        "name": "ข้าวผัดกระเพราไก่",
        "price": 45,
        "id": 1747754
    },
    {
        "name": "ผัดผักบุ้งไข่เจียว",
        "price": 50,
        "id": 1674011
    },
    {
        "name": "ก๋วยเตี๋ยวเส้นใหญ่น้ำตก",
        "price": 40,
        "id": 1782385
    },
    {
        "name": "ข้าวคลุกกะปิหมูกรอบ",
        "price": 55,
        "id": 8425826
    },
    {
        "name": "แกงคั่วหมู",
        "price": 60,
        "id": 1049451
    },
    {
        "name": "สปาเก็ตตี้ครีมซอสมะเขือเทศ",
        "price": 70,
        "id": 1677073
    },
    {
        "name": "ปลากระพงนึ่งมะนาว",
        "price": 75,
        "id": 1475084
    },
    {
        "name": "สลัดผักมะเขือเทศและเนยสด",
        "price": 65,
        "id": 1021324
    },
    {
        "name": "ข้าวต้มกุ้ง",
        "price": 70,
        "id": 1502955
    },
    {
        "name": "ไก่ย่าง",
        "price": 35,
        "id": 5766077
    },
    {
        "name": "ตำถั่วพลู",
        "price": 40,
        "id": 1742418
    },
    {
        "name": "ผัดซี่โครงหมูใบชะพลู",
        "price": 55,
        "id": 1224058
    },
    {
        "name": "กะหล่ำปลีผัดน้ำมันหอย",
        "price": 45,
        "id": 1434734
    },
    {
        "name": "ข้าวมันไก่หมู",
        "price": 55,
        "id": 1789075
    },
    {
        "name": "แกงส้มชะอมหมู",
        "price": 60,
        "id": 5742477
    },
    {
        "name": "ปลาเผา",
        "price": 70,
        "id": 1372885
    },
    {
        "name": "ยำไข่ดาว",
        "price": 45,
        "id": 6281754
    },
    {
        "name": "ก๋วยเตี๋ยวเส้นเล็กต้มยำ",
        "price": 50,
        "id": 8222815
    },
    {
        "name": "ข้าวหน้าเนื้อตุ๋น",
        "price": 65,
        "id": 1124897
    },
    {
        "name": "สเต็กเนื้อ",
        "price": 75,
        "id": 1324317
    },
    {
        "name": "หอยนางรมนึ่งมะนาว",
        "price": 60,
        "id": 1307985
    },
    {
        "name": "ผัดคะน้าหมูกรอบ",
        "price": 55,
        "id": 1604317
    },
    {
        "name": "ลาบเป็ด",
        "price": 60,
        "id": 5622014
    },
    {
        "name": "แกงส้มปลากระป๋อง",
        "price": 65,
        "id": 8472377
    },
    {
        "name": "ข้าวผัดอเมริกัน",
        "price": 70,
        "id": 1609731
    },
    {
        "name": "ไก่นุ่มทอดกรอบ",
        "price": 50,
        "id": 5049287
    },
    {
        "name": "ผัดกระเพราไก่ใส่ไข่ดาว",
        "price": 55,
        "id": 5485726
    },
    {
        "name": "ก๋วยเตี๋ยวเส้นใหญ่น้ำตกหมู",
        "price": 65,
        "id": 1022327
    },
    {
        "name": "ข้าวคลุกกะปิกุ้งสด",
        "price": 75,
        "id": 5026271
    },
    {
        "name": "แกงเขียวหวานปลาหมึก",
        "price": 70,
        "id": 1481814
    },
    {
        "name": "ปลาทูต้มราดข้าว",
        "price": 80,
        "id": 8762935
    },
    {
        "name": "ยำกุ้งสด",
        "price": 70,
        "id": 1582476
    },
    {
        "name": "สปาเก็ตตี้บะหมี่",
        "price": 60,
        "id": 1804798
    },
    {
        "name": "กุ้งแช่น้ำปลา",
        "price": 75,
        "id": 3679795
    },
    {
        "name": "ข้าวราดหน้าเนื้อ",
        "price": 65,
        "id": 3482098
    },
    {
        "name": "ผัดถั่วงอกหมูกรอบ",
        "price": 55,
        "id": 1042276
    },
    {
        "name": "หอยนางรมผัดฉ่า",
        "price": 60,
        "id": 1072286
    },
    {
        "name": "แกงมัสมั่นเนื้อ",
        "price": 70,
        "id": 1701315
    },
    {
        "name": "ปลานึ่งมะนาว",
        "price": 75,
        "id": 8141351
    },
    {
        "name": "ไข่เจียวน้ำเต้าหู้",
        "price": 55,
        "id": 1446754
    },
    {
        "name": "ผัดกระเพรากุ้ง",
        "price": 70,
        "id": 6627035
    },
    {
        "name": "ก๋วยเตี๋ยวเส้นใหญ่น้ำตกไก่",
        "price": 60,
        "id": 1324053
    },
    {
        "name": "ข้าวคลุกกะปิหมึก",
        "price": 65,
        "id": 1135297
    },
    {
        "name": "แกงส้มหมูต้ม",
        "price": 70,
        "id": 1004218
    },
    {
        "name": "สเต็กปลาหมึก",
        "price": 75,
        "id": 1721717
    },
    {
        "name": "หมูย่าง",
        "price": 80,
        "id": 1824087
    },
    {
        "name": "ผัดถั่วงอกกุ้ง",
        "price": 70,
        "id": 1841894
    },
    {
        "name": "ลาบปลาทู",
        "price": 75,
        "id": 5002216
    },
    {
        "name": "ข้าวราดหน้าหมู",
        "price": 70,
        "id": 8702217
    },
    {
        "name": "แกงเขียวหวานเต้าหู้หมู",
        "price": 75,
        "id": 5202277
    },
    {
        "name": "ปลากระพงทอดกระเทียมพริกไทย",
        "price": 80,
        "id": 1004497
    },
    {
        "name": "ยำมะม่วง",
        "price": 70,
        "id": 1084237
    },
    {
        "name": "สปาเก็ตตี้กุ้ง",
        "price": 75,
        "id": 6442074
    },
    {
        "name": "ก๋วยเตี๋ยวเส้นใหญ่น้ำตกทะเล",
        "price": 80,
        "id": 1722978
    }
]

# ? function หั่นเมนู 
def listSlicing(length = 100):
    global menu
    menu = menu[:length]
listSlicing(50)
shuffle(menu) # สุ่มรายการอาหาร

# สร้างเลข id แบบสุ่ม
# for item in menu: item["id"] = createID(6)

# ? ตัวแปรไว้เป็นค่าอ้างอิงเลข index ในการหาอาหารสินค้าในรายการเมนู
# ? สำคัญมาก
foodLi = []
idLi = []

# ? function ในการเปลี่ยนค่าข้อมูลใน foodLi , idLi เมื่อในรายการในเมนู (menu) มีการเปลี่ยนแลง ตัวแปรทั้ง 2 ตัวนี้จะเปลี่ยนตามด้วย
def setElements():
    global foodLi
    global idLi
    def getValue(li , key): # function ย่อยจะวน loop ดึง value ที่อยู่ใน dict ของ menu
        li = [] # ล้างค่า elements เก่าทุกครั้ง
        for item in menu: li.append(item[key]) # เพิ่ม element ใหม่ให้ parameter
        li = (*li,) # แปลง list เป็น tuple
        return li
    # เก็บค่า tuple ให้ 2 ตัวแปร
    foodLi = getValue(li = foodLi , key="name") 
    idLi = getValue(li = idLi , key="id")
setElements()

# ? ค้นหา dictionary ที่อยู่ใน list โดยใช้เลข id ส่งกลับเป็น dictionary
# searchId = lambda _id: menu[idLi.index(_id)] if int(_id) in idLi else None

# ? ค้นหา dictionary ที่อยู่ใน foodLi , idLi ส่งกลับเป็นเลข index
def searchMenu(param):
    try:
        if param in foodLi:
            idx = foodLi.index(param)
        elif int(param) in idLi:
            idx = idLi.index(int(param))
        elif (param not in foodLi ) or (int(param) not in idLi): raise
        return idx
    except ValueError as err: # เมื่อใส่ชื่อหรือ id ที่ไม่อยู่ในเมนู
        print(err)
        print(f'🔴 Error:\n{param} ไม่อยู่ในเมนูอาหารโปรดใส่ชื่ออาหารหรือรหัสสินค้าใหม่อีกครั้ง!')

# ? function แสดงเมนูอาหาร
def showMenu():
    # documentation: https://pypi.org/project/prettytable/
    table.clear() # reset ข้อมูลตารางใหม่ทุกครั้งเมื่อเรียกใช้ function
    table.field_names = ('ลำดับ' , 'อาหาร' , 'ราคา(บาท)' , 'รหัสสินค้า') 
    n = 1
    for item in menu:
        table.add_row((n , item["name"] , item["price"] , item["id"]) , divider=True)
        n += 1
    print('\n',table , '\n')
# showMenu()

# ? function แสดงคำสั่ง
# เพิ่มแต่ละ columns
commands.add_column('คำสั่ง', ("e" , "c", "m" , "b","a" , "d" , "edit") )
commands.add_column('ชื่อคำสั่งเต็ม', ("exit" , "commands", "menu" , "buy","add" , "delete" , "edit") )
commands.add_column("ความหมายของคำสั่ง" , ("ออกจากโปรแกรม" , "แสดงคำสั่ง" , "แสดงเมนูอาหาร" , "สั่งซื้อสินค้า" , "เพิ่มรายการสินค้าและราคา" , "ลบรายการสินค้า" ,"แก้ไขชื่อรายการสินค้า") )
def showCommands():
    print('\nเลือกพิมพ์คำสั่งเหล่านี้เพื่อดำเนินการ'.center(50))
    print(commands,'\n')
showCommands()

# รายการที่ผู้ใช้สั่งเมนูอาหารจะเก็บไว้ในตัวแปร order
order = {}  # key คือ ชื่ออาหาร , value คือ จำนวนสินค้าที่สั่ง
_sum = 0 # ยอดรวมจำนวนเงินทั้งหมด
totalMoney = 0
allOrders = []
orderNumber = 0

# ? function สั่งซื้อรายการสินค้า
def placeOrder():  
    global orderNumber
    global totalMoney
    global _sum
    showOrder = {}
    print('❔ พิมพ์ตัว "end" เพื่อออกจากการสั่งซื้อ\nพิมพ์ตัว "m" เพื่อแสดงเมนูอาหาร')
    while True:
        foodName = input("ชื่ออาหาร : ")
        foodName = foodName.lower().strip()
        isEnd = foodName == "end"
        if foodName == 'm' or foodName == 'menu': showMenu()
        elif foodName in foodLi:
            while True:
                try:
                    amount = int(input("จำนวน : "))
                    if (amount <= 0) and not (foodName.isdigit()):
                        raise Warning("❌ จำนวนอาหารไม่ถูกต้องโปรดใส่จำนวนใหม่อีกครั้ง!")
                except ValueError as err:
                    print(err)
                    print("❌ โปรดใส่เป็นเลขจำนวนเต็มเท่านั้น!")
                except Warning as err:
                    print(err)
                else:
                    break
            if foodName not in order:
                order[foodName] = amount
            elif foodName in order:
                order[foodName] += amount
        elif (foodName not in foodLi) and (not isEnd):
            print(f'❌ ไม่มีชื่อ "{foodName}" อยู่ในเมนูอาหาร!')
            
        # ! เมื่อหยุดการทำงานของ function placeOrder
        if isEnd:
            allOrders.append(order.copy())
            showOrder = order.copy()
            for item in order:  # loop รายชื่ออาหารที่ทำการสั่งหมด
                index = foodLi.index(item)  # หาเลข index อ้างอิงตามชื่อสินค้าที่สั่ง
                order[item] = (order[item] * menu[index]["price"])  # จำนวนสินค้า คูณ กับราคาสินค้าที่อยู่ในเมนู
            _sum = sum(order.values())
            totalMoney += _sum
            orderNumber += 1
            break
    return showOrder

# ? function เพิ่มรายการสินค้า
def addItems():
    try:
        name = input('ชื่ออาหารใหม่ : ') 
        price = int(input('ราคาอาหาร : ')) 
        if len(name) >= 28: 
            raise Warning('❌ ไม่สามารถตั้งชื่ออาหารที่มีความยาวเกินได้')
        elif price > 1000: 
            raise Warning('❌ ไม่สามารถตั้งราคาอาหารเกิน 1,000 บาทได้')
        elif price <= 0: 
            raise Warning('❌ ไม่สามารถตั้งราคาอาหารติดลบหรือเป็นศูนย์ได้')
        else :
            if name not in foodLi:
                # สร้างรายการอาหารใหม่
                menu.append({ 
                    "name": name,
                    "price": price,
                    "id": createID(6)
                })          
                print('✔ เพิ่มรายการอาหารใหม่เสร็จสิ้น')
                print(f'🍖 จำนวนรายการอาหารมีทั้งหมดตอนนี้ {len(menu)} รายการ')
                setElements()   
            else: print(f'❌ ไม่สามารถใช้ชื่อ "{name}" ในการตั้งเมนูใหม่ได้เนื่องจากมีชื่อซ้ำอยู่ในเมนูโปรดตั้งชื่อใหม่!')      
    except Warning as err:
        print(err)
    except ValueError as err:
        print(err)
        print('🔴 Error:\nราคาสินค้าต้องตั้งชื่อเป็นตัวเลขจำนวนเต็มเท่านั้น!')

# ? function ลบรายการสินค้า
def removeItems(index):
    try:  
        del menu[index]
        setElements()
    except IndexError as err:
        print(err)
        print('🔴 Error:\nเกิดข้อผิดพลาดขึ้นโปรดลองใหม่อีกครั้ง!')
    else: 
        print('✔ ลบรายการอาหารเสร็จสิ้น')
        print(f'🍖 จำนวนรายการอาหารมีทั้งหมดตอนนี้ {len(menu)} รายการ')
        
# ? function แก้ไขรายการ
def editItems():
    while True:
        try:
            _input = input('ใส่ชื่ออาหารหรือรหัสสินค้าเพื่อทำการแก้ไข : ')
            findIndex = searchMenu(_input)
            idx = findIndex
            print(f'คุณเลือกรายการสินค้าที่จะแก้ไข คือ {menu[idx]["name"]} ราคา {menu[idx]["price"]} บาท')
            name = input(f'แก้ไขชื่อ จาก "{menu[idx]["name"]}" เป็น -> : ')
            assert not(name in foodLi)
            assert not(name == '' or name.__len__() == 0)
            price = int(input(f'แก้ไขราคา จาก {menu[idx]["price"]} บาท เป็น -> : '))
            if price > 1000 or price <= 0: raise Warning
            # แก้ไขข้อมูล dict
            menu[idx]["name"] = name
            menu[idx]["price"] = price
            setElements()
        except ValueError as err:
            print(err)
            print('🔴 Error:\nราคาสินค้าต้องตั้งเป็นตัวเลขจำนวนเต็มเท่านั้น!')
        except AssertionError:
            print('🔴 Error:\nชื่อที่คุณทำการแก้ไขนั้นเป็นชื่อซ้ำอยู่ในเมนูอาหารโปรดแก้ไขชื่อที่ไม่เหมือนกัน หรือ ห้ามชื่อว่างเปล่า!')
        except Warning:
            print('🔴 Error:\nราคาสินค้าต้องตั้งอยู่ในราคาไม่เกิน 1,000 บาทเท่านั้น!')
        except TypeError as err: pass
        else:  
            print('✔ แก้ไขรายการอาหารเสร็จสิ้น')
            break
        
# ? function สรุปจำนวนเงินและการสั่งซื้อสินค้า
def conclusion(total , orders):
    quantity = 0
    for i in range(len(orders)):
        element = orders[i] # เข้าถึง dict แต่ละอันใน list
        for j in element: # เข้าถึง dist แล้วดึง key มาใช้
            quantity += element[j] # บวกจำนวนเพิ่มแต่ละอาหาร
    return f'🔵 จำนวนสั่งซื้ออาหารวันนี้ {len(orders)} รายการ {quantity} อย่าง ทำจำนวนเงินรวมไปได้ {total} บาท'

while True:
    try:
        inputCommand = input("🟢 พิมพ์คำสั่งเพื่อดำเนินการต่อไป >>> ")
        inputCommand = inputCommand.lower()
        isWorking = True
        # ! ตรวจสอบความถูกต้อง
        assert not(inputCommand == "") or len(inputCommand) == 0

        # ? หาชื่อคำสั่ง
        if inputCommand == "e" or inputCommand == "exit":
            isWorking = False
            allOrders.__len__() != 0 and print(conclusion(total=totalMoney , orders=allOrders))
            print("<------ จบการทำงานโปรแกรม ------>")
            break
        elif inputCommand == "c" or inputCommand == "commands": showCommands()
        elif inputCommand == "m" or inputCommand == "menu": showMenu()
        elif inputCommand == "b" or inputCommand == "buy":
            showOrder = placeOrder()
            if order.__len__() != 0: # ถ้าไม่ได่สั่งอะไรไม่ต้องแสดงรายการ
                print(f"\nหมายเลขรายการสั่งอาหารที่ {orderNumber}. รายการอาหารที่สั่งไปคือ : ")
                for number, key in enumerate(order):
                    print(f"🍽 {number + 1}. {key} จำนวน {showOrder[key]:,} อย่าง ราคารวม {order[key]:,} บาท")
                print(f"💸 ยอดเงินรวมท้งหมด {_sum:,} บาท")
                #  เริ่มสั่งรายการใหม่
                order.clear()
                showOrder.clear()
            else: pass
            # print(allOrders)
        elif inputCommand == "a" or inputCommand == "add": 
            addItems()
        elif inputCommand == "d" or inputCommand == "delete":
            print('❔ โปรดพิมพ์ตัว "end" เพื่อออกจากการลบเมนู\nโปรดพิมพ์ตัว "m" เพื่อแสดงเมนูอาหาร')
            def deleteElements(param):
                findIndex = searchMenu(param) # ส่งกลับเป็นเลข index
                removeItems(findIndex) # ลบรายการสินค้าตามลข index ใน menu
            while True:
                _input = input('🟢 ใส่ชื่ออาหารหรือรหัสสินค้าเพื่อทำการลบ : ')
                _input = _input.lower().strip()
                if _input == 'end': break
                elif _input == 'm' or _input == 'menu': showMenu()
                elif ',' in _input: # ถ้าใส่ , ให้ทำเงิอนไขนี้
                    li = _input.split(',')
                    # จัดระเบียบข้อความ
                    for i in range(li.__len__()): 
                        li[i] = li[i].strip()
                    # ลบสินค้าที่ละชิ้น
                    for item in li: 
                        if item in foodLi: deleteElements(param=item)
                        elif int(item) in idLi: deleteElements(param=item)
                        else:
                            print(f"❌ ไม่มี {item} อยู่ในเมนูอาหารโปรดกรอกชื่อหรือเลข id ")
                            break
                elif (_input in foodLi) or (int(_input) in idLi): deleteElements(param= _input)
                elif (_input not in foodLi) or (int(_input) not in idLi) : print(f"❌ ไม่มี \"{_input}\" อยู่ในเมนูอาหาร")
                else: raise Warning
        elif inputCommand == "edit": editItems()
        else: print(f'ไม่รู้จำคำสั่ง "{inputCommand}" โปรดเลือกใช้คำสั่งที่มีระบุไว้ให้')
    except Warning:
        print('🔴 Error:\nเกิดข้อผิดพลาดขึ้นโปรดลองใหม่อีกครั้ง!')
    except ValueError as err:
        print(err)
    except AssertionError:
        print("🔴 Error:\nคุณไม่ได้ป้อนคำสั่งโปรดพิมพ์คำสั่ง")
    finally:
        isWorking and print('โปรดเลือกพิมพ์คำสั่ง')