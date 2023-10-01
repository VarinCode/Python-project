from abc import abstractmethod 
from datetime import datetime as dt
from random import randint , random , choice
from math import floor
# นำเข้า module (ข้อมูลเมนู)
from menu import list_menu 
# pip install prettytable
from prettytable import PrettyTable 
# pip install typing
from typing import List , Dict , Union , Any

# |ขั้นตอนการใช้งาน|                 |คำสั่ง|
# ดาวโหลด์:                        git clone -b oop https://github.com/VarinCode/Python-project.git
# เข้าถึง directory ของ project:     cd Python-project
# ติดตั้ง virtual environment:       py -m venv .venv
# เปิดใช้งาน venv:                  .venv\Scripts\activate
# ติดตั้ง library ที่อยู่ใน project:     pip install -r requirement.txt
# คำสั่งรันโปรแกรม:                   py main.py หรือ py "C:\Users\ชื่อผู้ใช้งานคอมพิวเตอร์\Desktop\Python-project\main.py"
# ปิดใช้งาน venv:                   deactivate

class Configuration: #? กำหนดโครงสร้างของ Program
    #? กำหนด methods ที่สำคัญดังนี้
    #? abstract methods ทั้งหมดที่ประกาศไว้ถือว่าเป็น private methods ทั้งหมด
    
    @abstractmethod
    def __setElements__(self) -> None:
        pass
    
    @abstractmethod
    def __searchMenu__(self , param: str) -> int:
        pass
    
    @abstractmethod
    def __placeOrder__(self) -> None:
        pass
    
    @abstractmethod
    def __addItems__(self) -> None:
        pass
    
    @abstractmethod
    def __addItems__(self) -> None:
        pass
    
    @abstractmethod
    def __removeItems__(self) -> None:
        pass
    
    @abstractmethod
    def __editItems__(self) -> None:
        pass
    
    @abstractmethod
    def __deleteMenu__(self) -> None:
        pass
    
    @abstractmethod
    def __exitProgram__(self) -> None:
        pass

class Program(Configuration):
    #? กำหนด attributes
    #* วันที่
    days = ("จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์" , "อาทิตย์")
    months = ("มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม")
    #* วันเวลาปัจจุบัน
    now = dt.now()
    time = now.time()
    year = now.date().year + 543
    today = now.date().strftime('%d/%m/%Y') 
    #* ตัวแปรไว้เป็นค่าอ้างอิงเลข index ในการหาอาหารสินค้าในรายการเมนู
    __foodList__: List[str] = []
    __idList__: List[str] = []
    #* รายการที่ผู้ใช้สั่งเมนูอาหารจะเก็บไว้ในตัวแปร order
    currentOrder: Dict[str , int] = {} # key คือ ชื่ออาหาร , value คือ จำนวนสินค้าที่สั่ง
    __allOrders__: List[Dict[str , int]] = []    # order ทั้งหมดจะเก็บไว้ใน list 
    result = 0          # ยอดเงินรวมจำนวนล่าสุดของ currentOrder
    __totalMoney__ = 0    # ยอดเงินรวมทั้งหมดใน 1วัน
    orderNumber = 0   # หมายเลขจำนวนครั้งในการสั่ง order
    #* เก็บค่าสถานะทุกอย่างของโปรแกรม
    __programStatus__ = {
       "isDeleted": False, # สถานะการลบสินค้า
       "isWorking": None,  # สถานะการทำงาน
       "programeIsRunning" : False, # สถานะการทำงานอยู่ของโปรแกรมหลัก
       "isInvokeMethods": None # สถานะการทำงานของ method , True: method กำลังทำงาน , False: method หยุดทำงาน
    }
    #* ชื่อคำสั่งที่ใช้งานในโปรแกรม
    __KEYWORDS__ = ("e" , "c", "m" , "b", "a" , "d" , "ed" , "cl" , "exit" , "commands", "menu" , "buy" ,"add" , "delete" , "edit" , "clear")
    #* เช็คคำที่ใส่มาว่าเป็นคำสั่งหรือไม่
    def isKeyword(self , param: str) -> bool:
        return param in self.__KEYWORDS__

    #? รันโปรแกรมตอนเริ่มต้น
    def __init__(self , menu:List[Dict[str , Union[int , str]]] , table: Any) -> None:
        # เริ่มสถานะการทำงานของโปรแกรม
        self.__programStatus__["programeIsRunning"] = True 
        # รับค่า parameter(menu) มาเก็บไว้ใน attribute menu
        self.__menu__ = menu
        # สร้างตาราง
        self.__menuTable__ = table() # ตารางอาหาร
        self.__commandsTable__ = table() # ตารางคำสั่ง
        # สร้างเลข id(รหัสสินค้า)
        for item in self.__menu__: 
            item["id"] = self.createID()
        # เพิ่มคำสั่งแต่ละ columns
        self.__commandsTable__.add_column('คำสั่ง', self.__KEYWORDS__[:8]) # index ที่ 0 - 7
        self.__commandsTable__.add_column('ชื่อคำสั่งเต็ม', self.__KEYWORDS__[8:]) # index ที่ 8 ขึ้นไป
        self.__commandsTable__.add_column("ความหมายของคำสั่ง" , ("ออกจากโปรแกรม" , "แสดงคำสั่ง" , "แสดงเมนูอาหาร" , "สั่งซื้อสินค้า" , "เพิ่มรายการสินค้า" , "ลบรายการสินค้า" ,"แก้ไขชื่อรายการสินค้า" , "ลบรายการสินค้าทั้งหมด") )
        self.__setElements__() # นำเข้า property(value) ใน dict เรียงเก็บไว้ใน list ตอนเริ่มโปรแกรม
        self.greeting(self.time.hour) # ทักทายผู้ใช้งาน
        self.showCommands() # แสดงคำสั่ง
    
    #? function สวัสดีในแต่ละช่วงเวลา
    def greeting(self , h: int) -> None:
        hi = ''
        if 12 > h >= 0: hi = 'สวัสดีตอนเช้า'
        elif 18 >= h >= 12: hi = 'สวัสดีตอนบ่าย'
        elif 23 >= h >= 19: hi = 'สวัสดีตอนเย็น'
        # แสดงข้อความ
        print(f'🙏 {hi} วัน{self.days[self.now.date().weekday()]} ที่ {self.now.date().day} เดือน {self.months[self.now.date().month - 1]} ปี พ.ศ. {self.year} ({self.today})')
        print(f"🕓 เวลา {self.time.hour}:{f'0{self.time.minute}' if self.time.minute < 10 else self.time.minute}:{f'0{self.time.second}' if self.time.second < 10 else self.time.second}")
        print('โปรแกรมพร้อมให้บริการ 🙂')
        
    #? function สร้างเลข id
    def createID(self , length: int = 3) -> int:
        numbers = []  # เก็บตัวเลขที่สุ่มมาได้ไว้ใน list
        rand = lambda: str(floor(random() * randint(1,10000)))  # สุ่มเลขส่งคืนกลับมาเป็น string ก้อนใหญ่
        while True:
            num = choice(rand()) # สุ่มเลือก 1 element เลขของผลลัพธ์ 
            if len(numbers) == length: break # ถ้าเท่ากับความยาวที่ตั้งไว้ให้หยุด loop ซ้ำ
            else: 
                numbers.append(num)  # เก็บตัวเลขเข้าใน list
                if numbers[0] == '0': numbers.remove('0') # ไม่เอาเลข 0 นำหน้า
        newId = str("".join(numbers))  # รวม element ใน list ให้เป็นข้อความ
        numbers.clear()
        return newId
    
    #? function ในการเปลี่ยนค่าข้อมูลใน foodList , idList เมื่อในรายการในเมนู (menu) มีการเปลี่ยนแลง ตัวแปรทั้ง 2 ตัวนี้จะเปลี่ยนตามด้วย
    def __setElements__(self) -> None:
        # function getValue จะวน loop ดึง value ที่อยู่ใน dict ของ menu
        def getValue(setInitialValue: List[str] , keyName: str) -> List[str]: 
            setInitialValue.clear() # ล้างค่า elements เก่าทุกครั้ง
            for item in self.__menu__: setInitialValue.append(item[keyName]) # เพิ่ม element ใหม่ให้ parameter
            newValue = setInitialValue 
            return newValue
        # เก็บค่า list ที่ได้ให้ 2 ตัวแปร
        self.__foodList__ = getValue(setInitialValue=self.__foodList__ , keyName="name") 
        self.__idList__ = getValue(setInitialValue=self.__idList__ , keyName="id")
        
    #? function ในการค้นหา dictionary ที่อยู่ใน foodList , idList (อ่านค่าใน list) ส่งคืนกลับเป็นเลข index
    def __searchMenu__(self , param: str) -> int:
        try:
            # เช็ค parameter ที่ส่งมา 
            checked =  param.strip() # ตัดเว้นว่างออก
            if checked in self.__foodList__:
                idx = self.__foodList__.index(checked)
            elif checked in self.__idList__:
                idx = self.__idList__.index(checked)
            elif (checked not in self.__foodList__) and (checked not in self.__idList__): 
                raise Warning(f'❌ "{param}" ไม่อยู่ในเมนูอาหารโปรดใส่ชื่ออาหารหรือรหัสสินค้าใหม่ให้ถูกต้อง!')
            else:
                raise Warning(f'❌ "{param}" ไม่อยู่ในเมนูอาหารโปรดใส่ชื่ออาหารหรือรหัสสินค้าใหม่ให้ถูกต้อง!')
            return idx
        except Warning as err:
            print(err)
        
    #? function แสดงเมนูอาหาร
    def showMenu(self):
        # ตัวอย่างประกอบการใช้งาน API: https://pypi.org/project/prettytable
        self.__menuTable__.clear() # reset ข้อมูลตารางใหม่ทุกครั้งเมื่อเรียกใช้ function
        self.__menuTable__.field_names = ('ลำดับ' , 'อาหาร' , 'ราคา(บาท)' , 'รหัสสินค้า') # สร้าง field
        n = 1 
        for item in self.__menu__:
            # print(f'{n}. {item["name"]} ราคา {item["price"]} บาท รหัสสินค้า {item["id"]}')
            self.__menuTable__.add_row((n , item["name"] , item["price"] , int(item["id"])) , divider=True) # เพิ่ม row ใหม่ตามเมนูที่มีอยู่ในปัจจุบัน
            n += 1
        # แสดงตารางเมนูถ้าไม่พบข้อมูลสินค้าไม่ต้องแสดงตาราง (เขียนในรูแบบ ternary operator)
        print(f'🌟 ตอนนี้ไม่มีรายการสินค้าใดๆโปรดเพิ่มสินค้าก่อนแสดงรายการเมนู!') if self.__menu__.__len__() == 0 else print('\n',self.__menuTable__ , '\n')
    
    #? function แสดงคำสั่ง
    def showCommands(self) -> None:
        print('\nเลือกพิมพ์คำสั่งเหล่านี้เพื่อดำเนินการ'.center(50))
        print(self.__commandsTable__,'\n')
    
    # แสดงข้อความแจ้งเตือนทุกครั้งตอนเรียกใช้ methods
    def notify(self , text: str) -> None: # แสดงข้อความเมื่อเรียกคำสั่งที่พิมพ์ไป
        print(f'❔ พิมพ์ตัว "m" หรือ "menu เพื่อแสดงเมนูอาหาร\n❔ พิมพ์ตัว "e" หรือ "end" {text}')
        
    #? function สั่งซื้อรายการสินค้า
    def __placeOrder__(self) -> None:  
        self.notify("เพื่อออกจากการสั่งซื้อ")
        # infinite loop จนกว่าจะพิมพ์คำสั่ง "e" หรือ "end" เพื่อออกจาก loop
        while self.__programStatus__["isInvokeMethods"]:
            try:
                foodName = input("ชื่ออาหารหรือรหัสสินค้า : ")
                foodName = foodName.lower().strip()
                if foodName == 'm' or foodName == 'menu': # แสดงรายการเมนู
                    self.showMenu()
                    continue
                elif foodName == "e" or foodName == "end":
                    # ! เมื่อหยุดการทำงานของ function __placeOrder__
                    calculateOrder()
                    self.__programStatus__["isInvokeMethods"] = False
                elif (foodName in self.__foodList__) or (foodName in self.__idList__):
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
                    # แปลงรหัสสินค้าให้เป็นชื่ออาหาร
                    if foodName in self.__idList__: 
                        idx = self.__searchMenu__(foodName)
                        foodName = self.__menu__[idx]["name"]
                    # ถ้าเป็นชื่ออาหารที่ยังไม่มี key อยู่ใน dict    
                    if foodName not in self.currentOrder: 
                        self.currentOrder[foodName] = amount # เก็บจำนวนอาหาร
                    # ถ้ามีชื่อ key ซ้ำเป็นอยู่แล้วให้เพิ่มจำนวนอาหารเท่ากับของใหม่     
                    elif foodName in self.currentOrder: 
                        self.currentOrder[foodName] += amount # เพิ่มจำนวนอาหารที่มีอยู่แล้ว
                # ไม่มีชื่ออาหารอยู่ในเมนู    
                elif (foodName not in self.__foodList__) or (foodName not in self.__foodList__): 
                    raise UserWarning(f'❌ ไม่มีชื่อ "{foodName}" อยู่ในเมนูอาหาร!')
                else:
                    raise UserWarning(f'❌ ไม่มีชื่อ "{foodName}" อยู่ในเมนูอาหาร!')
            except ValueError:
                print("❌ โปรดใส่เป็นเลขจำนวนเต็มเท่านั้น!")
            except UserWarning as err:
                print(err)
                
            # เมื่อหยุดการทำงานของ method นี้ให้คำนวณยอดเงินรวม order ที่สั่งไป
            def calculateOrder() -> None:
                priceList:List[int] = [] # เก็บราคาอาหาร(ราคาจานละ)
                showOrder = self.currentOrder.copy() # dict ที่จะแสดงใน print                
                self.__allOrders__.append(self.currentOrder.copy()) # เก็บ order
                for item in self.currentOrder:  # loop รายชื่ออาหารที่ทำการสั่งมาทั้งหมด
                    idx = self.__searchMenu__(item) # หาเลข index แต่ละรายการมาอ้างอิงข้อมูลในเมนู
                    # จำนวนสินค้า X กับราคาสินค้าที่อยู่ในเมนู = ราคาอาหารทั้งหมดของอาหารนั้น
                    # currentOrder{ Key: แต่ละรายชื่ออาหาร , Value: แต่ละราคาอาหารรวมทั้งหมด }
                    self.currentOrder[item] = (self.currentOrder[item] * self.__menu__[idx]["price"])
                    # ราคารียงชื่ออาหารตามลำดับของ currentOrder
                    priceList.append(self.__menu__[idx]["price"])
                self.result = sum(self.currentOrder.values())
                self.__totalMoney__ += self.result
                self.orderNumber += 1
                # ถ้าไม่ได่สั่งอะไรไม่ต้องแสดงรายการ
                if self.currentOrder.__len__() != 0: 
                    print(f"\nหมายเลขรายการสั่งอาหารที่ {self.orderNumber}. รายการอาหารที่สั่งไปคือ : ")
                    for number, key in enumerate(showOrder):
                        print(f"🍽 {number + 1}. {key} จำนวน {showOrder[key]:,} อย่าง ราคาจานละ {priceList[number]} บาท รวมเป็นเงิน {self.currentOrder[key]:,} บาท")
                    print(f"💸 ยอดเงินรวมท้งหมด {self.result:,} บาท")
                # เริ่มสั่งรายการใหม่ให้ set ค่าเริ่มใหม่หมด (ลบสินค้า order ปัจจุบันออก)
                self.result = 0
                self.currentOrder.clear()
        
    #? function เพิ่มรายการสินค้า
    def __addItems__(self) -> None:
        self.notify('เพิ่อออกจาการเพิ่มสินค้า')
        # infinite loop จนกว่าจะพิมพ์คำสั่ง "e" หรือ "end" เพื่อออกจาก loop
        while True:
            try:
                newItem = input('ชื่ออาหารใหม่ : ') 
                newItem = newItem.strip().lower()
                if newItem == "e" or newItem == "end": # ออกจาการทำงานของ function 
                    break
                elif newItem == "m" or newItem == "menu": # แสดงรายการเมนู
                    self.showMenu()
                    continue
                elif (newItem in self.__foodList__) and not(newItem == "e" or newItem == "end") and not(newItem == "m" or newItem == "menu"):
                    raise UserWarning(f'❌ ไม่สามารถใช้ชื่อ "{newItem}" ในการตั้งเมนูใหม่ได้เนื่องจากมีชื่อซ้ำอยู่ในเมนูโปรดตั้งชื่อใหม่!')
                elif newItem.isdigit() or newItem[0].isdigit(): 
                    raise UserWarning(f'❌ ไม่สามารถตั้งชื่ออาหารที่เป็นเลขขึ้นต้นได้')
            except UserWarning as err:
                print(err)
            else:
                while True:
                    try:
                        price = int(input('ราคาอาหาร : '))         
                        if len(newItem) >= 28: 
                            raise UserWarning('❌ ไม่สามารถตั้งชื่ออาหารที่มีความยาวเกินได้')
                        elif price > 1000: 
                            raise UserWarning('❌ ไม่สามารถตั้งราคาอาหารเกิน 1,000 บาทได้')
                        elif price <= 0: 
                            raise UserWarning('❌ ไม่สามารถตั้งราคาอาหารติดลบหรือเป็นศูนย์ได้')
                        else:
                            if newItem not in self.__foodList__:
                                # สร้างรายการอาหารใหม่
                                self.__menu__.append({ 
                                    "name": newItem,
                                    "price": price,
                                    "id": self.createID()
                                })          
                                print('✔ เพิ่มรายการอาหารใหม่เสร็จสิ้น')
                                print(f'🍖 จำนวนรายการอาหารมีทั้งหมดตอนนี้ {len(self.__menu__)} รายการ')
                                self.__setElements__()   
                            else: 
                                raise UserWarning(f'❌ ไม่สามารถใช้ชื่อ "{newItem}" ในการตั้งเมนูใหม่ได้เนื่องจากมีชื่อซ้ำอยู่ในเมนูโปรดตั้งชื่อใหม่!')
                    except UserWarning as err:
                        print(err)
                    except ValueError:
                        print('❌ ไม่สามารถตั้งราคาสินค้าได้ราคาสินค้าต้องตั้งเป็นตัวเลขจำนวนเต็มเท่านั้น!')
                    else: break

    # ? function ลบรายการสินค้า
    def __removeItems__(self) -> None:
        self.notify("เพื่อออกจากการลบเมนู")
        def deleteElements(param):
            findIndex = self.__searchMenu__(param) # ส่งกลับเป็นเลข index
            del self.__menu__[findIndex]
            self.__setElements__()
            self.__programStatus__["isDeleted"] = True
        # infinite loop จนกว่าจะพิมพ์คำสั่ง "e" หรือ "end" เพื่อออกจาก loop
        while True:
            self.__programStatus__["isDeleted"] = False
            try:
                item = input('ใส่ชื่ออาหารหรือรหัสสินค้าเพื่อทำการลบ : ')
                item = item.lower().strip() 
                if item == 'e' or item == 'end':  # ออกจาการทำงานของ function
                    break
                elif item == 'm' or item == 'menu': # แสดงรายการเมนู
                    self.showMenu()
                    continue
                elif ',' in item or ',' in [*item]: # ถ้าใส่ , ให้ทำเงิอนไขนี้
                    formatList = item.split(',') # ลบ , ออก
                    # จัดระเบียบข้อความ
                    for i in range(formatList.__len__()): 
                        formatList[i] = formatList[i].strip()
                        # ถ้าใส่ , แล้วไม่มีชื่ออาหารหรือเลข id ต่อท้ายให้ลบช่องว่างเปล่าที่เกิดขึ้น
                    if '' in formatList:
                        count = formatList.count('')
                        for j in range(count):
                            formatList.remove('')
                    # ลบสินค้าที่ละชิ้น
                    for element in formatList: 
                        if element in self.__foodList__: 
                            deleteElements(element)
                        elif element in self.__idList__: 
                            deleteElements(element)
                        elif (element not in self.__foodList__) and (element not in self.__idList__):
                            raise UserWarning(f"❌ ไม่มี \"{item}\" อยู่ในเมนูอาหารโปรดกรอกชื่อหรือเลข id ใหม่")
                elif (item in self.__foodList__) or (item in self.__idList__): 
                    deleteElements(item)
                elif (item not in self.__foodList__) and (item not in self.__idList__):
                    raise UserWarning(f"❌ ไม่มี \"{item}\" อยู่ในเมนูอาหารโปรดกรอกชื่อหรือเลข id ใหม่")
                else: 
                    raise UserWarning(f"❌ ไม่มี \"{item}\" อยู่ในเมนูอาหารโปรดกรอกชื่อหรือเลข id ใหม่")
            except UserWarning as err:
                print(err)
            except ValueError:
                print(f"❌ ไม่มี \"{item}\" อยู่ในเมนูอาหาร")
            else:
                if self.__programStatus__["isDeleted"]:
                    print('✔ ลบรายการอาหารเสร็จสิ้น')
                    print(f'🍖 จำนวนรายการอาหารมีทั้งหมดตอนนี้ {len(self.__menu__)} รายการ')

    # ? function แก้ไขรายการสินค้า
    def __editItems__(self) -> None:
        self.notify("เพิ่อออกจาการแก้ไข")
        # infinite loop จนกว่าจะพิมพ์คำสั่ง "e" หรือ "end" เพื่อออกจาก loop
        while self.__programStatus__["isInvokeMethods"]:
            try:
                item = input('ใส่ชื่ออาหารหรือรหัสสินค้าเพื่อทำการแก้ไข : ')
                item = item.lower().strip()
                # ออกจาการทำงานของ method
                if item == 'e' or item == 'end': 
                    self.__programStatus__["isInvokeMethods"] = False
                # แสดงรายการเมนู    
                elif item == 'm' or item == 'menu': 
                    self.showMenu()
                    continue
                else:
                    # หาเลข index ของเมนูอาหาร
                    findIndex = self.__searchMenu__(item)
                    idx = findIndex
                    # แสดงข้อความใน terminal
                    print(f'คุณเลือกรายการสินค้าที่จะแก้ไข คือ {self.__menu__[idx]["name"]} ราคา {self.__menu__[idx]["price"]} บาท')
                    # ชื่ออาหารที่จะแก้ไขใหม่
                    changeFoodName = input(f'แก้ไขชื่อ จาก "{self.__menu__[idx]["name"]}" เป็น --> : ')
                    #! ตรวจสอบความถูกต้อง
                    assert not(changeFoodName in self.__foodList__) 
                    assert not(changeFoodName == '' or changeFoodName.__len__() == 0)
                    # ราคาที่จะแก้ไขใหม่
                    price = int(input(f'แก้ไขราคา จาก {self.__menu__[idx]["price"]} บาท เป็น --> : '))
                    if (price > 1000 or price <= 0) or (price not in range(1 , 1000)): # ยอดเงินต้องไม่เกิน 1000 บาท และ ต้องไม่ติดลบและไม่เป็นศูนย์
                        raise UserWarning('❌ ราคาสินค้าต้องตั้งอยู่ในราคาไม่เกิน 1,000 บาทเท่านั้น!')
                    else:
                        #* แก้ไขข้อมูล dictionary ในเมนู
                        self.__menu__[idx]["name"] = changeFoodName
                        self.__menu__[idx]["price"] = price
                        print('✔ แก้ไขรายการอาหารเสร็จสิ้น')                
                        self.__setElements__()
            except ValueError:
                print('🔴 Error:\nราคาสินค้าต้องตั้งเป็นตัวเลขจำนวนเต็มเท่านั้น!')
            except AssertionError:
                print('🔴 Error:\nชื่อที่คุณทำการแก้ไขนั้นเป็นชื่อซ้ำอยู่ในเมนูอาหารโปรดแก้ไขชื่อที่ไม่เหมือนกัน หรือ ห้ามชื่อว่างเปล่า!')
            except UserWarning as err:
                print(err)

    # ? function สรุปจำนวนเงินและการสั่งซื้อสินค้า
    def conclusion(self , total: int , orders: List[Dict[str , int]]) -> str:
        quantity = 0 # จำนวนอาหารที่สั่งไปทั้งหมด
        for i in range(len(orders)):
            element = orders[i] # เข้าถึง dict แต่ละอันใน list
            for j in element: # เข้าถึง dist แล้วดึง key มาใช้ , ตัวแปร j คือชื่ออาหารทำการเก็บจำนวนรายการเอาไว้ 
                quantity += element[j] # บวกจำนวนเพิ่มแต่ละอาหาร
        return f'\n🔵 จำนวนสั่งซื้ออาหารวันนี้ {len(orders):,} รายการ {quantity:,} อย่าง ทำจำนวนเงินรวมไปได้ {total:,} บาท'

    #? function ในการลบเมนูสินค้า
    def __deleteMenu__(self) -> None:
        if input('คุณแน่ใจว่าต้องการลบสินค้าทั้งหมดถ้าต้องการให้พิมพ์ "y" แต่โปรดรู้ไว้ข้อมูลสินค้าจะถูกลบถาวรและไม่สามารถกู้คืนได้ : ').lower() == "y":
            self.__menu__.clear()
            print('✔ ลบรายการเมนูทั้งหมดเสร็จสิ้น')
        else: print('❗ คุณยกเลิกการดำเนินการลบเมนูทั้งหมด')

    #? function ออกจากโปรแกรม
    def __exitProgram__(self) -> None:
        self.__programStatus__["isWorking"] = False
        #* ถ้ามีการสั่งอาหารให้แสดงรายการสรุปสินค้าที่ซื้อไปภายใน 1 วัน ถ้าไม่ได้สั่งซื้อไม่ต้องแสดง
        self.__allOrders__.__len__() != 0 and print(self.conclusion(total=self.__totalMoney__ , orders=self.__allOrders__))
        print('🙏 ขอบคุณที่มาใช้บริการโปรแกรมของเรา')
        print("<------ จบการทำงานโปรแกรม ------>")
        self.__programStatus__["programeIsRunning"] = False

    #? function ในการดำเนินการหลักของโปรแกรม
    def EXECUTE(self) -> None:
        while self.__programStatus__["programeIsRunning"]:
            self.__programStatus__["isWorking"] = True
            try:
                command = input("🟢 พิมพ์คำสั่งเพื่อดำเนินการต่อไป >>> ")
                command = command.lower().strip()
                # ! ตรวจสอบความถูกต้อง
                assert command != "" or len(command) == 0 # ถ้าไม่ได้พิมพ์คำสั่งอะไรมา
                # ? ค้นหาชื่อคำสั่ง
                if self.isKeyword(command):
                    # เปลี่ยนสถานะ attribute ตัวนี้ให้เป็น True หมายถึงกำลังทำการเรียกใช้ method(function) ของโปรแกรม
                    self.__programStatus__["isInvokeMethods"] = True
                    #* ออกจากโปรแกรม
                    if command == "e" or command == "exit":
                        self.__exitProgram__()
                    #* แสดงคำสั่ง
                    elif command == "c" or command == "commands": 
                        self.showCommands()
                    #* แสดงรายการเมนู
                    elif command == "m" or command == "menu": 
                        self.showMenu()
                    #* ซื้ออาหาร
                    elif command == "b" or command == "buy":
                        self.__placeOrder__()
                    #* เพิ่มสินค้า
                    elif command == "a" or command == "add": 
                        self.__addItems__()
                    #* ลบสินค้า
                    elif command == "d" or command == "delete":
                        self.__removeItems__()
                    #* แก้ไขสินค้า
                    elif command == "ed" or command == "edit": 
                        self.__editItems__()
                    #* ลบรายการสินค้าทั้งหมด
                    elif command == "cl" or command == "clear":
                        self.__deleteMenu__()
                #* ไม้มีคำสั่งที่ค้นหา
                else: 
                    raise UserWarning(f'🔴 Error: ไม่รู้จำคำสั่ง "{command}" โปรดเลือกใช้คำสั่งที่มีระบุไว้ให้')
            except UserWarning as err:
                print(err)
            except ValueError:
                print(f'🔴 Error: สิ่งที่ท่านหาไม่มีอยู่ในเมนูอาหารโปรดใส่ชื่ออาหารหรือรหัสสินค้าใหม่อีกครั้ง!')
            except AssertionError:
                print("🔴 Error: คุณไม่ได้ป้อนคำสั่งโปรดพิมพ์คำสั่ง")
            finally:
                self.__programStatus__["isWorking"] and print('โปรดเลือกพิมพ์คำสั่ง')

# สร้าง instance(object) เพื่อนำไปใช้งาน
program = Program(menu=list_menu[:20] , table=PrettyTable)
program.EXECUTE() # เรียกใช้ method เพื่อดำเนินการทำงานหลักของ program
