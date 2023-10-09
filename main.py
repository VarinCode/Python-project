from abc import abstractmethod 
from datetime import datetime as dt
from random import randint , random , choice
from math import floor
# นำเข้า module (ข้อมูลเมนู)
from menu import list_menu as data
# นำเข้า module ข้อมูลผู้ใช้งาน
from data import userData , addUser
# pip install prettytable
from prettytable import PrettyTable 
# pip install typing
from typing import List , Dict , Union , Any , Tuple
# pip install ascii-magic
from ascii_magic import AsciiArt 
from statistics import mean , mode
from sys import exit

# |ขั้นตอนการใช้งาน|                 |คำสั่ง|
# ดาวโหลด์:                        git clone -b oop https://github.com/VarinCode/Python-project.git
# เข้าถึง directory ของ project:     cd Python-project
# ติดตั้ง virtual environment:       py -m venv .venv
# เปิดใช้งาน venv:                  .venv\Scripts\activate
# ติดตั้ง library ที่อยู่ใน project:     pip install -r requirement.txt
# คำสั่งรันโปรแกรม:                   py main.py หรือ py "C:\Users\ชื่อผู้ใช้งานคอมพิวเตอร์\Desktop\Python-project\main.py"
# ปิดใช้งาน venv:                   deactivate

class Register: #? องค์ประกอบใน class: ระบบ login , logout , สมัครสมาชิก , ผู้ใช้งาน , ข้อมูลผู้ใช้งาน
    #* โครงสร้างข้อมูลผู้ใช้งาน กำหนดให้เป็นค่าว่างเปล่าตอนเริ่มต้น
    __user__ = {
        "name": None,
        "email": None,
        "password": None,
        "position": None,
        "AccessPermissions": {
            "AddData": None,      
            "DeleteData": None,    
            "ModifyData": None,    
            "DeleteAllData": None, 
            "DeleteAllData": None, 
            "ViewLog": None,       
            "SellFood": None 
        }
    }
    
    #* บันทึกข้อมูลผู้ใช้งานจากการ login
    __saveUserData__ = None
    #* บัญชีที่ใช้งานอยู่
    __activeUser__ = None
    
    #? method ในการ login 
    def __login__(self) -> Dict[str , str]:    
        #? function ในการ login 
        def loginFunction():
            # ข้อมูลที่ผู้ใช้งานต้องกรอก
            userLogin = {
                "nameOrEmail": None,
                "password": None
            }
            print('\n\tLogin')
            while not bool(userLogin["nameOrEmail"]) or not bool(userLogin["password"]):
                while not bool(userLogin["nameOrEmail"]):
                    try:
                        nameOrEmail = input("ชื่อผู้ใช้งานหรืออีเมล : ").strip()
                        if self.isEmpty(nameOrEmail):
                            raise UserWarning('❌ ชื่อผู้ใช้งานไม่ถูกต้องโปรดลองใหม่อีกครั้ง')
                        elif len(nameOrEmail) > self.WORD_LENGTH:
                            raise UserWarning('❌ ชื่อผู้ใช้งานของคุณมีความยาวมากเกินไป')
                        else:
                            userLogin['nameOrEmail'] = nameOrEmail
                    except UserWarning as err:
                        print(err)
                while not bool(userLogin["password"]):
                    try:
                        password = input("รหัสผ่าน : ").strip()
                        if self.isEmpty(password):
                            raise UserWarning('❌ รหัสผ่านผู้ใช้งานไม่ถูกต้องโปรดลองใหม่อีกครั้ง')
                        else:
                            userLogin['password'] = password
                    except UserWarning as err:
                        print(err)
            return { # ส่งค่าเป็น dict
                "status": bool(userLogin),  # สถานะข้อมูลของผู้ใช้งาน
                "user": userLogin # ข้อมูลผู้ใช้งานเป็น dictionary
            }
        
        #? function ในการตรวจสอบข้อมูลผู้ใช้งาน 
        def userVerification(status: bool , validateUser: Dict[str , str]) -> bool:
            # parameter status คือ ค่าสถานะที่ส่งมา True แปลว่าข้อมูลพร้อมตรวจสอบความถูกต้อง ถ้า False คือไม่พร้อมตรวจสอบ
            # parameter validateUser คือ ข้อมูลผู้ใช้งานที่ login มีการตรวจสอบมานิดนึงแล้วแต่ข้อมูลที่ส่งมานั้นจะอยู่ในระบบผู้ใช้งานโปรแกรมนี้หรือไม่ต้องนำมาตรวจสอบให็ถูกต้องถึงจะ login สำเร็จ
            isCorrect = { # ถ้าค่า True แปลว่ามีข้อมูลผู้ใช้งานมีอยู่ในระบบ
                "name": False,      # ชื่อถูกต้อง
                "password": False,  # รหัสผ่านถูกต้อง
                "email": False,     # อีเมลถูกต้อง
            }
            isValid = False # ค่าสถานะยืนยันว่าข้อมูล login ที่ผู้ใช้งานส่งมาถูกต้องและมีตามที่เก็บข้อมูลไว้ในไฟล์
            try:
                # ยืนยันค่าสถานะของข้อมูลผู้ใช้งานว่าไม่เป็นค่าว่างเปล่า
                if status:
                    # loop ข้อมูลผู้ใช้งานในไฟล์ data.py โดย userData เก็บข้อมูลเป็น list และ element คือ dictionary เป็นข้อมูลผู้ใช้งานในร้านค้าของแต่ละคน
                    # ให้เทียบแต่ละ dict หรือ เทียบข้อมูลผู้ใช้งานแต่ละคนถ้า loop ครบแล้วไม่มีหรือไม่ตรงกันแปลว่าข้อมูลผู้ใช้งานที่ส่งมาไม่มีอยู่จริง
                    for user in userData: # ดึง element (dict)แต่ละอันออกมาเช็คว่าตรงกันไหม
                        # ตรวจสอบ ชื่อ
                        if validateUser["nameOrEmail"] == user["name"]:
                            #ถ้ามีในไฟล์เก็บข้อมูลผู้ใช้งานให้ค่าสถานะเป็น True
                            isCorrect["name"] = True
                        else:
                            # เมื่อได้ค่าสถานะ True แล้วไม่ต้องเปลี่ยนค่า False , ถ้ายังไม่เจอก็ให้เป็น False
                            if not isCorrect["name"]: isCorrect["name"] = False
                        # ตรวจสอบ อีเมล
                        if validateUser["nameOrEmail"] == user["email"]:
                            isCorrect["email"] = True
                        else:
                            if not isCorrect["email"]: isCorrect["email"] = False
                        # ตรวจสอบ รหัสผ่าน
                        if validateUser["password"] == user["password"]:
                            isCorrect["password"] = True
                        else:
                            if not isCorrect["password"]: isCorrect["password"] = False
                        # เช็คค่า
                        # print(validateUser["nameOrEmail"] , '->' , user["name"])
                        # print(validateUser["nameOrEmail"] , '->' , user["email"])
                        # print(validateUser["password"] , '->' , user["password"])
                        # print((isCorrectName or isCorrectEmail) and isCorrectPassword) 
                        #* ตรวจสอบแล้วว่ามีข้อมูลผู้ใช้งานที่ส่งมาตรงและถูกต้องกับข้อมูลที่เก็บไว้ในไฟล์  
                        if (isCorrect["name"] or isCorrect["email"]) and isCorrect["password"]: 
                            # ให้ค่าสถานะถูกต้อง
                            isValid = True
                            del validateUser["nameOrEmail"] # ลบ property nameOrEmail ออกเพราะไม่ได้นำไปใช้งานต่อ
                            #* เก็บค่าของผู้ใช้งานที่ loop แต่ละ dict เก็บไว้เพราะข้อมูลตรงกัน 
                            validateUser["name"] = user["name"]
                            validateUser["email"] = user["email"]
                            validateUser["password"] = user["password"]
                            validateUser["position"] = user["position"]
                            break # เจอข้อมูลผู้ใช้งานแล้วให้หยุด loop
                        # ชื่อผู้ใช้ถูกต้อง หรือ อีเมลถูกต้อง แต่ รหัสผ่านผิดให้แสดง error ตามที่เขียนใน string 
                        if (isCorrect["name"] or isCorrect["email"]) and not isCorrect["password"]:
                            raise Warning('❗ รหัสผ่านไม่ถูกต้องโปรดใส่รหัสผ่านให้ถูกต้อง')
                        # ชื่อผู้ใช้ หรือ อีเมล ผิด แต่ รหัสผ่านถูกต้องให้แสดง error ตามที่เขียนใน string 
                        elif (not isCorrect["name"] or not isCorrect["email"]) and isCorrect["password"]:
                            raise Warning('❗ ชื่อผู้ใช้งานหรืออีเมลไม่ถูกต้องโปรดใส่ข้อมูลให้ถูกต้อง')
                else:
                    raise Warning('❗ เกิดข้อผิดพลาดขึ้นโปรดลองใหม่อีกครั้ง!')
                # ถ้าหาแล้วไม่เจอให้แสดง error ตามนี้
                if not isValid: 
                    raise Warning('❗ ไม่มีบัญชีผู้ใช้งานนี้อยู่ในฐานข้อมูลโปรดสมัครบัญชีเพื่อใช้งานโปรแกรม')
            except Warning as err:
                print(err)
            else:
                # บันทึกข้อมูลผู้ใช้งาน
                self.__saveUserData__ = validateUser
            # ส่งค่าสถานะถ้า ส่ง True แปลว่า login สำเร็จ ถ้า False แปลว่า login ไม่สำเร็จ
            return isValid
        
        counter = 0 # ตัวนับข้อผิดพลาดที่เกิดจากการ login
        #* อธิบาย 
        # function userVerification จะทำการ callbackfunction ให้เรียกใช้ function loginFunction ก่อนเมื่อดำเนินการตามคำสั่งเรียบร้อยแล้วจะคืนค่ากลับมา
        # เป็น dict เราสามารถใช้ method values ที่เป็นคำสั่งพื้นฐานของ dict ให้คืนค่ามาเป็น list ใน list คือค่าของข้อมูล property ที่ส่ง value คืนกลับมาเรียงลำดับ
        # ตาม element จากนั้นใช้เครื่องหมาย * เพื่อกระจาย element ส่งเป็น arguments เรียงลำดับรับตาม parameters ที่ประกาศไว้ใน function userVerification
        # เมื่อส่งค่ารับ parameter แล้วจะนำดำเนินตามคำสั่งที่เขียนใน funciton จนเสร็จสิ้นสุดท้ายแล้วจะคืนค่ากลับมาเป็น boolean (True/False)
        # ถ้าได้รับ True มาในความหมายของการทำงานนี้คือ การ login สำเร็จให้ยกเลิกการ วน loop ซ้ำๆ (infinity loop)
        # แต่ถ้าเป็น False คือ login ไม่สำเร็จจะวน loop ซ้ำๆไปเรื่อยๆจนกว่าจะ login สำเร็จ
        # การใส่ not คือ ทำให้ค่า boolean เปลี่ยนค่าตรงข้ามกัน not True -> False = login สำเร็จเลิกวนซ้ำ
        # not False -> True = login ซ้ำไปเรื่อยๆจนกว่าข้อมูลผู้ใช้งานจะถูกต้อง
        while not userVerification(*loginFunction().values()):
            counter += 1
            if counter > 4: # ถ้า login แล้วเกิดข้อผิดพลาดเกิน 4 ครั้งให้เสนอทางเลือกว่า สร้างบัญชีใหม่ก่อนแล้วค่อย login ทีหลัง
                if input('การ Login ล้มเหลวจำนวนหลายครั้งคุณต้องการ สมัครบัญชีผู้ใช้งานก่อนไหม (y) : ').lower().strip() == "y":
                    self.__createAccount__() # เรียกใช้ method สร้างบัญชีผู้ใช้งาน
                    break # ออกจาก loop นี้
        # ส่งข้อมูลผู้ใช้งาน
        return self.__saveUserData__
    
    #? method ในการ สมัครบัญชีผู้ใช้งานใหม่
    def __createAccount__(self) -> Dict[str , str]:
        print('\n','สมัครบัญชีผู้ใช้งานใหม่')
        newUser = self.__user__.copy()
        while (not bool(newUser["name"])) or (not bool(newUser["password"])) or (not bool(newUser["position"])) or (not bool(newUser["email"])):
            while not bool(newUser["name"]):
                try:
                    name = input("ตั้งชื่อผู้ใช้งาน : ").strip()
                    if self.isEmpty(name):
                        raise UserWarning('❌ ชื่อผู้ใช้งานไม่ถูกต้องโปรดลองใหม่อีกครั้ง')
                    elif len(name) > self.WORD_LENGTH:
                        raise UserWarning('❌ ชื่อผู้ใช้งานของคุณมีความยาวมากเกินไป')
                    elif len(name) <= self.NAME_LENGTH:
                        raise UserWarning('❌ ชื่อผู้ใช้งานของคุณมีสั้นน้อยเกินไป')
                    else:
                        newUser['name'] = name
                except UserWarning as err:
                    print(err)
            while not bool(newUser["email"]):
                try:
                    email = input("ใส่อีเมลที่ใช้ในบัญชีนี้ : ").strip()
                    if self.isEmpty(email):
                        raise UserWarning('❌ อีเมลไม่ถูกต้องโปรดลองใหม่อีกครั้ง')
                    elif "@" not in list(email) or "." not in list(email):
                        raise UserWarning(f'❌ {email} ไม่ใช้อีเมลโปรดลองใหม่อีกครั้ง')
                    else:
                        newUser['email'] = email
                except UserWarning as err:
                    print(err)
            while not bool(newUser["password"]):
                symbols = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',':', ';', '<', '=', '>', '?', '@' , '{', '|', '}', '~' , '[', '\\', ']', '^', '_', '`']
                isSymbol = False
                try:
                    password = input("ตั้งรหัสผ่าน : ").strip()
                    for letter in password:
                        if letter in symbols:
                            isSymbol = True
                    if not isSymbol:
                        raise UserWarning(f'❗ ต้องมีสัญลักษณ์พิเศษอย่างน้อย 1 ตัวในการตั้งรหัสผ่าน: {" ".join(symbols)}')
                    if self.isEmpty(password):
                        raise UserWarning('❌ รหัสผ่านผู้ใช้งานไม่ถูกต้องโปรดลองใหม่อีกครั้ง')
                    elif len(password) < self.PASSWORD_LENGTH:
                        raise UserWarning(f'❌ ความยาวของรหัสผ่านต้องมีความยาว {self.PASSWORD_LENGTH} ตัวขึ้นไป')
                    else:
                        confirmPassword = input("ยืนยันรหัสผ่าน : ").strip()
                        if confirmPassword == password:
                            newUser['password'] = password
                        elif confirmPassword != password:
                            raise UserWarning(f'รหัสผ่านที่ยืนยันไม่ถูกต้องกับรหัสผ่านที่ตั้ง')
                except UserWarning as err:
                    print(err)
            while not bool(newUser["position"]):
                allPositions = []
                print(f'💬 เลือกตำแหน่งงานในร้านอาหารที่คุณทำอยู่ :' , end=" ")
                for key in self.POSITIONS:
                    for position in self.POSITIONS[key]:
                        print(position , end=' , ')
                        allPositions.append(position)
                try:
                    selectedPosition = input("\nตำแหน่งงานหรือหน้าที่ของคุณคือ : ").strip()
                    if self.isEmpty(position):
                        raise UserWarning('❌ คุณไม่ได้ใส่ตำแหน่งงานของคุณโปรดกรอกตำแหน่งงานของคุณ')
                    elif selectedPosition not in allPositions:
                        raise UserWarning(f'❌ ตำแหน่ง "{selectedPosition}" ไม่มีอยู่ในร้านอาหารของเราโปรดลองใหม่อีกครั้ง')
                    else:
                        newUser['position'] = selectedPosition
                except UserWarning as err:
                    print(err)
        else:
            print('✔ สมัครบัญชีผู้ใช้งานใหม่นสำเร็จโปรด Login เพื่อเข้าใช้งานโปรแกรม')
            print('🔹 กลับมาที่หน้า Login')
            # เพื่มผู้ใช้งาน
            addUser(newUser)
            return self.__login__()
    
    #? method บัญชีผู้ใช้งานออกจากระบบ
    def __logout__(self):
        # เมื่อตอบ y ให้เอาข้อมูลผู้ใช้งานออกจากโปรแกรม 
        if input('คุณต้องการออกจากบัญชีผู้ใช้งานนี้ (y/n) : ').lower().strip() == "y":
            if bool(self.__activeUser__):
                self.__setUser__(isLogout=True) # set ข้อมูลผู้ใช้งานโปรแกรมเป็นค่าเริ่มต้นคือค่าว่างเปล่า
                # ให้ login ใหม่
                user = self.__getUser__()
                self.__setUser__(user)
                self.__setPermissions__(user)
                self.__activeUser__ = user
        else:
            print('❕ คุณยกเลิกการออกจากบัญชีนี้')

    #? method ในการให้ข้อมูลผู้ใช้งาน 
    def __getUser__(self) -> Dict[str , str | Union[str , Dict[str , str]]]:
        user = None
        # loop เรื่อยๆจนกว่าจะได้ข้อมูลผู้ใช้งาน
        while not bool(user):
            try:
                print(*('\n◻ พิมพ์ (1) เพื่อ Login เข้าสู่ระบบ' , '◻ พิมพ์ (2) เพื่อสมัครบัญชีผู้ใช้งาน' , '◻ พิมพ์ (3) ออกจากโปรแกรม') , sep='\n')
                selected = int(input('โปรดพิมพ์ตัวเลือก : '))
                # เลือก login
                if selected == 1:
                    user = self.__login__()
                # เลือกสมัครสมาชิกก่อนแล้วจะไปที่หน้า login
                elif selected == 2:
                    user = self.__createAccount__() # sign up
                # ออกจากโปรแกรม
                elif selected == 3:
                    print('ปิดโปรแกรม')
                    exit()
                else:
                    raise Warning(f'❌ ไม่มี "{selected}" ในตัวเลือกของการถาม โปรดพิมพ์แค่ 1 หรือ 2 เท่านั้น')
            except ValueError:
                print('❌ โปรดพิมพ์เป็นตัวเลขเท่านั้น')
            except Warning as err:
                print(err)
        return user
    
    #? method ในการตั้งค่าข้อมูลผู้ใช้งาน 
    def __setUser__(self , user:Dict[str , str] | None = None , isLogout: bool = False) -> None:
        #* เมื่อมีการต้องการออกจากบัญชีให้ set ข้อมูลค่าเริ่มต้นของผู้ใช้งาน 
        if isLogout:
            self.__user__ = {
                "name": None,
                "email": None,
                "password": None,
                "position": None,
                "AccessPermissions": {
                    "AddData": None,      
                    "DeleteData": None,    
                    "ModifyData": None,    
                    "DeleteAllData": None, 
                    "DeleteAllData": None, 
                    "ViewLog": None,       
                    "SellFood": None 
                }
            }
            self.__saveUserData__ = None
            self.__activeUser__ = None
        #* เมื่อมีการส่งข้อมูลผู้ใช้งานมาที่ parameter user 
        elif user != None:
            for key in user: # loop แล้วดึง key จาก property user ออกมา
                self.__user__[key] = user[key] # ให้ property ใน attribute user มีค่าเป็นข้อมูลของผู้ใช้งานที่ส่งมา
        
    
class Configuration(Register): #? องค์ประกอบใน class: กำหนดโครงสร้างหลักๆของ class Program และ สิทธิ์การใช้งาน
    
    #* ตำแหน่งในร้านอาหาร
    # Ref: https://www.waiterio.com/blog/th/raaychuue-phnakngaanraan-aahaarthanghmd-bthbaath-khwaamrabphidch-b
    POSITIONS = {
        "management": ("ผู้จัดการ" , "ผู้ดูแลระบบ"), # ตำแหน่งงานบริหาร 
        "kitchenStaff": ("หัวหน้าพ่อครัว" , "ผู้จัดการครัว" , "รองหัวหน้าพ่อครัว" , "กุ๊ก" , "ผู้ช่วยกุ๊ก"), # พนักงานครัว
        "receptionist":("หัวหน้าบริกร" , "พนักงานต้อนรับ", "ซอมเมลิเยร์" , "พนักงานบาร์" , "บริกร" , "แคชเชียร์") # พนักงานต้อนรับ
    }
    
    #* กำหนดการตั้งค่าพื้นฐานของโปรแกรม 
    # True: เปิดใช้งาน , False: ปิดใช้งาน
    #! ข้อบังคับ: การเปิดใช้งาน(ใส่ True/False)บางอย่างจะต้องสอดคล้องกัน เช่น EnableRegisterSystem == EnablePermissions
    __DEFAULTSETTING__ = {
        "EnableRegisterSystem": True,     # เปิดใช้งานระบบลงทะเบียน
        "EnableDecimalFoodPricing": False, # เปิดใช้งานการตั้งราคาอาหารเป็นด้วยเลขทศนิยม
        "EnableLog" : True,               # เปิดใช้งานการเก็บ log การทำงาน
        "EnablePermissions": True         # เปิดใช้งานสิทธิ์การเข้าถึง
    }
    
    # อธิบายค่า value ที่อยู่ใน Properties
    # None ค่า None ยังไม่ได้กำหนดสิทธิ์ใช้งาน
    # True ค่า True อณุญาติให้มีสิทธิ์ในการใช้งานคำสั่งนั้นได้ 
    # False ค่า False ไม่อณุญาติให้มีสิทธิ์ใช้งานคำสั่งนั้น
    #* สิทธิ์ในการใช้งานคำสั่งต่างๆในโปรแกรม 
    __PERMISSIONS__ = {
        "AddData": None,       # สิทธิ์ในการเพิ่มข้อมูล
        "DeleteData": None,    # สิทธิ์ในการลบข้อมูล
        "ModifyData": None,    # สิทธิ์ในการแก้ไขข้อมูล
        "DeleteAllData": None, # สิทธิ์ในการลบข้อมูลทั้งหมด
        "DeleteAllData": None, # สิทธิ์ในการลบข้อมูลทั้งหมด
        "ViewLog": None,       # สิทธิ์ในการดูข้อมูล
        "SellFood": None       # สิทธิ์ในการขายอาหาร
    }
    
    MIN = 1 # ค่าน้อยสุดจำนวนเงินที่สามารถตั้งได้น้อยสุด
    MAX = 1000 # ค่ามากสุดจำนวนเงินที่สามารถตั้งได้มากสุด
    PRODUCTCODE_LENGTH = 3 # ความยาวของรหัสสินค้า
    WORD_LENGTH = 28 # ความยาวของคำ(ความยาวของชื่ออาหารที่สามารถเพิ่มหรือแก้ไขได้)
    NAME_LENGTH = 2 # ความยาวของชื่อที่สามารถตั้งชื่อได้สั้นที่สุด
    PASSWORD_LENGTH = 8 # ความยาวของรหัสผ่าน
    __LOG__:List[str] = [] # log บันทึกการทำงานต่างๆของโปรแกรม
    
    #? method ในการตั้งค่าสิทธิ์การเข้าถึงใช้งานคำสั่งในโปรแกรม 
    def __setPermissions__(self , user: Dict[str , Any]) -> None:
        # ดึงแค่ตำแหน่งผู้ใช้งานมาเพื่อตั้งค่าระดับการเข้าถึง
        # ค่า True อณุญาติให้มีสิทธิ์เข้าถึงและใช้งานคำสั่งนั้น , ค่า False ไม่อณุญาติให้มีสิทธิ์เข้าถึงและไม่ให้ใช้คำสั่งนั้น
        p = user["position"] # ตำแหน่งของผู้ใช้งาน
        # ยิ่งตำแหน่งระดับสูงๆจะมีสิทธิ์การเข้าถึงคำสั่งโปรแกรมที่มาก
        if p in self.POSITIONS["management"]: # ตำแหน่งงานบริหาร
            # loop การเข้าถึงสิทธิ์ทั้งหมด อณุญาติสิทธิ์ทั้งหมด
            for key in self.__PERMISSIONS__: 
                self.__user__["AccessPermissions"][key] = True
        elif p in ("หัวหน้าพ่อครัว" , "ผู้จัดการครัว" , "รองหัวหน้าพ่อครัว"): # หัวหน้าหรือรองพนักงานครัว
            self.__user__["AccessPermissions"]["AddData"] = True
            self.__user__["AccessPermissions"]["ModifyData"] = True
            self.__user__["AccessPermissions"]["DeleteData"] = False
            self.__user__["AccessPermissions"]["DeleteAllData"] = False
            self.__user__["AccessPermissions"]["ViewLog"] = False
            self.__user__["AccessPermissions"]["SellFood"] = True
        elif p in ("กุ๊ก" , "ผู้ช่วยกุ๊ก") or p in self.POSITIONS["receptionist"]: # พนักงานครัว และ พนักงานต้อนรับ
            self.__user__["AccessPermissions"]["AddData"] = False
            self.__user__["AccessPermissions"]["ModifyData"] = False
            self.__user__["AccessPermissions"]["DeleteData"] = False
            self.__user__["AccessPermissions"]["DeleteAllData"] = False
            self.__user__["AccessPermissions"]["ViewLog"] = False
            self.__user__["AccessPermissions"]["SellFood"] = True
        else: # ไม่รู้ตำแหน่ง
            self.__user__["position"] = "unknown"
            for key in self.__PERMISSIONS__:  
                self.__user__["AccessPermissions"][key] = False # ไม่ให้มีสิทธิ์ใช้งานโปรแกรม(คำสั่งหลักๆ)
        # print(self.__user__)
    
    #? method ในการแปลงชนิดค่าข้อมูลที่ส่งมา 
    def convertValue(self , value: str) -> Union[int , float]:
        typeOf: Union[int , float] = lambda val , t: t(val)
        if self.__DEFAULTSETTING__["EnableDecimalFoodPricing"]:
            return typeOf(value , float)
        elif not self.__DEFAULTSETTING__["EnableDecimalFoodPricing"]:
            return typeOf(value , int)
        
    #? method ไว้เช็คค่าว่างเปล่าที่ส่งมา 
    def isEmpty(self , var: str) -> bool:
        return var == "" or var.__len__() == 0
    
    #? method ในการบันทึกข้อมูลการทำงานต่างๆของโปรแกรม 
    def __log__(self , text:str , Type:None | str = None , Item: None | Any = None) -> None:
        if self.__DEFAULTSETTING__["EnableLog"]:
            if bool(text) and (Type is None and Item is None):
                formatStr = f"{self.getTime(realTime=True)}\t {text}"
                
            if Type == "บันทึก":
                formatStr = f"{self.getTime(realTime=True)}\t ✓ เพิ่มสินค้า \"{Item}\" ในรายการเมนูสำเร็จ"
            elif Type == "ลบ":
                formatStr = f"{self.getTime(realTime=True)}\t ลบสินค้า \"{Item}\" ในรายการเมนู"
            elif Type == "แก้ไข":
                formatStr = f"{self.getTime(realTime=True)}\t 🔧 แก้ไขข้อมูลสินค้า \"{Item}\" ในรายการเมนู"
            elif Type == "ล้มเหลว":
                formatStr = f"{self.getTime(realTime=True)}\t เกิดปัญหาขึ้น {text} "
            elif Type == "สั่งซื้อ":
                formatStr = f"{self.getTime(realTime=True)}\t สั่งซื้ออาหาร \"{Item}\" จำนวน {Item} อย่าง"
            self.__LOG__.append(formatStr)
        else:
            pass
    
    #? กำหนด methods ที่สำคัญดังนี้
    #? ใช้ abstract method และเป็น private method
    @abstractmethod
    def __setElements__(self) -> None:
        pass
    
    @abstractmethod
    def __search__(self , param: str) -> int:
        pass
    
    @abstractmethod
    def __foodOrdering__(self) -> None:
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
    __totalMoney__ = []    # ยอดเงินรวมทั้งหมดใน 1วัน เก็บเป็นยอดสั่งอาหารเรียงแต่ละรายการ
    orderNumber = 0   # หมายเลขจำนวนครั้งในการสั่ง order
    
    #* ค่าสถานะทุกอย่างของโปรแกรม
    __programStatus__ = {
       "isDeleted": None,  # สถานะการลบสินค้า -> True: มีการลบสินค้าแล้ว , False: ไม่มีการลบสินค้า
       "isWorking": None,  # สถานะการทำงานของ method (EXECUTE) หลัก -> True: กำลังทำงาน , False: ไม่ได้ทำงาน
       "programeIsRunning" : False, # สถานะการทำงานอยู่ของโปรแกรม -> True: กำลังทำงาน , False: ไม่ได้ทำงาน
       "isInvokeMethods": None, # สถานะการทำงานของ method ->  True: method กำลังทำงาน , False: method หยุดทำงาน
       "isError": None, # สถานะการเกิดข้อผิดพลาดขึ้นใน method ที่กำลังทำงาน -> True: เกิดข้อผิดพลาด , False: ไม่เกิดข้อผิดพลาด
       "isContinue": None, # สถานะการดำเนินการต่อใน method -> True: ทำต่อ , Falnionse: หยุดทำ
    }
    
    #* ชื่อคำสั่งที่ใช้งานในโปรแกรม
    __KEYWORDS__ = ("e" , "c", "m" , "o", "a" , "d" , "l" , "ed" , "cl" , "logout" , "exit" , "commands", "menu" , "order" ,"add" , "delete" , "log" , "edit" , "clear" , "logout")
    
    #* เช็คคำที่ใส่มาว่าเป็นคำสั่งหรือไม่
    def isKeyword(self , param: str) -> bool:
        return param in self.__KEYWORDS__
    
    #? รันคำสั่งโปรแกรมตอนเริ่มต้น
    def __init__(self , menu:List[Dict[str , Union[int , str]]] , Table: Any) -> None:
        self.__log__(text="เริ่มต้นทำงานโปรแกรม")
        
        if self.__DEFAULTSETTING__["EnableRegisterSystem"]:
            # เรียกใช้ method จาก superclass 
            user = super().__getUser__()
            super().__setUser__(user)
            super().__setPermissions__(user)
            self.__activeUser__ = user
        # เริ่มสถานะการทำงานของโปรแกรม
        self.__programStatus__["programeIsRunning"] = True 
        # รับค่า parameter(menu) มาเก็บไว้ใน attribute menu
        self.__menu__ = menu
        # สร้างตาราง
        self.__menuTable__ = Table() # ตารางอาหาร
        self.__commandsTable__ = Table() # ตารางคำสั่ง
        # สร้างเลข id(รหัสสินค้า)
        for item in self.__menu__: 
            item["id"] = self.createId(self.PRODUCTCODE_LENGTH)
        # เพิ่มคำสั่งแต่ละ columns
        self.__commandsTable__.add_column('คำสั่ง', self.__KEYWORDS__[:10]) # index ที่ 0 - 8
        self.__commandsTable__.add_column('ชื่อคำสั่งเต็ม', self.__KEYWORDS__[10:]) # index ที่ 9 ขึ้นไป
        self.__commandsTable__.add_column("ความหมายของคำสั่ง" , ("ออกจากโปรแกรม" , "แสดงคำสั่ง" , "แสดงเมนูอาหาร" , "สั่งซื้ออาหาร" , "เพิ่มรายการสินค้า" , "ลบรายการสินค้า" , "แสดง log ของโปรแกรม" ,"แก้ไขชื่อรายการสินค้า" , "ลบรายการสินค้าทั้งหมด" , "ออกจากบัญชี"))
        # นำเข้า property(ค่า value) ใน dict เรียงเก็บไว้ใน list ตอนเริ่มโปรแกรม
        self.__setElements__() 
        # self.showLogo(path='./img/logo.png') # แสดง logo ร้านอาหาร
        self.greeting(self.time.hour) # ทักทายผู้ใช้งาน
        self.showCommands() # แสดงคำสั่ง
    
    #? method ในการรับค่าเวลามาแสดงผล 
    def getTime(self , realTime: bool = False) -> str:
        self.now = dt.now()
        self.time = self.now.time()
        self.year = self.now.date().year + 543
        self.today = self.now.date().strftime('%d/%m/%Y') 
        if realTime: # ใช้เวลาจริงในการเก็บ log
            return f"{dt.now().time()}"
        elif not realTime:
            return f"{self.time.hour}:{f'0{self.time.minute}' if self.time.minute < 10 else self.time.minute}:{f'0{self.time.second}' if self.time.second < 10 else self.time.second}"
    
    #? method สวัสดีในแต่ละช่วงเวลา
    def greeting(self , h: int) -> None:
        hi = ''
        if 12 > h >= 0: hi = 'สวัสดีตอนเช้า'
        elif 18 >= h >= 12: hi = 'สวัสดีตอนบ่าย'
        elif 23 >= h >= 19: hi = 'สวัสดีตอนเย็น'
        # แสดงข้อความ
        if self.__DEFAULTSETTING__["EnableRegisterSystem"]:
            print(f'🙏 {hi} คุณ {self.__user__["name"]} วันนี้ วัน{self.days[self.now.date().weekday()]} ที่ {self.now.date().day} เดือน {self.months[self.now.date().month - 1]} ปี พ.ศ. {self.year} ({self.today})')
        else:
            print(f'🙏 {hi} วันนี้ วัน{self.days[self.now.date().weekday()]} ที่ {self.now.date().day} เดือน {self.months[self.now.date().month - 1]} ปี พ.ศ. {self.year} ({self.today})')
        print(f"🕓 เวลา {f'0{self.time.hour}' if self.time.hour < 10 else self.time.hour}:{f'0{self.time.minute}' if self.time.minute < 10 else self.time.minute}:{f'0{self.time.second}' if self.time.second < 10 else self.time.second}")
        print('โปรแกรมพร้อมให้บริการ 🙂')
        
    #? method สร้างเลข id
    def createId(self , length: int = 7) -> int:
        numbers:List[str] = []  # เก็บตัวเลขที่สุ่มมาได้ไว้ใน list
        rand = lambda: str(floor(random() * randint(1,10000)))  # สุ่มเลขส่งคืนกลับมาเป็น string 
        while True:
            num = choice(rand()) # สุ่มเลือก 1 element เลขของผลลัพธ์ 
            if len(numbers) == length: break # ถ้าเท่ากับความยาวที่ตั้งไว้ให้หยุด loop ซ้ำ
            else: 
                numbers.append(num)  # เก็บตัวเลขเข้าใน list
                if numbers[0] == '0': numbers.remove('0') # ไม่เอาเลข 0 นำหน้า
        newId = str("".join(numbers))  # รวม element ใน list ให้เป็นข้อความ
        numbers.clear()
        return newId
    
    #? (method หลัก) ในการเปลี่ยนค่าข้อมูลใน foodList , idList เมื่อในรายการในเมนู (menu) มีการเปลี่ยนแลง ตัวแปรทั้ง 2 ตัวนี้จะเปลี่ยนตามด้วย
    def __setElements__(self) -> None:
        # method getValue จะวน loop ดึง value ที่อยู่ใน dict ของ menu
        def getValue(setInitialValue: List[str] , keyName: str) -> List[str]: 
            setInitialValue.clear() # ล้างค่า elements เก่าทุกครั้ง
            for item in self.__menu__: setInitialValue.append(item[keyName]) # เพิ่ม element ใหม่ให้ parameter
            newValue = setInitialValue 
            return newValue
        # ถ้าไม่มีรายการสินค้าอะไรในเมนูให้ลบข้อมูล li อันเก่าทั้งหมด 
        if self.__menu__ == []:
            self.__foodList__.clear()
            self.__idList__.clear()
        else:
            # เก็บค่า list ที่ได้ให้ 2 ตัวแปร
            self.__foodList__ = getValue(setInitialValue=self.__foodList__ , keyName="name") 
            self.__idList__ = getValue(setInitialValue=self.__idList__ , keyName="id")
        
    #? (method หลัก) ในการค้นหา dictionary ที่อยู่ใน foodList , idList (อ่านค่าใน list) ส่งคืนกลับเป็นเลข index หรือ None 
    def __search__(self , param: str) -> int | None:
        # เช็ค parameter ที่ส่งมา 
        checked =  param.strip() # ตัดเว้นว่างออก
        # มีข้อมูลใน รายการอาหาร
        if checked in self.__foodList__:
            idx = self.__foodList__.index(checked)
        # มีข้อมูลใน รายการรหัสสินค้า
        elif checked in self.__idList__:
            idx = self.__idList__.index(checked)
        # ถ้าไม่มีข้อมูลอยู่ในทั้ง 2 รายการให้ส่งค่า None
        elif (checked not in self.__foodList__) and (checked not in self.__idList__): 
            return None 
        return idx

    #? method แสดงเมนูอาหาร
    def showMenu(self):
        # เอกสารประกอบการใช้งาน API: https://pypi.org/project/prettytable
        self.__menuTable__.clear() # reset ข้อมูลตารางใหม่ทุกครั้งเมื่อเรียกใช้ function
        self.__menuTable__.field_names = ('ลำดับ' , 'อาหาร' , 'ราคา(บาท)' , 'รหัสสินค้า') # สร้าง field
        n = 1 
        for item in self.__menu__:
            # print(f'{n}. {item["name"]} ราคา {item["price"]} บาท รหัสสินค้า {item["id"]}')
            self.__menuTable__.add_row((n , item["name"] , item["price"] , int(item["id"])) , divider=True) # เพิ่ม row ใหม่ตามเมนูที่มีอยู่ในปัจจุบัน
            n += 1
        # แสดงตารางเมนูถ้าไม่พบข้อมูลสินค้าไม่ต้องแสดงตาราง (เขียนในรูแบบ ternary operator)
        print(f'🌟 ตอนนี้ไม่มีรายการสินค้าใดๆโปรดเพิ่มสินค้าก่อนแสดงรายการเมนู!') if self.__menu__.__len__() == 0 else print('\n',self.__menuTable__ , '\n')
    
    #? method แสดงคำสั่ง
    def showCommands(self) -> None:
        print('\nเลือกพิมพ์คำสั่งเหล่านี้เพื่อดำเนินการ'.center(50))
        print(self.__commandsTable__,'\n')
    
    #? method แสดง logo ของร้านอาหาร
    def showLogo(self , path: str) -> None:
        # เอกสารประกอบการใช้งาน API: https://pypi.org/project/ascii-magic/
        logo = AsciiArt.from_image(path)
        logo.to_terminal() 
    
    #? แสดงข้อความแจ้งเตือนทุกครั้งตอนเรียกใช้ methods
    def notify(self , context: str , *args: Tuple[str] | None) -> None: # แสดงข้อความเมื่อเรียกคำสั่งที่พิมพ์ไป
        print(f'❔ พิมพ์ตัว "n" เพื่อแสดงแจ้งเตือนนี้อีกครั้ง\n❔ พิมพ์ตัว "m" หรือ "menu เพื่อแสดงเมนู\n❔ พิมพ์ตัว "e" หรือ "end" {context}')
        # การส่งค่า parameter ตัวที่ 2 เป็น None คือไม่ต้องการแสดงข้อความอย่างอื่นเพิ่ม
        if args[0] == None: pass
        else: print(*args, sep='\n')
                                                                                                                                                                                                                 
    #? (method หลัก) สั่งซื้ออาหาร
    def __foodOrdering__(self) -> None:  
        # แสดงแจ้งเตือน
        self.notify("เพื่อออกจากการสั่งซื้อ" , "❔ พิมพ์ตัว \"c\" หรือ \"cancel\" เพื่อยกเลิก order ที่สั่งไปทั้งหมด"
        , "❔ พิมพ์ตัว \"s\" หรือ \"show\" เพื่อแสดงรายการที่สั่งไปทั้งหมด")
        
        #* เมื่อหยุดการทำงานของ method นี้ให้คำนวณยอดเงินรวม order ที่สั่งไป
        def calculateOrder() -> None:
            #* มีการสั่งอาหาร = ข้อมูลใน dict จะไม่เป็น 0
            if (self.currentOrder.__len__() != 0) or self.currentOrder != {}: 
                priceList:List[int] = [] # เก็บราคาอาหาร(ราคาจานละ)
                showOrder = self.currentOrder.copy() # dict ที่จะแสดงใน print                
                self.__allOrders__.append(self.currentOrder.copy()) # เก็บ order
                for item in self.currentOrder:  # loop รายชื่ออาหารที่ทำการสั่งมาทั้งหมด
                    idx = self.__search__(item) # หาเลข index แต่ละรายการมาอ้างอิงข้อมูลในเมนู
                    # จำนวนสินค้า X กับราคาสินค้าที่อยู่ในเมนู = ราคาอาหารทั้งหมดของอาหารนั้น
                    # currentOrder{ Key: แต่ละรายชื่ออาหาร , Value: แต่ละราคาอาหารรวมทั้งหมด }
                    self.currentOrder[item] = (self.currentOrder[item] * self.__menu__[idx]["price"])
                    # ราคารียงชื่ออาหารตามลำดับของ currentOrder
                    priceList.append(self.__menu__[idx]["price"])
                # ผลรวมจำนวนเงินที่ต้องจ่าย
                self.result = sum(self.currentOrder.values())
                # เก็บ li จำนวนแต่ละราคาอาหารที่สั่งไป
                self.__totalMoney__.extend(self.currentOrder.values())
                self.orderNumber += 1
                print(f"\nหมายเลขรายการสั่งอาหารที่ {self.orderNumber}. รายการอาหารที่สั่งไปคือ : ")
                for number, key in enumerate(showOrder):
                    print(f"🍽 {number + 1}. {key} จำนวน {showOrder[key]:,} อย่าง ราคาจานละ {priceList[number]} บาท รวมเป็นเงิน {self.currentOrder[key]:,} บาท")
                print(f"💸 ยอดเงินรวมท้งหมด {self.result:,} บาท")
                # เริ่มสั่งรายการใหม่ให้ set ค่าเริ่มใหม่หมด (ลบสินค้า order ปัจจุบันออก)
                self.result = 0
                self.currentOrder.clear()
                # ถ้าไม่ได่สั่งอะไรไม่ต้องแสดงรายการ
            else: 
                print('ไม่มีการสั่งอาหารรายการใดๆ')
                
        # infinity loop จนกว่าจะพิมพ์คำสั่ง "e" หรือ "end" เพื่อออกจาก loop
        while self.__programStatus__["isInvokeMethods"]:
            try:
                foodName = input("ชื่ออาหารหรือรหัสสินค้า : ")
                foodName = foodName.lower().strip()
                # แสดงรายการเมนู
                if foodName == "m" or foodName == "menu": 
                    self.showMenu()
                # ออกจาการทำงานของ method
                elif foodName == "e" or foodName == "end":
                    # ! เมื่อหยุดการทำงานของ function __foodOrdering__ ให้เรียกใช้ method คำนวณสินค้า
                    calculateOrder()
                    self.__programStatus__["isInvokeMethods"] = False
                # ยกเลิกอาหารที่สั่ง
                elif foodName == "c" or foodName == "cancel":
                    self.currentOrder.clear()
                    print('✔ ลบรายการ order ที่ทำการสั่งไปเรียบร้อย')
                # แสดง order ที่สั่งไป
                elif foodName == "s" or foodName == "show":
                    if self.currentOrder == {}:
                        print('❗ ยังไม่มีการสั่งเมนูอาหารโปรดสั่งอาหารเพื่อทำการแสดงรายการที่สั่ง')
                    count = 0
                    print('อาหารที่คุณสั่งไป')
                    for key , valaue in self.currentOrder.items():
                        count += 1
                        print(f'{count}.) {key} จำนวน {valaue} อย่าง')
                # แสดงแจ้งเตือนอีกครั้ง
                elif foodName == "n":
                    self.notify("เพื่อออกจากการสั่งซื้อ" , "❔ พิมพ์ตัว \"c\" หรือ \"cancel\" เพื่อยกเลิก order ที่สั่งไปทั้งหมด" , "❔ พิมพ์ตัว \"s\" หรือ \"show\" เพื่อแสดงรายการที่สั่งไปทั้งหมด")
                # เช็คชื่ออาหารหรือรหัสสินค้าว่าอยู่ใน list หรือไม่
                elif (foodName in self.__foodList__) or (foodName in self.__idList__):
                    self.__programStatus__["isContinue"] = True # ให้ทำงานต่อ
                    while self.__programStatus__["isContinue"]:
                        try:
                            amount = int(input("จำนวน : ")) # จำนวนสั่งซื้ออาหาร
                            if amount <= 0:
                                raise UserWarning("❌ สั่งจำนวนอาหารไม่ถูกต้องโปรดใส่จำนวนใหม่อีกครั้ง!")
                            elif amount >= 10:
                                raise UserWarning("❌ สั่งจำนวนอาหารเยอะเกินไปโปรดใส่จำนวนใหม่อีกครั้ง!")
                        except ValueError:
                            print("❌ โปรดใส่เป็นเลขจำนวนเต็มเท่านั้น!")
                        except UserWarning as err:
                            print(err)
                        else:
                            self.__programStatus__["isContinue"] = False
                    # ถ้าใส่ชื่อเป็นรหัสสินค้าให้แปลงรหัสสินค้าเป็นชื่ออาหาร
                    if foodName in self.__idList__: 
                        idx = self.__search__(foodName)
                        foodName = self.__menu__[idx]["name"]
                    # เพิ่มสินค้าที่สั่งลง order
                    # ถ้าเป็นชื่ออาหารที่ยังไม่มี key อยู่ใน dict    
                    if foodName not in self.currentOrder: 
                        # key: ชื่ออาหาร , value: จำนวนอาหาร
                        self.currentOrder[foodName] = amount # เก็บจำนวนอาหาร
                    # ถ้ามีชื่อ key ซ้ำเป็นอยู่แล้วให้เพิ่มจำนวนอาหารเท่ากับของใหม่     
                    elif foodName in self.currentOrder: 
                        self.currentOrder[foodName] += amount # เพิ่มจำนวนอาหารที่มีอยู่แล้ว
                # ไม่มีชื่ออาหารอยู่ในเมนู    
                elif (foodName not in self.__foodList__) and (foodName not in self.__foodList__): 
                    raise UserWarning(f'❌ ไม่มีชื่อ "{foodName}" อยู่ในเมนูอาหาร!')
                else:
                    raise UserWarning(f'❌ ไม่มีชื่อ "{foodName}" อยู่ในเมนูอาหาร!')
            except UserWarning as err:
                print(err)
                
    #? (method หลัก) เพิ่มรายการสินค้า
    def __addItems__(self) -> None:
        # แสดงแจ้งเตือน
        self.notify('เพื่อออกจาการเพิ่มสินค้า' , None)
        # infinity loop จนกว่าจะพิมพ์คำสั่ง "e" หรือ "end" เพื่อออกจาก loop
        while self.__programStatus__["isInvokeMethods"]:
            try:
                newProduct = input('ชื่ออาหารใหม่ : ') 
                newProduct = newProduct.strip().lower()
                # ออกจาการทำงานของ method
                if newProduct == "e" or newProduct == "end": 
                    self.__programStatus__["isInvokeMethods"] = False
                # แสดงรายการเมนู    
                elif newProduct == "m" or newProduct == "menu": 
                    self.showMenu()
                elif newProduct == "n":
                    self.notify('เพื่อออกจาการเพิ่มสินค้า' , None)
                else:
                    # ห้ามมีชื่ออาหารที่ตั้งมาใหม่ซ้ำกับข้อมูลในเมนู
                    if newProduct in self.__foodList__:
                        raise UserWarning(f'❌ ไม่สามารถใช้ชื่อ "{newProduct}" ในการตั้งเมนูใหม่ได้เนื่องจากมีชื่อซ้ำอยู่ในเมนูโปรดตั้งชื่อใหม่!')
                    # ห้ามเกินความยาวในการตั้งชื่ออาหารที่กำหนด
                    elif len(newProduct) >= self.WORD_LENGTH: 
                        raise UserWarning('❌ ไม่สามารถตั้งชื่ออาหารที่มีความยาวเกินได้')
                    # ห้ามตั้งชื่ออาหารขึ้นต้นเป็นตัวเลขหรือตั้งชื่อเป็นตัวเลข
                    elif newProduct.isdigit() or newProduct[0].isdigit():
                        raise UserWarning(f'❌ ไม่สามารถตั้งชื่ออาหารที่เป็นเลขขึ้นต้นได้')
                    # ตรวจแล้วไม่มีเงื่อนไข error ใดๆให้ดำเนินการต่อ
                    else:
                        self.__programStatus__["isContinue"] = True # set ค่าสถานะให้ดำเนินการต่อ
            except UserWarning as err:
                print(err)
            # เช็คแล้วว่าไม่ใช้คำสั่งหรือใส่ชื่อเรียบร้อยให้ใช้เงื่อนไขเพิ่มราคาสินค้า
            else:
                while self.__programStatus__["isContinue"]:
                    try:
                        print('💬 ราคาสินค้าสามารถตั้งอยู่ในช่วงราคา 1 ถึง 1,000 บาท')
                        pricing = self.convertValue(value=input('ราคาอาหาร : '))  
                        # ห้ามตั้งเกินราคาที่ตั้งไว้ 
                        if pricing > self.MAX: 
                            raise UserWarning('❌ ไม่สามารถตั้งราคาอาหารเกิน 1,000 บาทได้')
                        # ห้ามตั้งน้อยกว่าราคาที่ตั้งไว้ 
                        elif pricing <= self.MIN: 
                            raise UserWarning('❌ ไม่สามารถตั้งราคาอาหารติดลบหรือเป็นศูนย์ได้')
                        else:
                            # เมื่อชื่ออาหารที่ไม่มีอยู่ในเมนู (เช็คแล้วว่าไม่มีชื่อสินค้าซ้ำ) ให้เพิ่มสินค้าใหม่
                            if newProduct not in self.__foodList__:
                                # สร้างรายการอาหารใหม่
                                self.__menu__.append({ 
                                    "name": newProduct,
                                    "price": pricing,
                                    "id": self.createId(self.PRODUCTCODE_LENGTH)
                                })          
                                print('✔ เพิ่มรายการอาหารใหม่เสร็จสิ้น')
                                print(f'🍖 จำนวนรายการอาหารมีทั้งหมดตอนนี้ {len(self.__menu__)} รายการ')
                                self.__setElements__()   
                            else: 
                                raise UserWarning(f'❌ ไม่สามารถใช้ชื่อ "{newProduct}" ในการตั้งเมนูใหม่ได้เนื่องจากมีชื่อซ้ำอยู่ในเมนูโปรดตั้งชื่อใหม่!')
                    except UserWarning as err:
                        print(err)
                    except ValueError:
                        print('❌ ไม่สามารถตั้งราคาสินค้าได้ราคาสินค้าต้องตั้งเป็นตัวเลขจำนวนเต็มเท่านั้น!')
                    else: 
                        self.__programStatus__["isContinue"] = False

    # ? (method หลัก) ลบรายการสินค้า
    def __removeItems__(self) -> None:
        # แสดงแจ้งเตือน
        self.notify("เพื่อออกจากการลบเมนู" , None)
        # function ลบสินค้า
        def deleteElements(param: str) -> None:
            findIndex = self.__search__(param) # หาสินค้าที่ต้องการลบส่งกลับเป็นเลข index
            del self.__menu__[findIndex] # ลบสินค้า่โดยอ้างอิงเลข index
            self.__setElements__() # แก้ไข element ใน foodList และ idList เมื่อมีการลบสินค้าในเมนู
            self.__programStatus__["isDeleted"] = True
        # infinity loop จนกว่าจะพิมพ์คำสั่ง "e" หรือ "end" เพื่อออกจาก loop
        while self.__programStatus__["isInvokeMethods"]:
            self.__programStatus__["isDeleted"] = False
            try:
                item = input('ใส่ชื่ออาหารหรือรหัสสินค้าเพื่อทำการลบ : ').lower().strip() 
                # ออกจาการทำงานของ method
                if item == 'e' or item == 'end':  
                    self.__programStatus__["isInvokeMethods"] = False
                # แสดงรายการเมนู    
                elif item == 'm' or item == 'menu': 
                    self.showMenu()
                elif item == 'n':
                    self.notify("เพื่อออกจากการลบเมนู" , None)
                # ลบข้อมูลเป็นหลายๆอย่างโดยใส่ , 
                # จะใช่เงื่อนไขนี้ได้เมื่อใส่ข้อมูลตรงตามนี้: a , b , c ,...
                elif ',' in item or ',' in [*item]: # ถ้าใส่ , ให้ทำเงิอนไขนี้
                    formatList = item.split(',') # ลบ , ออกจะได้ ข้อมูลเป็น list
                    # จัดระเบียบข้อความ
                    for i in range(formatList.__len__()): 
                        formatList[i] = formatList[i].strip() # ลบทุก elements ทุกตัวให้เอาเว้นว่างออก
                    # ถ้าใส่ , แล้วไม่มีชื่ออาหารหรือเลข id ต่อท้ายให้ลบช่องว่างเปล่าที่เกิดขึ้น
                    if '' in formatList:
                        count = formatList.count('') 
                        for j in range(count):
                            formatList.remove('') # ลบ sting เปล่าออก
                    # ลบสินค้าที่ละชิ้น
                    for element in formatList: 
                        if element in self.__foodList__: 
                            deleteElements(element)
                        elif element in self.__idList__: 
                            deleteElements(element)
                        elif (element not in self.__foodList__) and (element not in self.__idList__):
                            self.__programStatus__["isError"] = True
                            raise UserWarning(f"❌ ไม่มี \"{element}\" อยู่ในเมนูอาหารโปรดกรอกชื่อหรือเลข id ใหม่")
                # เมื่อมีข้อมูลให้ลบออก
                elif (item in self.__foodList__) or (item in self.__idList__): 
                    deleteElements(item)
                elif (item not in self.__foodList__) and (item not in self.__idList__):
                    raise UserWarning(f"❌ ไม่มี \"{item}\" อยู่ในเมนูอาหารโปรดกรอกชื่อหรือเลข id ใหม่")
                else: 
                    raise UserWarning(f"❌ ไม่มี \"{item}\" อยู่ในเมนูอาหารโปรดกรอกชื่อหรือเลข id ใหม่")
            except UserWarning as err:
                print(err)
                if self.__programStatus__["isError"]:
                    print('ยกเลิกการดำเนินการลบสินค้าล่าสุด')
            except ValueError:
                print(f"❌ ไม่มี \"{item}\" อยู่ในเมนูอาหาร")
            else:
                if self.__programStatus__["isDeleted"]:
                    print('✔ ลบรายการอาหารเสร็จสิ้น')
                    print(f'🍖 จำนวนรายการอาหารมีทั้งหมดตอนนี้ {len(self.__menu__)} รายการ')

    # ? (method หลัก) แก้ไขรายการสินค้า
    def __editItems__(self) -> None:
        # แสดงแจ้งเตือน
        self.notify("เพิ่อออกจาการแก้ไข" , None)
        # infinity loop จนกว่าจะพิมพ์คำสั่ง "e" หรือ "end" เพื่อออกจาก loop
        while self.__programStatus__["isInvokeMethods"]:
            try:
                self.__programStatus__["isError"] = False # set ค่าสถานะ
                # ถามข้อมูล
                product = input('ใส่ชื่ออาหารหรือรหัสสินค้าเพื่อทำการแก้ไข : ')
                product = product.lower().strip()
                # ออกจาการทำงานของ method
                if product == 'e' or product == 'end': 
                    self.__programStatus__["isInvokeMethods"] = False
                # แสดงรายการเมนู    
                elif product == 'm' or product == 'menu': 
                    self.showMenu()
                elif product == 'n':
                    self.notify("เพิ่อออกจาการแก้ไข" , None)
                else:
                    # หาเลข index ของเมนูอาหาร
                    findIndex = self.__search__(product)
                    idx = findIndex # เลข index
                    if idx == None: # ใส่ข้อมูลไม่ถูกต้อง
                        raise UserWarning(f'❌ "{product}" ไม่ค้นพบชื่ออาหารและรหัสสินค้าอยู่ในรายการสินค้าโปรดลองใหม่อีกครั้ง!')
                    else:
                        # แสดงข้อความ
                        print(f'คุณเลือกรายการสินค้าที่จะแก้ไข คือ {self.__menu__[idx]["name"]} ราคา {self.__menu__[idx]["price"]} บาท รหัสสินค้าคือ {self.__menu__[idx]["id"]}')
                        # ชื่ออาหารที่จะแก้ไขใหม่
                        changeFoodName = input(f'แก้ไขชื่อ จาก "{self.__menu__[idx]["name"]}" เป็น --> ')
                        #! ตรวจสอบความถูกต้อง
                        assert changeFoodName not in self.__foodList__ # ชื่อห้ามซ้ำกับรายการอื่นๆ
                        assert not(changeFoodName == '' or changeFoodName.__len__() == 0) # ไม่ใส่ชื่อ
                        if changeFoodName.isdigit() or changeFoodName[0].isdigit():
                            raise UserWarning('❌ ไม่สามารถตั้งชื่อขึ้นต้นด้วยตัวเลขได้หรือตั้งชื่อเป็นตัวเลขได้!')
                        print('💬 ราคาสินค้าสามารถตั้งอยู่ในช่วงราคา 1 ถึง 1,000 บาท') # แสดงข้อความ
                        # ราคาที่จะแก้ไขใหม่
                        changePrice = int(input(f'แก้ไขราคา จาก {self.__menu__[idx]["price"]} บาท เป็น --> '))
                        # ยอดเงินต้องไม่เกิน 1000 บาท และ ต้องไม่ติดลบและไม่เป็นศูนย์
                        if (changePrice > self.MAX or changePrice <= self.MIN) or (changePrice not in range(self.MIN , self.MAX)): 
                            raise UserWarning('❌ ราคาสินค้าต้องตั้งอยู่ในราคาไม่เกิน 1,000 บาทเท่านั้น!')
                        print(f'💬 รหัสสินค้าต้องตั้งเป็นเลขจำนวนเต็มจำนวน {self.PRODUCTCODE_LENGTH} ตัว')
                        # เลข id ที่จะแก้ไข
                        changeId = int(input(f'แก้ไขรหัสสินค้า จากรหัส {self.__menu__[idx]["id"]} เป็น --> '))
                        if str(changeId).__len__() != self.PRODUCTCODE_LENGTH:
                            raise UserWarning(f'❌ ต้องตั้งความของรหัสสินค้าเป็น {self.PRODUCTCODE_LENGTH} เท่านั้น!')
                        #* แก้ไขข้อมูล dictionary ในเมนู
                        self.__menu__[idx]["name"] = changeFoodName
                        self.__menu__[idx]["price"] = changePrice
                        self.__menu__[idx]["id"] = changeId
                        print('✔ แก้ไขรายการอาหารเสร็จสิ้น')          
                        # เปลี่ยนแปลงค่า li ใหม่   
                        self.__setElements__()
            except ValueError:
                self.__programStatus__["isError"] = True
                print('🔴 Error: ราคาสินค้าและรหัสสินค้าต้องตั้งเป็นตัวเลขจำนวนเต็มเท่านั้น!')
            except AssertionError:
                self.__programStatus__["isError"] = True
                print('🔴 Error: ชื่อที่คุณทำการแก้ไขนั้นเป็นชื่อซ้ำอยู่ในเมนูอาหารโปรดแก้ไขชื่อที่ไม่เหมือนกัน หรือ ห้ามใส่ชื่อว่างเปล่า!')
            except UserWarning as err:
                self.__programStatus__["isError"] = True
                print(err)
            finally:
                self.__programStatus__["isError"] and print('❗ เกิดข้อผิดพลาดขึ้นเริ่มทำรายการใหม่ตั้งแต่เริ่มต้น')

    # ? method สรุปจำนวนเงินและการสั่งซื้อสินค้า
    def conclusion(self , total: List[int] , orders: List[Dict[str , int]]) -> str:
        quantity = 0 # จำนวนอาหารที่สั่งไปทั้งหมด
        me:List[int] = mean(total) # หาค่าเฉลี่ย
        mo:List[str] = [] # ฐานนิยม
        for i in range(len(orders)):
            element = orders[i] # dict แต่ละอันใน list 
            for j in element: # เข้าถึง dist แล้วดึง key มาใช้ , ตัวแปร j คือชื่ออาหารทำการเก็บจำนวนรายการเอาไว้ 
                key = j # ชื่ออาหาร
                value = element[j] # จำนวนของอาหารที่สั่ง
                li = [key for k in range(value)] # loop ตามจำนวนครั้ง ของ value ทุกๆครั้งที่ loop จะคืนค่า(เพิ่ม) ชื่ออาหารให้ li
                mo.extend(li) # เพิ่ม li ให้ mo เพื่อนำไปหาฐานนิยมต่อไป
                quantity += value # บวกจำนวนเพิ่มแต่ละอาหาร
        mo = mode(mo) # หาฐานนิยม: return ชื่ออาหารที่มีชื่อนั้นมากสุด ถ้าไม่มีชื่ออาหารตัวไหนมากกว่ากันจะคืน element ตัวแรก
        return f"""🔷 จำนวนสั่งซื้ออาหารวันนี้ {len(orders):,} รายการ {quantity:,} อย่าง ทำจำนวนเงินรวมไปได้ {sum(total):,} บาท 
มีค่าเฉลี่ยการสั่งซื้ออาหารอยู่ที่ {me:,.2f}
อาหารที่สั่งบ่อยหรือสั่งเยอะที่สุดในวันนี้คือ {mo}
        """
                
    #? method ในการแสดงข้อมูลการทำงานต่างๆของโปรแกรม 
    def __showLog__(self) -> None:
        print('\n\tบันทึกของโปรแกรม')
        for i in self.__LOG__:
            print(i)
        print('\n')

    #? method ในการลบเมนูสินค้า
    def __deleteMenu__(self) -> None:
        if input('คุณแน่ใจว่าต้องการลบสินค้าทั้งหมดถ้าต้องการให้พิมพ์ "y" แต่โปรดรู้ไว้ข้อมูลสินค้าจะถูกลบถาวรและไม่สามารถกู้คืนได้ (y/n): ').lower().strip() == "y":
            self.__menu__.clear()
            print('✔ ลบรายการสินค้าทั้งหมดเสร็จสิ้น')
        else: print('❗ คุณยกเลิกการดำเนินการลบสินค้าทั้งหมด')

    #? method ออกจากโปรแกรม
    def __exitProgram__(self) -> None:
        self.__log__(text="จบการทำงานโปรแกรม")
        self.__programStatus__["isWorking"] = False
        #* ถ้ามีการสั่งอาหารให้แสดงรายการสรุปสินค้าที่ซื้อไปภายใน 1 วัน ถ้าไม่ได้สั่งซื้อไม่ต้องแสดง
        self.__allOrders__.__len__() != 0 and print(self.conclusion(total=self.__totalMoney__ , orders=self.__allOrders__))
        print('🙏 ขอบคุณที่มาใช้บริการของเรา')
        self.__programStatus__["programeIsRunning"] = False

    #? (method หลัก) ในการดำเนินการหลักของโปรแกรม
    def EXECUTE(self) -> None:
        self.__log__(text="เริ่มทำงาน function หลัก")
        # infinity loop จนกว่าจะพิมพ์คำสั่ง "e" หรือ "exit" เพื่อออกจาก loop
        while self.__programStatus__["programeIsRunning"]:
            self.__programStatus__["isWorking"] = True
            self.__programStatus__["isWorking"] and self.__log__(text="โปรแกรมรอคำสั่งเพื่อเริ่มดำเนินการทำงาน")
            try:
                command = input("🟢 พิมพ์คำสั่งเพื่อดำเนินการต่อไป >>> ")
                command = command.lower().strip()
                #! ตรวจสอบความถูกต้อง
                assert command != "" or len(command) == 0 # ถ้าไม่ได้พิมพ์คำสั่งอะไรมา
                # #? ค้นหาชื่อคำสั่ง
                if self.isKeyword(command):
                    # เปลี่ยนสถานะ attribute ตัวนี้ให้เป็น True หมายถึงกำลังทำการเรียกใช้ methods ของโปรแกรม
                    self.__programStatus__["isInvokeMethods"] = True
                    #* ออกจากโปรแกรม
                    if command == "e" or command == "exit":
                        self.__log__(text="มีการเรียกใช้คำสั่ง ออกจากโปรแกรม")
                        self.__exitProgram__()
                    #* แสดงคำสั่ง
                    elif command == "c" or command == "commands": 
                        self.__log__(text="มีการเรียกใช้คำสั่ง แสดงคำสั่ง")
                        self.showCommands()
                    #* แสดงรายการเมนู
                    elif command == "m" or command == "menu": 
                        self.__log__(text="มีการเรียกใช้คำสั่ง แสดงเมนู")
                        self.showMenu()
                    #* ซื้ออาหาร
                    elif command == "o" or command == "order":
                        self.__log__(text="มีการเรียกใช้คำสั่ง สั่งซื้อสินค้า")
                        self.__foodOrdering__()
                    #* เพิ่มสินค้า
                    elif command == "a" or command == "add": 
                        self.__log__(text="มีการเรียกใช้คำสั่ง เพิ่มสินค้า")
                        self.__addItems__()
                    #* ลบสินค้า
                    elif command == "d" or command == "delete":
                        self.__log__(text="มีการเรียกใช้คำสั่ง ลบสินค้า")
                        self.__removeItems__()
                    #* แก้ไขสินค้า
                    elif command == "ed" or command == "edit": 
                        self.__log__(text="มีการเรียกใช้คำสั่ง แก้ไขสินค้า")
                        self.__editItems__()
                    #* ลบรายการสินค้าทั้งหมด
                    elif command == "cl" or command == "clear":
                        self.__log__(text="มีการเรียกใช้คำสั่ง ล้างรายการสินค้าทั้งหมด")
                        self.__deleteMenu__()
                    #* แสดงกิจกรรมการทำงานต่างๆของโปรแกรม
                    elif command == "l" or command == "log":
                        self.__showLog__()
                    #* ออกจากบัญชี
                    elif command == "logout":
                        self.__log__(text=f"{self.__user__['name']} ออกใช้งานจากบัญชี {self.__user__['email']}")
                        self.__logout__()   
                        self.greeting(h=self.time.hour)
                        self.showCommands()
                #* ไม่มีคำสั่งที่ค้นหา
                else: 
                    raise UserWarning(f'🔴 Error: ไม่รู้จำคำสั่ง "{command}" โปรดเลือกใช้คำสั่งที่มีระบุไว้')
            except UserWarning as err:
                print(err)
                self.__log__(Type='ล้มเหลว' , text="ไม่พบคำสั่งที่มีอยู่ในโปรแกรม")
            except AssertionError:
                print("🔴 Error: คุณไม่ได้ป้อนคำสั่งโปรดพิมพ์คำสั่ง")
                self.__log__(Type='ล้มเหลว' , text="ไม่พบคำสั่งที่มีอยู่ในโปรแกรม")
            finally:
                self.__programStatus__["isWorking"] and print('โปรดเลือกพิมพ์คำสั่ง')

# สร้าง instance(object) เพื่อนำไปใช้งาน
program = Program(menu=data[:30] , Table=PrettyTable)
program.EXECUTE() # เรียกใช้ method จาก object เพื่อดำเนินการทำงาน