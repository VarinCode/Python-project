from abc import abstractmethod 
from datetime import datetime as dt 
from time import sleep
from random import randint , random , choice
from math import floor
# นำเข้า module (ข้อมูลเมนู)
from menu import Menu
# นำเข้า module ข้อมูลผู้ใช้งาน
from data import Users
# pip install typing
from typing import List , Dict , Union , Any , Tuple 
# pip install ascii-magic
from ascii_magic import AsciiArt 
from statistics import mean , mode
from sys import exit
from colorama import init , Fore , Back , Style
from pyconsole import Box , YELLOW 
# pip install rich
from rich.console import Console
from rich.table import Table
from rich.box import HEAVY , HEAVY_EDGE , ROUNDED
init() # ติตดตั้งการใช้สีในข้อความ

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
            "AddData": True,
            "ModifyData": True,
            "DeleteData": True, 
            "DeleteAllData": True,
            "ViewLog": True,
            "SellFood": True
        }
    }
    
    #* บันทึกข้อมูลผู้ใช้งานจากการ login
    __saveUserData__ = None
    console = Console()
    
    #? method ในการ login 
    def __login__(self) -> Dict[str , str]:   
        
        #? function ในการเช็คค่าว่าง  True เป็นค่าว่างเปล่า , False ไม่เป็นค่าว่างเปล่า
        isEmpty = lambda var: var == "" or var.__len__() == 0
        
        #? function ในการ login 
        def loginFunction() -> Dict[str , Any]:
            # ข้อมูลที่ผู้ใช้งานต้องกรอก
            userLogin = {
                "nameOrEmail": None,
                "password": None
            }
            
            self.console.print('\n\t[blue bold underline]Login[/]')

            while not bool(userLogin["nameOrEmail"]) or not bool(userLogin["password"]):
                while not bool(userLogin["nameOrEmail"]):
                    try:
                        nameOrEmail = input("ชื่อผู้ใช้งานหรืออีเมล : ").strip()
                        if isEmpty(nameOrEmail):
                            raise UserWarning('❌ ชื่อผู้ใช้งานไม่ถูกต้องโปรดลองใหม่อีกครั้ง')
                        elif len(nameOrEmail) > self.WORD_LENGTH:
                            raise UserWarning('❌ ชื่อผู้ใช้งานของคุณมีความยาวมากเกินไป')
                        else:
                            userLogin['nameOrEmail'] = nameOrEmail
                    except UserWarning as err:
                        self.console.print(f'[red]{err.__str__()}[/]')
                while not bool(userLogin["password"]):
                    try:
                        password = input("รหัสผ่าน : ").strip()
                        if isEmpty(password):
                            raise UserWarning('❌ รหัสผ่านผู้ใช้งานไม่ถูกต้องโปรดลองใหม่อีกครั้ง')
                        else:
                            userLogin['password'] = password
                    except UserWarning as err:
                        self.console.print(f'[red]{err.__str__()}[/]')
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
                # ยืนยันค่าสถานะของ# The above code is written in Python. However, it seems to be
                if status:
                    # loop ข้อมูลผู้ใช้งานในไฟล์ data.py โดย userData เก็บข้อมูลเป็น list และ element คือ dictionary เป็นข้อมูลผู้ใช้งานในร้านค้าของแต่ละคน
                    # ให้เทียบแต่ละ dict หรือ เทียบข้อมูลผู้ใช้งานแต่ละคนถ้า loop ครบแล้วไม่มีหรือไม่ตรงกันแปลว่าข้อมูลผู้ใช้งานที่ส่งมาไม่มีอยู่จริง
                    for user in Users.getUser(self=Users): # ดึง element (dict)แต่ละอันออกมาเช็คว่าตรงกันไหม
                        # ตรวจสอบ ชื่อ
                        if validateUser["nameOrEmail"] == user["name"]:
                            #ถ้ามีในไฟล์เก็บข้อมูลผู้ใช้งานให้ค่าสถานะเป็น True
                            isCorrect["name"] = True
                        # ตรวจสอบ อีเมล
                        if validateUser["nameOrEmail"] == user["email"]:
                            isCorrect["email"] = True
                        # ตรวจสอบ รหัสผ่าน
                        if validateUser["password"] == user["password"]:
                            isCorrect["password"] = True
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
                            #* เก็บค่าของผู้ใช้งานที่ loop แต่ละ dict เก็บไว้ในตัวแปร validateUser เพราะข้อมูลตรงกัน 
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
                self.console.print(f'[red]{err.__str__()}[/]')
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
        else: # หลังออกจาก loop
            self.console.print('[cyan]🔹 กำลัง login เข้าสู่ระบบ กรุณารอสักครู่ ████████░░░[/]')
            # sleep(3)
            self.console.print('[green bold]✓ login ผู้ใช้งานสำเร็จ[/]\n')
        # ส่งข้อมูลผู้ใช้งาน
        return self.__saveUserData__
    
    #? method ในการ สมัครบัญชีผู้ใช้งานใหม่
    def __createAccount__(self) -> Dict[str , str]:
        
        #? function ในการเช็คค่าว่าง  True เป็นค่าว่างเปล่า , False ไม่เป็นค่าว่างเปล่า
        isEmpty = lambda var: var == "" or var.__len__() == 0
        newUser = {
            "name": None,
            "password": None,
            "email": None,
            "position": None
        }        
        
        self.console.print('\n[blue bold underline]สมัครบัญชีผู้ใช้งานใหม่[/]')
        
        while (not bool(newUser["name"])) or (not bool(newUser["password"])) or (not bool(newUser["position"])) or (not bool(newUser["email"])):
            while not bool(newUser["name"]):
                try:
                    name = input("ตั้งชื่อผู้ใช้งาน : ").strip()
                    if isEmpty(name):
                        raise UserWarning('❌ ชื่อผู้ใช้งานไม่ถูกต้องโปรดลองใหม่อีกครั้ง')
                    elif len(name) > self.WORD_LENGTH:
                        raise UserWarning('❌ ชื่อผู้ใช้งานของคุณมีความยาวมากเกินไป')
                    elif len(name) <= self.NAME_LENGTH:
                        raise UserWarning('❌ ชื่อผู้ใช้งานของคุณมีสั้นน้อยเกินไป')
                    else:
                        newUser['name'] = name
                except UserWarning as err:
                    self.console.print(f'[red]{err.__str__()}[/]')
            while not bool(newUser["email"]):
                try:
                    email = input("ใส่อีเมลที่ใช้ในบัญชีนี้ : ").strip().lower()
                    if isEmpty(email):
                        raise UserWarning('❌ อีเมลไม่ถูกต้องโปรดลองใหม่อีกครั้ง')
                    elif "@" not in email: # ต้องมี @ 
                        raise UserWarning(f'❌ "{email}" ไม่ใช้อีเมลโปรดลองใหม่อีกครั้ง')
                    spilt = email.split('@') # หั่น email ออกจะได้ ['....' , '....'] el1 คือชื่อ , el2 คืออีเมลของบริษัทหรือองค์กรอะไรเราจะเช็คที่ el2
                    if spilt[0] == '' or spilt[1] == '': # ถ้าใส่ el1 หรือ el2 เป็นค่าว่างเปล่า 
                        raise UserWarning(f'❌ "{email}" ไม่ใช้อีเมลโปรดลองใหม่อีกครั้ง')
                    checkEmail = '@' + spilt[1] # เติม '@' ใน el2 จะได้ประเภทของ email เพื่อนำไปเช็ค 
                    if checkEmail in ("@gmail.com" , "@yahoo.com" , "@outlook.com",  "@outlook.co.th" , "@hotmail.com" , "@ku.th" , "@live.ku.th" , "@icloud.com" , "@protonmail.com" , "@zoho.com" , "@aol.com"):
                        newUser['email'] = email
                    else:
                        raise UserWarning(f'❌ "{email}" ไม่ใช้อีเมลโปรดลองใหม่อีกครั้ง')
                except UserWarning as err:
                    self.console.print(f'[red]{err.__str__()}[/]')
            while not bool(newUser["password"]):
                symbols = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',':', ';', '<', '=', '>', '?', '@' , '{', '|', '}', '~' , '[', '\\', ']', '^', '_', '`']
                isSymbol = False
                try:
                    password = input("ตั้งรหัสผ่าน : ").strip()
                    for letter in password:
                        if letter in symbols:
                            isSymbol = True
                    if not isSymbol:
                        raise UserWarning(f'❗ ต้องมีสัญลักษณ์พิเศษอย่างน้อย 1 ตัวในการตั้งรหัสผ่านสามารถใช้สัญลักษณ์ได้ดังนี้: {" ".join(symbols)}')
                    if isEmpty(password):
                        raise UserWarning('❌ รหัสผ่านผู้ใช้งานไม่ถูกต้องโปรดลองใหม่อีกครั้ง')
                    elif len(password) < self.PASSWORD_LENGTH:
                        raise UserWarning(f'❌ ความยาวของรหัสผ่านต้องมีความยาว {self.PASSWORD_LENGTH} ตัวขึ้นไป')
                    else:
                        confirmPassword = input("ยืนยันรหัสผ่าน : ").strip()
                        if confirmPassword == password:
                            newUser['password'] = password
                        elif confirmPassword != password:
                            raise UserWarning(f'รหัสผ่านที่ยืนยันไม่ถูกต้องกับรหัสผ่านที่ตั้งโปรดตั้งรหัสผ่านให้ตรงกัน')
                except UserWarning as err:
                    self.console.print(f'[red]{err.__str__()}[/]')
            while not bool(newUser["position"]):
                allPositions = []
                print(f'💬 โปรดเลือกตำแหน่งงานในร้านอาหารของที่คุณทำงานอยู่:' , end=" ")
                for key in self.POSITIONS:
                    allPositions.extend(self.POSITIONS[key])
                print(" , ".join(allPositions))
                try:
                    selectedPosition = input("ตำแหน่งงานหรือหน้าที่ของคุณคือ : ").strip()
                    if isEmpty(selectedPosition):
                        raise UserWarning('❌ คุณไม่ได้ใส่ตำแหน่งงานของคุณโปรดกรอกตำแหน่งงานของคุณ')
                    elif selectedPosition not in allPositions:
                        raise UserWarning(f'❌ ตำแหน่ง "{selectedPosition}" ไม่มีอยู่ในร้านอาหารของเราโปรดลองใหม่อีกครั้ง')
                    else:
                        newUser['position'] = selectedPosition
                except UserWarning as err:
                    self.console.print(f'[red]{err.__str__()}[/]')
        else: # เมื่อออกจาก while loop เสร็จ 
            self.console.print('[cyan]กำลังสร้างบัญชีผู้ใช้งาน กรุณารอสักครู่ ████████░░░ [/]')
            # sleep(3)
            self.console.print('[green bold]✓ สร้างบัญชีผู้ใช้งานสำเร็จโปรด Login เพื่อเข้าใช้งานโปรแกรม[/]')
            self.console.print('🔹[blue] กลับไปที่หน้า Login[/]')
            Users.addUser(self=Users , newUser=newUser) # เพื่มข้อมูลผู้ใช้งานคนใหม่
            return self.__login__() # เรียกใช้ method login
    
    #? method บัญชีผู้ใช้งานออกจากระบบ
    def __logout__(self , callBackFunction: Any) -> bool:
        status = False # สถานะออกจากบัญชี True ออกจากบัญชี , False ไม่ได้ออกจากบัญชี
        # เมื่อตอบ y ให้เอาข้อมูลผู้ใช้งานออกจากโปรแกรม 
        if input('คุณต้องการออกจากบัญชีผู้ใช้งานนี้ (y/n) : ').lower().strip() == "y":
            callBackFunction(typeOfLog=self.INFO , text=f"{self.__user__['name']} ได้ออกจากการใช้งานบัญชี {self.__user__['email']} แล้ว")
            status = True
            self.__setUser__(isLogout=True) # set ข้อมูลผู้ใช้งานโปรแกรมเป็นค่าเริ่มต้นคือค่าว่างเปล่า
            self.console.print('[cyan]กำลังนำคุณออกจากบัญชี ...[/]')
            # sleep(3)
            self.console.print('[blue]คุณออกจากบัญชีนี้เรียบร้อย[/]')
        else:
            self.console.print('[orange1]⚠ คุณยกเลิกการออกจากบัญชีนี้[/]')
        return status

    #? method ในการให้ข้อมูลผู้ใช้งาน 
    def __getUser__(self , callBackFunction) -> Dict[str , str | Union[str , Dict[str , str]]]:
        user = None
        # loop เรื่อยๆจนกว่าจะได้ข้อมูลผู้ใช้งาน
        while not bool(user):
            try:
                self.console.print(*('\n◻ พิมพ์ [gold1](1)[/] เพื่อ Login เข้าสู่ระบบ' , '◻ พิมพ์ [gold1](2)[/] เพื่อสมัครบัญชีผู้ใช้งาน' , '◻ พิมพ์ [gold1](3)[/] ออกจากโปรแกรม') , sep='\n')
                selected = int(input('โปรดพิมพ์ตัวเลือก : '))
                # เลือก login
                if selected == 1:
                    user = self.__login__()
                    callBackFunction(typeOfLog=self.INFO ,text=f'{user["name"]} ได้ login เข้าใช้งาน')
                # เลือกสมัครสมาชิกก่อนแล้วจะไปที่หน้า login
                elif selected == 2:
                    user = self.__createAccount__() # sign up
                    callBackFunction(typeOfLog=self.INFO ,text=f'มีการสร้างบัญชีผู้ใช้งาน {user["name"]}')
                # ออกจากโปรแกรม
                elif selected == 3:
                    print('ปิดโปรแกรม')
                    exit()
                else:
                    raise Warning(f'❌ ไม่มี "{selected}" ในตัวเลือกของการถาม โปรดพิมพ์แค่ 1 หรือ 2 เท่านั้น')
            except ValueError:
                self.console.print('[red]❌ โปรดพิมพ์เป็นตัวเลขเท่านั้น[/]')
            except Warning as err:
                self.console.print(f'[red]{err.__str__()}[/]')
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
                "AccessPermissions": dict({})
            }
            self.__saveUserData__ = None
        #* เมื่อมีการส่งข้อมูลผู้ใช้งานมาที่ parameter user 
        elif user != None:
            for key in user: # loop แล้วดึง key จาก property user ออกมา
                self.__user__[key] = user[key] # ให้ property ใน attribute user มีค่าเป็นข้อมูลของผู้ใช้งานที่ส่งมา

class Date:
    # วัน และ เดือน
    days = ("จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์" , "อาทิตย์")
    months = ("มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม")
    
    # วันที่ เวลา
    now = dt.now()
    time = now.time()
    year = now.date().year + 543
    today = now.date().strftime('%d/%m/%Y') 
    
    #? method สวัสดีผู้ใช้งานในแต่ละช่วงเวลา
    def greeting(self , h: int) -> None:
        hi = ''
        # Ref: https://www.aepenglishschool.com/content/5024/english-time
        if h >= 5 and h <= 11: hi = 'สวัสดีตอนเช้า'
        elif h >= 12  and h <= 17: hi = 'สวัสดีตอนบ่าย'
        elif h >= 18 and h <= 21: hi = 'สวัสดีตอนเย็น'
        elif h >= 22 and h >= 4: hi = 'สวัสดีตอนกลางคืน'
        # แสดงข้อความ
        print(f'🙏 {hi} คุณ {self.__user__["name"]} วันนี้ วัน{self.days[self.now.date().weekday()]} ที่ {self.now.date().day} เดือน {self.months[self.now.date().month - 1]} ปี พ.ศ. {self.year} ({self.today})')
        print(f"🕓 เวลา {f'0{self.time.hour}' if self.time.hour < 10 else self.time.hour}:{f'0{self.time.minute}' if self.time.minute < 10 else self.time.minute}:{f'0{self.time.second}' if self.time.second < 10 else self.time.second}")
        print('โปรแกรมพร้อมให้บริการ 🙂')
        
    #? method ในการรับค่าเวลามาแสดงผล 
    def getTime(self , realTime: bool = False) -> str:
        # อัปเดตค่าของมัน 
        self.now = dt.now()
        self.time = self.now.time()
        if realTime: # ใช้เวลาจริงในการเก็บ log
            return f"{self.time}"[:11 + 1] # ตัด str ให้เหลือข้อความ 11 ตัว
        else:
            return f"{self.time.hour}:{f'0{self.time.minute}' if self.time.minute < 10 else self.time.minute}:{f'0{self.time.second}' if self.time.second < 10 else self.time.second}"
        
    def getDate(self) -> str:
        return self.today
class Configuration(Register , Date): #? องค์ประกอบใน class: กำหนดโครงสร้างหลักๆของ class Program และ สิทธิ์การใช้งาน
    
    #* ตำแหน่งในร้านอาหาร
    # Ref: https://www.waiterio.com/blog/th/raaychuue-phnakngaanraan-aahaarthanghmd-bthbaath-khwaamrabphidch-b
    POSITIONS = {
        "management": ("ผู้จัดการ" , "ผู้ดูแลระบบ"), # ตำแหน่งงานบริหาร 
        "kitchenStaff": ("หัวหน้าพ่อครัว" , "ผู้จัดการครัว" , "รองหัวหน้าพ่อครัว" , "กุ๊ก" , "ผู้ช่วยกุ๊ก"), # พนักงานครัว
        "receptionist":("หัวหน้าบริกร" , "พนักงานต้อนรับ", "ซอมเมลิเยร์" , "พนักงานบาร์" , "บริกร" , "แคชเชียร์") # พนักงานต้อนรับ
    }
    
    #* อธิบายค่า value ที่อยู่ใน Properties
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
    AMOUNT = 30 # จำนวนอาหารที่ขายในร้านอาหารต่อเมนู
    # การบันทึกข้อมูล
    __LOG__:List[str] = [] # log บันทึกข้อมูลการทำงานต่างๆของโปรแกรม
    # ประเภทของ log ในโปรแกรมนี้
    GENERAL = 'general'
    INFO = 'info'
    ERROR = 'error'
    EDIT = 'edit'
    SELL = 'sell'
    SAVE = 'save'
    DEL = 'delete'
    DELALL = 'delete all'
    ADD = 'add'
    WARN = 'warn'
    RESTORE = 'restore'
    COMMAND = 'command'
    
    #? method ในการตั้งค่าสิทธิ์การเข้าถึงใช้งานคำสั่งในโปรแกรม 
    def __setPermissions__(self , user: Dict[str , Any] = None) -> None:
        # เปิดใช้งานสิทธิ์การเข้าถึง
        # ดึงแค่ตำแหน่งผู้ใช้งานมาเพื่อตั้งค่าระดับการเข้าถึง
        # ค่า True อณุญาติให้มีสิทธิ์เข้าถึงและใช้งานคำสั่งนั้น , ค่า False ไม่อณุญาติให้มีสิทธิ์เข้าถึงและไม่ให้ใช้คำสั่งนั้น
        position = user["position"] # ตำแหน่งของผู้ใช้งาน
        # ยิ่งตำแหน่งระดับสูงๆจะมีสิทธิ์การเข้าถึงคำสั่งโปรแกรมที่มาก
        if position in self.POSITIONS["management"]: # ตำแหน่งงานบริหาร
            # loop การเข้าถึงสิทธิ์ทั้งหมด อณุญาติสิทธิ์ทั้งหมด
            for key in self.__PERMISSIONS__: 
                self.__user__["AccessPermissions"][key] = True
        elif position in ("หัวหน้าพ่อครัว" , "ผู้จัดการครัว" , "รองหัวหน้าพ่อครัว"): # หัวหน้าหรือรองพนักงานครัว
            self.__user__["AccessPermissions"]["AddData"] = True
            self.__user__["AccessPermissions"]["ModifyData"] = True
            self.__user__["AccessPermissions"]["DeleteData"] = False
            self.__user__["AccessPermissions"]["DeleteAllData"] = False
            self.__user__["AccessPermissions"]["ViewLog"] = False
            self.__user__["AccessPermissions"]["SellFood"] = True
        elif position in ("กุ๊ก" , "ผู้ช่วยกุ๊ก") or position in self.POSITIONS["receptionist"]: # พนักงานครัว และ พนักงานต้อนรับ
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
        
    #? method ในการบันทึกข้อมูลการทำงานต่างๆของโปรแกรม 
    def __log__(self , text:str = "", typeOfLog: None | str = None , item: None | List[str | int] | Any = None) -> None:
        userName: str = self.__user__["name"]
        data = f"[blue][{self.getTime(realTime=True)}][/]\t "
        if bool(text) and (typeOfLog is None or typeOfLog == "general" and item is None):
            data += f"{text}"
        elif typeOfLog == self.ADD:
            data += f"{userName} ได้เพิ่มสินค้า \"{item}\" ในรายการเมนู"
        elif typeOfLog == self.DEL:
            data += f"{userName} ได้ทำการลบสินค้า \"{item}\" ในรายการเมนู"
        elif typeOfLog == self.EDIT:
            data += f"{userName} ทำการแก้ไขข้อมูลสินค้า \"{item[0]}\" ไปเป็น \"{item[1]}\" ในรายการเมนู"
        elif typeOfLog == self.ERROR:
            data += f"เกิดปัญหาขึ้น {text} "
        elif typeOfLog == self.SELL:
            data += f"{userName} ได้กดสั่งซื้ออาหารให้ลูกค้าอาหาร \"{item[0]}\" จำนวน {item[1]} อย่าง"
        elif typeOfLog == self.COMMAND:
            data += f"{userName} กดใช้งานคำสั่ง {text}"
        elif typeOfLog == self.INFO:
            data += f"{text}"
        elif typeOfLog == self.WARN:
            data += f"{userName} พยายามเข้าถึงคำสั่งที่ไม่ได้รับอณุญาติให้ใช้งาน คือคำสั่ง {text}"
        self.__LOG__.append(data)

    
    def notAuthorizedToAccess(self , context: str) -> None:
        noPermission = '[bold red on grey3]⨉ คุณไม่มีสิทธิ์ที่จะใช้งานคำสั่งนี้ได้[/]'
        self.__log__(typeOfLog=self.WARN , text=context)
        raise UserWarning(noPermission)
    
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
    def __addItem__(self) -> None:
        pass
    
    @abstractmethod
    def __addItem__(self) -> None:
        pass
    
    @abstractmethod
    def __removeItem__(self) -> None:
        pass
    
    @abstractmethod
    def __editItem__(self) -> None:
        pass
    
    @abstractmethod
    def __deleteMenu__(self) -> None:
        pass
    
    @abstractmethod
    def __exitProgram__(self) -> None:
        pass
                
class Program(Configuration , Date): 
    #? กำหนด attributes
    
    #* ตัวแปรไว้เป็นค่าอ้างอิงเลข index ในการหาอาหารสินค้าในรายการเมนู
    __foodList__: List[str] = []
    __idList__: List[str] = []
    
    #* รายการที่ผู้ใช้สั่งเมนูอาหารจะเก็บไว้ในตัวแปร order
    currentOrder: Dict[str , int] = {} # key คือ ชื่ออาหาร , value คือ จำนวนสินค้าที่สั่ง
    __allOrders__: List[Dict[str , int]] = []    # order ทั้งหมดจะเก็บไว้ใน list 
    __allOrdersCode__: List[Dict[str , str]] = []
    orderNumber = 0   # หมายเลขจำนวนครั้งในการสั่ง order
    orderCode = ''
    orderDate = ''
    orderQuantity: Dict[str , int] = {}
    result = 0          # ยอดเงินรวมจำนวนล่าสุดของ currentOrder
    __totalMoney__ = []    # ยอดเงินรวมทั้งหมดใน 1วัน เก็บเป็นยอดสั่งอาหารเรียงแต่ละรายการ
    
    #* ค่าสถานะทุกอย่างของโปรแกรม
    __programStatus__ = {
       "isDeleted": None,  # สถานะการลบสินค้า -> True: มีการลบสินค้าแล้ว , False: ไม่มีการลบสินค้า
       "isWorking": None,  # สถานะการทำงานของ method (EXECUTE) หลัก -> True: กำลังทำงาน , False: ไม่ได้ทำงาน
       "programeIsRunning" : False, # สถานะการทำงานอยู่ของโปรแกรม -> True: กำลังทำงาน , False: ไม่ได้ทำงาน
       "isInvokeMethods": None, # สถานะการทำงานของ method ->  True: method กำลังทำงาน , False: method หยุดทำงาน
       "isError": None, # สถานะการเกิดข้อผิดพลาดขึ้นใน method ที่กำลังทำงาน -> True: เกิดข้อผิดพลาด , False: ไม่เกิดข้อผิดพลาด
       "isContinue": None, # สถานะการดำเนินการต่อใน method -> True: ทำต่อ , Falnionse: หยุดทำ
       "isCreateTable": None
    }
    
    #* ชื่อคำสั่งที่ใช้งานในโปรแกรม
    __KEYWORDS__ = ("e" , "c", "m" , "o", "a" , "d" , "l" , "ed" , "cl" , "out" , "exit" , "commands", "menu" , "order" ,"add" , "delete" , "log" , "edit" , "clear" , "logout")
    
    #* เช็คคำที่ใส่มาว่าเป็นคำสั่งหรือไม่
    def isKeyword(self , param: str) -> bool:
        return param in self.__KEYWORDS__
    
    #? รันคำสั่งโปรแกรมตอนเริ่มต้น
    def __init__(self , menu:List[Dict[str , Union[int , str]]] ) -> None:
        self.__log__(typeOfLog=self.GENERAL , text="เริ่มต้นทำงานโปรแกรม")
        # login และ ตั้งค่าสิทธิ์การใช้งานก่อน
        # เรียกใช้ method จาก superclass 
        # user = super().__getUser__(callBackFunction=self.__log__)
        # super().__setUser__(user)
        # super().__setPermissions__(user)
        # เริ่มสถานะการทำงานของโปรแกรม
        self.__programStatus__["programeIsRunning"] = True 
        # รับค่า parameter(menu) มาเก็บไว้ใน attribute menu
        self.__menu__ = menu
        # สร้าง console เพื่อแสดงข้อความใน terminal แบบใส่ลูกเล่นต่างๆได้
        self.console = Console()        
        # สร้างตาราง
        self.__menuTable__ = Table(title='เมนูอาหาร' , title_style='yellow italic', show_lines=True, show_footer=True, box=HEAVY_EDGE)
        self.__commandsTable__ = Table(title='คำสั่งของโปรแกรม' , caption='เลือกพิมพ์คำสั่งเหล่านี้เพื่อดำเนินการ', title_style='purple italic', caption_style='purple italic', box=ROUNDED) # ตารางคำสั่ง
        self.__programStatus__["isCreateTable"] = True
        # นำเข้า property(ค่า value) ใน dict เรียงเก็บไว้ใน list ตอนเริ่มโปรแกรม
        self.__setElements__() 
        # self.showLogo(path='./img/logo.png') # แสดง logo ร้านอาหาร
        self.greeting(self.time.hour) # ทักทายผู้ใช้งาน
        self.showCommands() # แสดงคำสั่ง
  
    #? method สร้างเลข id
    def createId(self , length: int = 7) -> str:
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
    
    #? method ในการสร้าง code รหัสสินค้าการสั่งซื้อ
    def generateOrderCode(self) -> str:
        chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = "".join([str(randint(0,9)) for i in range(6)])
        code = f'{choice(chars)}{choice(chars)}{choice(chars)}{numbers}'
        return code
    
    #? method ในการสร้าง bill ใบเสร็จ
    def generateBill(self , n: int , price: List[int] , quantity: List[int] , order: Dict[str , int]) -> None:
        contents = ''
        contents += f'\n\t\t{Fore.YELLOW}ใบเสร็จของร้านอาหาร {self.getDate()} เวลา {self.getTime()}{Fore.RESET}'
        contents += f"\n\tรายการอาหารที่ {n}. หมายเลขอ้างอิงการสั่งซื้อ {Back.LIGHTWHITE_EX}{self.generateOrderCode()}{Back.RESET}"
        contents += f'\nอาหารที่สั่งไปคือ: '
        for index , key in enumerate(order):
            contents += f"{index + 1}. {key} \tจำนวน {quantity[index]} อย่าง \tราคาจานละ {price[index]} บาท \tรวมเป็นเงิน {order[key]:,} บาท\n"
        contents += f"\n{Fore.GREEN}💸 ยอดเงินรวมท้งหมด {self.result:,} บาท{Fore.RESET}\n"
        bill = Box(contents=contents , color=YELLOW , width=90)
        print('\n' , bill , '\n' , sep='')
    
    #? (method หลัก) ในการเปลี่ยนค่าข้อมูลใน foodList , idList เมื่อในรายการในเมนู (menu) มีการเปลี่ยนแลง ตัวแปรทั้ง 2 ตัวนี้จะเปลี่ยนตามด้วย
    def __setElements__(self) -> None:
        # method getValue จะวน loop ดึง value ที่อยู่ใน dict ของ menu
        def getValue(variable: List[str] , keyName: str) -> List[str]: 
            variable.clear() # ล้างค่า elements เก่าทุกครั้ง
            for item in self.__menu__: variable.append(str(item[keyName])) # เพิ่ม element ใหม่ให้ parameter
            newVariable = variable 
            return newVariable
        # ถ้าไม่มีรายการสินค้าอะไรในเมนูให้ลบข้อมูล li อันเก่าทั้งหมด 
        if self.__menu__ == []:
            self.__foodList__.clear()
            self.__idList__.clear()
        else:
            # เก็บค่า list ที่ได้ให้ 2 ตัวแปร
            self.__foodList__ = getValue(variable=self.__foodList__ , keyName="name") 
            self.__idList__ = getValue(variable=self.__idList__ , keyName="id")
        
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
        allAmount = 0
        for i in self.__menu__:
            allAmount += i["amount"]
        # ก่อนเริ่มสร้างตารางเมนูให้ ล้างค่า columns และ rows อันเก่าออกทั้งหมดก่อนๆจะเริ่มสร้างตารางใหม่ (อัปเดตตาราง)
        self.__menuTable__.columns = []
        self.__menuTable__.rows = []
        # เอกสารประกอบการใช้งาน Library: https://pypi.org/project/prettytable
        self.__menuTable__.add_column(header='ลำดับ' , footer='รวม' , justify='center')
        self.__menuTable__.add_column(header='อาหาร', footer=f'{self.__menu__.__len__()} เมนู' , justify='center')
        self.__menuTable__.add_column(header='ราคา', footer= '-', justify='center' , style='green')
        self.__menuTable__.add_column(header='จำนวน', footer= f'{allAmount} จำนวน', justify='center' , style='light_sky_blue1')
        self.__menuTable__.add_column(header='รหัสสินค้า', footer= '-', justify='center' , style='light_goldenrod1')
        n = 1 
        for item in self.__menu__:
            # print(f'{n}. {item["name"]} ราคา {item["price"]} บาท รหัสสินค้า {item["id"]}')
            self.__menuTable__.add_row(f'{n}' , item["name"] , f'{item["price"]} บาท' , f'{item["amount"]}' ,f'{item["id"]}') # เพิ่ม row ใหม่ตามเมนูที่มีอยู่ในปัจจุบัน
            n += 1
        # แสดงตารางเมนูถ้าไม่พบข้อมูลสินค้าไม่ต้องแสดงตาราง (เขียนในรูแบบ ternary operator)
        self.console.print(f'🌟 ตอนนี้ไม่มีรายการสินค้าใดๆโปรดเพิ่มสินค้าก่อนแสดงรายการเมนู!') if self.__menu__.__len__() == 0 else self.console.print('\n' , self.__menuTable__ , '\n')
    
    #? method แสดงคำสั่ง
    def showCommands(self) -> None:
        if self.__programStatus__["isCreateTable"]: #สร้างตารางคำสั่งแค่รอบเดียวแค่รอบเดียว
            self.__commandsTable__.add_column(header='คำสั่ง' , justify='center') # index ที่ 0 - 9
            self.__commandsTable__.add_column(header='ชื่อคำสั่งเต็ม' , justify='center') # index ที่ 10 ถึง index สุดท้าย
            self.__commandsTable__.add_column(header="ความหมายของคำสั่ง" , justify='center')
            commandsTu = ("ออกจากโปรแกรม" , "แสดงคำสั่ง" , "แสดงเมนูอาหาร" , "สั่งซื้ออาหาร" , "เพิ่มรายการสินค้า" , "ลบรายการสินค้า" , "แสดง log ของโปรแกรม" ,"แก้ไขชื่อรายการสินค้า" , "ลบรายการสินค้าทั้งหมด" , "ออกจากบัญชี")
            index = 10
            for i in range(index):
                self.__commandsTable__.add_row(f'[dark_magenta]{self.__KEYWORDS__[i]}' , f'[blue_violet]{self.__KEYWORDS__[index + i]}' , f'{commandsTu[i]}')
            self.__programStatus__["isCreateTable"] = False
        else:
            pass
        self.console.print('\n' , self.__commandsTable__,'\n')
    
    #? method แสดง logo ของร้านอาหาร
    def showLogo(self , path: str) -> None:
        # เอกสารประกอบการใช้งาน Library: https://pypi.org/project/ascii-magic/
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
                foodQuantity  = list(self.currentOrder.values()) # dict ที่จะแสดงใน print                
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
                self.generateBill(n=self.orderNumber , price=priceList , quantity=foodQuantity , order=self.currentOrder)
                self.__log__(text=f'มีการสั่งอาหารใน order หมายเลขที่ {self.orderNumber} คิดเป็นเงินจำนวนทั้งหมด {self.result:,} บาท')
                # เริ่มสั่งรายการใหม่ให้ set ค่าเริ่มใหม่หมด (ลบสินค้า order ปัจจุบันออก)
                self.result = 0
                self.currentOrder.clear()
                # ถ้าไม่ได่สั่งอะไรไม่ต้องแสดงรายการ
            else: 
                print('ไม่มีการสั่งอาหารรายการใดๆ')
        
        remaining = 10
    
        #* function ในการลดจำนวนสินค้าลง
        def decrement(key: str , amount: int , restore: bool = False) -> None:
            self.__programStatus__["isError"] = False
            if restore:
                pass
            else:
                if amount >= 8:
                    self.__programStatus__["isError"] = True
                    raise UserWarning('❌ ท่านสั่งอาหารจำนวนเยอะเกินไม่สามารถทำการดำเนินการสั่งได้')
                else:
                    if key not in self.orderQuantity:
                        self.orderQuantity[key] = remaining
                        self.orderQuantity[key] -= amount
                    elif key in self.orderQuantity:
                        if self.orderQuantity[key] <= 0:
                            self.orderQuantity[key] = 0
                            self.__programStatus__["isError"] = True
                            raise UserWarning(f'❌ ไม่สามารถดำเนินการสั่งอาหารเมนู "{key}" ได้อีกแล้วท่านโปรดสั่งอาหารอื่นแทน')
                        self.orderQuantity[key] = self.orderQuantity[key] - amount
                    idx = self.__search__(key)
                    self.__menu__[idx]["amount"] -= amount
                
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
                    print('✓ ลบรายการ order ที่ทำการสั่งไปเรียบร้อย')
                    self.__log__(text=f'ลบรายการ order ที่กดสั่งไป หมายเลข order ที่ {self.orderNumber + 1} ')
                # แสดง order ที่สั่งไป
                elif foodName == "s" or foodName == "show":
                    if self.currentOrder == {}:
                        print('❕ ยังไม่มีการสั่งเมนูอาหารโปรดสั่งอาหารเพื่อทำการแสดงรายการที่สั่ง')
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
                            self.console.print("[red]❌ โปรดใส่เป็นเลขจำนวนเต็มเท่านั้น![/]")
                        except UserWarning as err:
                            self.console.print(f'[red]{err.__str__()}[/]')
                        else:
                            # ถ้าใส่ชื่อเป็นรหัสสินค้าให้แปลงรหัสสินค้าเป็นชื่ออาหาร
                            if foodName in self.__idList__: 
                                idx = self.__search__(foodName)
                                foodName = self.__menu__[idx]["name"]
                            self.__programStatus__["isContinue"] = False
                        # เพิ่มสินค้าที่สั่งลง order
                        # ถ้าเป็นชื่ออาหารที่ยังไม่มี key อยู่ใน dict    
                        if foodName not in self.currentOrder: 
                            decrement(key=foodName , amount=amount)
                            if self.__programStatus__["isError"]:
                                pass
                            else:
                                # key: ชื่ออาหาร , value: จำนวนอาหาร
                                self.currentOrder[foodName] = amount # เก็บจำนวนอาหาร
                                self.__log__(typeOfLog=self.SELL , item=[foodName , amount])
                        # ถ้ามีชื่อ key ซ้ำเป็นอยู่แล้วให้เพิ่มจำนวนอาหารเท่ากับของใหม่     
                        elif foodName in self.currentOrder: 
                            decrement(key=foodName , amount=amount)
                            if self.__programStatus__["isError"]:
                                pass
                            else:
                                self.currentOrder[foodName] += amount # เพิ่มจำนวนอาหารที่มีอยู่แล้ว
                                self.__log__(text=f'{self.__user__["name"]} ได้สั่ง "{foodName}" เพิ่มอีก {amount} จำนวน รวมเป็น {self.currentOrder[foodName]}')
                # กรณีค้นหาแล้วไม่มีชื่ออาหาร หรือ ไม่มีรหัสสินค้า อยู่ในเมนู    
                elif (foodName not in self.__foodList__) and (foodName not in self.__foodList__): 
                    raise UserWarning(f'❌ ไม่มีชื่อ "{foodName}" อยู่ในเมนูอาหาร!')
                else:
                    raise UserWarning(f'❌ ไม่มีชื่อ "{foodName}" อยู่ในเมนูอาหาร!')
            except UserWarning as err:
                self.console.print(f'[red]{err.__str__()}[/]')
                
    #? (method หลัก) เพิ่มรายการสินค้า
    def __addItem__(self) -> None:
        
        # แสดงแจ้งเตือน
        self.notify('เพื่อออกจาการเพิ่มสินค้า' , None)
        # infinity loop จนกว่าจะพิมพ์คำสั่ง "e" หรือ "end" เพื่อออกจาก loop
        while self.__programStatus__["isInvokeMethods"]:
            try:
                newItem = input('ชื่ออาหารใหม่ : ').strip().lower()
                # ออกจาการทำงานของ method
                if newItem == "e" or newItem == "end": 
                    self.__programStatus__["isInvokeMethods"] = False
                # แสดงรายการเมนู    
                elif newItem == "m" or newItem == "menu": 
                    self.showMenu()
                # แสดงแจ้งเตือนอีกครั้ง
                elif newItem == "n":
                    self.notify('เพื่อออกจาการเพิ่มสินค้า' , None)
                else:
                    # ห้ามมีชื่ออาหารที่ตั้งมาใหม่ซ้ำกับข้อมูลในเมนู
                    if newItem in self.__foodList__:
                        raise UserWarning(f'❌ ไม่สามารถใช้ชื่อ "{newItem}" ในการตั้งเมนูใหม่ได้เนื่องจากมีชื่อซ้ำอยู่ในเมนูโปรดตั้งชื่อใหม่!')
                    # ห้ามเกินความยาวในการตั้งชื่ออาหารที่กำหนด
                    elif len(newItem) >= self.WORD_LENGTH: 
                        raise UserWarning('❌ ไม่สามารถตั้งชื่ออาหารที่มีความยาวเกินได้')
                    # ห้ามตั้งชื่ออาหารขึ้นต้นเป็นตัวเลขหรือตั้งชื่อเป็นตัวเลข
                    elif newItem.isdigit() or newItem[0].isdigit():
                        raise UserWarning(f'❌ ไม่สามารถตั้งชื่ออาหารที่เป็นตัวเลขขึ้นต้นได้')
                    # ตรวจแล้วไม่มีเงื่อนไข error ใดๆให้ดำเนินการต่อ
                    else:
                        self.__programStatus__["isContinue"] = True # set ค่าสถานะให้ดำเนินการต่อ
            except UserWarning as err:
                self.console.print(f'[red]{err.__str__()}[/]')
            # เช็คแล้วว่าไม่ใช้คำสั่งหรือใส่ชื่อเรียบร้อยให้ใช้เงื่อนไขเพิ่มราคาสินค้า
            else:
                while self.__programStatus__["isContinue"]:
                    try:
                        print('💬 ราคาสินค้าสามารถตั้งอยู่ในช่วงราคา 1 ถึง 1,000 บาท')
                        pricing = int(input('ราคาอาหาร : ')) 
                        # ห้ามตั้งเกินราคาที่ตั้งไว้ 
                        if pricing > self.MAX: 
                            raise UserWarning('❌ ไม่สามารถตั้งราคาอาหารเกิน 1,000 บาทได้')
                        # ห้ามตั้งน้อยกว่าราคาที่ตั้งไว้ 
                        elif pricing <= self.MIN: 
                            raise UserWarning('❌ ไม่สามารถตั้งราคาอาหารติดลบหรือเป็นศูนย์ได้')
                        else:
                            # เมื่อชื่ออาหารที่ไม่มีอยู่ในเมนู (เช็คแล้วว่าไม่มีชื่อสินค้าซ้ำ) ให้เพิ่มสินค้าใหม่
                            if newItem not in self.__foodList__:
                                self.__log__(typeOfLog=self.ADD , item=newItem) # เก็บ log
                                # สร้างรายการอาหารใหม่
                                self.__menu__.append({ 
                                    "name": newItem,
                                    "price": pricing,
                                    "id": self.createId(self.PRODUCTCODE_LENGTH),
                                    "amount": self.AMOUNT
                                })          
                                self.console.print(f'[green bold]✓ เพิ่มเมนูอาหารใหม่เสร็จสิ้น[/]')
                                self.console.print(f'🍖 จำนวนรายการอาหารที่มีทั้งหมดในตอนนี้มีอยู่ [yellow]{len(self.__menu__)}[/] เมนู')
                                self.__setElements__()   
                            else: 
                                raise UserWarning(f'❌ ไม่สามารถใช้ชื่อ "{newItem}" ในการตั้งเมนูใหม่ได้เนื่องจากมีชื่อที่ซ้ำอยู่ในเมนูอาหารโปรดตั้งชื่อใหม่!')
                    except UserWarning as err:
                        self.console.print(f'[red]{err.__str__()}[/]') 
                    except ValueError:
                        self.console.print('[red]❌ ไม่สามารถตั้งราคาสินค้าได้ราคาสินค้าต้องตั้งเป็นตัวเลขจำนวนเต็มเท่านั้น![/]')
                    else: 
                        self.__programStatus__["isContinue"] = False

    # ? (method หลัก) ลบรายการสินค้า
    def __removeItem__(self) -> None:
        # แสดงแจ้งเตือน
        self.notify("เพื่อออกจากการลบเมนู" , None)
        
        # function ลบสินค้า
        def deleteElements(param: str) -> None:
            findIndex = self.__search__(param) # หาสินค้าที่ต้องการลบส่งกลับเป็นเลข index
            if findIndex is None:
                self.console.print(f'[red]❌ ไม่พบ [bold]"{param}"[/] อยู่ในเมนูอาหาร[/]')
            else:
                self.__log__(typeOfLog=self.DEL , item=self.__menu__[findIndex]["name"]) # เก็บ log
                foodName = self.__menu__[findIndex]["name"] # เก็บรายชื่ออาหาร
                del self.__menu__[findIndex] # ลบสินค้า่โดยอ้างอิงเลข index
                self.__setElements__() # แก้ไข element ใน foodList และ idList เมื่อมีการลบสินค้าในเมนู
                self.console.print(f'[green bold]✓ ลบ [bold]"{foodName}"[/] ในรายการเมนูอาหารเสร็จสิ้น[/]')
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
                else:
                    # ลบอาหารแบบหลายๆอย่างโดยใส่ , 
                    # จะใช่เงื่อนไขนี้ได้เมื่อใส่ข้อมูลตรงตามนี้: a , b , c ,...
                    if ',' in item or ',' in [*item]: # ถ้าใส่ , ให้ทำเงิอนไขนี้
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
                        if self.console.input(f'[dark_orange]คุณแน่ใจว่าต้องการลบสินค้าเหล่านี้ออกจากรายการเมนูอาหารของร้านอาหาร (y/n) : [/]').lower().strip() == "y":        
                            for element in formatList:
                                deleteElements(element)
                        else:
                            print('คุณยกเลิกการลบ')
                    # เมื่อมีข้อมูลให้ลบออก
                    elif (item in self.__foodList__) or (item in self.__idList__): 
                        if self.console.input(f'[dark_orange]คุณแน่ใจว่าต้องการลบ [bold]"{item}"[/] ออกจากรายการเมนูอาหารของร้านอาหาร (y/n) : [/]').lower().strip() == "y":
                            deleteElements(item)
                        else:
                            print('คุณยกเลิกการลบ')  
                    elif item == "":
                        raise UserWarning(f"❌ คุณไม่ได้ใส่ชื่ออาหารหรือรหัสสินค้าโปรดใส่ก่อนที่จะทำการลบ")
                    else: 
                        raise UserWarning(f"❌ ไม่มี \"{item}\" อยู่ในเมนูอาหารโปรดกรอกชื่อหรือเลข id ใหม่")
            except UserWarning as err:
                self.console.print(f'[red]{err.__str__()}[/]')
            else:
                if self.__programStatus__["isDeleted"]:
                    self.console.print(f'🍖 จำนวนรายการในเมนูอาหารตอนนี้มีทั้งหมดอยู่ [yellow]{len(self.__menu__)}[/] เมนู')

    # ? (method หลัก) แก้ไขรายการสินค้า
    def __editItem__(self) -> None:
        # แสดงแจ้งเตือน
        self.notify("เพิ่อออกจาการแก้ไข" , None)
        # infinity loop จนกว่าจะพิมพ์คำสั่ง "e" หรือ "end" เพื่อออกจาก loop
        while self.__programStatus__["isInvokeMethods"]:
            try:
                self.__programStatus__["isError"] = False # set ค่าสถานะ
                # ถามข้อมูล
                item = input('ใส่ชื่ออาหารหรือรหัสสินค้าเพื่อทำการแก้ไข : ')
                item = item.lower().strip()
                # ออกจาการทำงานของ method
                if item == 'e' or item == 'end': 
                    self.__programStatus__["isInvokeMethods"] = False
                # แสดงรายการเมนู    
                elif item == 'm' or item == 'menu': 
                    self.showMenu()
                elif item == 'n':
                    self.notify("เพิ่อออกจาการแก้ไข" , None)
                else:
                    # หาเลข index ของเมนูอาหาร
                    findIndex = self.__search__(item)
                    idx = findIndex # เลข index
                    notEdit = 0
                    if idx == None: # ใส่ข้อมูลไม่ถูกต้อง
                        raise UserWarning(f'❌ "{item}" ไม่ค้นพบชื่ออาหารและรหัสสินค้าอยู่ในรายการสินค้าโปรดลองใหม่อีกครั้ง!')
                    else:
                        editItem = {
                            "name": None,
                            "price": None,
                            "id": None
                        }
    
                        while (not editItem["name"]) and (not editItem["price"]) and (not editItem["id"]):
                            # แสดงข้อความ
                            self.console.print(f'คุณเลือกรายการสินค้าที่จะแก้ไข คือ [orange1 bold]"{self.__menu__[idx]["name"]}"[/] ราคา [orange1 bold]{self.__menu__[idx]["price"]}[/] บาท รหัสสินค้าคือ [orange1 bold]{self.__menu__[idx]["id"]}[/]')
                            self.console.print(f'ถ้าไม่ต้องการแก้ไขชื่ออาหารให้ใช้เครื่องหมายลบ [yellow bold](-)[/]')
                            while not editItem["name"]:
                                try:
                                    # ชื่ออาหารที่จะแก้ไขใหม่
                                    changeFoodName = self.console.input(f'แก้ไขชื่อ จาก [orange1 bold]"{self.__menu__[idx]["name"]}"[/] เป็น --> ').strip()   
                                    #! ตรวจสอบความถูกต้อง
                                    assert changeFoodName not in self.__foodList__ # ชื่อห้ามซ้ำกับรายการอื่นๆ
                                    assert not(changeFoodName == '' or changeFoodName.__len__() == 0) # ไม่ใส่ชื่อ
                                    if changeFoodName.isdigit() or changeFoodName[0].isdigit():
                                        raise UserWarning('❌ ไม่สามารถตั้งชื่อขึ้นต้นด้วยตัวเลขได้หรือตั้งชื่อเป็นตัวเลขได้!')
                                    elif changeFoodName == '-':
                                        changeFoodName = self.__menu__[idx]["name"]
                                        notEdit += 1
                                except AssertionError:
                                    self.console.print('[red]❌ ชื่อที่คุณทำการแก้ไขนั้นเป็นชื่อซ้ำอยู่ในเมนูอาหารโปรดแก้ไขชื่อที่ไม่เหมือนกัน หรือ ห้ามใส่ชื่อว่างเปล่า![/]')
                                except UserWarning as err:
                                    self.console.print(f'[red]{err.__str__()}[/]')
                                else:
                                    editItem["name"] = changeFoodName
                            # แสดงข้อความ    
                            print('💬 ราคาสินค้าสามารถตั้งอยู่ในช่วงราคา 1 ถึง 1,000 บาท') 
                            self.console.print(f'ถ้าไม่ต้องการแก้ไขราคาอารให้ใช้เครื่องหมายลบ [yellow bold](-)[/]')
                            while not editItem["price"]:
                                try:
                                    # ราคาที่จะแก้ไขใหม่
                                    changePrice = self.console.input(f'แก้ไขราคา จาก [orange1 bold]{self.__menu__[idx]["price"]}[/] บาท เป็น --> ').strip()
                                    if changePrice == '-':
                                        changePrice = self.__menu__[idx]["price"]
                                        notEdit += 1
                                    else:
                                        changePrice = int(changePrice)
                                    #! ตรวจสอบความถูกต้อง
                                    # ยอดเงินต้องไม่เกิน 1000 บาท และ ต้องไม่ติดลบและไม่เป็นศูนย์
                                    if (changePrice > self.MAX or changePrice <= self.MIN) or (changePrice not in range(self.MIN , self.MAX)): 
                                        raise UserWarning('❌ ราคาสินค้าต้องตั้งอยู่ในราคาไม่เกิน 1,000 บาทเท่านั้น!')
                                except ValueError:
                                    self.console.print('[red]❌ ราคาสินค้าและรหัสสินค้าต้องตั้งเป็นตัวเลขจำนวนเต็มเท่านั้น![/]')
                                except UserWarning as err:
                                    self.console.print(f'[red]{err.__str__()}[/]')
                                else:
                                    editItem["price"] = changePrice
                            # แสดงข้อความ
                            self.console.print(f'💬 รหัสสินค้าต้องตั้งเป็นเลขจำนวนเต็มจำนวน {self.PRODUCTCODE_LENGTH} ตัว')
                            self.console.print(f'ถ้าคุณไม่ต้องการตั้งรหัสสินค้าเองให้ใส่เครื่องหมายสแลช [yellow bold](/)[/] หรือถ้าต้องการใช้รหัสสินค้าเดิมให้ใส่เครื่องหมายลบ [yellow bold](-)[/]')
                            while not editItem["id"]:
                                try:
                                    # เลข id ที่จะแก้ไข
                                    changeId = self.console.input(f'แก้ไขรหัสสินค้า จากรหัส [orange1 bold]"{self.__menu__[idx]["id"]}"[/] เป็น --> ').strip() 
                                    #! ตรวจสอบความถูกต้อง
                                    if changeId.__len__() != self.PRODUCTCODE_LENGTH and changeId != '-' and changeId != '/':
                                        raise UserWarning(f'❌ ต้องตั้งรหัสสินค้าในความยาวของ {self.PRODUCTCODE_LENGTH} เท่านั้น!')
                                    elif changeId == '-':
                                        changeId = self.__menu__[idx]["id"]
                                        notEdit += 1
                                    elif changeId == '/':
                                        changeId = self.createId(length=self.PRODUCTCODE_LENGTH)
                                except UserWarning as err:
                                    self.console.print(f'[red]{err.__str__()}[/]')
                                else:
                                    editItem["id"] = changeId
                        else:
                            #* แก้ไขข้อมูล dictionary ในเมนู
                            for key in editItem:
                                self.__menu__[idx][key] = editItem[key]
                            if notEdit == 3:
                                self.console.print('[indian_red1]ไม่มีการแก้ไขข้อมูลใดๆ[/]')
                                self.__log__(typeOfLog=self.GENERAL , text=f'{self.__user__["name"]} ไม่ได้มีการแก้ไขค่าข้อมูลใดๆในรายการเมนูอาหาร')
                            else:
                                self.console.print('[green]✓ แก้ไขรายการอาหารเสร็จสิ้น[/]') 
                                self.__log__(typeOfLog=self.EDIT , item=[self.__menu__[idx]["name"] , changeFoodName]) 
                            # เปลี่ยนแปลงค่า li ใหม่   
                            self.__setElements__()
            except UserWarning as err:
                self.console.print(f'[red]{err.__str__()}[/]')

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
มีค่าเฉลี่ยการสั่งซื้ออาหารอยู่ที่ {me:,}
อาหารที่สั่งบ่อยหรือสั่งเยอะที่สุดในวันนี้คือ {mo}"""
                
    #? method ในการแสดงข้อมูลการทำงานต่างๆของโปรแกรม 
    def __showLog__(self) -> None:
        self.console.rule(title='[yellow bold]บันทึกของโปรแกรม[/]')
        self.console.print(*self.__LOG__ , sep='\n')
        self.console.rule()

    #? method ในการลบเมนูสินค้า
    def __deleteMenu__(self) -> None:
        if input('คุณแน่ใจว่าต้องการลบสินค้าทั้งหมดถ้าต้องการให้พิมพ์ "y" แต่โปรดรู้ไว้ข้อมูลสินค้าจะถูกลบถาวรและไม่สามารถกู้คืนได้ (y/n): ').lower().strip() == "y":
            self.__log__(typeOfLog=self.DELALL)
            self.__menu__.clear()
            self.console.print('[green]✓ ลบรายการเมนูอาหารทั้งหมดเสร็จสิ้นเรียบร้อย[/]')
        else: self.console.print('[magenta]❗ คุณยกเลิกการดำเนินการลบสินค้าทั้งหมด[/]')

    #? method ออกจากโปรแกรม
    def __exitProgram__(self) -> None:
        #* ถ้ามีการสั่งอาหารให้แสดงรายการสรุปสินค้าที่ซื้อไปภายใน 1 วัน ถ้าไม่ได้สั่งซื้อไม่ต้องแสดง
        self.__allOrders__.__len__() != 0 and print(self.conclusion(total=self.__totalMoney__ , orders=self.__allOrders__))
        print('🙏 ขอบคุณที่มาใช้บริการของเรา')
        # ตั้งค่าสถานะให้เป็น False เพื่ออกจาก loop แล้วโปรแกรมจบการทำงาน
        self.__programStatus__["isWorking"] = False
        self.__programStatus__["programeIsRunning"] = False

    #? (method หลัก) ในการดำเนินการหลักของโปรแกรม
    def EXECUTE(self) -> None:
        # infinity loop จนกว่าจะพิมพ์คำสั่ง "e" หรือ "exit" เพื่อออกจาก loop
        while self.__programStatus__["programeIsRunning"]:
            self.__programStatus__["isWorking"] = True
            try:
                command = self.console.input("[medium_turquoise]พิมพ์คำสั่งเพื่อดำเนินการต่อไป >>> [/]")
                command = command.lower().strip()
                #! ตรวจสอบความถูกต้อง
                assert command != "" or len(command) == 0 # ถ้าไม่ได้พิมพ์คำสั่งอะไรมา
                # #? ค้นหาชื่อคำสั่ง
                if self.isKeyword(command):
                    # เปลี่ยนสถานะ attribute ตัวนี้ให้เป็น True หมายถึงกำลังทำการเรียกใช้ methods ของโปรแกรม
                    self.__programStatus__["isInvokeMethods"] = True
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
                    #* ซื้ออาหาร
                    elif command == "o" or command == "order":
                        #* ตรวจสอบสิทธิ์การเข้าถึง 
                        if self.__user__["AccessPermissions"]["SellFood"]:
                            self.__log__(typeOfLog=self.COMMAND , text="การสั่งซื้ออาหาร")
                            self.showMenu()
                            self.__foodOrdering__()
                        else: 
                            self.notAuthorizedToAccess(context="การสั่งซื้ออาหาร")
                    #* เพิ่มสินค้า
                    elif command == "a" or command == "add": 
                        #* ตรวจสอบสิทธิ์การเข้าถึง 
                        if self.__user__["AccessPermissions"]["AddData"]:
                            self.__log__(typeOfLog=self.COMMAND , text="การเพิ่มเมนูอาหาร")
                            self.__addItem__()
                        else: 
                            self.notAuthorizedToAccess(context="การเพิ่มเมนูอาหาร")
                    #* ลบสินค้า
                    elif command == "d" or command == "delete":
                        if self.__user__["AccessPermissions"]["DeleteData"]:
                            self.__log__(typeOfLog=self.COMMAND , text="การลบเมนูอาหาร")
                            self.showMenu()
                            self.__removeItem__()
                        else:
                            self.notAuthorizedToAccess(context="การลบเมนูอาหาร")
                    #* แก้ไขสินค้า
                    elif command == "ed" or command == "edit": 
                        if self.__user__["AccessPermissions"]["ModifyData"]:
                            self.__log__(typeOfLog=self.COMMAND , text="การแก้ไขเมนูอาหาร")
                            self.showMenu()
                            self.__editItem__()
                        else:
                            self.notAuthorizedToAccess(context="การแก้ไขเมนูอาหาร")
                    #* ลบรายการสินค้าทั้งหมด
                    elif command == "cl" or command == "clear":
                        if self.__user__["AccessPermissions"]["DeleteAllData"]:
                            self.__log__(typeOfLog=self.COMMAND , text="การลบรายการเมนูอาหารทั้งหมด")
                            self.__deleteMenu__()
                        else:
                            self.notAuthorizedToAccess(context="การลบรายการเมนูอาหารทั้งหมด")
                    #* แสดงกิจกรรมการทำงานต่างๆของโปรแกรม
                    elif command == "l" or command == "log":
                        if self.__user__["AccessPermissions"]["ViewLog"]:
                            self.__showLog__()
                        else:
                            self.notAuthorizedToAccess(context="การดู log ของโปรแกรม")
                    #* ออกจากบัญชี
                    elif command == "out" or command == "logout":
                        # ต้องเปิดใช้งานระบบ login (True) ถึงจะ logout ได้
                        if self.__logout__(callBackFunction=self.__log__): # method logout จะส่งค่าสถานะมาถ้า True เงื่อนไขนี้จะทำงาน
                            self.__programStatus__["isWorking"] = False
                            # ให้ login ใหม่
                            user = self.__getUser__(callBackFunction=self.__log__) # รอรับข้อมูลผู้ใช้งาน
                            self.__setUser__(user) # ตั้งค่าผู้ใช้งาน
                            self.__setPermissions__(user) # ตั้งค่าสิทธิ์
                            self.showLogo(path='./img/logo.png') # แสดง logo ร้านอาหาร
                            self.greeting(h=self.time.hour) # ทักทายผู้ใช้งาน
                            self.showCommands() # แสดงคำสั่ง
                #* ไม่มีคำสั่งที่ค้นหา
                else: 
                    raise UserWarning(f'[bold underline red on grey0]Error:[/][red] ไม่รู้จำคำสั่ง [bold]"{command}"[/] โปรดเลือกใช้คำสั่งที่มีระบุไว้[/]')
            except UserWarning as err:
                self.console.print(err.__str__())
            except AssertionError:
                self.console.print("[bold underline red on grey0]Error:[/][red] คุณไม่ได้ป้อนคำสั่งโปรดพิมพ์คำสั่ง[/]")
            finally:
                self.__programStatus__["isWorking"] and print('โปรดเลือกพิมพ์คำสั่ง')

# สร้าง instance(object) เพื่อนำไปใช้งาน
program = Program(menu=Menu().getMenu()[:20])
program.EXECUTE() # เรียกใช้ method จาก object เพื่อดำเนินการทำงาน