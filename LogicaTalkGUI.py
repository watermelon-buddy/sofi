from customtkinter import *
import socket
import threading
#from PIL import Image
SERVER_NAME ='localhost'
PORT = 8080
class ChatClient(CTk):
    def __init__(self):

        super().__init__()
        self.nickname = "Unknown"
        self.title("LOGIKA TALK")
        self.geometry("500x500")
        #img = CTkImage(light_image=Image.open("D:\\LOGICA\\сб10.00\\LogikaTalk\\pic2.jpg"),size=(500,500))
        #self.image_lb =CTkLabel(self,text="",image=img)
        #self.image_lb.pack()
        self.configure(fg_color="lightyellow")
        self.configure(bg_color="maroon")
        
        self.sock =None
        self.running=None
        self.recv_thread=None
        self.nicknameframe = CTkFrame(self)
        self.nicknameframe.configure(fg_color="ivory")
        self.nicknameframe.pack(pady=50)
        self.nickname_lb = CTkLabel(
            self.nicknameframe,
            text="Введіть ваш нік нейм:",
            text_color="black"
            #fg_color="maroon",
            #bg_color="black",
            #corner_radius=40,
            #border_width=2
        )
        self.nickname_lb.pack(pady=10, padx=10)
        self.nickname_entry = CTkEntry(
            self.nicknameframe,
            width=300,
            height=50,
            placeholder_text="Введіть нік тут",
            #border_color="blue",
        )
        self.nickname_entry.pack(pady=10, padx=10)

        self.chat_frame = CTkFrame(self,width=500,height=500)
        self.chat_box = CTkTextbox(
            self.chat_frame, width=460, height=300, state="disabled"
        )
        #self.chat_box.configure(text_color="blue",fg_color="red",border_color="white",corner_radius=100)
        self.chat_box.place(y=20, x=20)
        self.chat_entry = CTkEntry(
            self.chat_frame,
            width=320,
            height=40,
            placeholder_text="Введіть повідомлення",
            #border_color="white",
        )
        self.chat_entry.place(x=20, y=330)

        self.connect_btn = CTkButton(
            self.nicknameframe,
            text="Увійти у чат",
            width=140,
            height=50,
            command=self.start_chat,
        )
        self.connect_btn.pack(pady=10, padx=10)
        self.chat_frame.pack_forget()

        self.send_bth = CTkButton(
            self.chat_frame,
            text="Відправити",
            width=120,
            height=50,
            command=self.sent_message,
        )
        self.send_bth.place(x=350, y=330)
    def switch_mode(self):
         self.send_bth.configure(fg_color="red")

    def start_chat(self):
        self.nickname = self.nickname_entry.get().strip()
        self.nickname = self.nickname if self.nickname else "Unknown"
        self.nicknameframe.pack_forget()
        self.chat_frame.place(x=0, y=0)
        self.append_local("[SYSTEM] Спроба підкючення")
        threading.Thread(target=self.connent_to_server).start()
    def connent_to_server(self):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((SERVER_NAME,PORT))
            self.client =client
            self.running = True
            self.append_local(f"[SYSTEM] Підключено до {SERVER_NAME}:{PORT}")
            text = f"{self.nickname}"
            self.client.send(text.encode())
            self.recv_thread=threading.Thread(target=self.recv_loop)
            self.recv_thread.start()
        except Exception as a: 
            self.append_local(f"[SYSTEM] [ERROR] {a}")
    def append_local(self,text):
        self.chat_box.configure(state='normal')
        self.chat_box.insert(END,self.nickname+" : "+text+"\n")
        self.chat_box.see(END)
        self.chat_box.configure(state='disabled')
    def sent_message(self):
        text = self.chat_entry.get().strip()
        if not text:
            return
        self.append_local(text)
        self.client.send(f"{text}\n".encode())
        self.chat_entry.delete(0,END)
    def recv_loop(self):
        buffer =''
        try:
            while self.running:
                text =self.client.recv(4096).decode()
                if not text:
                    break
                buffer+=text
                while "\n" in buffer:
                    line,buffer =buffer.split("\n",1)
                    self.handle_line(line.strip())
        except Exception as e:
            self.append_local(f"[SYSTEM] [ERROR] {e}")
        finally:
            try: 
                self.client.close()
            except:
                pass
            self.append_local(f"[SYSTEM] Відєднано від серверу")
    def handle_line(self,line):
        if not line:
            return
        parts = line.split("@",2)
        if len(parts)>=3 and parts[0] =="TEXT":
            a = parts[1]
            msg=parts[2]
            self.after(0,self.append_local(f'{a}: {msg}'))
        else:
            self.after(0,self.append_local(f'{line}'))

    
window = ChatClient()

window.mainloop()
