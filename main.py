from Louvain import *
from Walktrap import *
from Visualization import *
import tkinter as tk
import tkinter.messagebox
from PIL import Image, ImageTk

d = 4038
update = False


class Info(object):
    def __init__(self, max_i):
        self.method = None
        self.id = 'a'
        self.max_id = max_i
        self.degree = 0
        self.center = 0
        self.depth = 0

    def set_method(self, m):
        self.method = m

    def set_id(self, i):
        self.id = i

    def set_degree(self, d1, c, d2):
        self.degree = d1
        self.center = c
        self.depth = d2

    def check_error(self):
        if self.method is None:
            return 1
        elif self.id == '':
            return 2
        elif not self.id.isdigit() or int(self.id) != float(self.id) or int(self.id) < 0 or int(self.id) > self.max_id:
            return 3
        else:
            return 4


def error_handling(err):
    if err == 1:
        tkinter.messagebox.showwarning(title='Warning', message='Select an algorithm!')
    elif err == 2:
        tkinter.messagebox.showwarning(title='Warning', message='Input user id!')
    elif err == 3:
        tkinter.messagebox.showerror(title='Error', message='Invalid user id!')


if __name__ == '__main__':
    info = Info(d)
    window = tk.Tk()
    window.title('Community detection')
    window.geometry('700x680')

    var = tk.StringVar()


    def method_selection():
        info.set_method(var.get())


    def button_click1():
        info.set_id(e.get())
        error_handling(info.check_error())
        if info.check_error() == 4:
            label, edges, center = louvain(int(info.id))
            aim_cluster = label[int(info.id)][1]
            aim_community = []
            aim_edges = []
            for i in range(len(label)):
                if label[i][1] == aim_cluster:
                    aim_community.append(label[i][0])
            for i in range(len(edges)):
                if edges[i][0] in aim_community and edges[i][0] in aim_community:
                    aim_edges.append(edges[i])
            distance, degree = show_img(aim_edges, len(label), center, int(info.id))
            info.set_degree(degree, center, distance)
            tk.messagebox.showinfo(title='Notice', message='Click "Update Information" for the next step')

    def update_canvas():
        global n_img
        n_img = ImageTk.PhotoImage(Image.open('tmp.png'))
        canvas.itemconfigure(img_canvas, image=n_img)
        l3.configure(text='Id of center point is ' + str(info.center))
        l4.configure(text='It\'s neighbor take part of ' + str(round(info.degree)) + '% of the vertices, Maximum depth is '+ str(info.depth))

    img = ImageTk.PhotoImage(Image.open('tmp.png'))
    canvas = tk.Canvas(window, width=640, height=480, bg='white')
    canvas.pack(pady=5)
    img_canvas = canvas.create_image(0, 0, image=img, anchor='nw')

    fml1 = tk.Frame(window)
    fml1.pack()
    l1 = tk.Label(fml1, text='Select Algorithm', font=('Arial', 10), width=15, height=1).pack(side='left', padx=10, pady=3)
    r1 = tk.Radiobutton(fml1, text='Louvain', variable=var, value='Louvain', command=method_selection).pack(side='left', padx=10, pady=3)
    r2 = tk.Radiobutton(fml1, text='Walktrap', variable=var, value='Walktrap', command=method_selection).pack(side='left', padx=10, pady=3)

    fml2 = tk.Frame(window)
    fml2.pack()
    l2 = tk.Label(fml2, text='Input user id', font=('Arial', 10), width=15, height=1).pack(side='left', padx=10, pady=3)
    e = tk.Entry(fml2, show=None, width=10)
    e.pack(side='left', padx=10, pady=3)

    fml3 = tk.Frame(window)
    fml3.pack()
    b1 = tk.Button(fml3, text="Run Algorithm", width=15, height=1, command=button_click1).pack(side='left', padx=10, pady=3)
    b2 = tk.Button(fml3, text="Update Information", width=15, height=1, command=update_canvas).pack(side='left', padx=10, pady=3)

    fml4 = tk.Frame(window)
    fml4.pack(pady=10)
    l3 = tk.Label(fml4, text='Id of center point is ' + str(info.center), font=('Arial', 10), height=1)
    l3.pack(side='top')

    l4 = tk.Label(fml4, text='It\'s neighbor take part of ' + str(round(info.degree)) + '% of the vertices, Maximum depth is '+ str(info.depth), font=('Arial', 10), height=1)
    l4.pack(side='top')

    window.mainloop()
