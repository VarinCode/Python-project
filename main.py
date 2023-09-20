from random import randint , random , shuffle , choice
from math import floor
from datetime import datetime as dt
from menu import list_menu # นำเข้าข้อมูลรายการเมนู

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
def createID(length=7):
    id_li = []  # เก็บตัวเลขที่สุ่มมาได้
    randomNum = lambda: str(floor(id({}) * randint(1, 10) * random()))  # สุ่มเลขส่งคืนกลับมาเป็น string ก้อนใหญ่
    for i in range(length):
        ran = choice(randomNum())
        id_li.append(ran)  # เก็บตัวเลขเข้าใน list
    _id = "".join(id_li)  # รวม element ใน list ให้เป็นข้อความ
    _id = int(_id)
    id_li.clear()
    return _id

# ? เมนูอาหาร
menu = list_menu

# ? function หั่นเมนู 
# def listSlicing(length = 100):
#     global menu
#     menu = menu[:length]
# listSlicing(50)
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
        if param == 'm' or param == 'menu': 
            pass
        if param in foodLi:
            idx = foodLi.index(param)
        elif int(param) in idLi:
            idx = idLi.index(int(param))
        elif (param not in foodLi ) or (int(param) not in idLi): 
            raise Warning(f'🔴 Error:\n"{param}" ไม่อยู่ในเมนูอาหารโปรดใส่ชื่ออาหารหรือรหัสสินค้าใหม่อีกครั้ง!')
        return idx
    except ValueError: # เมื่อใส่ชื่อหรือ id ที่ไม่อยู่ในเมนู
        print(f'🔴 Error:\n"{param}" ไม่อยู่ในเมนูอาหารโปรดใส่ชื่ออาหารหรือรหัสสินค้าใหม่อีกครั้ง!')
    except Warning as err:
        print(err)
        
# ? function แสดงเมนูอาหาร
def showMenu():
    # documentation: https://pypi.org/project/prettytable/
    table.clear() # reset ข้อมูลตารางใหม่ทุกครั้งเมื่อเรียกใช้ function
    table.field_names = ('ลำดับ' , 'อาหาร' , 'ราคา(บาท)' , 'รหัสสินค้า') 
    n = 1
    for item in menu:
        table.add_row((n , item["name"] , item["price"] , item["id"]) , divider=True)
        n += 1
    print(f'🌟 ตอนนี้ไม่มีรายการสินค้าใดๆโปรดเพิ่มสินค้าก่อนแสดงรายการเมนู!') if menu.__len__() == 0 else print('\n',table , '\n')
# showMenu()

# ? function แสดงคำสั่ง
# เพิ่มแต่ละ columns
commands.add_column('คำสั่ง', ("e" , "c", "m" , "b","a" , "d" , "edit" , "clear") )
commands.add_column('ชื่อคำสั่งเต็ม', ("exit" , "commands", "menu" , "buy","add" , "delete" , "edit" , "clear") )
commands.add_column("ความหมายของคำสั่ง" , ("ออกจากโปรแกรม" , "แสดงคำสั่ง" , "แสดงเมนูอาหาร" , "สั่งซื้อสินค้า" , "เพิ่มรายการสินค้าและราคา" , "ลบรายการสินค้า" ,"แก้ไขชื่อรายการสินค้า" , "ลบรายการสินค้าทั้งหมด") )
def showCommands():
    print('\nเลือกพิมพ์คำสั่งเหล่านี้เพื่อดำเนินการ'.center(50))
    print(commands,'\n')
showCommands()

def notify(text): #เพื่อออกจากการลบเมนู
    print(f'❔ พิมพ์ตัว "end" {text}\n❔ พิมพ์ตัว "m" เพื่อแสดงเมนูอาหาร')

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
    notify("เพื่อออกจากการสั่งซื้อ")
    while True:
        foodName = input("ชื่ออาหาร : ")
        foodName = foodName.lower().strip()
        isEnd = foodName == "end"
        if foodName == 'm' or foodName == 'menu': 
            showMenu()
        elif foodName in foodLi:
            while True:
                try:
                    amount = int(input("จำนวน : "))
                    if (amount <= 0) and not (foodName.isdigit()):
                        raise UserWarning("❌ จำนวนอาหารไม่ถูกต้องโปรดใส่จำนวนใหม่อีกครั้ง!")
                except ValueError:
                    print("❌ โปรดใส่เป็นเลขจำนวนเต็มเท่านั้น!")
                except UserWarning as err:
                    print(err)
                else:
                    break
            if foodName not in order:
                order[foodName] = amount
            elif foodName in order:
                order[foodName] += amount
        elif (foodName not in foodLi) and (not isEnd):
            raise UserWarning(f'❌ ไม่มีชื่อ "{foodName}" อยู่ในเมนูอาหาร!')
            
        # ! เมื่อหยุดการทำงานของ function placeOrder
        if isEnd:
            price_li = []
            allOrders.append(order.copy())
            showOrder = order.copy()
            for item in order:  # loop รายชื่ออาหารที่ทำการสั่งหมด
                idx = foodLi.index(item)  # หาเลข index อ้างอิงตามชื่อสินค้าที่สั่ง
                order[item] = (order[item] * menu[idx]["price"])  # จำนวนสินค้า คูณ กับราคาสินค้าที่อยู่ในเมนู
                price_li.append(menu[idx]["price"])
            _sum = sum(order.values())
            totalMoney += _sum
            orderNumber += 1
            # ถ้าไม่ได่สั่งอะไรไม่ต้องแสดงรายการ
            if order.__len__() != 0: 
                print(f"\nหมายเลขรายการสั่งอาหารที่ {orderNumber}. รายการอาหารที่สั่งไปคือ : ")
                for number, key in enumerate(order):
                    print(f"🍽 {number + 1}. {key} จำนวน {showOrder[key]:,} อย่าง ราคาจานละ {price_li[number]} รวมเป็นเงิน {order[key]:,} บาท")
                print(f"💸 ยอดเงินรวมท้งหมด {_sum:,} บาท")
                #  เริ่มสั่งรายการใหม่
                order.clear()
                showOrder.clear()
            break

# ? function เพิ่มรายการสินค้า
def addItems():
    notify('เพิ่อออกจาการเพิ่มสินค้า')
    while True:
        try:
            name = input('ชื่ออาหารใหม่ : ') 
            name = name.strip().lower()
            if name == "e" or name == "end":break
            elif name == "m" or name == "menu": showMenu()
            else:
                price = int(input('ราคาอาหาร : '))         
                if len(name) >= 28: 
                    raise UserWarning('❌ ไม่สามารถตั้งชื่ออาหารที่มีความยาวเกินได้')
                elif price > 1000: 
                    raise UserWarning('❌ ไม่สามารถตั้งราคาอาหารเกิน 1,000 บาทได้')
                elif price <= 0: 
                    raise UserWarning('❌ ไม่สามารถตั้งราคาอาหารติดลบหรือเป็นศูนย์ได้')
                else :
                    if name not in foodLi and (name != "m" or name != "menu") and (name != "e" or name != "end"):
                        # สร้างรายการอาหารใหม่
                        menu.append({ 
                            "name": name,
                            "price": price,
                            "id": createID(7)
                        })          
                        print('✔ เพิ่มรายการอาหารใหม่เสร็จสิ้น')
                        print(f'🍖 จำนวนรายการอาหารมีทั้งหมดตอนนี้ {len(menu)} รายการ')
                        setElements()   
                    else: 
                        raise UserWarning(f'❌ ไม่สามารถใช้ชื่อ "{name}" ในการตั้งเมนูใหม่ได้เนื่องจากมีชื่อซ้ำอยู่ในเมนูโปรดตั้งชื่อใหม่!')
        except UserWarning as err:
            print(err)
        except ValueError:
            print('🔴 Error:\nราคาสินค้าต้องตั้งชื่อเป็นตัวเลขจำนวนเต็มเท่านั้น!')

# ? function ลบรายการสินค้า
def removeItems():
    isDeleted = False
    notify("เพื่อออกจากการลบเมนู")
    def deleteElements(param):
        global isDeleted
        findIndex = searchMenu(param) # ส่งกลับเป็นเลข index
        del menu[findIndex]
        isDeleted = True
        setElements()
    while True:
        try:
            _input = input('ใส่ชื่ออาหารหรือรหัสสินค้าเพื่อทำการลบ : ')
            checkeInput = _input.lower().strip() 
            
            if checkeInput == 'end' or checkeInput == 'e': 
                break
            elif checkeInput == 'm' or checkeInput == 'menu': 
                showMenu()
            elif ',' in _input: # ถ้าใส่ , ให้ทำเงิอนไขนี้
                li = _input.split(',')
                # จัดระเบียบข้อความ
                for i in range(li.__len__()): 
                    li[i] = li[i].strip()
                    # ถ้าใส่ , แล้วไม่มีชื่ออาหารหรือเลข id ต่อท้ายให้ลบช่องว่างเปล่าที่เกิดขึ้น
                if '' in li:
                    count = li.count('')
                    for j in range(count):
                        li.remove('')
                # ลบสินค้าที่ละชิ้น
                for item in li: 
                    if item in foodLi: 
                        deleteElements(param=item)
                        isDeleted = True
                    elif int(item) in idLi: 
                        deleteElements(param=item)
                        setElements()
                        isDeleted = True
                    elif (item not in foodLi) and (int(item) not in idLi):
                        raise UserWarning(f"❌ ไม่มี \"{item}\" อยู่ในเมนูอาหารโปรดกรอกชื่อหรือเลข id ใหม่\n❗ ยกเลิกการลบสินค้าปัจจุบัน")
                    else:
                        pass
            elif (_input in foodLi) or (int(_input) in idLi): 
                deleteElements(param= _input)
                isDeleted = True
            else: 
                raise UserWarning(f"❌ ไม่มี \"{_input}\" อยู่ในเมนูอาหาร")
        except UserWarning as err:
            print(err)
        except ValueError:
            print(f"❌ ไม่มี \"{_input}\" อยู่ในเมนูอาหาร")
        except IndexError:
            print('🔴 Error:\nเกิดข้อผิดพลาดขึ้นโปรดลองใหม่อีกครั้ง!')
        else: 
            if isDeleted:
                print('✔ ลบรายการอาหารเสร็จสิ้น')
                print(f'🍖 จำนวนรายการอาหารมีทั้งหมดตอนนี้ {len(menu)} รายการ')

# ? function แก้ไขรายการ
def editItems():
    notify("เพิ่อออกจาการแก้ไข")
    while True:
        try:
            _input = input('ใส่ชื่ออาหารหรือรหัสสินค้าเพื่อทำการแก้ไข : ')
            _input = _input.lower()
            if _input == 'end': 
                break
            if _input == 'menu' or _input == 'm':
                showMenu()
            else:
                findIndex = searchMenu(_input)
                idx = findIndex
                print(f'คุณเลือกรายการสินค้าที่จะแก้ไข คือ {menu[idx]["name"]} ราคา {menu[idx]["price"]} บาท')
                name = input(f'แก้ไขชื่อ จาก "{menu[idx]["name"]}" เป็น -> : ')
                assert not(name in foodLi) 
                assert not(name == '' or name.__len__() == 0)
                price = int(input(f'แก้ไขราคา จาก {menu[idx]["price"]} บาท เป็น -> : '))
                if price > 1000 or price <= 0: 
                    raise UserWarning('❌ ราคาสินค้าต้องตั้งอยู่ในราคาไม่เกิน 1,000 บาทเท่านั้น!')
                # แก้ไขข้อมูล dict
                menu[idx]["name"] = name
                menu[idx]["price"] = price
                print('✔ แก้ไขรายการอาหารเสร็จสิ้น')                
                setElements()
        except ValueError:
            print('🔴 Error:\nราคาสินค้าต้องตั้งเป็นตัวเลขจำนวนเต็มเท่านั้น!')
        except AssertionError:
            print('🔴 Error:\nชื่อที่คุณทำการแก้ไขนั้นเป็นชื่อซ้ำอยู่ในเมนูอาหารโปรดแก้ไขชื่อที่ไม่เหมือนกัน หรือ ห้ามชื่อว่างเปล่า!')
        except UserWarning as err:
            print(err)
        except TypeError as err: pass
        
# ? function สรุปจำนวนเงินและการสั่งซื้อสินค้า
def conclusion(total , orders):
    quantity = 0
    for i in range(len(orders)):
        element = orders[i] # เข้าถึง dict แต่ละอันใน list
        for j in element: # เข้าถึง dist แล้วดึง key มาใช้
            quantity += element[j] # บวกจำนวนเพิ่มแต่ละอาหาร
    return f'🔵 จำนวนสั่งซื้ออาหารวันนี้ {len(orders):,} รายการ {quantity:,} อย่าง ทำจำนวนเงินรวมไปได้ {total:,} บาท'

while True:
    try:
        command = input("🟢 พิมพ์คำสั่งเพื่อดำเนินการต่อไป >>> ")
        command = command.lower().strip()
        isWorking = True
        # ! ตรวจสอบความถูกต้อง
        assert not(command == "") or len(command) == 0
        # ? หาชื่อคำสั่ง
        if command == "e" or command == "exit":
            isWorking = False
            allOrders.__len__() != 0 and print(conclusion(total=totalMoney , orders=allOrders))
            print("<------ จบการทำงานโปรแกรม ------>")
            break
        elif command == "c" or command == "commands": 
            showCommands()
        elif command == "m" or command == "menu": 
            showMenu()
        elif command == "b" or command == "buy":
            placeOrder()
        elif command == "a" or command == "add": 
            addItems()
        elif command == "d" or command == "delete":
            removeItems()
        elif command == "edit": 
            editItems()
        elif command == "clear":
            if input('คุณแน่ใจว่าต้องการลบสินค้าทั้งหมดถ้าต้องการให้พิมพ์ "y" แต่โปรดรู้ไว้ข้อมูลสินค้าจะถูกลบถาวรและไม่สามารถกู้คืนได้ : ').lower() == "y":
                menu.clear()
                print('✔ ลบรายการเมนูทั้งหมดเสร็จสิ้น')
            else: print('คุณยกเลิกการดำเนินการลบเมนูทั้งหมด')
        else: 
            raise UserWarning(f'🔴 Error:\nไม่รู้จำคำสั่ง "{command}" โปรดเลือกใช้คำสั่งที่มีระบุไว้ให้')
    except UserWarning as err:
        print(err)
    except ValueError:
        print(f'🔴 Error:\nสิ่งที่ท่านหาไม่มีอยู่ในเมนูอาหารโปรดใส่ชื่ออาหารหรือรหัสสินค้าใหม่อีกครั้ง!')
    except AssertionError:
        print("🔴 Error:\nคุณไม่ได้ป้อนคำสั่งโปรดพิมพ์คำสั่ง")
    finally:
        isWorking and print('โปรดเลือกพิมพ์คำสั่ง')