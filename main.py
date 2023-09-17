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

# ? รายการสินค้า
menu = [
    {
        "name": "ข้าวผัดกะเพราหมู",
        "price": 50,
        "id": 641756
    },
    {
        "name": "ผัดไทยกุ้งสด",
        "price": 60,
        "id": 149780
    },
    {
        "name": "ต้มยำกุ้ง",
        "price": 80,
        "id": 413758
    },
    {
        "name": "ส้มตำ",
        "price": 40,
        "id": 282708
    },
    {
        "name": "ปาตองโก",
        "price": 30,
        "id": 679770
    },
    {
        "name": "ข้าวมันไก่",
        "price": 45,
        "id": 119006
    },
    {
        "name": "ผัดซีอิ๊ว",
        "price": 55,
        "id": 672608
    },
    {
        "name": "หมูสะเต๊ะ",
        "price": 35,
        "id": 828402
    },
    {
        "name": "ก๋วยเตี๋ยวเรือ",
        "price": 40,
        "id": 181326
    },
    {
        "name": "ข้าวหมูแดง",
        "price": 50,
        "id": 162729
    },
    {
        "name": "แกงเขียวหวานไก่",
        "price": 70,
        "id": 425434
    },
    {
        "name": "ไข่เจียว",
        "price": 25,
        "id": 943654
    },
    {
        "name": "ก๋วยจั๊บ",
        "price": 45,
        "id": 727626
    },
    {
        "name": "ข้าวต้ม",
        "price": 30,
        "id": 413008
    },
    {
        "name": "แกงมัสมั่นหมู",
        "price": 65,
        "id": 812306
    },
    {
        "name": "ปลาทอดกระเทียม",
        "price": 75,
        "id": 248602
    },
    {
        "name": "ขนมจีนนำยา",
        "price": 50,
        "id": 985779
    },
    {
        "name": "ผัดผักบุ้งไฟแดง",
        "price": 45,
        "id": 623006
    },
    {
        "name": "ลาบหมู",
        "price": 60,
        "id": 212438
    },
    {
        "name": "สปาเก็ตตี้พริกสด",
        "price": 70,
        "id": 127402
    },
    {
        "name": "ข้าวไก่ทอด",
        "price": 55,
        "id": 717774
    },
    {
        "name": "ไก่ป่า",
        "price": 75,
        "id": 493704
    },
    {
        "name": "หมูผัดน้ำพริกเผา",
        "price": 60,
        "id": 821386
    },
    {
        "name": "ข้าวเหนียวหมูย่าง",
        "price": 40,
        "id": 743370
    },
    {
        "name": "แกงเผ็ดหมู",
        "price": 65,
        "id": 223756
    },
    {
        "name": "ผัดพริกแกงหมูกรอบ",
        "price": 55,
        "id": 741638
    },
    {
        "name": "ก๋วยเตี๋ยวต้มยำกุ้ง",
        "price": 70,
        "id": 321079
    },
    {
        "name": "ข้าวผัดปู",
        "price": 80,
        "id": 221658
    },
    {
        "name": "ผัดเห็ดรวมหมู",
        "price": 60,
        "id": 783426
    },
    {
        "name": "ปลากะพงทอดน้ำปลา",
        "price": 75,
        "id": 772606
    },
    {
        "name": "ยำกุนเชียง",
        "price": 40,
        "id": 114328
    },
    {
        "name": "ข้าวหน้าเป็ด",
        "price": 50,
        "id": 828786
    },
    {
        "name": "ส้มตำไก่ย่าง",
        "price": 65,
        "id": 821782
    },
    {
        "name": "ไก่ทอด",
        "price": 35,
        "id": 464302
    },
    {
        "name": "แกงกะหรี่",
        "price": 45,
        "id": 971429
    },
    {
        "name": "ข้าวหมูทอดกระเทียม",
        "price": 50,
        "id": 217386
    },
    {
        "name": "แกงมัสมั่นไก่",
        "price": 70,
        "id": 928326
    },
    {
        "name": "หอยนางรมทอด",
        "price": 60,
        "id": 328456
    },
    {
        "name": "น้ำพริกปลาทู",
        "price": 25,
        "id": 741006
    },
    {
        "name": "ไข่เจียวมะระ",
        "price": 45,
        "id": 745776
    },
    {
        "name": "ผัดกระเพราหมูกรอบ",
        "price": 65,
        "id": 397474
    },
    {
        "name": "บะหมี่เส้นใหญ่",
        "price": 40,
        "id": 113378
    },
    {
        "name": "ข้าวขาหมู",
        "price": 55,
        "id": 712302
    },
    {
        "name": "แกงเขียวหวานหมูสับ",
        "price": 70,
        "id": 422609
    },
    {
        "name": "ปลาเป้า",
        "price": 75,
        "id": 617408
    },
    {
        "name": "ยำสาหร่าย",
        "price": 60,
        "id": 195008
    }
]
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
    except ValueError as err:
        print(err)
        print(f'🔴 Error:\n{param} ไม่อยู่ในเมนูอาหารโปรดใส่ชื่ออาหารหรือรหัสสินค้าใหม่อีกครั้ง!')

# ? function แสดงเมนูอาหาร
def showMenu():
    # documentation: https://pypi.org/project/prettytable/
    table.clear() 
    table.field_names = ('ลำดับ' , 'อาหาร' , 'ราคา(บาท)' , 'รหัสสินค้า') 
    n = 1
    for item in menu:
        table.add_row((n , item["name"] , item["price"] , item["id"]) , divider=True)
        n += 1
    print('\n',table , '\n')
# showMenu()

# ? function แสดงคำสั่ง
commands.add_column('คำสั่ง', ("e" , "c", "m" , "b","a" , "d" , "edit") )
commands.add_column('ชื่อคำสั่งเต็ม', ("exit" , "commands", "menu" , "buy","add" , "delete" , "edit") )
commands.add_column("ความหมายของคำสั่ง" , ("ออกจากโปรแกรม" , "แสดงคำสั่ง" , "แสดงเมนูอาหาร" , "สั่งซื้อสินค้า" , "เพิ่มรายการสินค้าและราคา" , "ลบรายการสินค้า" ,"แก้ไขชื่อรายการสินค้า") )
def showCommands():
    print('\nเลือกพิมพ์คำสั่งเหล่านี้เพื่อดำเนินการ'.center(50))
    print(commands,'\n')
showCommands()

order = {}  # key คือ ชื่ออาหาร , value คือ จำนวนสินค้าที่สั่ง
_sum = 0

# ? function สั่งซื้อรายการสินค้า
def placeOrder():  
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
                except Exception as err:
                    print(err)
                    print("โปรดใส่เป็นเลขจำนวนเต็มเท่านั้น!")
                else:
                    break
            if (amount <= 0) and not (foodName.isdigit()):
                print("จำนวนอาหารไม่ถูกต้องโปรดใส่จำนวนใหม่อีกครั้ง")
                pass
            if foodName not in order:
                order[foodName] = amount
            elif foodName in order:
                order[foodName] += amount
        elif (foodName not in foodLi) and (not isEnd):
            print(f'ไม่มีชื่อ "{foodName}" อยู่ในเมนูอาหาร')
            
        # ! เมื่อหยุดการทำงานของ function placeOrder
        if isEnd:
            showOrder = order.copy()
            for item in order:  # loop รายชื่ออาหารที่ทำการสั่งหมด
                index = foodLi.index(item)  # หาเลข index อ้างอิงตามชื่อสินค้าที่สั่ง
                order[item] = (order[item] * menu[index]["price"])  # จำนวนสินค้า คูณ กับราคาสินค้าที่อยู่ในเมนู
            _sum = sum(order.values())
            break
    return showOrder

# ? function เพิ่มรายการสินค้า
def addItems():
    try:
        name=input('🟢 ชื่ออาหารใหม่ : ') 
        price=int(input('🟢 ราคาอาหาร : ')) 
        if len(name) >= 28: 
            print('❌ ไม่สามารถตั้งชื่ออาหารที่มีความยาวเกินได้')
            raise Warning
        elif price > 1000: 
            print('❌ ไม่สามารถตั้งราคาอาหารเกิน 1,000 บาทได้')
            raise Warning
        elif price <= 0: 
            print('❌ ไม่สามารถตั้งราคาอาหารติดลบหรือเป็นศูนย์ได้')
            raise Warning
        else :
            if name not in foodLi:
                # สร้างรายการอาหารใหม่
                menu.append({ 
                    "name": name,
                    "price": price,
                    "id": createID(6)
                })          
                print('✅ เพิ่มรายการอาหารใหม่เสร็จสิ้น')
                print(f'จำนวนรายการอาหารมีทั้งหมดตอนนี้ {len(menu)} รายการ')
                setElements()   
            else: print(f'ไม่สามารถใช้ชื่อ "{name}" ในการตั้งเมนูใหม่ได้เนื่องจากมีชื่อซ้ำอยู่ในเมนูโปรดตั้งชื่อใหม่!')      
    except Warning:
        print(False)
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
        print('✅ ลบรายการอาหารเสร็จสิ้น')
        print(f'จำนวนรายการอาหารมีทั้งหมดตอนนี้ {len(menu)} รายการ')
        
# ? function แก้ไขรายการ
def editItems():
    while True:
        try:
            _input = input('🟢 ใส่ชื่ออาหารหรือรหัสสินค้าเพื่อทำการแก้ไข : ')
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
            print('✅ แก้ไขรายการอาหารเสร็จสิ้น')
            break
        
while True:
    try:
        inputCommand = input("🟢 พิมพ์คำสั่งเพื่อดำเนินการต่อไป >>> ")
        inputCommand = inputCommand.lower()
        # ! ตรวจสอบความถูกต้อง
        assert not(inputCommand == "") or len(inputCommand) == 0

        # ? ตรวจสอบชื่อคำสั่ง
        if inputCommand == "e" or inputCommand == "exit":
            print("<------ จบการทำงานโปรแกรม ------>")
            break
        elif inputCommand == "c" or inputCommand == "commands": showCommands()
        elif inputCommand == "m" or inputCommand == "menu": showMenu()
        elif inputCommand == "b" or inputCommand == "buy":
            showOrder = placeOrder()
            if order.__len__() != 0:
                print("\nรายการอาหารที่สั่งไป : ")
                for number, key in enumerate(order):
                    print(f"🥘 {number + 1}. {key} จำนวน {showOrder[key]:,} อย่าง ราคารวม {order[key]:,} บาท")
                print(f"💸 ยอดเงินรวมท้งหมด {_sum:,} บาท")
        elif inputCommand == "a" or inputCommand == "add": 
            addItems()
        elif inputCommand == "d" or inputCommand == "delete":
            print('❔ โปรดพิมพ์ตัว "end" เพื่อออกจากการลบเมนู\nโปรดพิมพ์ตัว "m" เพื่อแสดงเมนูอาหาร')
            def deleteElements(param):
                findIndex = searchMenu(param)
                removeItems(findIndex)
            while True:
                _input = input('🟢 ใส่ชื่ออาหารหรือรหัสสินค้าเพื่อทำการลบ : ')
                _input = _input.lower().strip()
                if _input == 'end': break
                elif _input == 'm' or _input == 'menu': showMenu()
                elif ',' in _input:
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
        
""" TODO:
พิมพ์ e (exit)      ออกจากโปรแกรม      // เสร็จ    
พิมพ์ c (commands)  แสดงคำสั่ง          // เสร็จ
พิมพ์ m (menu)      แสดงเมนูอาหาร       // เสร็จ
พิมพ์ b (buy)       สั่งซื้อสินค้า          // เสร็จ
พิมพ์ a (add)       เพิ่มรายการสินค้า      // เสร็จ
พิมพ์ d (delete)    ลบรายการสินค้า       // เสร็จ
พิมพ์ edit (edit)   แก้ไขชื่อรายการสินค้า   // เสร็จ
"""