from random import randint , shuffle , choice
from math import floor
from datetime import datetime as dt
# นำเข้าข้อมูลรายการเมนู
from menu import list_menu 

# pip install prettytable
from prettytable import PrettyTable 

class Program:    
    # ? ตัวแปรไว้เป็นค่าอ้างอิงเลข index ในการหาอาหารสินค้าในรายการเมนู
    foodLi = []
    idLi = []
    # รายการที่ผู้ใช้สั่งเมนูอาหารจะเก็บไว้ในตัวแปร order
    order = {}      # key คือ ชื่ออาหาร , value คือ จำนวนสินค้าที่สั่ง
    allOrders = []  # order ทั้งหมดจะเก็บไว้ใน list 
    _sum = 0        # ยอดเงินรวมจำนวนเงินทั้งหมดในแต่ละ order
    totalMoney = 0  # ยอดเงินรวมทั้งหมดใน 1วัน
    orderNumber = 0 # หมายเลขจำนวนครั้งในการสั่ง order
    isDeleted = False
    
    # ตั้งค่าเริ่มต้น
    def __init__(self , menu , table):
        self.menu = menu
        # ? สร้างตาราง
        self.table = table() # ตารางอาหาร
        self.commands = table()# ตารางคำสั่ง
        # สร้างเลข id
        for item in self.menu: 
            item["id"] = self.createID()
        shuffle(self.menu)
        # เพิ่มแต่ละ columns
        self.commands.add_column('คำสั่ง', ("e" , "c", "m" , "b", "a" , "d" , "ed" , "cl") )
        self.commands.add_column('ชื่อคำสั่งเต็ม', ("exit" , "commands", "menu" , "buy","add" , "delete" , "edit" , "clear") )
        self.commands.add_column("ความหมายของคำสั่ง" , ("ออกจากโปรแกรม" , "แสดงคำสั่ง" , "แสดงเมนูอาหาร" , "สั่งซื้อสินค้า" , "เพิ่มรายการสินค้า" , "ลบรายการสินค้า" ,"แก้ไขชื่อรายการสินค้า" , "ลบรายการสินค้าทั้งหมด") )
        self.setElements()
        self.showCommands()
        
    # ? function สวัสดีในแต่ละช่วงเวลา
    def greeting(self , h = dt.now().time().hour):
        # ? วันที่
        days = ("จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์" , "อาทิตย์")
        months = ("มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม")
        # ? วันเวลาปัจจุบัน
        now = dt.now()
        time = now.time()
        today = now.date().strftime('%d/%m/%Y') 
        hi = ''
        if 12 > h >= 0: hi = 'สวัสดีตอนเช้า'
        elif 18 >= h >= 12: hi = 'สวัสดีตอนบ่าย'
        elif 23 >= h >= 19: hi = 'สวัสดีตอนเย็น'
        print(f'''{hi} วัน{days[now.date().weekday()]} ที่ {now.date().day} เดือน {months[now.date().month - 1]} ปี พ.ศ. {now.year + 543} ({today})
        เวลา {time.hour}:{f'0{time.minute}' if time.minute < 10 else time.minute}:{f'0{time.second}' if time.second < 10 else time.second}
        โปรแกรมพร้อมให้บริการ 🙂''')
        
    # ? function สร้างเลข id
    def createID(self , length = 4):
        id_li = []  # เก็บตัวเลขที่สุ่มมาได้
        randomNum = lambda: str(floor(id({}) * randint(1,100)))  # สุ่มเลขส่งคืนกลับมาเป็น string ก้อนใหญ่
        while True:
            ran = choice(randomNum()) #สุ่ม 1 เลขของผลลัพธ์ 
            if len(id_li) == length: break
            else: 
                id_li.append(ran)  # เก็บตัวเลขเข้าใน list
                if id_li[0] == '0': id_li.remove('0')
        _id = "".join(id_li)  # รวม element ใน list ให้เป็นข้อความ
        _id = int(_id)
        id_li.clear()
        return _id
    
    # ? function ในการเปลี่ยนค่าข้อมูลใน foodLi , idLi เมื่อในรายการในเมนู (menu) มีการเปลี่ยนแลง ตัวแปรทั้ง 2 ตัวนี้จะเปลี่ยนตามด้วย
    def setElements(self):
        # function getValue จะวน loop ดึง value ที่อยู่ใน dict ของ menu
        def getValue(li , key): 
            li = [] # ล้างค่า elements เก่าทุกครั้ง
            for item in self.menu: li.append(item[key]) # เพิ่ม element ใหม่ให้ parameter
            li = (*li,) # แปลง list เป็น tuple
            return li
        # เก็บค่า tuple ให้ 2 ตัวแปร
        self.foodLi = getValue(li= self.foodLi , key="name") 
        self.idLi = getValue(li= self.idLi , key="id")
        
    # ? function ในการค้นหา dictionary ที่อยู่ใน foodLi , idLi ส่งกลับเป็นเลข index
    def searchMenu(self , param):
        try:
            if param == 'm' or param == 'menu': 
                pass
            if param in self.foodLi:
                idx = self.foodLi.index(param)
            elif int(param) in self.idLi:
                idx = self.idLi.index(int(param))
            elif (param not in self.foodLi ) or (int(param) not in self.idLi): 
                raise Warning(f'❌ "{param}" ไม่อยู่ในเมนูอาหารโปรดใส่ชื่ออาหารหรือรหัสสินค้าใหม่อีกครั้ง!')
            return idx
        except ValueError: # เมื่อใส่ชื่อหรือ id ที่ไม่อยู่ในเมนู
            print(f'❌ "{param}" ไม่อยู่ในเมนูอาหารโปรดใส่ชื่ออาหารหรือรหัสสินค้าใหม่ให้ถูกต้อง!')
        except Warning as err:
            print(err)
            
    # ? function แสดงเมนูอาหาร
    def showMenu(self):
        # documentation: https://pypi.org/project/prettytable/
        self.table.clear() # reset ข้อมูลตารางใหม่ทุกครั้งเมื่อเรียกใช้ function
        self.table.field_names = ('ลำดับ' , 'อาหาร' , 'ราคา(บาท)' , 'รหัสสินค้า') 
        n = 1
        for item in self.menu:
            # print(f'{n}. {item["name"]} ราคา {item["price"]} บาท รหัสสินค้า {item["id"]}')
            self.table.add_row((n , item["name"] , item["price"] , item["id"]) , divider=True)
            n += 1
        print(f'🌟 ตอนนี้ไม่มีรายการสินค้าใดๆโปรดเพิ่มสินค้าก่อนแสดงรายการเมนู!') if self.menu.__len__() == 0 else print('\n',self.table , '\n')
    
    # ? function แสดงคำสั่ง
    def showCommands(self):
        print('\nเลือกพิมพ์คำสั่งเหล่านี้เพื่อดำเนินการ'.center(50))
        print(self.commands,'\n')
    
    def notify(self , text): #เพื่อออกจากการลบเมนู
        print(f'❔ พิมพ์ตัว "e" หรือ "end" {text}\n❔ พิมพ์ตัว "m" หรือ "menu เพื่อแสดงเมนูอาหาร')
        
    # ? function สั่งซื้อรายการสินค้า
    def placeOrder(self):  
        showOrder = {}
        self.notify("เพื่อออกจากการสั่งซื้อ")
        while True:
            try:
                foodName = input("ชื่ออาหาร : ")
                foodName = foodName.lower().strip()
                isEnd = foodName == "end" or foodName == "e"
                if foodName == 'm' or foodName == 'menu': 
                    self.showMenu()
                elif foodName in self.foodLi:
                    while True:
                        try:
                            amount = int(input("จำนวน : ")) # จำนวนอาหาร
                            if (amount <= 0) and not (foodName.isdigit()):
                                raise UserWarning("❌ จำนวนอาหารไม่ถูกต้องโปรดใส่จำนวนใหม่อีกครั้ง!")
                        except ValueError:
                            print("❌ โปรดใส่เป็นเลขจำนวนเต็มเท่านั้น!")
                        except UserWarning as err:
                            print(err)
                        else:
                            break
                    if foodName not in self.order: # ถ้าเป็นชื่ออาหารที่ยังไม่มี key อยู่ใน dict
                        self.order[foodName] = amount # เก็บจำนวนอาหาร
                    elif foodName in self.order: # ถ้ามีชื่อ key ซ้ำเป็นอยู่แล้วให้เพิ่มจำนวนอาหารเท่ากับของใหม่ 
                        self.order[foodName] += amount
                elif (foodName not in self.foodLi) and (not isEnd): # ไม่มีชื่ออาหารอยู่ในเมนู
                    raise UserWarning(f'❌ ไม่มีชื่อ "{foodName}" อยู่ในเมนูอาหาร!')
            except ValueError:
                print("❌ โปรดใส่เป็นเลขจำนวนเต็มเท่านั้น!")
            except UserWarning as err:
                print(err)

            # ! เมื่อหยุดการทำงานของ function placeOrder
            if isEnd:
                price_li = [] # เก็บราคาอาหาร
                self.allOrders.append(self.order.copy()) # เก็บ order
                showOrder = self.order.copy() # dict ที่จะแสดงใน print
                for item in self.order:  # loop รายชื่ออาหารที่ทำการสั่งหมด
                    idx = self.foodLi.index(item)  # หาเลข index อ้างอิงตามชื่อสินค้าที่สั่ง
                    self.order[item] = (self.order[item] * self.menu[idx]["price"])  # จำนวนสินค้า คูณ กับราคาสินค้าที่อยู่ในเมนู
                    price_li.append(self.menu[idx]["price"])
                _sum = sum(self.order.values())
                self.totalMoney += self._sum
                self.orderNumber += 1
                # ถ้าไม่ได่สั่งอะไรไม่ต้องแสดงรายการ
                if self.order.__len__() != 0: 
                    print(f"\nหมายเลขรายการสั่งอาหารที่ {self.orderNumber}. รายการอาหารที่สั่งไปคือ : ")
                    for number, key in enumerate(self.order):
                        print(f"🍽 {number + 1}. {key} จำนวน {showOrder[key]:,} อย่าง ราคาจานละ {price_li[number]} บาท รวมเป็นเงิน {self.order[key]:,} บาท")
                    print(f"💸 ยอดเงินรวมท้งหมด {_sum:,} บาท")
                    #  เริ่มสั่งรายการใหม่
                    self.order.clear()
                    showOrder.clear()
                break
        
    # ? function เพิ่มรายการสินค้า
    def addItems(self):
        self.notify('เพิ่อออกจาการเพิ่มสินค้า')
        while True:
            try:
                foodName = input('ชื่ออาหารใหม่ : ') 
                foodName = foodName.strip().lower()
                if foodName == "e" or foodName == "end": 
                    break
                elif foodName == "m" or foodName == "menu":
                    self.showMenu()
                    continue
                elif (foodName in self.foodLi) and not(foodName == "e" or foodName == "end") and not(foodName == "m" or foodName == "menu"):
                    raise UserWarning(f'❌ ไม่สามารถใช้ชื่อ "{foodName}" ในการตั้งเมนูใหม่ได้เนื่องจากมีชื่อซ้ำอยู่ในเมนูโปรดตั้งชื่อใหม่!')
            except UserWarning as err:
                print(err)
            else:
                while True:
                    try:
                        price = int(input('ราคาอาหาร : '))         
                        if len(foodName) >= 28: 
                            raise UserWarning('❌ ไม่สามารถตั้งชื่ออาหารที่มีความยาวเกินได้')
                        elif price > 1000: 
                            raise UserWarning('❌ ไม่สามารถตั้งราคาอาหารเกิน 1,000 บาทได้')
                        elif price <= 0: 
                            raise UserWarning('❌ ไม่สามารถตั้งราคาอาหารติดลบหรือเป็นศูนย์ได้')
                        else:
                            if foodName not in self.foodLi:
                                # สร้างรายการอาหารใหม่
                                self.menu.append({ 
                                    "name": foodName,
                                    "price": price,
                                    "id": self.createID()
                                })          
                                print('✔ เพิ่มรายการอาหารใหม่เสร็จสิ้น')
                                print(f'🍖 จำนวนรายการอาหารมีทั้งหมดตอนนี้ {len(self.menu)} รายการ')
                                self.setElements()   
                            # else: 
                            #     raise UserWarning(f'❌ ไม่สามารถใช้ชื่อ "{foodName}" ในการตั้งเมนูใหม่ได้เนื่องจากมีชื่อซ้ำอยู่ในเมนูโปรดตั้งชื่อใหม่!')
                    except UserWarning as err:
                        print(err)
                    except ValueError:
                        print('❌ ไม่สามารถตั้งราคาสินค้าได้ราคาสินค้าต้องตั้งเป็นตัวเลขจำนวนเต็มเท่านั้น!')
                    else: break
                    
    # ? function ลบรายการสินค้า
    def removeItems(self):
        self.notify("เพื่อออกจากการลบเมนู")
        def deleteElements(param):
            findIndex = self.searchMenu(param) # ส่งกลับเป็นเลข index
            del self.menu[findIndex]
            self.setElements()
            self.isDeleted = True
        while True:
            self.isDeleted = False
            try:
                inp = input('ใส่ชื่ออาหารหรือรหัสสินค้าเพื่อทำการลบ : ')
                inp = inp.lower().strip() 
                if inp == 'e' or inp == 'end': 
                    break
                elif inp == 'm' or inp == 'menu': 
                    self.showMenu()
                elif ',' in inp or ',' in [*inp]: # ถ้าใส่ , ให้ทำเงิอนไขนี้
                    li = inp.split(',')
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
                        if item in self.foodLi: 
                            deleteElements(item)
                        elif int(item) in self.idLi: 
                            deleteElements(item)
                        elif (item not in self.foodLi) and (int(item) not in self.idLi):
                            raise UserWarning(f"❌ ไม่มี \"{item}\" อยู่ในเมนูอาหารโปรดกรอกชื่อหรือเลข id ใหม่")
                elif (inp in self.foodLi) or (int(inp) in self.idLi): 
                    deleteElements(inp)
                elif (inp not in self.foodLi) and (int(inp) not in self.idLi):
                    raise UserWarning(f"❌ ไม่มี \"{inp}\" อยู่ในเมนูอาหารโปรดกรอกชื่อหรือเลข id ใหม่")
                else: 
                    raise UserWarning(f"❌ ไม่มี \"{inp}\" อยู่ในเมนูอาหารโปรดกรอกชื่อหรือเลข id ใหม่")
            except UserWarning as err:
                print(err)
            except ValueError:
                print(f"❌ ไม่มี \"{inp}\" อยู่ในเมนูอาหาร")
            else:
                if self.isDeleted:
                    print('✔ ลบรายการอาหารเสร็จสิ้น')
                    print(f'🍖 จำนวนรายการอาหารมีทั้งหมดตอนนี้ {len(self.menu)} รายการ')
                    
    # ? function แก้ไขรายการ
    def editItems(self):
        self.notify("เพิ่อออกจาการแก้ไข")
        while True:
            try:
                inp = input('ใส่ชื่ออาหารหรือรหัสสินค้าเพื่อทำการแก้ไข : ')
                inp = inp.lower()
                if inp == 'end' or inp == 'e': 
                    break
                if inp == 'menu' or inp == 'm':
                    self.showMenu()
                    continue
                else:
                    findIndex = self.searchMenu(inp)
                    idx = findIndex
                    print(f'คุณเลือกรายการสินค้าที่จะแก้ไข คือ {self.menu[idx]["name"]} ราคา {self.menu[idx]["price"]} บาท')
                    changeFoodName = input(f'แก้ไขชื่อ จาก "{self.menu[idx]["name"]}" เป็น -> : ')
                    assert not(changeFoodName in self.foodLi) 
                    assert not(changeFoodName == '' or changeFoodName.__len__() == 0)
                    price = int(input(f'แก้ไขราคา จาก {self.menu[idx]["price"]} บาท เป็น -> : '))
                    if price > 1000 or price <= 0: 
                        raise UserWarning('❌ ราคาสินค้าต้องตั้งอยู่ในราคาไม่เกิน 1,000 บาทเท่านั้น!')
                    # แก้ไขข้อมูล dict
                    self.menu[idx]["name"] = changeFoodName
                    self.menu[idx]["price"] = price
                    print('✔ แก้ไขรายการอาหารเสร็จสิ้น')                
                    self.setElements()
            except ValueError:
                print('🔴 Error:\nราคาสินค้าต้องตั้งเป็นตัวเลขจำนวนเต็มเท่านั้น!')
            except AssertionError:
                print('🔴 Error:\nชื่อที่คุณทำการแก้ไขนั้นเป็นชื่อซ้ำอยู่ในเมนูอาหารโปรดแก้ไขชื่อที่ไม่เหมือนกัน หรือ ห้ามชื่อว่างเปล่า!')
            except UserWarning as err:
                print(err)
            except TypeError as err: 
                pass
            
    # ? function สรุปจำนวนเงินและการสั่งซื้อสินค้า
    def conclusion(self , total , orders):
        quantity = 0
        for i in range(len(orders)):
            element = orders[i] # เข้าถึง dict แต่ละอันใน list
            for j in element: # เข้าถึง dist แล้วดึง key มาใช้
                quantity += element[j] # บวกจำนวนเพิ่มแต่ละอาหาร
        return f'🔵 จำนวนสั่งซื้ออาหารวันนี้ {len(orders):,} รายการ {quantity:,} อย่าง ทำจำนวนเงินรวมไปได้ {total:,} บาท'
    
    def PROGRESS(self):
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
                    self.allOrders.__len__() != 0 and print(self.conclusion(total=self.totalMoney , orders=self.allOrders))
                    print("<------ จบการทำงานโปรแกรม ------>")
                    break
                # แสดงคำสั่ง
                elif command == "c" or command == "commands": 
                    self.showCommands()
                # แสดงรายการเมนู
                elif command == "m" or command == "menu": 
                    self.showMenu()
                # ซื้ออาหาร
                elif command == "b" or command == "buy":
                    self.placeOrder()
                # เพิ่มสินค้า
                elif command == "a" or command == "add": 
                    self.addItems()
                # ลบสินค้า
                elif command == "d" or command == "delete":
                    self.removeItems()
                # แก้ไขสินค้า
                elif command == "ed" or command == "edit": 
                    self.editItems()
                # ลบรายการสินค้าทั้งหมด
                elif command == "cl" or command == "clear":
                    if input('คุณแน่ใจว่าต้องการลบสินค้าทั้งหมดถ้าต้องการให้พิมพ์ "y" แต่โปรดรู้ไว้ข้อมูลสินค้าจะถูกลบถาวรและไม่สามารถกู้คืนได้ : ').lower() == "y":
                        self.menu.clear()
                        print('✔ ลบรายการเมนูทั้งหมดเสร็จสิ้น')
                    else: print('คุณยกเลิกการดำเนินการลบเมนูทั้งหมด')
                else: 
                    raise UserWarning(f'🔴 Error: ไม่รู้จำคำสั่ง "{command}" โปรดเลือกใช้คำสั่งที่มีระบุไว้ให้')
            except UserWarning as err:
                print(err)
            except ValueError:
                print(f'🔴 Error: สิ่งที่ท่านหาไม่มีอยู่ในเมนูอาหารโปรดใส่ชื่ออาหารหรือรหัสสินค้าใหม่อีกครั้ง!')
            except AssertionError:
                print("🔴 Error: คุณไม่ได้ป้อนคำสั่งโปรดพิมพ์คำสั่ง")
            finally:
                isWorking and print('โปรดเลือกพิมพ์คำสั่ง')

program = Program(menu = list_menu , table = PrettyTable)
program.PROGRESS()