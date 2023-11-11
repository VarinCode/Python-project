from abc import abstractmethod 
from datetime import datetime as dt , _Time
from time import sleep
from random import randint , random , choice
from math import floor
from typing import List , Dict , Any , Tuple , Optional
from ascii_magic import AsciiArt 
from statistics import mean , mode
from sys import exit
from rich.console import Console , Group
from rich.table import Table
from rich.box import HEAVY , HEAVY_EDGE , MINIMAL , SIMPLE , SQUARE
from rich.panel import Panel
from rich.progress import track
from passlib.hash import pbkdf2_sha256
from yapf.yapflib.yapf_api import FormatFile

console: Console = Console()

class ReadWrite:
    """ อ่านและเขียนไฟล์ข้อมูลนำไปใช้ในการอ่านเขียนข้อมูลเมนูอาหารในแต่ละไฟล์ """
    
    @staticmethod
    def read(initialValue: Optional[Any] = None , 
        path: str = r'C:\Users\ACER USER5949486\Desktop\Python-project\data\menu.py') -> Any:
        #? method อ่านไฟล์เนื้อหามีการคืนกลับของข้อมูล 
        #? มีการรับค่า parameter มา 1 ตัว path คือตำแน่งไฟล์เป้าหมายที่จะไปเปิดอ่านถ้าตำแหน่ง path ที่ส่งมานั้นไม่มีอยู่จริงจะเกิด error ขึ้นได้
        #? วิธีการให้ copy path ที่จะทำการอ่านไฟล์นั้นให้ส่งค่า argument เป็น string จัด \ การโดยใช้ r เติมหน้า string เช่น r"C:\Users\ACER USER5949486\Desktop\Python-project\data\menu.py" 
        
        data: Optional[Any]
        try:
            with open(file=path , mode='r' , encoding='utf-8') as file:
                if file.readable():
                    data = file.read()
                else:
                    raise IOError
        except IOError:
            # console.print('เกิดข้อผิดพลาดในการอ่านไฟล์โปรดลงใหม่อีกครั้ง' , style='red')
            return data
        else:
            # console.print('✓ อ่านไฟล์เสร็จเรียบร้อย' , style='green')
            #* ทำให้ข้อความที่อยู่ใน string นั้นเป็นคำสั่ง python สามารถนำข้อมูลที่อ่านมานำไปใช้งานหรือคำนวณต่างๆได้
            # ternary operator: ถ้าข้อมูลที่ไปทำการอ่านไฟล์มามันว่างเปล่า ให้คืนค่าเริ่มต้นที่ส่งมา ถ้าไม่ใด้ คืนค่าข้อมูลที่อ่านมาได้ส่งไป
            return initialValue if data == '' else eval(data) 
    
    @staticmethod
    def write(data: Any , isList: bool = False , 
        path: str = r'C:\Users\ACER USER5949486\Desktop\Python-project\data\menu.py' , mode: str ="w") -> None:
        #? method เขียนไฟล์ หรือ เขียนข้อมูลเพิ่มเติมได้
        #? มีการรับค่า parameters มา 4 ตัวคือ data , path , isList และ mode
        #? parameter ใช้หลักการเดียวกับ method read ส่วน parameter data ต้องส่งข้อมูลเป็น list เท่านั้น ใน elements จะเป็น dict ปรับแต่งใช้ภายใน project
        #? mode คือการเลือกว่าจะดำเนินการอย่างไรในการเปิดไฟล์ ในที่นี้ set เป็น default parameter ให้เป็น w คือเขียนไฟล์ ถ้าต้องการเพิ่มเนื้อหาข้อมูลของไฟล์ให้เปลี่ยน mode เป็น a  
        #? isList เขียนข้อมูลให้เป็น list โดยส่งค่า (True/False) ไป 
        
        try:
            with open(file=path , mode=mode , encoding='utf-8') as file:
                if file.writable():
                    if isinstance(data , list) and isList: # สำหรับเขียนข้อมูลทั่วไป ข้อมูลผู้ใช้งาน ข้อมูลเมนู
                        file.write('[')
                        newData = [f'{i},' for i in data] # ต้องทำให้ elments ที่อยู่ใน list นั้นเป็น string ก่อน
                        file.writelines(newData) # ข้อมูลที่จะเขียนลงไปต้องเป็น list
                        file.write(']')
                    elif isinstance(data , dict):
                        file.write('{')
                        for key , val in data.items():
                            file.write(f'"{key}":{val},')
                        file.write('}')
                    elif isinstance(data , list): # สำหรับเขียน log file
                        print(*data , sep='\n' , file=file)
                    elif isinstance(data , str): # สำหรับเขียนข้อความทั่วๆไป
                        file.write(data)
                    else:
                        raise Exception
                else:
                    raise IOError
        except IOError:
            # console.print('เกิดข้อผิดพลาดในการอ่านไฟล์โปรดลงใหม่อีกครั้ง' , style='red')
            ...
        except Exception:
            # console.print('ข้อมูลที่ส่งมาจะต้องส่งมาเป็น list เท่านั้นถึงจะเขียนไฟล์ได้' , style='red')
            ...
        else:
            # console.print(f'[green]✓ เขียนไฟล์เสร็จเรียบร้อยที่ตำแหน่ง [/][underline blue]{path}[/]')
            ...
            
class Date:
    """ วันเวลาปัจจุบัน """

    #* วัน และ เดือน
    days: Tuple[str , ...] = ("จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์" , "อาทิตย์")
    months: Tuple[str , ...] = ("มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม")
    
    #* วันที่ เวลา
    now: dt = dt.now()
    time: _Time = now.time()
    year: int = now.date().year + 543
    today: str = now.date().strftime('%d/%m/%Y') 
    
    def greeting(self , userName: str) -> None:
        """ method ทักทายผู้ใช้งานและบอกวันเวลาปัจจุบัน """
        hour: int = self.time.hour 
        hi: str = ''
        # Ref: https://www.aepenglishschool.com/content/5024/english-time
        if hour >= 5 and hour <= 11: hi = 'สวัสดีตอนเช้า'
        elif hour >= 12  and hour <= 17: hi = 'สวัสดีตอนบ่าย'
        elif hour >= 18 and hour <= 21: hi = 'สวัสดีตอนเย็น'
        elif hour >= 22 and hour >= 4: hi = 'สวัสดีตอนกลางคืน'
        # อัปเดตค่า attribute
        self.now = dt.now()
        self.time = self.now.time()
        # แสดงข้อความ
        console.print(f'🙏 {hi} คุณ [medium_spring_green]{userName}[/] วันนี้ วัน{self.days[self.now.date().weekday()]} ที่ {self.now.date().day} เดือน {self.months[self.now.date().month - 1]} ปี พ.ศ. {self.year} ({self.today})')
        console.print(f"🕓 เวลา {f'0{self.time.hour}' if self.time.hour < 10 else self.time.hour}:{f'0{self.time.minute}' if self.time.minute < 10 else self.time.minute}:{f'0{self.time.second}' if self.time.second < 10 else self.time.second}")
        console.print("🙂 โปรแกรมพร้อมให้บริการ")

    def getTime(self , log: bool = False) -> str:
        """ method รับค่าเวลา """
        # อัปเดตค่า attribute
        self.now = dt.now()
        self.time = self.now.time()
        if log: # ใช้เวลาจริงในการเก็บ log file
            return f"{self.now.date()} {str(self.time)[:11 + 1]}" # ตัด str ให้เหลืออักษร 11 ตัว
        else:
            return f"{self.time.hour}:{f'0{self.time.minute}' if self.time.minute < 10 else self.time.minute}:{f'0{self.time.second}' if self.time.second < 10 else self.time.second}"
    
    def getDate(self) -> str:
        """ method รับค่าวันที่ """
        return self.today
    
class Configuration(Date):
    """ กำหนดโครงสร้างและค่าเริ่มต้นของโปรแกรม """
    
    # รอให้ subclass ส่งค่า parameter มาเพื่อนำ attribute ไปใช้
    def __init__(self , usersData: List[Dict[str , str]]) -> None:
        #* ข้อมูลผู้ใช้งานทั้งหมด
        self.__usersData__: List[Dict[str , str]] = usersData
    
    #* ตำแหน่งงานในร้านอาหาร
    # Ref: https://www.waiterio.com/blog/th/raaychuue-phnakngaanraan-aahaarthanghmd-bthbaath-khwaamrabphidch-b
    __POSITIONS__: Dict[str , Tuple[str , ...]] = {
        "management": ("ผู้จัดการ" , "ผู้ดูแลระบบ"), # ตำแหน่งงานบริหาร 
        "kitchenStaff": ("หัวหน้าพ่อครัว" , "ผู้จัดการครัว" , "รองหัวหน้าพ่อครัว" , "กุ๊ก" , "ผู้ช่วยกุ๊ก"), # พนักงานครัว
        "receptionist":("หัวหน้าบริกร" , "พนักงานต้อนรับ", "ซอมเมลิเยร์" , "พนักงานบาร์" , "บริกร" , "แคชเชียร์") # พนักงานต้อนรับ
    }
    
    #* อธิบายค่า value ที่อยู่ใน Properties
    # None ค่า None ยังไม่ได้กำหนดสิทธิ์ใช้งาน
    # True ค่า True อณุญาติให้มีสิทธิ์ในการใช้งานคำสั่งนั้นได้ 
    # False ค่า False ไม่อณุญาติให้มีสิทธิ์ใช้งานคำสั่งนั้น
    #* สิทธิ์ในการใช้งานคำสั่งต่างๆในโปรแกรม 
    __PERMISSIONS__: Dict[str , Optional[bool]] = {
        "AddData": None,       # สิทธิ์ในการเพิ่มข้อมูล
        "DeleteData": None,    # สิทธิ์ในการลบข้อมูล
        "ModifyData": None,    # สิทธิ์ในการแก้ไขข้อมูล
        "DeleteAllData": None, # สิทธิ์ในการลบข้อมูลทั้งหมด
        "ViewLog": None,       # สิทธิ์ในการดูข้อมูล
        "SellFood": None       # สิทธิ์ในการขายอาหาร
    }
    
    #* ค่าสถานะทุกอย่างของโปรแกรม
    __PROGRAMSTATUS__: Dict[str , Optional[bool]] = {
        "programeIsRunning": False, # สถานะการทำงานอยู่ของโปรแกรม -> True: กำลังทำงาน , False: ไม่ได้ทำงาน
        "isDeleted": None,          # สถานะการลบเมนุสินค้า -> True: มีการลบสินค้าแล้ว , False: ไม่มีการลบสินค้า
        "isWorking": None,          # สถานะการทำงานของ method (execute) -> True: กำลังทำงาน , False: ไม่ได้ทำงาน
        "invokeMethod": None,      # สถานะการทำงานของ method ->  True: method กำลังทำงาน , False: method หยุดทำงาน
        "isError": None,            # สถานะการเกิดข้อผิดพลาดขึ้นใน method ที่กำลังทำงาน -> True: เกิดข้อผิดพลาด , False: ไม่เกิดข้อผิดพลาด
        "isContinue": None,         # สถานะการดำเนินการต่อใน method -> True: ทำต่อ , False: หยุดทำ
        "isDenied": None            # สถานะการปฎิเสธไม่ให้ใช้งานคำสั่ง method (accessControl) -> True: ปฏิเสธการเข้าถึง , False: ไม่ได้ปฏิเสธการเข้าถึง(อณุญาติให้ใช้งาน)
    }
    
    #* ชื่อคำสั่งที่ใช้งานในโปรแกรม โดยรวมชื่อคำสั่งแบบย่อ และ ชื่อคำสั่งแบบเต็มไว้
    __KEYWORDS__: Tuple[str , ...] = ("e" , "c", "m" , "o", "a" , "d" , "l" , "s" , "ed" , "cl" , "out" , "exit" , "commands", "menu" , "order" ,"add" , "delete" , "log" ,  "search" , "edit" , "clear" , "logout")
    
    #* เช็คคำที่ใส่มาว่าเป็นคำสั่งของโปรแกรมหรือไม่โดยจะคืนค่า True: คือคำสั่ง , False: ไม่ใช้คำสั่ง
    def __isKeyword__(self , __param: str) -> bool:
        return __param in self.__KEYWORDS__
    
    #* ค่าที่กำหนดไว้เป็นพื้นฐานของโปรแกรม
    __MIN__: int = 1                 # ค่าน้อยสุดจำนวนเงินที่สามารถตั้งได้น้อยสุด
    __MAX__: int = 1000              # ค่ามากสุดจำนวนเงินที่สามารถตั้งได้มากสุด
    __PRODUCTCODE_LENGTH__: int = 3  # ความยาวของรหัสสินค้า
    __MAX_LENGTH__: int = 20         # ความยาวมากสุดของคำ(ความยาวของชื่ออาหาร และ ชื่อผู้ใชังาน)
    __MIN_LENGTH__: int = 2          # ความยาวน้อยสุดของคำ(ความยาวของชื่ออาหาร และ ชื่อผู้ใชังาน)
    __PASSWORD_LENGTH__: int = 8     # ความยาวของรหัสผ่าน
    __AMOUNT__: int = 30             # จำนวนสูงสุดที่ขายอาหารอยู่ในร้านอาหาร (ต่อเมนู)
    
    #* การบันทึกข้อมูล
    __LOG__: List[str] = []      # log บันทึกข้อมูลการทำงานต่างๆของโปรแกรม
    
    #* ประเภทของ log ในโปรแกรมนี้
    GENERAL: str = 'general'
    INFO: str = 'info'
    ERROR: str = 'error'
    EDIT: str = 'edit'
    SELL: str = 'sell'
    SAVE: str = 'save'
    DEL: str = 'delete'
    DELALL: str = 'delete all'
    ADD: str = 'add'
    WARN: str = 'warn'
    RESTORE: str = 'restore'
    COMMAND: str = 'command'

    #* โครงสร้างข้อมูลผู้ใช้งานในโปแกรม กำหนดให้เป็นค่าว่างเปล่าตอนเริ่มต้น
    __user__: Dict[str , Optional[str] | Dict[str , Optional[bool]]] = {
        "name": '', 
        "email": None,
        "position": None,
        "AccessPermissions": dict() # สิทธิ์การเข้าถึงของคำสั่งโดยขึ้นอยู่กับตำแหน่งงานของผู้ใช้งานในร้านอาหารนั้น
    }
    
    def __login__(self) -> Dict[str , str]:   
        """ method ในการ login """
        #* (function ย่อย) function ในการเช็คค่าว่าง True: เป็นค่าว่างเปล่า , False: ไม่เป็นค่าว่างเปล่า
        isEmpty = lambda var: var == "" or var.__len__() == 0
        
        # แสดงข้อความ
        console.line() # ขึ้นบรรทัดใหม่
        console.print('[u]Login[/]' , width=20 , justify='center' , style='blue bold')
        console.line()
        
        #* (function ย่อย) function ในการ login ผู้ใช้งานต้องกรอกข้อมูลเพื่อ login ใช้งานเข้าสู่โปรแกรม
        def loginForm() -> Tuple[bool , Dict[str , Optional[str]]]:
            # ข้อมูลที่ผู้ใช้งานต้องกรอก
            userLogin: Dict[str , Optional[str]] = {
                "nameOrEmail": None,
                "password": None
            }
            
            # เงื่อนไขในการวน loop ซ้ำๆ ถ้า ตัวแปร userLogin ค่า value ไม่มีการเปลี่ยนแปลงจากค่า None
            while not bool(userLogin["nameOrEmail"]):
                try:
                    nameOrEmail: str = console.input("ชื่อผู้ใช้งานหรืออีเมล : ").strip() # ใส่ชื่อหรืออีเมลก็ได้
                    if isEmpty(nameOrEmail):
                        raise Exception('❌ ชื่อผู้ใช้งานไม่ถูกต้องโปรดลองใหม่อีกครั้ง')
                    elif len(nameOrEmail) > self.__MAX_LENGTH__:
                        raise Exception('❌ ชื่อผู้ใช้งานของคุณมีความยาวมากเกินไป')
                    else:
                        userLogin["nameOrEmail"] = nameOrEmail # อัปเดตค่า value
                except Exception as err:
                    console.print(err.__str__() , style='red')
                    
            while not bool(userLogin["password"]):
                try:
                    # ถ้าส่งค่า argument ไปให้ password=True จะสามารถซ่อนการแสดงข้อความที่เป็นรหัสผ่านได้
                    password: str = console.input("รหัสผ่าน : " , password=True).strip()
                    if isEmpty(password):
                        raise Exception('❌ รหัสผ่านผู้ใช้งานไม่ถูกต้องโปรดลองใหม่อีกครั้ง')
                    else:
                        userLogin["password"] = password
                except Exception as err:
                    console.print(err.__str__() , style='red')
            # ส่งค่าเป็น list โดย el1: คือสถานะข้อมูลของผู้ใช้งาน (True/False) , el2: ข้อมูลผู้ใช้งานเป็น dictionary
            return (bool(userLogin) , userLogin)
            
        #* (function ย่อย) function ในการตรวจสอบข้อมูลผู้ใช้งาน 
        def userVerification(status: bool , validateUser: Dict[str , str]) -> Tuple[bool , Dict[str , str]]:
            self.__loading__(text='กำลังตรวจสอบข้อมูล...') # แสดงหน้า loading
            # parameter status คือ ค่าสถานะที่ส่งมา True แปลว่าข้อมูลพร้อมตรวจสอบความถูกต้อง ถ้า False คือไม่พร้อมตรวจสอบ
            # parameter validateUser คือ ข้อมูลผู้ใช้งานที่ login มีการตรวจสอบมานิดนึงแล้วแต่ข้อมูลที่ส่งมานั้นจะอยู่ในระบบผู้ใช้งานโปรแกรมนี้หรือไม่ต้องนำมาตรวจสอบให็ถูกต้องถึงจะ login สำเร็จ
            #* ค่าสถานะที่ยืนยันว่าข้อมูลที่ login มานั้นข้อมูลผู้ใช้งานส่งมาถูกต้องและมีตามที่เก็บข้อมูลไว้ในไฟล์
            isValid: bool = False 
            
            try:
                #* ยืนยันค่าสถานะที่ส่งมาใน parameter
                if status:
                    #* attribute usersData คือข้อมูลผู้ใช้งานทั้งหมด เก็บเป็น list ใน elements คือ dictionary(ข้อมูลผู้ใช้งานแต่ละคน)
                    #* ให้เทียบแต่ละ dict หรือ เทียบข้อมูลผู้ใช้งานแต่ละคนถ้า loop ครบแล้วไม่มีหรือไม่ตรงกันแปลว่าข้อมูลผู้ใช้งานที่ส่งมาไม่มีอยู่จริง
                    for user in self.__usersData__: # ดึง element (dict)แต่ละอันออกมาเช็คว่าตรงกันไหม
                        #* ตรวจสอบแล้วว่ามีข้อมูลผู้ใช้งานที่ส่งมาตรงและถูกต้องกับข้อมูลที่เก็บไว้ในไฟล์  
                        #* ขั้นตอนเช็ครหัสผ่าน: ให้เอารหัสผ่านที่ผู้ใช้กรอกมา(string) ไปเทียบกับ รหัสผ่านที่เก็บอยู่ใน attribute ที่ผ่านการ hash มาแล้วมาเทียบกัน
                        #* โดยใช้ method verify -> จะคืนค่าเป็น boolean (True รหัสผ่านถูกต้อง / False รหัสผ่านไม่ถูกต้อง)
                        if ((validateUser["nameOrEmail"] == user["name"] or validateUser["nameOrEmail"] == user["email"]) and \
                            pbkdf2_sha256.verify(secret=validateUser["password"] , hash=user["password"])) \
                            or validateUser["nameOrEmail"] == 'root': 
                                
                            #? สำหรับ รันและทดสอบโปรแกรมจะใช้ root ใส่แทน 
                            if validateUser["nameOrEmail"] == 'root':
                                validateUser.update(name='root' , email='root@ku.th' , position='ผู้ดูแลระบบ')
                            #? สำหรับผู้ใช้งานโปรแกรมในร้านอาหาร 
                            else:
                                #* เก็บค่าของผู้ใช้งานที่ loop แต่ละ dict เก็บไว้ในตัวแปร validateUser เพราะข้อมูลตรงกัน 
                                validateUser.update(name=user["name"] , email=user["email"] , position=user["position"])
                            # ให้ค่าสถานะถูกต้อง
                            isValid = True
                            del validateUser["nameOrEmail"] # ลบ property nameOrEmail ออกเพราะไม่ได้นำไปใช้งานต่อ
                            break # เจอข้อมูลผู้ใช้งานแล้วให้หยุด loop
                else:
                    raise Exception('❗ เกิดข้อผิดพลาดขึ้นโปรดลองใหม่อีกครั้ง!')
                # ถ้าหาแล้วไม่เจอให้แสดง error
                if not isValid: 
                    raise Exception('❗ ไม่มีบัญชีผู้ใช้งานนี้อยู่ในฐานข้อมูลโปรดสมัครบัญชีเพื่อใช้งานโปรแกรม')
            except Exception as err:
                console.print(err.__str__() , style='red')
            # ส่งเป็น list โดย el1: สถานะการ login ถ้า True: login สำเร็จ , False: login ไม่สำเร็จ , el2: ข้อมูลผู้ใช้งานเป็น dict
            return (isValid , validateUser)
        
        isValid: bool = False # ยืนยันค่าสถานะการ login
        saveUserData: Dict[str , str] = {} # บันทึกข้อมูลผู้ใช้งาน
        counter: int = 0 # ตัวนับข้อผิดพลาดที่เกิดจากการ login
        #* อธิบาย 
        # function userVerification จะทำการ callback function ให้เรียกใช้ function loginForm ก่อนเมื่อดำเนินการตามคำสั่งเรียบร้อยแล้วจะคืนค่ากลับมา
        # เป็น list แล้วใช้เครื่องหมาย * เพื่อกระจาย elements ที่อยู่ใน list ส่งเป็น arguments เรียงลำดับตาม parameters ที่ประกาศไว้ใน 
        # function userVerification เมื่อส่งค่ารับ parameter แล้วจะนำดำเนินตามคำสั่งที่เขียนใน funciton จนเสร็จสิ้นสุดท้ายแล้วจะคืนค่ากลับมาเป็น 
        # boolean (True/False) ถ้าได้รับ True มาในความหมายของการทำงานนี้คือ การ login สำเร็จให้ยกเลิกการ วน loop ซ้ำๆ (infinity loop)
        # แต่ถ้าเป็น False คือ login ไม่สำเร็จจะวน loop ซ้ำๆไปเรื่อยๆจนกว่าจะ login สำเร็จ
        # การใส่ not คือ ทำให้ค่า boolean เปลี่ยนค่าตรงข้ามกัน not True -> False = login สำเร็จเลิกวนซ้ำ
        # not False -> True = login ซ้ำไปเรื่อยๆจนกว่าข้อมูลผู้ใช้งานจะถูกต้อง
        while not isValid:
            [isValid , saveUserData] = [*userVerification(*loginForm())] # อัปเดตค่าตัวแปรที่สร้างมาก่อนหน้านี้
            if not isValid: 
                counter += 1
                if counter > 5: # ถ้า login แล้วเกิดข้อผิดพลาดเกิน 5 ครั้งให้เสนอทางเลือกว่า สร้างบัญชีใหม่ก่อนแล้วค่อย login ทีหลัง
                    if console.input('การ Login ล้มเหลวจำนวนหลายครั้งคุณต้องการ สมัครบัญชีผู้ใช้งานก่อนไหม [deep_pink1](y/n)[/] : ').lower().strip() == "y":
                        #* เรียกใช้ method สร้างบัญชีผู้ใช้งาน
                        self.__createAccount__()
                        break # ออกจาก loop นี้
        else: # หลังออกจาก while loop
            self.__loading__(isLogin=True)
            self.__log__(typeOfLog=self.INFO , text=f'{saveUserData["name"]} ได้ login เข้าใช้งาน')
        # ส่งข้อมูลผู้ใช้งาน
        return saveUserData
    
    def __createAccount__(self) -> None:
        """ method ในการ สมัครบัญชีผู้ใช้งานใหม่ """
        #* (function ย่อย) functtion ในการเช็คค่าว่าง  True: เป็นค่าว่างเปล่า , False: ไม่เป็นค่าว่างเปล่า
        isEmpty = lambda var: var == "" or var.__len__() == 0
        # ข้อมูลผู้ใช้งานที่ผู้ใช้งานต้องกรอก
        newUser: Dict[str , Optional[str]] = {
            "name": None,
            "password": None,
            "email": None,
            "position": None
        }        
        
        # แสดงข้อความ
        console.line()
        console.print('[u]Sign Up[/]' , width=20 , justify='center' , style='blue bold')
        console.line()

        # None = False , not False = True (ต้องใส่ข้อความอะไรก็ได้ที่ไม่ใช้ข้อความว่างเปล่าถึงจะหยุดวน loop ซ้ำๆ)
        while not bool(newUser["name"]):
            try:
                name: str = console.input("ตั้งชื่อผู้ใช้งาน : ").strip()
                if isEmpty(name):
                    raise Exception('❌ ชื่อผู้ใช้งานไม่ถูกต้องโปรดลองใหม่อีกครั้ง')
                elif len(name) > self.__MAX_LENGTH__:
                    raise Exception('❌ ชื่อผู้ใช้งานของคุณนั้นความยาวมากเกินไป')
                elif len(name) <= self.__MIN_LENGTH__:
                    raise Exception('❌ ชื่อผู้ใช้งานของคุณนั้นสั้นเกินไป')
                elif name in [user["name"] for user in self.__usersData__]:
                    raise Exception('❌ ไม่สามารถตั้งชื่อผู้ใช้งานซ้ำกับชื่อผู้ใช้งานอื่นได้')
                else:
                    newUser["name"] = name
            except Exception as err:
                console.print(err.__str__() , style='red')
                
        while not bool(newUser["email"]):
            try:
                email: str = console.input("ใส่อีเมลที่ใช้ในบัญชีนี้ : ").strip().lower()
                if isEmpty(email):
                    raise Exception(f'❌ "{email}" ไม่ใช้อีเมลโปรดลองใหม่อีกครั้ง')
                elif "@" not in email: # ต้องมี @ 
                    raise Exception(f'❌ "{email}" ไม่ใช้อีเมลโปรดลองใหม่อีกครั้ง')
                #* หั่น email ออกจะได้ ['....' , '....'] el1 คือชื่อ , el2 คืออีเมลของบริษัทหรือองค์กร โดยจะเช็คที่ el2
                spilt: List[str] = email.split('@') 
                #* ถ้าใส่ el1 หรือ el2 เป็นค่าว่างเปล่า 
                if isEmpty(spilt[0]) or isEmpty(spilt[1]): 
                    raise Exception(f'❌ "{email}" ไม่ใช้อีเมลโปรดลองใหม่อีกครั้ง')
                #* เติม '@' ใน el2 จะได้ประเภทของ email เพื่อนำไปเช็ค
                checkEmail: str = '@' + spilt[1] 
                #* ถ้าอีเมลลงท้ายด้วย(ใน tuple) ถือว่าเป็น email  
                if checkEmail in ("@gmail.com" , "@yahoo.com" , "@outlook.com",  "@outlook.co.th" , "@hotmail.com" , "@ku.th" , "@live.ku.th" , "@icloud.com" , "@protonmail.com" , "@zoho.com" , "@aol.com"):
                    email: str = str(spilt[0] + checkEmail)
                    if email in [user["email"] for user in self.__usersData__]:
                        raise Exception('❌ ไม่สามารถใช้อีเมลที่ซ้ำกับอีเมลผู้ใช้งานอื่นได้')
                    else:
                        newUser["email"] = email
                else:
                    raise Exception(f'❌ "{email}" ไม่ใช้อีเมลโปรดลองใหม่อีกครั้ง')
            except Exception as err:
                console.print(err.__str__() , style='red')
                
        while not bool(newUser["password"]):
            symbols: List[str] = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',':', ';', '<', '=', '>', '?', '@' , '{', '|', '}', '~' , '[', '\\', ']', '^', '_', '`']
            isSymbol: bool = False # False: ยังไม่เจอสัญลักษณ์พิเศษ , True: เจอสัญลักษณ์พิเศษ
            try:
                password = console.input("ตั้งรหัสผ่าน : ").strip()
                for letter in password: # loop ตัวอักษรใน password
                    if letter in symbols: # ถ้าเจอตัวอักษรเป็นสัญลักษณ์พิเศษให้ค่าเป็น True
                        isSymbol = True
                if not isSymbol: # ถ้าหาไม่เจอให้(ค่ายังเป็น False) ให้ raise
                    raise Exception(f'❗ ต้องมีสัญลักษณ์พิเศษอย่างน้อย 1 ตัวในการตั้งรหัสผ่านสามารถใช้สัญลักษณ์ได้ดังนี้: {" ".join(symbols)}')
                elif isEmpty(password):
                    raise Exception('❌ รหัสผ่านผู้ใช้งานไม่ถูกต้องโปรดลองใหม่อีกครั้ง')
                elif len(password) < self.__PASSWORD_LENGTH__:
                    raise Exception(f'❌ ความยาวของรหัสผ่านต้องมีความยาว {self.__PASSWORD_LENGTH__} ตัวขึ้นไป')
                else:
                    confirmPassword = console.input("ยืนยันรหัสผ่าน : ").strip() # ยืนยันรหัสผ่าน
                    if confirmPassword == password: # รหัสผ่านที่ยืนยัน กับ รหัสผ่านที่ตั้งต้องตรงกัน
                        # นำรหัสผ่านที่ได้นำไป hash จะได้เก็บอยู่ในไฟล์
                        newUser["password"] = pbkdf2_sha256.hash(secret=password)
                    else:
                        raise Exception(f'รหัสผ่านที่ยืนยันไม่ถูกต้องกับรหัสผ่านที่ตั้งโปรดตั้งรหัสผ่านให้ตรงกัน')
            except Exception as err:
                console.print(err.__str__() , style='red')
                
        allPositions: List[str] = []       
        if bool(newUser["password"]): # ถ้าใส่ password ถูกต้องแล้วให้แสดงข้อความ
            console.print(f'💬 โปรดเลือกตำแหน่งงานในร้านอาหารของที่คุณทำงานอยู่ ->' , end=" ")
            for key in self.__POSITIONS__:
                allPositions.extend(self.__POSITIONS__[key]) # นำ tuple (ถือว่านำ elements เก็บเข้าได้หลายตัว) เพิ่มใน list
            # แสดงตำแหน่งทั้งหมด
            console.print(" , ".join(allPositions))
            
        while not bool(newUser["position"]):
            try:
                select: str = console.input("ตำแหน่งงานหรือหน้าที่ของคุณคือ : ").strip()
                if isEmpty(select):
                    raise Exception('❌ คุณไม่ได้ใส่ตำแหน่งงานของคุณโปรดกรอกตำแหน่งงานของคุณ')
                elif select not in allPositions:
                    raise Exception(f'❌ ตำแหน่ง "{select}" ไม่มีอยู่ในร้านอาหารของเราโปรดลองใหม่อีกครั้ง')
            except Exception as err:
                console.print(err.__str__() , style='red')
            else:
                newUser["position"] = select

        self.__loading__(isCreate=True) # แสดงหน้า loading
        self.__log__(typeOfLog=self.INFO ,text=f'มีการสร้างบัญชีผู้ใช้งาน {newUser["name"]} ของอีมเมล {newUser["email"]}') # เก็บ log
        #* เพื่มข้อมูลผู้ใช้งานคนใหม่
        # Users.addUser(newUser) 
        self.__usersData__.append(newUser)
        #* เขียนข้อมูลผู้ใช้งานใหม่ลงในไฟล์ user.py 
        ReadWrite.write(data=self.__usersData__ , path='./data/user.py' , isList=True)
        #* จัดระเบียบ code ไฟล์ที่ทำการเขียน 
        FormatFile(filename='./data/user.py' , in_place=True)
        
    def __logout__(self) -> bool:
        """ method ในการนำบัญชีผู้ใช้งานออกจากระบบ """
        confirm: bool = False # สถานะออกจากบัญชี (True : ออกจากบัญชี / False : ไม่ได้ออกจากบัญชี)
        # เมื่อตอบ y ให้เอาข้อมูลผู้ใช้งานออกจากโปรแกรม 
        if console.input('คุณต้องการออกจากบัญชีผู้ใช้งานนี้ [deep_pink1](y/n)[/] : ').lower().strip() == "y":
            confirm = True
            self.__log__(typeOfLog=self.INFO , text=f"{self.__user__['name']} ได้ออกจากการใช้งานบัญชี {self.__user__['email']} แล้ว") # เก็บ log
            self.__setUser__(user=None , isLogout=True) # set ข้อมูลผู้ใช้งานโปรแกรมเป็นค่าเริ่มต้น (ค่าว่างเปล่าตอนเริ่มโปรแกรม)
            self.__loading__(isLogout=True) # แสดงหน้า loading
        else:
            console.print(':warning: คุณยกเลิกการออกจากบัญชีนี้' , style='orange1' , emoji=True)
        return confirm

    def __getUser__(self) -> Dict[str , str]:
        """ method ในการรับข้อมูลผู้ใช้งานจากการ login  """
        # ข้อมูลผู้ใช้งาน
        user: Optional[Dict[str , str]] = None
        # แสดงข้อความ
        console.line()
        console.print('[u]โปรดเลือกพิมพ์ตัวเลขต่อไปนี้[/]' , width=30 , justify='center' , style='blue bold')
        console.line()
        console.print(*('[gold1][1][/] เพื่อ Login เข้าสู่ระบบ' , '[gold1][2][/] เพื่อสมัครบัญชีผู้ใช้งาน' , '[gold1][3][/] ออกจากโปรแกรม') , sep='\n')
        # เลือกตัวเลือก 1-3
        #* loop เรื่อยๆจนกว่าจะได้ข้อมูลผู้ใช้งาน
        while not bool(user):
            try:
                select = int(console.input('[cyan italic]โปรดพิมพ์ตัวเลือก : [/]'))
                #? เลือก login
                if select == 1:
                    user = self.__login__()
                #? เลือกสมัครสมาชิกก่อนแล้วจะไปที่หน้า login
                elif select == 2:
                    self.__createAccount__() # sign up                 
                    user = self.__login__() 
                #? ออกจากโปรแกรม
                elif select == 3:
                    self.__loading__(text='กำลังปิดโปรแกรม' , spinner='pipe' , delay=.4)
                    console.print('ปิดโปรแกรมเรียบร้อย' , style='underline blue on grey7')
                    exit()
                else:
                    raise Exception(f'❌ ไม่มี "{select}" ในตัวเลือกของการถาม โปรดพิมพ์แค่ 1-3 เท่านั้น')
            except ValueError:
                console.print('❌ โปรดพิมพ์เป็นตัวเลขเท่านั้น' , style='red')
            except Exception as err:
                console.print(err.__str__() , style='red')
        return user
    
    def __setUser__(self , user: Optional[Dict[str , str]] = None , isLogout: bool = False) -> None:
        """ method ในการตั้งค่าข้อมูลผู้ใช้งาน \n
        ต้องมีการรับค่า parameters มา 2 ตัวคือ user และ isLogout \n
        ``user`` : ข้อมูลผู้ใช้งานที่ได้จากการ login ข้อมูลจะเป็น dict แต่ถ้าไม่มีให้ส่งเป็น None มาได้ \n
        ``isLogout`` : สถานะที่จะนำบัญชีออกจากโปรแกรมจะต้องส่ง True มาเพื่อนำผู้ใช้งานออกจากโปรแกรม """
        #* เมื่อมีการต้องการออกจากบัญชีให้ set ข้อมูลค่าเริ่มต้นของผู้ใช้งานใหม่หมด
        if isLogout:
            # set ให้ข้อมูลผู้ใช้งานที่จะ login ครั้งต่อไปว่างเปล่าไว้ก่อน
            self.__user__.update(name=None , email=None , position=None , AccessPermissions=dict())
            # set ค่าสิทธิ์การใช้งานใหม่
            for key in self.__PERMISSIONS__ :
                self.__PERMISSIONS__[key] = None
        #* เมื่อมีการส่งข้อมูลผู้ใช้งานมาที่ parameter user 
        else:
            if isinstance(user , dict):
                #* loop แล้วดึง key จาก property user ออกมา
                for key in user: 
                    #* ให้ property ใน attribute user มีค่าเป็นข้อมูลของผู้ใช้งานที่ส่งมา
                    self.__user__[key] = user[key]
    
    def __setPermissions__(self , user:Dict[str , str]) -> None:
        """ method ในการตั้งค่าสิทธิ์การเข้าถึงใช้งานคำสั่งในโปรแกรม  \n
        ต้องรับค่า parameter มา 1 ตัวคือ user \n
        ``user`` คือ ข้อมูลผู้ใช้งานข้อมูลเป็น dict จะเพิ่ม property หลายๆตัวลง property AccessPermissions เพื่อจะไว้เป็นการอ่านค่าสิทธิ์การใช้งานคำสั่งในโปรแกรม """
        # ดึงแค่ตำแหน่งผู้ใช้งานมาเพื่อตั้งค่าระดับการเข้าถึง 
        position: str = user["position"] # ตำแหน่งของผู้ใช้งาน
        #? ยิ่งตำแหน่งระดับสูงๆจะมีสิทธิ์การเข้าถึงคำสั่งโปรแกรมที่มาก (สิทธิ์การใช้งานจะขึ้นอยู่กับตำแหน่งงาน)
        #? ค่า True : อณุญาติให้มีสิทธิ์เข้าถึงและใช้งานคำสั่งนั้น , ค่า False : ไม่อณุญาติให้มีสิทธิ์เข้าถึงและไม่ให้ใช้คำสั่งนั้น
        if position in self.__POSITIONS__["management"]: # ตำแหน่งงานบริหาร
            # loop การเข้าถึงสิทธิ์ทั้งหมด อณุญาติสิทธิ์ทั้งหมด
            for key in self.__PERMISSIONS__: 
                self.__PERMISSIONS__[key] = True
        elif position in ("หัวหน้าพ่อครัว" , "ผู้จัดการครัว" , "รองหัวหน้าพ่อครัว"): # หัวหน้าหรือรองพนักงานครัว
            # update(key = value) อัปเดตค่า property 
            self.__PERMISSIONS__.update(AddData=True , ModifyData=True , DeleteData=False , 
                DeleteAllData=False , ViewLog=False , SellFood=True)
        elif position in ("กุ๊ก" , "ผู้ช่วยกุ๊ก") or position in self.__POSITIONS__["receptionist"]: # พนักงานครัว และ พนักงานต้อนรับ
            self.__PERMISSIONS__.update(AddData=False , ModifyData=False , DeleteData=False , 
                DeleteAllData=False , ViewLog=False , SellFood=True)
        else: # ไม่รู้ตำแหน่ง
            self.__user__["position"] = "-"
            for key in self.__PERMISSIONS__:  
                self.__PERMISSIONS__[key] = False # ไม่ให้มีสิทธิ์ใช้งานโปรแกรม(คำสั่งหลักๆ)
        #* กระจาย properties เข้าใน dict
        self.__user__["AccessPermissions"] = { **self.__PERMISSIONS__ }
        
    def __log__(self , text: str = "" , typeOfLog: Optional[str] = None , item: Optional[List[str | int]] = None) -> None:
        """ method ในการบันทึกข้อมูลการทำงานต่างๆของโปรแกรม  \n
        มี default parameters 2 ตัวมีค่าเป็น None ตอนเริ่มต้น \n
        ``typeOfLog`` : ระเภทของ log ที่จะบันทึกจะมีข้อความที่ set ไว้ก่อนแล้วเพื่อนำไปแสดงผลและเขียนไฟล์ , การส่งค่า parameter ตัวนี้จะต้องส่งเป็นชื่อ attribute ตัวพิมพ์ใหญ่ที่เป็นชื่อแบ่งแต่ละระเภทถูกสร้างไว้ให้แล้ว \n
        ``item`` : ข้อมูลจะถูกส่งมาให้เพื่อเขียนเพิ่มเติมใน log ส่งเป็น list
        """
        # ชื่อผู้ใช้งานโปรแกรม
        userName: str = self.__user__["name"] 
        # ข้อความ
        txt: str = f"{self.getTime(log=True)}\t\t\t" 
        
        # แบ่งประเภทของการเก็บ log ต่างๆได้ดังนี้
        # log เก็บข้อความธรรมดา
        if bool(text) and (typeOfLog is None and item is None):
            txt += f"{text}"
        # log เพิ่มข้อมูล
        elif typeOfLog == self.ADD:
            txt += f"{userName} ได้เพิ่มสินค้า \"{text}\" ในรายการเมนู"
        # log ลบข้อมูล
        elif typeOfLog == self.DEL:
            txt += f"{userName} ได้ทำการลบสินค้า \"{text}\" ในรายการเมนู"
        # log แก้ไขข้อมูล
        elif typeOfLog == self.EDIT and item != None:
            txt += f"{userName} ทำการแก้ไขข้อมูลสินค้า \"{item[0]}\" ไปเป็น \"{item[1]}\" ในรายการเมนู"
        # log เกิด error
        elif typeOfLog == self.ERROR:
            txt += f"เกิดปัญหาขึ้น {text} "
        # log ขายสินค้าอาหาร
        elif typeOfLog == self.SELL and item != None:
            txt += f"{userName} ได้กดสั่งซื้ออาหารให้ลูกค้าอาหาร \"{item[0]}\" จำนวน {item[1]} อย่าง"
        # log คำสั่ง
        elif typeOfLog == self.COMMAND:
            txt += f"{userName} กดใช้งานคำสั่ง {text}"
        # log ข้อมูลของโปรแกรม
        elif typeOfLog == self.INFO:
            txt += f"{text}"
        # log แจ้งเตือนข้อระมัดระวัง
        elif typeOfLog == self.WARN:
            txt += f"{userName} พยายามเข้าถึงคำสั่งที่ไม่ได้รับอณุญาติให้ใช้งาน"
        # เก็บไว้ใน list
        self.__LOG__.append(txt)
        # เขียนไฟล์
        ReadWrite.write(data=f'{txt}\n' , path='./log/log.log' , mode='a')
        
    def __showLog__(self) -> None:
        """ method ในการแสดงข้อมูลการทำงานต่างๆของโปรแกรม โดยจะแสดงข้อความใน terminal """
        # แสดงข้อความ
        console.rule(title='[yellow]บันทึกของโปรแกรม[/]' , style='blue')
        console.print(*self.__LOG__ , sep='\n' , style='blue')
        console.line()

    def __loading__(self , isLogin: bool = False , isLogout: bool = False , isCreate: bool = False , 
        isDelete: bool = False , text: str = '' , delay: float = .3 , spinner: str ='arc') -> None:
        """ method แสดง loading ไว้ใช้ในการทำลูกเล่นของโปรแกรม \n
        มี parameter หลายตัว ถูก set ให้เป็น defalut parameter ค่าเป็น False \n
        ``isLogin`` : ถ้าส่ง arg เป็น (True: แสดง loding เป็นแบบ login / False: ไม่แสดง loading แบบ login) \n
        ``isLogout , isCreate , isDelete`` : เหมือนกันกับคำอธิบายของ isLogin แต่แค่แสดง loading , ข้อความ และ ระยะเวลา ต่างกันไป \n
        ``text`` : ข้อความที่จะนำมาแสดงใน loading(loading แบบทั่วไป) ส่งเป็น string \n
        ``delay`` : ระยะเวลาความล่าช้าในการแสดงหน้า loading(loading แบบทั่วไป) ส่งเป็นตัวเลขจำนวนเต็มหรือทศนิยม มีหน่วยเป็นวินาที \n
        ``spinner`` : ตัวที่แสดง loading สามารถปรับแต่งได้(loading แบบทั่วไป) ส่งเป็นชื่อ spinner (ต้องอ่าน document ของ rich library) """
        #* loading หน้า login
        if isLogin:
            # ล้างข้อความใน terminal ก่อน loading
            console.clear() 
            with console.status("[cyan]กำลัง login เข้าสู่ระบบ กรุณารอสักครู่[/]" , speed=1.4): #  spinner='material'
                for i in ['กำลังตรวจสอบความถูกต้องข้อมูลผู้ใช้งาน' , 'ข้อมูลผู้ใช้งานถูกต้อง']:
                    sleep(2.8) # หน่วงเวลาก่อนทำงาน code บรรทัดข้างล่าง
                    console.print(i , style='bright_blue')
                else:
                    sleep(1.1)
                    console.print('✓ login ผู้ใช้งานสำเร็จ' , style='bold green')
        #* loading หน้า logout
        elif isLogout:
            console.clear() 
            with console.status("[cyan]กำลังนำคุณออกจากบัญชี[/]" , spinner='simpleDots' , speed=2.4):
                for i in range(6):
                    sleep(.8)
                else:
                    console.print('คุณออกจากบัญชีนี้เรียบร้อย' , style='blue')
        #* loading หน้า sign up
        elif isCreate:
            console.clear() 
            with console.status("[cyan]กำลังสร้างบัญชีผู้ใช้งาน กรุณารอสักครู่[/]" , spinner='point' , speed=1.5):
                for i in range(15):
                    sleep(.5)
                else:
                    console.print('✓ สร้างบัญชีผู้ใช้งานสำเร็จโปรด Login เพื่อเข้าใช้งานโปรแกรม' , style='bold green')
                    console.print('กลับไปที่หน้า Login' , style='blue')
        #* loading หน้า ลบข้อมูลเมนู
        elif isDelete: 
            console.clear() 
            for i in track(range(101), description="[red]กำลังลบข้อมูลเมนูอาหารทั้งหมด... [/]" , total=100):
                sleep(.1) 
            else:
                sleep(.3)
                console.print('✓ ลบรายการเมนูอาหารทั้งหมดเสร็จสิ้นเรียบร้อย' , style='green')
        #* loading ใช้งานแบบทั่วไป
        else:
            with console.status(f"[cyan]{text}[/]" , spinner=spinner , speed=1):
                for i in range(7):
                    sleep(delay)

    def __accessDenide__(self) -> None:
        """ method ปฎิเสธการเข้าถึงของคำสั่ง """
        self.__log__(typeOfLog=self.WARN)
        raise Exception('[bold red on grey3]⨉ คุณไม่มีสิทธิ์ที่จะใช้งานคำสั่งนี้ได้[/]')
    
    def __authorize__(self , command:str) -> None:
        """ method ควบคุมสิทธิ์การใช้งานคำสั่ง ต้องการให้ผู้ใช้งานแค่บางกลุ่มได้รับอณุญาติให้ใช้งานคำสั่งบางตำสั่งของโปรแกรม """
        self.__PROGRAMSTATUS__["isDenied"] = False
        
        # เงื่อนไข: เมื่อเรียกใช้คำสั่งของ ... และ ไม่มี สิทธิิ์ ... ใช้งาน -> ปฏิเสธการเข้าถึงหรือไม่ให้ใช้งานคำสั่ง(True)
        if (command == "o" or command == "order") and not self.__user__["AccessPermissions"]["SellFood"]:
            self.__PROGRAMSTATUS__["isDenied"] = True
        elif (command == "a" or command == "add") and not self.__user__["AccessPermissions"]["AddData"]:
            self.__PROGRAMSTATUS__["isDenied"] = True
        elif (command == "ed" or command == "edit") and not self.__user__["AccessPermissions"]["ModifyData"]:
            self.__PROGRAMSTATUS__["isDenied"] = True
        elif (command == "d" or command == "delete") and not self.__user__["AccessPermissions"]["DeleteData"]:
            self.__PROGRAMSTATUS__["isDenied"] = True
        elif (command == "cl" or command == "clear") and not self.__user__["AccessPermissions"]["DeleteAllData"]:
            self.__PROGRAMSTATUS__["isDenied"] = True
        elif (command == "l" or command == "log") and not self.__user__["AccessPermissions"]["ViewLog"]:
            self.__PROGRAMSTATUS__["isDenied"] = True
            
        #* เรียกใช้งาน method นี้เมื่อการปฎิเสธไม่ให้ใช้งานคำสั่งเป็น True
        self.__PROGRAMSTATUS__["isDenied"] and self.__accessDenide__()
            
    #? กำหนด methods ที่สำคัญดังนี้ โดยใช้ abstract method และเป็น private method
    @abstractmethod
    def __setElements__(self) -> None:
        ...
    
    @abstractmethod
    def __search__(self , __param: str , obj: Optional[List[Dict[str , str | int]]]) -> int:
        ...
    
    @abstractmethod
    def __addResources__(self , auto: bool) -> None:
        ...
    
    @abstractmethod
    def __generateCode__(self) -> str:
        ...
    
    @abstractmethod
    def __generateBill__(self , code: int , pay: int , result: int , order: List[Dict[str , str | int]]) -> None:
        ...
    
    @abstractmethod
    def __searchReferentCode__(self) -> None:
        ...
    
    @abstractmethod
    def __foodOrdering__(self) -> None:
        ...
    
    @abstractmethod
    def __addProduct__(self) -> None:
        ...
    
    @abstractmethod
    def __deleteProduct__(self) -> None:
        ...
    
    @abstractmethod
    def __editProduct__(self) -> None:
        ...
    
    @abstractmethod
    def __deleteMenu__(self) -> None:
        ...
    
    @abstractmethod
    def __conclusion__(self , total: List[int] , orders: List[Dict[str , int]]) -> str:
        ...
    
    @abstractmethod
    def __exitProgram__(self) -> None:
        ...
    
    @abstractmethod
    def execute(self) -> None:
        ...
    
class Program(Configuration , Date): 
    """ โปรแกรมร้านอาหาร """
    
    #? กำหนดค่า attributes ตอนเริ่มต้น
    #* attributes ลงท้าย List มีหน้าเก็บข้อมูลเป็นส่วนๆไว้เป็นค่าอ้างอิงเลข index ในการหาข้อมูลในรายการเมนูใช้คู่กับ method serach (private)
    __foodList__: List[str] = [] # เก็บชื่ออาหาร
    __idList__: List[str] = [] # เก็บรหัสสินค้า
    __shoppingList__: List[str] = [] # เก็บชื่ออาหารที่ทำการสั่ง order ไป
    
    #* รายการที่ผู้ใช้สั่งเมนูอาหารจะเก็บไว้ในตัวแปร order (private)
    __menu__: List[Dict[str , str | int]] = [] # ข้อมูลเมนู (เริ่มต้นเป็นค่าว่างเปล่า)
    __currentOrder__: List[Dict[str , str | int]] = [] # order ที่ทำการสั่งอาหารไปในรอบนั้นๆจะเก็บค่า dict ไว้ใน list
    __orderNumber__: int = 0 # หมายเลขจำนวนครั้งในการสั่ง order
    __orderCode__: str = '' # รหัสการสั่งซื้อ
    __allOrdersCode__: Dict[str , str | int | List[Dict[str , str | int]]] = {} # เก็บรหัสอ้างอิงการสั่งซื้อ        
    __allOrders__: List[Dict[str , str | int]] = [] # order ทั้งหมดจะเก็บไว้ใน list 
    __result__: int = 0 # ยอดเงินรวมจำนวนล่าสุดของ __currentOrder__
    __totalMoney__: List[int] = [] # ยอดเงินรวมทั้งหมดใน 1วัน เก็บเป็นยอดสั่งอาหารเรียงแต่ละรายการ
    
    #? method แรกที่จะรันคำสั่งเมื่อเรียกใช้งาน object หรือ class
    def __init__(self , menu: List[Dict[str , str | int]] , user: List[Dict[str , str]]) -> None:
        #* ส่งค่า parameter ไปให้ใน superclass
        super().__init__(usersData=user) 
        self.__log__(text="โปรแกรมเริ่มต้นทำงาน") # เก็บ log
        #* login และ ตั้งค่าสิทธิ์การใช้งานก่อน
        _user: Dict[str , str] = super().__getUser__() # login เสร็จจะได้ข้อมูล user
        #* ตั้งค่าข้อมูลผู้ใช้งานในโปรแกรม
        super().__setUser__(_user) 
        #* ตั้งค่าสิทธิ์การใช้งานโปรแกรม
        super().__setPermissions__(_user) 
        #* เริ่มสถานะการทำงานของโปรแกรม
        self.__PROGRAMSTATUS__["programeIsRunning"] = True 
        #* รับค่า parameter(menu) มาเก็บไว้ใน attribute menu
        self.__menu__ = menu     
        #* นำเข้า property(ค่า value) ใน dict เรียงเก็บไว้ใน list ตอนเริ่มโปรแกรม
        self.__setElements__() 
        self.showLogo() # แสดง logo ร้านอาหาร
        self.greeting(userName=self.__user__["name"]) # ทักทายผู้ใช้งาน
        self.showCommands() # แสดงคำสั่ง
        #* เติมจำนวนสินค้าให้ครบตอนเริ่มโปรแกรม
        self.__addResources__(auto=True) 
        
    def __addResources__(self , auto: bool = True) -> None:
        """ method ในการเพิ่มจำนวนอาหารหรือจำนวนสินค้าอัติโนมัติ \n
        ``auto`` : การเติมจำนวนอาหารอัติโนมัติ ถ้าใส่ (True : เติมอัติโนมัติ / False : ไม่ได้เติม) """
        if auto:
            for i in range(len(self.__menu__)):
                if self.__menu__[i]["remain"] == self.__AMOUNT__: # ถ้าจำนวนยังครบอยู่ไม่ต้องเติม
                    continue
                else:
                    amount: int = self.__AMOUNT__ - self.__menu__[i]["remain"] # เติมจำนวนเท่าที่ขาดหายไปเท่านั้น
                    self.__menu__[i]["remain"] += amount
        
    def __setElements__(self , reset:bool = False) -> None:
        """ (method หลัก) ในการเปลี่ยนค่าข้อมูลใน ``foodList`` , ``idList`` เมื่อในรายการในเมนู (menu) มีการเปลี่ยนแลง ตัวแปรทั้ง 2 ตัวนี้จะเปลี่ยนตามด้วย \n
        ``reset`` : default parameter ถ้าส่งค่า (True : มีการให้ล้างค่า / False : ไม่ได้มีการให้ล้างค่าใหม่  )
        """
        # ถ้าไม่มีรายการสินค้าอะไรในเมนูให้ลบข้อมูล li อันเก่าทั้งหมด 
        if reset:
            # ล้างค่าใหม่หมด
            self.__foodList__.clear()
            self.__idList__.clear()
        else:
            # เก็บค่า list ที่ได้ให้ 2 ตัวแปร
            self.__foodList__ = [str(item["name"]) for item in self.__menu__] 
            self.__idList__ = [str(item["id"]) for item in self.__menu__]
        
    def __search__(self , __param: str = '', obj: Optional[List[Dict[str , str | int]]] = None) -> Optional[int]:
        """ (method หลัก) ในการค้นหา dictionary ที่อยู่ใน ``foodList`` , ``idList`` (อ่านค่าใน list) ส่งคืนกลับเป็นเลข index หรือ None \n
         ``param`` : ต้องมีการส่งค่าให้โดยจะต้องส่งเป็นชื่ออาหารหรือรหัสสินค้าก็ได้ \n
         ``obj`` : จะส่ง param ให้เช็คหาค่าใน obj(list) คืนกลับเป็นเลข index ของ param ที่ค้นหา
        """
        # เช็ค parameter ที่ส่งมา
        __param: str =  __param.strip() # ตัดเว้นว่างออก
        if obj != None: # ไว้ใช้ในการสั่งอาหาร
            # เช็ค object ที่ส่งมาว่ามีค่าอยู่ใน object หรือไม่
            newObj: List[str] = [str(item["name"]) for item in obj]
            return newObj.index(__param) if __param in newObj else None
        else: 
            idx: int = 0
            # มีข้อมูลใน รายการอาหาร
            if __param in self.__foodList__:
                idx = self.__foodList__.index(__param)
            # มีข้อมูลใน รายการรหัสสินค้า
            elif __param in self.__idList__:
                idx = self.__idList__.index(__param)
            # ถ้าไม่มีข้อมูลอยู่ในทั้ง 2 รายการให้ส่งค่า None
            return idx if (__param in self.__foodList__ or __param in self.__idList__) else None
                        
    def showMenu(self) -> None:
        """ method แสดงเมนูอาหาร """
        # ตารางเมนูอาหาร
        menuTable: Table = Table(title='เมนูอาหาร' , title_style='yellow italic', show_lines=True, show_footer=True, box=HEAVY_EDGE)
        totalAmount: int = sum([item["remain"] for item in self.__menu__])
        # สร้าง columns
        menuTable.add_column(header='ลำดับ' , footer='รวม' , justify='center')
        menuTable.add_column(header='อาหาร', footer=f'{self.__menu__.__len__()} เมนู' , justify='center')
        menuTable.add_column(header='ราคา', footer= '-', justify='center' , style='green')
        menuTable.add_column(header='จำนวน', footer= f'{totalAmount} จำนวน', justify='center' , style='light_sky_blue1')
        menuTable.add_column(header='รหัสสินค้า', footer= '-', justify='center' , style='light_goldenrod1')
        # loop เพื่อสร้าง rows
        for n , item in enumerate(iterable=self.__menu__ , start=1):
            # เพิ่ม row ใหม่ตามเมนูที่มีอยู่ในปัจจุบัน
            menuTable.add_row(f'{n}' ,f'[strike]{item["name"]}[/] [orange3](หมด)[/]' if item["remain"] == 0 else item["name"] , 
                f'{item["price"]} บาท' , f'{item["remain"]}' ,f'{item["id"]}') 
        # แสดงตารางเมนูถ้าไม่พบข้อมูลสินค้าไม่ต้องแสดงตาราง 
        if self.__menu__.__len__() == 0:
            console.print(f'🌟 ตอนนี้ไม่มีรายการสินค้าใดๆโปรดเพิ่มสินค้าก่อนแสดงรายการเมนู!' , style='yellow')
        else:
            console.line()
            console.print(menuTable)
            console.line()
    
    def showCommands(self) -> None:
        """ method แสดงคำสั่ง """
        # ตารางคำสั่ง
        commandsTable: Table = Table(title='คำสั่งของโปรแกรม' , caption='เลือกพิมพ์คำสั่งเหล่านี้เพื่อดำเนินการ', 
        title_style='purple italic', caption_style='purple italic', box=HEAVY , leading=1)
        # สร้าง column
        commandsTable.add_column(header='คำสั่ง' , justify='center')
        commandsTable.add_column(header='ชื่อคำสั่งเต็ม' , justify='center')
        commandsTable.add_column(header="ความหมายของคำสั่ง" , justify='center')
        # ความหมายของคำสั่ง
        meaning: Tuple[str , ...] = ("ออกจากโปรแกรม" , "แสดงคำสั่ง" , "แสดงเมนูอาหาร" , "สั่งซื้ออาหาร" , "เพิ่มรายการสินค้า" , "ลบรายการสินค้า" , "แสดง log ของโปรแกรม" , "ค้นหาอาหารที่สั่งซื้อไป" ,"แก้ไขชื่อรายการสินค้า" , "ลบรายการสินค้าทั้งหมด" , "ออกจากบัญชี")
        # เลข index ที่อยู่ตรงกลางของ __KEYWORDS__ ระหว่าง ชื่อคำสั่งย่อ และ คำสั่งเต็ม
        idx: int = int(self.__KEYWORDS__.__len__() / 2)
        for i in range(idx): # วน loop เพิ่ม row
            commandsTable.add_row(f'[dark_magenta]{self.__KEYWORDS__[i]}' , f'[blue_violet]{self.__KEYWORDS__[idx + i]}' , f'{meaning[i]}')
        self.__PROGRAMSTATUS__["isFirstCreateTable"] = False
        # แสดงตารางออกมา
        console.line()
        console.print(commandsTable)
        console.line()
    
    def showLogo(self , path:str = './img/logo.png') -> None:
        """ method แสดง logo ของร้านอาหาร \n
        ``path`` : default parameter ที่ set ไว้ให้แสดง logo ของร้านอาหารตอนเริ่มโปรแกรม โดยให้อ้างอิงตำแหน่ง logo ที่อยู่ในโปรเจค """
        logo: AsciiArt = AsciiArt.from_image(path)
        logo.to_terminal() 
        
    #? แสดงข้อความแจ้งเตือนทุกครั้งตอนเรียกใช้ methods
    def __alert__(self , context: str , *args: Optional[Tuple[str , ...]]) -> None: # แสดงข้อความเมื่อเรียกคำสั่งที่พิมพ์ไป
        """ method แสดงข้อความแจ้งเตือนทุกครั้งตอนเรียกใช้ methods \n
        ``context`` : ข้อความที่จะนำมาแสดงใน terminal เพื่อเข้ากับบริบทของคำสั่ง \n
        ``args`` : จะแสดงแจ้งเตือนเพื่มเติมตาม arguments ที่ส่งให้มา แต่ถ้าไม่ต้องการส่งข้อความแจ้งเตือนเพิ่มให้ส่ง argument ในลำดับที่ 2 เป็น None """
        console.print(f'❔ พิมพ์ตัว "n" เพื่อแสดงแจ้งเตือนนี้อีกครั้ง\n❔ พิมพ์ตัว "m" หรือ "menu" เพื่อแสดงเมนู\n❔ พิมพ์ตัว "e" หรือ "end" {context}')
        # การส่งค่า parameter ตัวที่ 2 เป็น None คือไม่ต้องการแสดงข้อความอย่างอื่นเพิ่ม
        if args[0] is None: 
            ...
        else: # แสดงแจ้งเตือนเพิ่ม
            console.print(*args, sep='\n')
        
    def __createId__(self , length: int = 7) -> str:
        """ method สร้างเลข id \n
        ``length`` : ความยาวของการสร้างเลข id แบบสุ่ม """
        numbers: List[str] = []  # เก็บตัวเลขที่สุ่มมาได้ไว้ใน list
        rand = lambda: str(floor(random() * randint(1,10000))) # สุ่มเลขส่งคืนกลับมาเป็น string 
        while True:
            num: str = choice(rand()) # สุ่มเลือก 1 element เลขของผลลัพธ์ 
            # เมื่อครบตามจำนวนความยาวที่ตั้งไว้
            if len(numbers) == length: 
                if str("".join(numbers)) in self.__idList__: # เช็คค่าว่ามีเลข id ที่สร้างขึ้นมาใหม่ว่าซ้ำกับ id ที่ใช้งานอยู่ไหมถ้าเช็คแล้วว่ามี ให้ล้างค่าใน list แล้ววนใหม่
                    numbers.clear() 
                else:
                    break # ถ้าเท่ากับความยาวที่ตั้งไว้และ id ไม่ซ้ำให้หยุดวน loop ซ้ำ
            else: 
                numbers.append(num)  # เก็บตัวเลขเข้าใน list
                numbers[0] == '0' and numbers.remove('0') # ไม่เอาเลข 0 นำหน้า
        newId: str = str("".join(numbers))  # รวม element ใน list ให้เป็นข้อความ
        return newId
    
    def __generateCode__(self) -> str:
        """ method ในการสร้าง code รหัสสินค้าการสั่งซื้อ """
        chars: List[str] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers: str = "".join([str(randint(0,9)) for i in range(6)]) # สุ่มตัวเลขได้เป็น string
        code: str = f'{choice(chars)}{choice(chars)}{choice(chars)}{numbers}' # นำตัวอักษรมารวมกับตัวเลข
        return code
    
    def __generateBill__(self , code: int , pay: int , total: int , order: List[Dict[str , str | int]] , change:int) -> None:
        """ method ในการสร้างและแสดง บิลใบเสร็จ \n
        ต้องมีการรับค่า parameters เข้ามา 5 อันได้แก่ \n
        ``code`` : รหัสอ้างอิงการสั่งซื้อ สร้างมาจากการใช้ method generateCode \n
        ``pay`` : จำนวนเงินที่จ่ายเข้ามา \n
        ``total`` : จำนวนเงินทั้งหมดที่ต้องจ่าย \n
        ``order`` : order ที่ทำการสั่งไป \n
        ``change`` : คือเงินทอน """
        totalAmount: int = 0 # จำนวนอาหารทั้งหมด
        # สร้างตารางรายละเอียดการสั่งซื้ออาหาร
        details: Table = Table(title='[yellow]รายการ[/]' , caption=f"[green]💸 ยอดเงินรวมทั้งหมด [bold]{total:,}[/] บาท[green]" , 
            box=MINIMAL , show_lines=True)
        # เพิ่ม columns
        details.add_column('ลำดับ' , justify='center')
        details.add_column('อาหาร' , justify='center')
        details.add_column('จำนวน' , justify='center')
        details.add_column('ราคาจานละ' , justify='center')
        details.add_column('รวม' , justify='center')
        # วน loop เพื่ม rows
        for n , item in enumerate(iterable=order , start=1): # loop ตามจำนวนข้อมูลที่ส่งมาจะได้ dictionary ที่เก็บอยู่ใน list
            totalAmount += item["amount"]
            details.add_row(f'{n}' , f'{item["name"]}' , f'{item["amount"]}' , f'{item["price"]}' , f'{item["total"]:,} บาท')
        # เนื้อหาที่จะนำไปแสดงใน terminal
        contents: Group = Group(
            Panel('\nอาหารที่สั่งไปคือ: ' , title=f"รหัสอ้างอิงการสั่งซื้อ [deep_sky_blue1 on grey3]{code}[/]" , box=SIMPLE),
            Panel(details , box=SIMPLE),
            Panel(f'จำนวนอาหารที่สั่งทั้งหมด {totalAmount:,} อย่าง' , box=SIMPLE),
            Panel(f'เงินสดที่จ่ายมา: {pay:,} บาท / เงินทอน: {"จ่ายครบจำนวนไม่ต้องทอนเงิน" if change == 0 else f"{change:,} บาท"}' , box=SIMPLE),
        )
        # สร้างใบเสร็จโดยใส่เนื้อหาข้อความเข้าไป
        bill: Panel = Panel(contents , title='[yellow italic underline]บิลใบเสร็จร้านอาหาร[/]' , 
            subtitle=f'ออกใบเสร็จให้ใน วันที่ [blue1 bold]{self.getDate()}[/] เวลา [blue1 bold]{self.getTime()}[/]' ,
            expand=False , box=HEAVY , padding=(1,2,1,2))
        # แสดงใบเสร็จออกมา
        console.line()
        console.print(bill)
        console.line()
        
    def __searchReferentCode__(self) -> None:
        """ method ค้นหาแสดงรายการการสั่งซื้อที่ผ่านมาแล้วโดยจะต้องมี code เพื่ออ้างอิง """
        # แสดงเส้นขั้น
        console.rule(title='[yellow]ค้นหา order[/]' , style='blue')
        # แสดงแจ้งเตือน
        self.__alert__("เพื่อออกจากการค้นหา" , None)
        #* อ่านข้อมูลมาใหม่ทำให้มีข้อมูลทั้งหมดไปใช้อ้างอิง รหัสอ้างอิงการสั่งซื้อได้
        self.__allOrdersCode__ = ReadWrite.read(path='./data/order.py' , initialValue=dict())
        
        #* infinity loop จนกว่าจะพิมพ์คำสั่ง "e" หรือ "end" เพื่อออกจาก loop
        while self.__PROGRAMSTATUS__["invokeMethod"]:
            try:
                code = console.input('รหัสอ้างอิงการสั่งซื้อ : ').strip() # รหัสอ่างอิงการสั่งซื้อ
                # ออกจาการทำงานของ method
                if code.lower() == "e" or code.lower() == "end":
                    self.__PROGRAMSTATUS__["invokeMethod"] = False
                # แสดงรายการเมนู
                elif code.lower() == "m" or code.lower() == "menu":
                    self.showMenu()
                # แสดงแจ้งเตือนอีกครั้ง
                elif code.lower() == "n":
                    self.__alert__("เพื่อออกจากการค้นหา" , None)
                # ถ้ารหัสอยู่ใน dict
                elif code in self.__allOrdersCode__:
                    self.__loading__(text='กำลังค้นหา order' , spinner='dots8')
                    totalAmount: int = 0
                    # เข้าถึง property โดยใช้ key ที่เป็น รหัสเข้าไป
                    order: Dict[str , str | int | List[Dict[str , str | int]]] = self.__allOrdersCode__[code]
                    change: int = order["change"]
                    # สร้างตาราง
                    details: Table = Table(title='[yellow]รายการ[/]' , caption=f'[green]💸 ยอดเงินรวมทั้งหมด [bold]{order["total"]}[/] บาท[green]' , 
                        box=MINIMAL , show_lines=True)
                    # เพิ่ม columns
                    details.add_column('ลำดับ' , justify='center')
                    details.add_column('อาหาร' , justify='center')
                    details.add_column('จำนวน' , justify='center')
                    details.add_column('ราคาจานละ' , justify='center')
                    details.add_column('รวม' , justify='center')
                    # วน loop เพื่ม rows
                    for i in range(len(order["order"])):
                        item: Dict[str , str | int] = order["order"][i] # เข้าถึง dict ในแต่ละอันใน list
                        totalAmount += item["amount"]
                        # เพิ่ม row ของแต่ละอาหาร
                        details.add_row(f'{i + 1}' , item['name'] , f'{item["amount"]}' , f'{item["price"]}' , f'{item["total"]:,} บาท')
                    # นำ panel ทั้งหมดมารวมใส่ใน group
                    contents: Group = Group(
                        Panel('' , title=f'รหัสอ้างอิงการสั่งซื้อ [deep_sky_blue1 on grey3]{code}[/]/ เลข order ที่ [bright_cyan]{order["number"]}[/] ของวันที่ {order["date"]}' , box=SIMPLE),
                        Panel(f'รายละเอียดการสั่งมีดังนี้' , box=SIMPLE),
                        Panel(details , box=SIMPLE),   
                        Panel(f'จำนวนอาหารที่สั่งทั้งหมด {totalAmount:,} อย่าง' , box=SIMPLE),
                        Panel(f'เงินสดที่จ่ายมา: {order["pay"]} บาท / เงินทอน: {"จ่ายครบจำนวนไม่ต้องทอนเงิน" if change == 0 else f"{change} บาท"}' , box=SIMPLE),
                    )
                    # นำ group ที่ได้มาใส่ใน panel อีกที
                    card: Panel = Panel(contents , title=f'[yellow italic underline]รายละเอียดการสั่งซื้อของรหัส {code}[/]' , 
                        subtitle=f'สั่งซื้ออาหารในวันที่ [blue1 bold]{order["date"]}[/] เวลา [blue1 bold]{order["time"]}[/]',
                        expand=False , box=HEAVY , padding=(1,2,1,2))
                    # แสดงรายละเอียดทั้งหมดออกมา
                    console.line()
                    console.print(card)
                    console.line()
                else:
                    self.__loading__(text='กำลังค้นหา order' , spinner='dots8')
                    raise Exception(f'[red]หมายเลข [bold]"{code}"[/] ไม่มีอยู่ในรายการสั่งซื้อของระบบ[/]') 
            except Exception as err:
                console.print(err.__str__())            
                                                                                                                                                                    
    def __foodOrdering__(self) -> None:  
        """ ``(method หลัก)`` สั่งซื้ออาหาร """
        # แสดงเส้นขั้น
        console.rule(title='[yellow]สั่งอาหาร[/]' , style='blue')
        # แสดงแจ้งเตือน
        self.__alert__("เพื่อออกจากการสั่งซื้อ" , "❔ พิมพ์ตัว \"c\" หรือ \"cancel\" เพื่อยกเลิก order ที่สั่งไปทั้งหมด"
        , "❔ พิมพ์ตัว \"s\" หรือ \"show\" เพื่อแสดงรายการที่สั่งไปทั้งหมด")
        
        #* (function ย่อย) function ในการเริ่มต้นค่าใหม่ในการสั่ง order 
        def resetOrder(isCancel:bool = False) -> None:
            if isCancel:
                if isCancel and self.__currentOrder__ == []:
                    console.print('❕ ยังไม่มีการสั่งเมนูอาหารโปรดสั่งอาหารก่อนยกเลิกรายการที่สั่ง')
                else:
                    console.print('✓ ยกเลิกรายการ order ที่ทำการสั่งไปเรียบร้อย' , style='green')
                    # เก็บ log
                    self.__log__(text=f'ลบรายการ order ที่กดสั่งไป หมายเลข order ที่ {self.__orderNumber__ + 1} ')
            # ล้างรายการ order
            self.__currentOrder__.clear()
            self.__shoppingList__.clear()
        
        #* (function ย่อย) function ในการแสดง order ที่สั่งไป
        def showOrder() -> None:
            if self.__currentOrder__ == []:
                console.print('❕ ยังไม่มีการสั่งเมนูอาหารโปรดสั่งอาหารเพื่อทำการแสดงรายการที่สั่ง')
            else:
                totalAmount: int = 0
                money: int = 0
                content: str = ''
                # loop เอาข้อมูลใน dict
                for n , item in enumerate(iterable=self.__currentOrder__ , start=1):
                    totalAmount += item["amount"]
                    money += (item["price"] * item["amount"])
                    content += f'{n}.) {item["name"]} จำนวน [steel_blue3]{item["amount"]}[/] อย่าง\n'
                content += f'\nจำนวนอาหารรวมทั้งหมด [steel_blue3]{totalAmount}[/] อย่าง\n'
                content += f'ราคารวมทั้งหมด [green4 bold]{money:,}[/] บาท'
                # แสดงข้อความ
                console.line()
                console.print(Panel(content, title='[dark_blue]อาหารที่คุณสั่งไปคือ[/]' , expand=False , box=SQUARE , padding=1))
                console.line()
                
        #* (function ย่อย) เมื่อหยุดการทำงานของ method นี้ให้คำนวณยอดเงินรวม order ที่สั่งไป
        def calculateOrder() -> None:
            # มีการสั่งอาหาร = จำนวนข้อมูลใน list จะไม่เป็น 0
            if (self.__currentOrder__.__len__() != 0) or (self.__currentOrder__ != []):     
                # loop รายชื่ออาหารที่ทำการสั่งมาทั้งหมด     
                for i in range(self.__currentOrder__.__len__()):  
                    # ราคาอาหารทั้งหมดของอาหารนั้น = จำนวนสินค้า x กับราคาสินค้าที่อยู่ในเมนู
                    self.__currentOrder__[i]["total"] = self.__currentOrder__[i]["amount"] * self.__currentOrder__[i]["price"]
                    # ผลรวมจำนวนเงินที่ต้องจ่าย
                    self.__result__ += self.__currentOrder__[i]["total"]
                    self.__totalMoney__.append(self.__currentOrder__[i]["total"])
                self.__orderNumber__ += 1
                # แสดงยอดที่ต้องชำระ
                console.print(f'จำนวนเงินทั้งหมดคือ {self.__result__:,}' , style='green on grey7')
                # set ค่าสถานะให้ทำงานขั้นตอนต่อไป
                self.__PROGRAMSTATUS__["isContinue"] = True
                while self.__PROGRAMSTATUS__["isContinue"]:
                    try:
                        pay: int = int(input('จำนวนเงินที่ลูกค้าจ่ายมาคือ : '))
                        assert pay >= self.__result__
                    except AssertionError:
                        console.print(f'❌ เกิดข้อผิดพลาดขึ้นจำนวนเงินที่จ่ายมาไม่ถูกต้อง!' , style='red')
                    except ValueError:
                        console.print(f'❌ โปรดใส่แค่ตัวเลขจำนวนเต็มเท่านั้น' , style='red')
                    else:
                        self.__orderCode__ = self.__generateCode__() # สร้างรหัสอ้างอิงการสั่งซื้อ
                        order: List[Dict[str , str | int]] = self.__currentOrder__.copy() # order ที่สั่งซื้ออาหาร ข้อมูลเป็น list , elements คือ dict
                        # เก็บ order
                        self.__allOrders__.extend(order) 
                        #* เก็บหมายเลขอ้างอิง -> key: ชื่อรหัสอ้างอิง , value: เป็น dict
                        self.__allOrdersCode__.setdefault(self.__orderCode__ , {
                            "date": self.getDate(), # วันที่สั่งซื้อ
                            "time": self.getTime(), # เวลาสั่งซื้อ
                            "number": self.__orderNumber__, # เลข order (order สั่งครั้งที่ n)
                            "pay": pay,  # เงินที่จ่ายไป
                            "change": abs(pay - self.__result__), # เงินทอน
                            "total": self.__result__, # จำนวนเงินทั้งหมด                            
                            "order": order # อาหารที่สั่ง (ข้อมูลเป็น list)
                        }) 
                        #* อ่านข้อมูลในไฟล์ order.py จะเก็บรายละเอียดการสั่งซื้อทั้งหมดของโปรแกรม
                        data: Dict[str , str | int | List[Dict[str , str | int]]] = ReadWrite.read(path='./data/order.py' , initialValue=dict())
                        #* loop ข้อมูล orders ทั้งหมดที่โปรแกรมทำการเก็บข้อมูลไว้เพื่อนำไปเขียนไฟล์ 
                        for key in self.__allOrdersCode__:
                            if key in data: #? ถ้ามี key(รหัสอ้างอิงการสั่งซื้อ) อยู่ใน ข้อมูลที่ไปทำการอ่านไฟล์มาไม่ต้องเก็บข้อมูลซ้ำไม่ต้องเขียนข้อมูลซ้ำเดิมเพิ่ม 
                                pass
                            else:
                                data[key] = self.__allOrdersCode__[key] #? เก็บ รหัสอ้างอิง อันที่พึ่งมีมาใหม่
                        #* เขียนข้อมูลที่ได้มาลงในไฟล์ order.py 
                        ReadWrite.write(data=data , path='./data/order.py')
                        #* จัดระเบียบไฟล์ python 
                        FormatFile(filename='./data/order.py' , in_place=True)
                        # แสดง loading 
                        self.__loading__(text='กำลังสร้างบิลใบเสร็จ' , spinner='dots8' , delay=.1)
                        #* สร้างบิลใบเสร็จ
                        self.__generateBill__(code=self.__orderCode__, order=self.__currentOrder__ , pay=pay , 
                            change=abs(pay - self.__result__) , total=self.__result__)
                        # เก็บ log
                        self.__log__(text=f'มีการสั่งอาหารใน order หมายเลขที่ {self.__orderNumber__} รหัสอ้างอิง {self.__orderCode__} คิดเป็นเงินจำนวนทั้งหมด {self.__result__:,} บาท')                        
                        self.__PROGRAMSTATUS__["isContinue"] = False
                #* เริ่มสั่งรายการใหม่ให้ set ค่าเริ่มใหม่หมด (ลบสินค้า order ปัจจุบันออก)
                self.__result__ = 0
                self.__orderCode__ = ''
                resetOrder()
            # ถ้าไม่ได่สั่งอะไรไม่ต้องแสดงรายการ
            else: 
                console.print('ไม่มีการสั่งอาหารรายการใดๆ')
    
        #* (function ย่อย) function ในการจัดการจำนวนอาหารในรายการเมนู
        def management(name: str = '', decrement: int = 0, restore: bool = False) -> None:
            # คืนค่าจำนวนอาหารที่สั่งไป
            if restore:
                for order in self.__currentOrder__: # loop ข้อมูลใน order ที่สั่งเพื่อคืนจำนวนอาหารที่สั่งให้เมนู
                    idx: Optional[int] = self.__search__(order["name"])
                    # คืนค่าจำนวนอาหารที่สั่งไป
                    self.__menu__[idx]["remain"] += order["amount"]
            else:
                # หาเลข index เพื่ออ้างอิงตำแหน่ง elements ใน list 
                idx: Optional[int] = self.__search__(name)
                # ลดจำนวนอาหารตามจำนวนที่สั่งไป
                self.__menu__[idx]["remain"] -= decrement
                    
        #* infinity loop จนกว่าจะพิมพ์คำสั่ง "e" หรือ "end" เพื่อออกจาก loop
        while self.__PROGRAMSTATUS__["invokeMethod"]:
            try:
                product: str = console.input("ชื่ออาหารหรือรหัสสินค้า : ").lower().strip()
                # แสดงรายการเมนู
                if product == "m" or product == "menu": 
                    self.showMenu()
                # ออกจาการทำงานของ method
                elif product == "e" or product == "end":
                    self.__loading__(text='กำลังคำนวณรายการสินค้าทั้งหมด' , spinner='dots8')
                    # ! เมื่อหยุดการทำงานของ function __foodOrdering__ ให้เรียกใช้ method คำนวณสินค้า
                    calculateOrder()
                    self.__PROGRAMSTATUS__["invokeMethod"] = False
                # ยกเลิกอาหารที่สั่ง
                elif product == "c" or product == "cancel":
                    management(restore=True) # คืนค่าจำนวนสินค้าที่ลดจำนวนลงจากการสั่งซื้อ                    
                    resetOrder(isCancel=True)
                # แสดง order ที่สั่งไป
                elif product == "s" or product == "show":
                    showOrder()
                # แสดงแจ้งเตือนอีกครั้ง
                elif product == "n":
                    self.__alert__("เพื่อออกจากการสั่งซื้อ" , "❔ พิมพ์ตัว \"c\" หรือ \"cancel\" เพื่อยกเลิก order ที่สั่งไปทั้งหมด" , "❔ พิมพ์ตัว \"s\" หรือ \"show\" เพื่อแสดงรายการที่สั่งไปทั้งหมด")
                #* เช็คชื่ออาหารหรือรหัสสินค้าว่าอยู่ใน list หรือไม่
                elif (product in self.__foodList__) or (product in self.__idList__):        
                    self.__PROGRAMSTATUS__["isContinue"] = True # ให้ทำงานต่อ
                    while self.__PROGRAMSTATUS__["isContinue"]:
                        try:
                            amount: int = int(console.input("จำนวน : ")) # จำนวนสั่งซื้ออาหาร
                            assert not (amount <= 0) , "❌ สั่งจำนวนอาหารไม่ถูกต้องโปรดใส่จำนวนใหม่อีกครั้ง!"
                            assert not (amount > self.__AMOUNT__) , "❌ ท่านสั่งอาหารจำนวนเยอะเกินไม่สามารถทำการดำเนินการสั่งได้"
                        except ValueError:
                            console.print("❌ โปรดใส่เป็นเลขจำนวนเต็มเท่านั้น!" , style='red')
                        except AssertionError as err:
                            console.print(err.__str__() , style='red')
                        else:
                            # หาเลข index โดยใช้ชื่อหรือรหัสสินค้าที่ป้อนเข้ามา
                            # เลข index ไว้อ้างอิง elements(dict) ใน list เพื่อนำข้อมูลเมนูไปใช้งาน
                            idx: Optional[int] = self.__search__(product) 
                            #* ถ้าใส่ชื่อเป็นรหัสสินค้าให้แปลงรหัสสินค้าเป็นชื่ออาหาร
                            if product in self.__idList__: 
                                product: str = self.__menu__[idx]["name"]
                            
                            #! ตรวจสอบจำนวนอาหารในร้านอาหารก่อนเพิ่มเข้ารายการ order ที่สั่งซื้อ
                            #! เมื่อเช็คว่าจำนวนอาหารของอาหาร ... นั้นหมดแล้วจะไม่สามาถสั่งอาหารได้
                            if self.__menu__[idx]["remain"] <= 0: 
                                raise Exception(f'❌ ไม่สามารถดำเนินการสั่งอาหาร [bold]"{product}"[/] ได้เนื่องจากอาหารขายหมดแล้ว')
                            #! เมื่อเช็คว่าจำนวนอาหารที่เหลือของอาหาร ... นั้นรวมกับจำนวนที่สั่งแล้วไม่เหลือเป็นจำนวนติดลบ(สั่งเกินจำนวนที่ตั้งไว้ 30 จำนวน)
                            elif (self.__menu__[idx]["remain"] - amount) < 0:
                                raise Exception(f'❌ ไม่สามารถดำเนินการสั่งอาหาร [bold]"{product}"[/] ได้เนื่องจากจำนวนอาหารที่สั่งมามีมากเกินกว่าจำนวนอาหารที่มีอยู่ในร้านอาหาร')
                            
                            #* เช็คว่าสั่งอาหาร ... นั้นเป็นครั้งแรกหรือยัง (พึ่งเริ่มสั่งอาหารนั้น)
                            if product not in self.__shoppingList__: 
                                self.__shoppingList__.append(product) # เพิ่มชื่ออาหารเข้าไปใน list แปลว่ามีการสั่งอาหาร ... เริ่มเข้าไปในรายการ order แล้ว
                                #* เพิ่มรายการ order ที่สั่งไปได้แก่ ชื่ออาหาร , จำนวน , ราคา , จำนวนเงินทั้งหมด
                                self.__currentOrder__.append({ 
                                    "name": product, # ชื่ออาหาร
                                    "amount": amount, # จำนวนอาหาร
                                    "price": self.__menu__[idx]["price"], # ราคา (เก็บราคาเริ่มต้นจากเมนูเอาไว้เพื่อใช้คำนวณ)
                                    "total": 0 # จำนวนเงินทั้งหมด
                                })
                                # จัดการจำนวนอาหารในเมนู (สั่งอาหารแล้วจำนวนอาหารในเมนูจะลดลง)
                                management(name=product , decrement=amount)
                                self.__log__(typeOfLog=self.SELL , item=[product , amount]) # เก็บ log
                                
                            #* ถ้ามีชื่ออยู่ใน list ให้เพิ่มจำนวนอาหาร ... เพิ่มขึ้น   
                            elif product in self.__shoppingList__: 
                                # หาเลข index ใน list ข้างใน elements คือ dict ต้องการตรวจสอบชื่อ ... ว่าอยู่ index ที่ ... ใน list เพื่อนำมาใช้อ้างอิง
                                idx: Optional[int] = self.__search__(product , self.__currentOrder__)
                                #! ก่อนเพิ่มจำนวนอาหารที่เคยสั่งไปแล้วให้ลองเช็คจำนวน อาหารที่เคยสั่งจะมีจำนวนอาหารอยู่ รวม กับจำนวนที่พึ่งสั่ง ถ้าเกินจำนวนอาหารค่ามากสุดที่ตั้งไว้ให้ raise
                                if (self.__currentOrder__[idx]["amount"] + amount) > self.__AMOUNT__:
                                    raise Exception(f'❌ จำนวนอาหารที่สั่งต้องไม่เกิน {self.__AMOUNT__} อย่างต่อเมนู!')
                                else:
                                    management(name=product , decrement=amount)
                                    # เพิ่มจำนวนอาหารที่มีอยู่แล้วรวมกับจำนวนอาหารที่พึ่งเพิ่มไป (อัปเดตจำนวนอาหาร)
                                    self.__currentOrder__[idx]["amount"] += amount 
                                    self.__log__(text=f'{self.__user__["name"]} ได้สั่ง "{product}" เพิ่มอีก {amount} จำนวน รวมเป็น {self.__currentOrder__[idx]["amount"]} จำนวน') # เก็บ log
                            # ออกจาก loop 
                            self.__PROGRAMSTATUS__["isContinue"] = False 
                # กรณีค้นหาแล้วไม่มีชื่ออาหาร หรือ ไม่มีรหัสสินค้า อยู่ในเมนู    
                else:
                    raise Exception(f'❌ ไม่มี "{product}" อยู่ในเมนูอาหาร!')
            except Exception as err:
                console.print(err.__str__() , style='red')
                
    def __addProduct__(self) -> None:
        """ ``(method หลัก)`` เพิ่มรายการสินค้า """
        # แสดงเส้นขั้น
        console.rule(title='[yellow]เพิ่มเมนูอาหาร[/]' , style='blue')
        # แสดงแจ้งเตือน
        self.__alert__('เพื่อออกจาการเพิ่มสินค้า' , None)
        
        #* infinity loop จนกว่าจะพิมพ์คำสั่ง "e" หรือ "end" เพื่อออกจาก loop
        while self.__PROGRAMSTATUS__["invokeMethod"]:
            try:
                newProduct: str = console.input('ชื่ออาหารใหม่ : ').strip()
                # ออกจาการทำงานของ method
                if newProduct == "e" or newProduct == "end": 
                    self.__PROGRAMSTATUS__["invokeMethod"] = False
                # แสดงรายการเมนู    
                elif newProduct == "m" or newProduct == "menu": 
                    self.showMenu()
                # แสดงแจ้งเตือนอีกครั้ง
                elif newProduct == "n":
                    self.__alert__('เพื่อออกจาการเพิ่มสินค้า' , None)
                else:
                    # ห้ามมีชื่ออาหารที่ตั้งมาใหม่ซ้ำกับข้อมูลในเมนู
                    if newProduct in self.__foodList__:
                        raise Exception(f'❌ ไม่สามารถใช้ชื่อ "{newProduct}" ในการตั้งเมนูใหม่ได้เนื่องจากมีชื่อซ้ำอยู่ในเมนูโปรดตั้งชื่อใหม่!')
                    # ห้ามเกินความยาวในการตั้งชื่ออาหารที่กำหนด
                    elif len(newProduct) >= self.__MAX_LENGTH__: 
                        raise Exception(f'❌ ไม่สามารถตั้งชื่ออาหารที่มีความยาวเกิน {self.__MAX_LENGTH__} ตัวอักษรได้')
                    elif len(newProduct) < self.__MIN_LENGTH__:
                        raise Exception(f'❌ ไม่สามารถตั้งชื่ออาหารที่มีความยาวสั้นน้อยกว่า {self.__MIN_LENGTH__} ตัวอักษรได้')
                    # ห้ามตั้งชื่ออาหารขึ้นต้นเป็นตัวเลขหรือตั้งชื่อเป็นตัวเลข
                    elif newProduct.isdigit() or newProduct[0].isdigit():
                        raise Exception(f'❌ ไม่สามารถตั้งชื่ออาหารที่เป็นตัวเลขขึ้นต้นได้')
                    elif newProduct == "":
                        raise Exception(f'❌ ไม่สามารถตั้งชื่ออาหารเป็นค่าว่างเปล่าได้')
                    elif newProduct in self.__foodList__:
                        raise Exception(f'❌ ไม่สามารถใช้ชื่อ "{newProduct}" ในการตั้งเมนูใหม่ได้เนื่องจากมีชื่อที่ซ้ำอยู่ในเมนูอาหารโปรดตั้งชื่อใหม่!')
                    # ตรวจแล้วไม่มีเงื่อนไข error ใดๆให้ดำเนินการต่อ
                    else:
                        self.__PROGRAMSTATUS__["isContinue"] = True # set ค่าสถานะให้ดำเนินการต่อ
            except Exception as err:
                console.print(err.__str__() , style='red')
            # เช็คแล้วว่าไม่ใช้คำสั่งหรือใส่ชื่อเรียบร้อยให้ใช้เงื่อนไขเพิ่มราคาสินค้า
            else:
                while self.__PROGRAMSTATUS__["isContinue"]:
                    console.print('💬 ราคาสินค้าสามารถตั้งอยู่ในช่วงราคา [bright_cyan]1[/] ถึง [bright_cyan]1,000[/] บาท')
                    try:
                        pricing: int = int(console.input('ราคาอาหาร : ')) 
                        # ห้ามตั้งเกินราคาที่ตั้งไว้ 
                        if pricing > self.__MAX__: 
                            raise Exception('❌ ไม่สามารถตั้งราคาอาหารเกิน 1,000 บาทได้')
                        # ห้ามตั้งน้อยกว่าราคาที่ตั้งไว้ 
                        elif pricing < self.__MIN__: 
                            raise Exception('❌ ไม่สามารถตั้งราคาอาหารติดลบหรือเป็นศูนย์ได้')
                        else:
                            #* เมื่อชื่ออาหารที่ไม่มีอยู่ในเมนู (เช็คแล้วว่าไม่มีชื่อสินค้าซ้ำ) ให้เพิ่มสินค้าใหม่
                            self.__log__(typeOfLog=self.ADD , text=newProduct) # เก็บ log
                            self.__loading__(text='กำลังเพิ่มข้อมูล' , delay=.1 , spinner='dots8')
                            # สร้างสินค้าใหม่
                            self.__menu__.append({ 
                                "name": newProduct,
                                "price": pricing,
                                "id": self.__createId__(self.__PRODUCTCODE_LENGTH__),
                                "remain": self.__AMOUNT__
                            })          
                            console.print(f'[green]✓ เพิ่มเมนูอาหารใหม่เสร็จสิ้น[/]')
                            console.print(f'🍖 จำนวนรายการอาหารที่มีทั้งหมดในตอนนี้มีอยู่ [yellow]{len(self.__menu__)}[/] เมนู')
                            self.__setElements__()   
                    except ValueError:
                        console.print('❌ ไม่สามารถตั้งราคาสินค้าได้ราคาสินค้าต้องตั้งเป็นตัวเลขจำนวนเต็มเท่านั้น!' , style='red')
                    except Exception as err:
                        console.print(err.__str__() , style='red') 
                    else: 
                        self.__PROGRAMSTATUS__["isContinue"] = False

    def __editProduct__(self) -> None:
        """ ``(method หลัก)`` แก้ไขรายการสินค้า """
        # แสดงเส้นขั้น
        console.rule(title='[yellow]แก้ไขเมนูอาหาร[/]' , style='blue')
        # แสดงแจ้งเตือน
        self.__alert__("เพิ่อออกจาการแก้ไข" , None)
        
        #* infinity loop จนกว่าจะพิมพ์คำสั่ง "e" หรือ "end" เพื่อออกจาก loop
        while self.__PROGRAMSTATUS__["invokeMethod"]:
            try:
                self.__PROGRAMSTATUS__["isError"] = False # set ค่าสถานะ
                # ถามข้อมูล
                product: str = console.input('ใส่ชื่ออาหารหรือรหัสสินค้าเพื่อทำการแก้ไข : ').lower().strip()
                # ออกจาการทำงานของ method
                if product == 'e' or product == 'end': 
                    self.__PROGRAMSTATUS__["invokeMethod"] = False
                # แสดงรายการเมนู    
                elif product == 'm' or product == 'menu': 
                    self.showMenu()
                # แสดงแจ้งเตือนอีกครั้ง
                elif product == 'n':
                    self.__alert__("เพื่อออกจาการแก้ไข" , None)
                # มีอยู่ขื่อ หรือ id อยู่ในเมนู 
                elif (product in self.__foodList__ ) or (product in self.__idList__):
                    # หาเลข index ของเมนูอาหาร
                    idx: Optional[int] = self.__search__(product)
                    editProduct: Dict[str , Optional[str] | Optional[int]] = {
                            "name": None,
                            "price": None,
                            "id": None
                        }
                    isEmpty = lambda var: var == '' or len(var) == 0
                    # แสดงข้อความ
                    console.print(f'คุณเลือกรายการสินค้าที่จะแก้ไข คือ [orange1 bold]"{self.__menu__[idx]["name"]}"[/] ราคา [orange1 bold]{self.__menu__[idx]["price"]}[/] บาท รหัสสินค้าคือ [orange1 bold]{self.__menu__[idx]["id"]}[/]')
                    console.print(f'ถ้าไม่ต้องการแก้ไขชื่ออาหารให้ใช้เครื่องหมายลบ [yellow bold](-)[/]')            
                    
                    while not bool(editProduct["name"]):
                        try:
                            # ชื่ออาหารที่จะแก้ไขใหม่
                            changeFoodName: str = console.input(f'แก้ไขชื่อ จาก [orange1 bold]"{self.__menu__[idx]["name"]}"[/] เป็น --> ').strip()   
                            if changeFoodName == '-':
                                changeFoodName = self.__menu__[idx]["name"]
                            # ชื่อห้ามซ้ำกับรายการอื่นๆ
                            elif changeFoodName in self.__foodList__:
                                raise Exception('❌ ชื่อที่คุณทำการแก้ไขนั้นเป็นชื่อซ้ำอยู่ในเมนูอาหารโปรดแก้ไขชื่อที่ไม่ให้ซ้ำกัน')
                            # ไม่ใส่ชื่อ
                            elif isEmpty(changeFoodName):
                                raise Exception('❌ ไม่สามารถใส่ชื่อว่างเปล่าได้!')
                            elif changeFoodName.isdigit() or changeFoodName[0].isdigit():
                                raise Exception('❌ ไม่สามารถตั้งชื่อขึ้นต้นด้วยตัวเลขได้หรือตั้งชื่อเป็นตัวเลขได้!')
                            elif changeFoodName == self.__menu__[idx]["name"]:
                                raise Exception('❌ ไม่สามารถแก้ไขชื่ออาหารที่ชื่อเหมือนเดิมได้!')
                        except Exception as err:
                            console.print(err.__str__() , style='red')
                        else:
                            editProduct["name"] = changeFoodName
                            self.__log__(typeOfLog=self.EDIT , item=[self.__menu__[idx]["name"] , changeFoodName]) # เก็บ log
                            
                    # แสดงข้อความ    
                    console.print('💬 ราคาสินค้าสามารถตั้งอยู่ในช่วงราคา 1 ถึง 1,000 บาท') 
                    console.print(f'ถ้าไม่ต้องการแก้ไขราคาอารให้ใช้เครื่องหมายลบ [yellow bold](-)[/]')
                        
                    while not bool(editProduct["price"]):
                        try:
                            # ราคาที่จะแก้ไขใหม่
                            changePrice: Any = console.input(f'แก้ไขราคา จาก [orange1 bold]{self.__menu__[idx]["price"]}[/] บาท เป็น --> ').strip()
                            if changePrice == '-':
                                changePrice = self.__menu__[idx]["price"]
                            elif isEmpty(changePrice):
                                raise Exception('❌ ไม่สามารถใส่ค่าว่างเปล่าได้!')
                            else:
                                changePrice = int(changePrice)
                                # ยอดเงินต้องไม่เกิน 1000 บาท และ ต้องไม่ติดลบและไม่เป็นศูนย์
                                if (changePrice > self.__MAX__ or changePrice < self.__MIN__) or (changePrice not in range(self.__MIN__ , self.__MAX__)): 
                                    raise Exception('❌ ราคาสินค้าต้องตั้งอยู่ในราคาไม่เกิน 1,000 บาทเท่านั้น!')
                                elif changePrice == self.__menu__[idx]["price"]:
                                    raise Exception('❌ ไม่สามารถแก้ไขราคาสินค้าที่ราคาเหมือนเดิมได้!')
                        except ValueError:
                            console.print('❌ ราคาสินค้าต้องตั้งเป็นตัวเลขจำนวนเต็มเท่านั้น!' , style='red')
                        except Exception as err:
                            console.print(err.__str__() , style='red')
                        else:
                            editProduct["price"] = changePrice
                            self.__log__(typeOfLog=self.EDIT , item=[f'{editProduct["name"]} จากราคา {self.__menu__[idx]["price"]} บาท' , f'{changePrice} บาท']) # เก็บ log
                                
                    # แสดงข้อความ
                    console.print(f'💬 รหัสสินค้าต้องตั้งเป็นเลขจำนวนเต็มจำนวน {self.__PRODUCTCODE_LENGTH__} ตัว')
                    console.print(f'ถ้าคุณไม่ต้องการตั้งรหัสสินค้าเองให้ใส่เครื่องหมายสแลช [yellow bold](/)[/] หรือถ้าต้องการใช้รหัสสินค้าเดิมให้ใส่เครื่องหมายลบ [yellow bold](-)[/]')
                    
                    while not bool(editProduct["id"]):
                        try:
                            # เลข id ที่จะแก้ไข
                            changeId: str = console.input(f'แก้ไขรหัสสินค้า จากรหัส [orange1 bold]"{self.__menu__[idx]["id"]}"[/] เป็น --> ').strip() 
                            if changeId == '-':
                                changeId = self.__menu__[idx]["id"]
                            elif changeId == '/':
                                changeId = self.__createId__(length=self.__PRODUCTCODE_LENGTH__)
                            elif isEmpty(changeId):
                                raise Exception('❌ ไม่สามารถใส่ค่าว่างเปล่าได้!')
                            # ชื่อห้ามซ้ำกับรายการอื่นๆ
                            elif changeId in self.__idList__:
                                raise Exception('❌ รหัสสินค้าที่คุณทำการแก้ไขนั้นเป็นรหัสสินค้าซ้ำอยู่ในเมนูอาหารโปรดแก้ไขไม่ให้ซ้ำกัน')
                            else:
                                if changeId.__len__() != self.__PRODUCTCODE_LENGTH__:
                                    raise Exception(f'❌ ต้องตั้งรหัสสินค้าในความยาว {self.__PRODUCTCODE_LENGTH__} เท่านั้น!')
                                elif changeId == self.__menu__[idx]["id"]:
                                    raise Exception('❌ ไม่สามารถแก้ไขราคารหัสสินค้าที่รหัสเหมือนเดิมได้!')
                        except Exception as err:
                            console.print(err.__str__() , style='red')
                        else:
                            editProduct["id"] = changeId
                            self.__log__(typeOfLog=self.EDIT , item=[f'{editProduct["name"]} จากรหัสสินค้า {self.__menu__[idx]["id"]} ' , f'{changeId}']) # เก็บ log
                    
                    self.__loading__(text='กำลังแก้ไขข้อมูล' , delay=.1 , spinner='dots8')
                    #* แก้ไขข้อมูล dictionary ในเมนู
                    for key in editProduct:
                        self.__menu__[idx][key] = editProduct[key]
                    else:
                        console.print('✓ แก้ไขสินค้าเสร็จสิ้น' , style='green') 
                    #* เปลี่ยนแปลงค่า elements ใหม่     
                    self.__setElements__()    
                # ไม่มีชื่ออาหาร หรือ id อยู่ในเมนู 
                else:
                    raise Exception(f'❌ "{product}" ไม่ค้นพบชื่ออาหารและรหัสสินค้าอยู่ในรายการสินค้าโปรดลองใหม่อีกครั้ง!')
            except Exception as err:
                console.print(err.__str__() , style='red')
                
    def __deleteProduct__(self) -> None:
        """ ``(method หลัก)`` ลบรายการสินค้า """
        # แสดงเส้นขั้น
        console.rule(title='[yellow]ลบรายการเมนูอาหาร[/]' , style='blue')
        # แสดงแจ้งเตือน
        self.__alert__("เพื่อออกจากการลบเมนู" , None)
        
        #* (function ย่อย) ลบสินค้า
        def delete(item:str) -> None:
            findIndex: Optional[int] = self.__search__(item) # หาสินค้าที่ต้องการลบส่งกลับเป็นเลข index
            if findIndex is None: # ไม่มีอยู่ในเมนู
                console.print(f'[red]❌ ไม่พบ [bold]"{item}"[/] อยู่ในเมนูอาหาร[/]')
            else:
                idx: int = findIndex
                self.__loading__(text='กำลังลบข้อมูล' , delay=.1 , spinner='dots8')
                self.__log__(typeOfLog=self.DEL , text=self.__menu__[idx]["name"]) # เก็บ log
                #* ลบสินค้า่โดยอ้างอิงเลข index
                del self.__menu__[idx]
                #* อัปเดตการเปลี่ยนแปลงของ elements ใน foodList และ idList เมื่อมีการลบสินค้าในเมนู
                self.__setElements__() 
                console.print(f'[green]✓ ลบ "{item}" ในรายการเมนูอาหารเสร็จสิ้น[/]')
                self.__PROGRAMSTATUS__["isDeleted"] = True
                
        #* infinity loop จนกว่าจะพิมพ์คำสั่ง "e" หรือ "end" เพื่อออกจาก loop
        while self.__PROGRAMSTATUS__["invokeMethod"]:
            self.__PROGRAMSTATUS__["isDeleted"] = False
            try:
                product: str = console.input('ใส่ชื่ออาหารหรือรหัสสินค้าเพื่อทำการลบ : ').lower().strip() 
                # ออกจาการทำงานของ method
                if product == 'e' or product == 'end':  
                    self.__PROGRAMSTATUS__["invokeMethod"] = False
                # แสดงรายการเมนู    
                elif product == 'm' or product == 'menu': 
                    self.showMenu()
                # แสดงแจ้งเตือนอีกครั้ง
                elif product == 'n':
                    self.__alert__("เพื่อออกจากการลบเมนู" , None)
                else:
                    #* ลบอาหารแบบหลายๆอย่างโดยใส่ , 
                    #* จะใช่เงื่อนไขนี้ได้เมื่อใส่ข้อมูลตรงตามนี้: a , b , c ,...
                    if ',' in product or ',' in [*product]: # ถ้าใส่ , ให้ทำเงิอนไขนี้
                        formatList: List[str] = product.split(',') # ลบ , ออกจะได้ ข้อมูลเป็น list
                        # จัดระเบียบข้อความ
                        for i in range(formatList.__len__()): 
                            formatList[i] = formatList[i].strip() # ลบทุก elements ทุกตัวให้เอาเว้นว่างออก
                        # ถ้าใส่ , แล้วไม่มีชื่ออาหารหรือเลข id ต่อท้ายให้ลบช่องว่างเปล่าที่เกิดขึ้น
                        if '' in formatList:
                            count: int = formatList.count('') # นับจำนวนช่องว่างใน list
                            for j in range(count):
                                formatList.remove('') # ลบ sting เปล่าออกตามจำนวน loop ที่มีใน lit
                        # ลบสินค้าที่ละชิ้น
                        if console.input(f'[dark_orange]คุณแน่ใจว่าต้องการลบสินค้าเหล่านี้ออกจากรายการเมนูอาหารของร้านอาหาร [deep_pink1](y/n)[/] : [/]').lower().strip() == "y":        
                            for element in formatList:
                                delete(element)
                        else:
                            console.print('คุณยกเลิกการลบ' , style='dark_orange')
                    #* เมื่อมีข้อมูลอยู่ในเมนูให้ลบออก
                    elif (product in self.__foodList__) or (product in self.__idList__): 
                        idx: Optional[int] = self.__search__(product)
                        foodName: str = self.__menu__[idx]["name"]
                        if console.input(f'[dark_orange]คุณแน่ใจว่าต้องการลบ [bold]"{foodName}"[/] ออกจากรายการเมนูอาหารของร้านอาหาร [deep_pink1](y/n)[/] : [/]').lower().strip() == "y":
                            delete(foodName)
                        else:
                            console.print('คุณยกเลิกการลบ' , style='dark_orange')  
                    #* ใส่ค่าว่างเปล่า 
                    elif product == "":
                        raise Exception(f"❌ คุณไม่ได้ใส่ชื่ออาหารหรือรหัสสินค้าโปรดใส่ก่อนที่จะทำการลบ")
                    #* ไม่มีอยู่ในเมนู 
                    else: 
                        raise Exception(f"❌ ไม่มี [bold]\"{product}\"[/] อยู่ในเมนูอาหารโปรดกรอกชื่อหรือเลข id ใหม่")
            except Exception as err:
                console.print(err.__str__() , style='red')
            else:
                self.__PROGRAMSTATUS__["isDeleted"] and console.print(f'🍖 จำนวนรายการในเมนูอาหารตอนนี้มีทั้งหมดอยู่ [yellow]{len(self.__menu__)}[/] เมนู')

    def __deleteMenu__(self) -> None:
        """ method ในการลบเมนูสินค้า """
        # แสดงเส้นขั้น
        console.rule(title='[red bold]ลบเมนูทั้งหมด[/]' , style='red')
        if console.input('[orange_red1]คุณแน่ใจว่าต้องการลบสินค้าทั้งหมดถ้าต้องการให้พิมพ์ [bold]"y"[/] แต่โปรดรู้ไว้ข้อมูลสินค้าจะถูกลบถาวรและไม่สามารถกู้คืนได้[/] [deep_pink1](y/n)[/] : ').lower().strip() == "y":
            self.__log__(typeOfLog=self.DELALL)
            # loading 
            self.__loading__(text='กำลังตรวจสอบข้อมูลเมนู' , spinner='bouncingBall')
            self.__loading__(isDelete=True)
            # ลบข้อมูลเมนูทั้งหมด
            self.__menu__.clear()
            self.__setElements__(reset=True)
        else: 
            console.print('❗ คุณยกเลิกการดำเนินการลบสินค้าทั้งหมด' , style='magenta')
        
    def __conclusion__(self , total: List[int] , orders: List[Dict[str , str | int]]) -> Tuple[str , ...]:
        """ method สรุปจำนวนเงินและการสั่งซื้ออาหารในหนึ่งวัน """
        quantity: int = 0 # จำนวนอาหารที่สั่งไปทั้งหมด
        #* หาค่าเฉลี่ย
        me: float = mean(total) 
        #* หาฐานนิยมต้องวน loop ข้อมูลแล้วเก็บใน list ก่อนถึงจะหาได้
        mo: List[str] = [] 
        # loop ข้อมูลทั้งหมด จาก allOrders
        for item in orders:
            foodName: str = item["name"] # เก็บชื่ออาหาร
            amount: int = item["amount"] # เก็บจำนวนของอาหารที่สั่ง
            # loop ตามจำนวนครั้ง ของ value ทุกๆครั้งที่ loop จะคืนค่า(เพิ่ม) ชื่ออาหารให้ li
            li: List[str] = [foodName for i in range(amount)] 
            # เพิ่ม li ให้ mo เพื่อนำไปหาฐานนิยมต่อไป
            mo.extend(li) 
            quantity += amount # บวกจำนวนเพิ่มแต่ละอาหาร
        #* หาฐานนิยมจะ: return ชื่ออาหารที่มีชื่อนั้นมากสุด ถ้าไม่มีชื่ออาหารตัวไหนมากกว่ากันจะคืน element ตัวแรกเสมอ    
        mo: str = mode(mo) 
        return (
            f'จำนวนสั่งซื้ออาหารวันนี้ {self.__orderNumber__} รายการ {quantity:,} อย่าง ทำจำนวนเงินรวมไปได้ [green]{sum(total):,}[/] บาท ',
            '[yellow underline]สรุป[/]',
            f'มีค่าเฉลี่ยการสั่งซื้ออาหารอยู่ที่ : [yellow bold]{me:,.2f}[/]',
            f'อาหารที่สั่งบ่อยหรือสั่งเยอะที่สุดในวันนี้คือ : [yellow bold]"{mo}"[/]'
        )
                
    def __exitProgram__(self) -> None:
        """ method ออกจากโปรแกรม """
        #* ถ้ามีการสั่งอาหารให้แสดงรายการสรุปสินค้าที่ซื้อไปภายใน 1 วัน ถ้าไม่ได้สั่งซื้อไม่ต้องแสดง
        if self.__allOrders__.__len__() != 0:
            console.print(*self.__conclusion__(total=self.__totalMoney__ , orders=self.__allOrders__) , sep='\n')
        console.print('🙏 ขอบคุณที่มาใช้บริการของเรา')     
        #* เขียนไฟล์ (อัปเดตข้อมูลรายการเมนูอาหาร) ให้เป็นข้อมูลที่อัปเดตเป็นปัจจุบันล่าสุด
        ReadWrite.write(data=self.__menu__ , path='./data/menu.py' , isList=True)
        #* จัดระเบียบไฟล์ python 
        FormatFile(filename='./data/menu.py' , in_place=True)
        # ตั้งค่าสถานะให้เป็น False เพื่ออกจาก loop แล้วโปรแกรมจบการทำงาน
        self.__PROGRAMSTATUS__["isWorking"] = False
        self.__PROGRAMSTATUS__["programeIsRunning"] = False

    def execute(self) -> None:
        """ ``(method หลัก)`` การดำเนินการทำงานหลักของโปรแกรม เป็นคำสั่งที่ใช้ในการรันโปรแกรม """
        #* infinity loop จนกว่าจะพิมพ์คำสั่ง "e" หรือ "exit" เพื่อออกจาก loop
        while self.__PROGRAMSTATUS__["programeIsRunning"]:
            self.__PROGRAMSTATUS__["isWorking"] = True
            try:
                command: str = console.input("[medium_turquoise italic]พิมพ์คำสั่งเพื่อดำเนินการต่อไป : [/]").lower().strip()
                #! ตรวจสอบความถูกต้อง
                # ไม่ได้พิมพิมพ์คำสั่งมา
                assert not (command == "") , 'คุณไม่ได้ป้อนคำสั่งโปรดพิมพ์คำสั่ง' # ถ้าไม่ได้พิมพ์คำสั่งอะไรมา
                # ไม่ใช้คำสั่ง (True: เป็นคำสั่ง / False: ไม่มีคำสั่งที่ค้นหา)
                assert self.__isKeyword__(command) , f'ไม่รู้จักคำสั่ง [bold]"{command}"[/] โปรดเลือกใช้คำสั่งที่มีระบุไว้ให้'
                
                #? เปลี่ยนสถานะ attribute ตัวนี้ให้เป็น True หมายถึงกำลังทำการเรียกใช้ methods ของโปรแกรม
                self.__PROGRAMSTATUS__["invokeMethod"] = True
                #? เช็คว่าได้รับสิทธิ์ให้ใช้งานคำสั่งบางคำสั่งได้หรือไม่ 
                self.__authorize__(command)
                
                #* ออกจากโปรแกรม
                if command == "e" or command == "exit":
                    self.__log__(text="จบการทำงานของโปรแกรม")
                    self.__exitProgram__()
                #* แสดงคำสั่ง
                elif command == "c" or command == "commands": 
                    self.__log__(typeOfLog=self.COMMAND , text="แสดงรายการคำสั่ง")
                    self.showCommands()
                #* แสดงรายการเมนู
                elif command == "m" or command == "menu": 
                    self.__log__(typeOfLog=self.COMMAND , text="แสดงเมนูอาหาร")
                    self.showMenu()
                #* สั่งอาหาร
                elif command == "o" or command == "order":
                    self.__log__(typeOfLog=self.COMMAND , text="การสั่งซื้ออาหาร")
                    self.showMenu()
                    self.__foodOrdering__()
                #* เพิ่มสินค้า
                elif command == "a" or command == "add": 
                    self.__log__(typeOfLog=self.COMMAND , text="การเพิ่มเมนูอาหาร")
                    self.__addProduct__()
                #* ลบสินค้า
                elif command == "d" or command == "delete":
                    self.__log__(typeOfLog=self.COMMAND , text="การลบเมนูอาหาร")
                    self.showMenu()
                    self.__deleteProduct__()
                #* แก้ไขสินค้า
                elif command == "ed" or command == "edit": 
                    self.__log__(typeOfLog=self.COMMAND , text="การแก้ไขเมนูอาหาร")
                    self.showMenu()
                    self.__editProduct__()
                #* ลบรายการสินค้าทั้งหมด
                elif command == "cl" or command == "clear":
                    self.__log__(typeOfLog=self.COMMAND , text="การลบรายการเมนูอาหารทั้งหมด")
                    self.__deleteMenu__()
                #* แสดงกิจกรรมการทำงานต่างๆของโปรแกรม
                elif command == "l" or command == "log":
                    self.__showLog__()
                #* ค้นหา order ที่สั่งไป
                elif command == "s" or command == "search":
                    self.__log__(typeOfLog=self.COMMAND , text="การค้นหารหัสอ้างอิง")
                    self.__searchReferentCode__()
                #* ออกจากบัญชี
                elif command == "out" or command == "logout":
                    self.__log__(typeOfLog=self.COMMAND , text="ออกจากระบบบัญชี")
                    # method logout จะส่งค่าสถานะมาถ้า True เงื่อนไขนี้จะทำงาน
                    if self.__logout__():
                        self.__PROGRAMSTATUS__["isWorking"] = False
                        #* login ใหม่
                        user: Dict[str , str] = super().__getUser__() # รอรับข้อมูลผู้ใช้งาน
                        super().__setUser__(user)
                        super().__setPermissions__(user)
                        self.showLogo()
                        self.greeting(userName=user["name"])
                        self.showCommands()
            except AssertionError as err:
                console.print(f'[bold underline red on grey0]Error:[/] [red]{err.__str__()}[/]')
            except Exception as err:
                console.print(err.__str__())
            finally:
                self.__PROGRAMSTATUS__["isWorking"] and console.print('โปรดเลือกพิมพ์คำสั่ง' , style='cyan italic')

#? สร้าง object 
program: Program = Program(menu=ReadWrite.read(path='./data/menu.py') , user=ReadWrite.read(path='./data/user.py'))
program.execute()