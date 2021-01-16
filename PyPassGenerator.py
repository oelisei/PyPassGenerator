import tkinter as tk
import secrets, string
from os import path
from math import log2 

class FunctionBlockset:
    # Generic function to determine whether a character is a punctuation mark
    def ispunct(self, ch):
        return ch in string.punctuation

class MainApplication(tk.Frame):     
    # Generate random password and calculate its entropy
    def handleGenerate(self):
        length = int(self.input.get())
        
        password_characters = string.digits
        pool = len(string.digits)
        if(self.opLet.get() == 1):
            password_characters += string.ascii_letters
            pool += len(string.ascii_letters)
        if(self.opSym.get() == 1):
            password_characters += string.punctuation
            pool += len(string.punctuation)

        # Calculate password entropy
        entropy = log2(pool ** int(length))

        if entropy < 28:
            self.label5.configure(text="Very Weak", fg="red")
        elif entropy < 36:
            self.label5.configure(text="Weak", fg="orange")
        elif entropy < 60:
            self.label5.configure(text="Reasonable", fg="dark goldenrod")
        elif entropy < 128:
            self.label5.configure(text="Strong", fg="green")
        else:
            self.label5.configure(text="Very Strong", fg="blue")
        
        password = []
        # Password with numbers, letters and symbols
        if(self.opLet.get() == 1 and self.opSym.get() == 1):
            while True:
                password = ''.join(secrets.choice(password_characters) for i in range(length))
                if (any(c.isdigit() for c in password)
                    and any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and any(self.func.ispunct(c) for c in password)):
                        break
        # Password with numbers and letters
        elif(self.opLet.get() == 1 and self.opSym.get() == 0):
            while True:
                password = ''.join(secrets.choice(password_characters) for i in range(length))
                if (any(c.isdigit() for c in password)
                    and any(c.islower() for c in password)
                    and any(c.isupper() for c in password)):
                        break
         # Password with numbers and symbols
        elif(self.opLet.get() == 0 and self.opSym.get() == 1):
            while True:
                password = ''.join(secrets.choice(password_characters) for i in range(length))
                if (any(c.isdigit() for c in password)
                    and any(self.func.ispunct(c) for c in password)):
                        break
        # Password with numbers only
        else:
            password = ''.join(secrets.choice(password_characters) for i in range(length))              

        self.output1.delete(0, tk.END)
        self.output1.insert(0, password)
        self.output2.configure(state='normal')
        self.output2.delete(0, tk.END)
        self.output2.insert(0, (str(round(entropy)) + ' bits'))
        self.output2.configure(state='readonly')

    # Copy password to clipboard
    def handleCopy(self):
        root.clipboard_clear()
        root.clipboard_append(self.output1.get())

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.func = FunctionBlockset()

        # Labels
        label1 = tk.Label(root, text="Secure Random Password Generator", borderwidth=3, bg='dark blue', fg='white')
        label1.place(x=10, y=10, height=20, width=240)

        label2 = tk.Label(root, text="Password Length:")
        label2.place(x=10, y=40, height=20)

        label3 = tk.Label(root, text="Entropy:")
        label3.place(x=10, y=160, height=20)

        label4 = tk.Label(root, text="Strength:")
        label4.place(x=130, y=160, height=20)
        
        self.label5 = tk.Label(root, text="")
        self.label5.place(x=185, y=160, height=20)

        # Inputs/Outputs
        self.input = tk.Spinbox(root, from_=4, to=2048, textvariable=tk.DoubleVar(value=16))  
        self.input.place(x=120, y=40, height=20, width=60)

        self.output1 = tk.Entry(root)
        self.output1.place(x=10, y=130, height=20, width=240)

        self.output2 = tk.Entry(root, state='readonly')
        self.output2.place(x=60, y=160, height=20, width=60)

        # Checkboxes
        self.opNum = tk.IntVar(value=1)
        checkBox1 = tk.Checkbutton(root, text="Numbers", variable=self.opNum, state='disabled') 
        checkBox1.place(x=10, y=60)
        self.opLet = tk.IntVar(value=1)
        checkBox2 = tk.Checkbutton(root, text="Letters", variable=self.opLet, onvalue=1, offvalue=0)
        checkBox2.place(x=90, y=60)
        self.opSym = tk.IntVar(value=1)
        checkBox3 = tk.Checkbutton(root, text="Symbols", variable=self.opSym, onvalue=1, offvalue=0)
        checkBox3.place(x=160, y=60)
        
        # Buttons
        button1 = tk.Button(text='Generate',command=self.handleGenerate, bg='dark blue',fg='white')
        button1.place(x=10, y=100, height=20, width=120)

        button2 = tk.Button(text='Copy to Clipboard',command=self.handleCopy, bg='dark blue',fg='white')
        button2.place(x=10, y=190, height=20, width=120)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("260x230")
    root.resizable(width=False, height=False)
    root.title("PyPassGenerator")

    myPath = path.dirname(path.abspath(__file__))
    try:
        root.iconbitmap(myPath + '/icons/lock.ico')
    except:
        pass
    MainApplication(root)  
    root.mainloop()