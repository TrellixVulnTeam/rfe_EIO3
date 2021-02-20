import manageSSH  # the file with funcs that connect to the ssh
import LoginRegister
# import manageSERVER
import tkinter
from tkinter import ttk
import socket
import os
from PIL import ImageTk, Image
import tkinter.messagebox
from tkinter import simpledialog  # opens the popup for the new folder name input
import pyperclip  # copy to clipboard module
import re
import wx  # get screen resolution
# import win32api  # a module that shows the drives that are connected to the PC

# global cur_path, ROOT_PROJ_DIR, bttns_dict, icons_dict

system_drive = os.getenv("SystemDrive")


# from fontTools.ttLib import TTFont
# font = TTFont('ERASBD.TTF')
# font.save(rf'{system_drive}\Users\{username}\AppData\Local\Microsoft\Windows\Fonts')#\ERASBD.TTF')
# print(rf'{system_drive}\Users\{username}\AppData\Local\Microsoft\Windows\Fonts')
# print(rf'{system_drive}\Windows\Fonts')
# font.save(rf'{system_drive}\Windows\Fonts')
# print(os.path.expanduser('~') + '\Desktop\Fonts\ERASBD.TTF')
# font.save(os.path.expanduser('~') + '\Desktop\Fonts\ERASBD.TTF', reorderTables=True)

# from PIL import ImageFont
# font = ImageFont.load('ERASBD.TTF')


MENU_BAR_HEIGHT = 20

app = wx.App(False)
screen_width, screen_height = wx.GetDisplaySize()
# screen_width = 1000  # temp
# screen_height = 700  # temp
# screen_width = 1280  # temp
# screen_height = 720  # temp

if screen_width / screen_height != (1920 / 1080):
    screen_height = screen_width / (1920 / 1080)

if screen_width >= 1070 and screen_height >= 700:
    screen_width = 1920
    screen_height = 1080

app_width = int(screen_width / 1.794)
app_height = int(screen_height / 1.542)# + MENU_BAR_HEIGHT
print(screen_width, screen_height, app_width, app_height)  # temp

bttns_dict = dict()
icons_dict = dict()

ROOT_PROJ_DIR = os.path.dirname(os.path.abspath(__file__))

# cur_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
# cur_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\apple')
# cur_path = r'C:\Users\yaniv\Desktop\כיתה יב\10 יחידות מחשבים\cyber project'
# cur_path = r'D:\Program Files\obs-studio\screen records'
# cur_path = r'C:\Users\yaniv\Desktop\Remote File Explorer'
cur_path = 'C:\\'

# MAYBE DELETE
# def resize(event):
#     global app_width, app_height
#     if event.width > screen_width:
#         app_width = screen_width
#     if event.height > screen_height:
#         app_height = screen_height
#     # root.geometry(f'{app_width}x{app_height}+{x}+{y}')
#     print("New size is: {}x{}".format(event.width, event.height))


def calc_width(size):
    if size == 0:
        return 0
    else:
        return int(app_width / (1070 / size))


def calc_height(size):
    if size == 0:
        return 0
    else:
        return int(app_height / (700 / size))


def get_icons_dict():
    icons_list = os.listdir(f'{ROOT_PROJ_DIR}\\icons')  # change to get from the server instead of local
    for icon in icons_list:
        icons_dict[icon] = ImageTk.PhotoImage(Image.open(f'{ROOT_PROJ_DIR}\\icons\\{icon}'))#.resize((61, 50),Image.ANTIALIAS))
    return icons_dict

# def sort_files_list(items_list):
#     i = 0
#     # items_list.sort() # not sorted when going back
#     for item in items_list:
#         if os.path.isdir(item):
#             items_list.insert(i, items_list.pop(items_list.index(item)))
#             i += 1
#     return items_list


def create_bttn(frame):
    global icons_dict, bttns_dict, sftp
    clm = 0
    rw = 2
    # os.chdir(r'D:\PycharmProjects\School\Remote File Explorer\GUI\files icons')

    dirs_list, files_list = manageSSH.get_dirs_files_lists(sftp, cur_path)
    items_list = dirs_list + files_list
    for item in items_list:
        btn_text = item
        if item in dirs_list:
            file_type = '.dir_folder'  # .png'
            if len(item) > 30:
                btn_text = item[0:30] + '...'
        elif item in files_list:
            # if 'item' is a file
            end_index = item.rfind('.')
            file_type = item[end_index:].lower()# + '.png'

            if len(item) > 30:
                btn_text = item[0:30] + '...' + file_type
        else:
            file_type = '.none'


        # img = imgs_dict[file_ending]
        # photo = ImageTk.PhotoImage(Image.open(r'D:\PycharmProjects\School\Remote File Explorer\GUI\files icons\.dir_folder.png').resize((61, 50), Image.ANTIALIAS))
        # photo.resize((61, 50), Image.ANTIALIAS))

        # photo = icons_dict['.dir_folder.png'] # worked

        try:
            icon = icons_dict[file_type + '.png']
        except KeyError:
            icon = icons_dict['.none.png']
        bttns_dict[f'{item}_btn_{items_list.index(item)}'] = tkinter.Button(frame, bg="gray", wraplength=100, text=btn_text, compound=tkinter.TOP, justify=tkinter.CENTER, image=icon, height=120, width=120)
        bttns_dict[f'{item}_btn_{items_list.index(item)}'].grid(column=clm, row=rw, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W, padx=9, pady=9)
        # bttns_dict[f'{item}_btn_{items_list.index(item)}'].bind("<Button-1>", left_click)
        bttns_dict[f'{item}_btn_{items_list.index(item)}'].bind("<Button-2>", right_click)
        bttns_dict[f'{item}_btn_{items_list.index(item)}'].bind("<Button-3>", right_click)
        bttns_dict[f'{item}_btn_{items_list.index(item)}'].bind('<Double-Button-1>', double_click)
        clm += 1
        if clm == 7:
            clm = 0
            rw += 1

        # for i in range(len(items_list) - 1):
        #     # for item in items_list:
        #     end_index = items_list[i].rfind('.')
        #     file_ending = items_list[i][end_index:]
        #     # button = tkinter.Label(root, background="gray", text=items_list[i])
        #     button = tkinter.Label(frame, background="gray", text=items_list[i])
        #     button.grid(column=clm, row=rw, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W, padx=10, pady=10)
        #     button.bind("<Button-1>", left_click)
        #     button.bind("<Button-2>", right_click)
        #     button.bind("<Button-3>", right_click)
        #     clm += 1
        #     if clm == 8:
        #         clm = 0
        #         rw += 1
        #     i += 1


def double_click(event):
    event.widget.configure(bg="light blue")  # DEL
    global items_list, cur_path, frame, bttns_dict

    key_list = list(bttns_dict.keys())
    val_list = list(bttns_dict.values())
    item_name = key_list[val_list.index(event.widget)]
    item_name = item_name[0:item_name.find('_btn_')]
    temp = cur_path + '\\' + item_name
    print(temp)
    item_type = manageSSH.check_if_item_is_dir(sftp, cur_path, item_name)
    if item_type == 'dir':
        cur_path = temp
        manageSSH.chdir(sftp, cur_path)
        items_list = sftp.listdir()
        update_frame(items_list)
    elif item_type == 'file':
        # not working - only png works
        manageSSH.run_action(ssh, f'"{temp}"')
        # pass

    elif item_type == 'item not found':
        print(f'{item_name} - not found')
    else:
        pass

# def left_click(event):
#     # DELETE THIS FUNC - NO NEED
#     event.widget.configure(bg="green")


def right_click(event):
    event.widget.configure(bg="blue")


def DELE():
    # DELETE THIS FUNC AND BUTTON
    manageSSH.disconnect_ssh(ssh)
    root.destroy()

# def up_button():
#     # global items_list, cur_path, frame
#     cur_path = os.path.dirname(os.getcwd())
#     root.title(cur_path)
#     if os.path.isdir(cur_path):
#         os.chdir(cur_path)
#         manageSSH.chdir(sftp, cur_path)
#         # items_list = sftp.listdir()
#         items_list = os.listdir(cur_path)
#         update_frame(items_list)


def up_button():
    global cur_path
    manageSSH.chdir(sftp, '..')
    cur_path = sftp.getcwd()[1:].replace('/', '\\')
    while cur_path.endswith('\\'):
        cur_path = cur_path[:len(cur_path) - 1]
    print(f'up:{cur_path}')
    items_list = sftp.listdir()
    update_frame(items_list)
    # manageSSH.run_action(ssh, r'cd..')
    # cur_path = sftp.getcwd()

    # if len(cur_path) <= 3:
    #     pass
    # else:
    #     cur_path = cur_path[:cur_path.rfind('\\')]
    #     root.title(cur_path)  # TEMP
    #     # if os.path.isdir(cur_path):
    #     #     os.chdir(cur_path)
    #     manageSSH.chdir(sftp, cur_path)
    #     items_list = sftp.listdir()
    #     update_frame(items_list)


def forward_button():
    # wrapper2.update() # not working - maybe wont use update()
    # save the current folder when back is pressed then go back to that folder when forward is clicked
    # new_button = tkinter.Button(frame, bg="gray", wraplength=100, compound=tkinter.TOP, justify=tkinter.CENTER, height=100, width=100)
    new_button = tkinter.Button(frame, bg="gray", height=100, width=100)
    new_button.grid(column=5, row=3)#, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W, padx=10, pady=10)
    # entry_in_button = tkinter.Entry(new_button)#, text='New folder')
    # entry_in_button.insert(tkinter.END, 'New folder')
    # entry_in_button.pack()


def refresh_button():
    print(cur_path) # temp - DEL later
    # sftp.chdir(cur_path)
    manageSSH.chdir(sftp, cur_path)
    items_list = sftp.listdir()
    # items_list = os.listdir(cur_path)
    update_frame(items_list)


def drives_box_change(event):
    global cur_path
    selected_drive = event.widget.get()
    print(selected_drive)
    cur_path = selected_drive
    manageSSH.chdir(sftp, cur_path)
    items_list = sftp.listdir()
    update_frame(items_list)


def close_window():
    discon_msg_box = tkinter.messagebox.askquestion(title='Disconnect & Close', message='Are you sure you want to close the window and disconnect?')
    if discon_msg_box == 'yes':
        manageSSH.disconnect_ssh(ssh)
        root.destroy()  # add disconnecting form the machine (SSH)


def copy_path_button(event):
    # import time
    pyperclip.copy(cur_path)

    # doesnt work
    # event.widget.configure(text='Copied!')
    # time.sleep(1)
    # event.widget.configure(text='Copy Path2')


import warnings
def new_dir_button():
    warnings.filterwarnings("ignore")
    # Get the name of the folder with entry
    manageSSH.chdir(sftp, cur_path)
    items_list = sftp.listdir()
    lower_items_list = list()
    for item in items_list:
        lower_items_list.append(item.lower())

    invalid_names_list = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']

    new_folder_name = simpledialog.askstring('New folder', 'Enter a name for the folder:')
    while True:
        # new_folder_name = simpledialog.askstring('input string', 'please enter your name')
        if new_folder_name == None or new_folder_name == '':
            break

        elif new_folder_name.lower() in lower_items_list:
            new_folder_name = simpledialog.askstring('New folder', 'This name is already taken, Try again:')

        elif new_folder_name in invalid_names_list or new_folder_name.__contains__('..'):
            new_folder_name = simpledialog.askstring('New folder', 'This name is invalid, Try again:')

        elif not re.match(r"^[^\\/:*?\"<>|]+$", new_folder_name):
            new_folder_name = simpledialog.askstring('New folder', """The name can't contain: \/:*?"<>| Try again:""")

        elif new_folder_name.endswith('.') or new_folder_name.endswith(' '):
            new_folder_name = new_folder_name[:-1]
            sftp.mkdir(new_folder_name)
            print(new_folder_name)  #####
            items_list = sftp.listdir()
            update_frame(items_list)
        else:
            sftp.mkdir(new_folder_name)
            print(new_folder_name)  #####
            items_list = sftp.listdir()
            update_frame(items_list)


def update_frame(items_list):
    # global back_img, forw_img, ref_img
    # items_list = sort_files_list(items_list)
    wrapper1.destroy()
    wrapper2.destroy()
    frame.destroy()
    create_frame(items_list)#back_img, forw_img, ref_img)
    create_bttn(frame)

def create_frame(items_list):#back_img, forw_img, ref_img):
    global frame, wrapper1, wrapper2, count, drives_list

    def f_refresh(event):
        refresh_button()
    root.bind('<F5>', f_refresh)

    count = 0
    def mouse_wheel(event):
        global count
        if len(items_list) > 21:
            if event.num == 5 or event.delta == -120:
                count -= 1
            if event.num == 4 or event.delta == 120:
                count += 1
            mycanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            pass

    wrapper1 = tkinter.LabelFrame(root, height=10, bg='yellow')
    wrapper2 = tkinter.LabelFrame(root)

    mycanvas = tkinter.Canvas(wrapper2)
    mycanvas.pack(side=tkinter.LEFT, fill='both', expand='yes')

    yscrollbar = ttk.Scrollbar(wrapper2, orient='vertical', command=mycanvas.yview)
    yscrollbar.pack(side=tkinter.RIGHT, fill='y')

    yscrollbar.config(command=mycanvas.yview)

    mycanvas.configure(yscrollcommand=yscrollbar.set)

    mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))
    mycanvas.bind_all("<MouseWheel>", mouse_wheel)

    frame = tkinter.Frame(mycanvas)
    mycanvas.create_window((0, 0), window=frame, anchor='nw')

    wrapper1.pack(fill='both', expand='no', padx=10, pady=10)
    wrapper2.pack(fill='both', expand='yes', padx=10, pady=10)

    # good
    tkinter.Grid.columnconfigure(wrapper1, 0, weight=1)
    tkinter.Grid.rowconfigure(wrapper1, 0, weight=1)
    # good

    menu_window = wrapper1 # f1

    cur_path_label = tkinter.Label(menu_window, text=cur_path, wraplength=450)
    cur_path_label.grid(column=3, row=0, sticky=tkinter.W + tkinter.E)

    copy_btn = tkinter.Button(menu_window, text='Copy Path')
    copy_btn.bind("<Button-1>", copy_path_button)
    copy_btn.grid(column=4, row=0, sticky=tkinter.W)# + tkinter.E)

    up_btn = tkinter.Button(menu_window, image=icons_dict['up.png'], command=up_button)
    up_btn.grid(column=0, row=1)

    answr = str(manageSSH.run_action(ssh, 'wmic logicaldisk get caption').read())
    drives_list = answr[answr.find('Caption') + 9:answr.rfind(r'       \r\r\n\r\r\n')].split(r'       \r\r\n')
    drives_list[0] = drives_list[0].replace(r'\r\r\n', '')
    for i in range(len(drives_list)):
        drives_list[i] += '\\'
    drivers_combobox = ttk.Combobox(menu_window, values=drives_list, state='readonly')
    default_value = cur_path[0:3]
    try:
        drivers_combobox.current(drives_list.index(default_value))
    except ValueError:
        default_value = cur_path[0:2] + '\\'
        drivers_combobox.current(drives_list.index(default_value))
    drivers_combobox.current(drives_list.index(default_value))
    drivers_combobox.bind("<<ComboboxSelected>>", drives_box_change)
    drivers_combobox.grid(column=2, row=1)

    new_dir_btn = tkinter.Button(menu_window, text='New folder', compound=tkinter.TOP, justify=tkinter.CENTER, image=icons_dict['new_dir.png'], command=new_dir_button)
    new_dir_btn.grid(column=3, row=1)

    ref_btn = tkinter.Button(menu_window, image=icons_dict['refresh.png'], command=refresh_button)
    ref_btn.grid(column=4, row=1)

    def search():
        tree_items_list = manageSSH.tree_items(sftp, cur_path)
        search_key = search_bar_entry.get()
        for item in tree_items_list:
            if search_key.contains(item[item.rfind('\\'):]):
                items_list.append(item)
        update_frame(items_list)

    def entry_click(event):
        search_bar_entry.delete(0, 'end')
        search_bar_entry.bind('<FocusOut>', entry_lost)

    def entry_lost(event):
        search_bar_entry.insert(0, 'Search')
        search_bar_entry.bind('<FocusIn>', entry_click)

    search_bar_entry = tkinter.Entry(menu_window, text='Search', font=(calc_width(20)))
    search_bar_entry.delete(0, 'end')
    search_bar_entry.insert(0, 'Search')
    search_bar_entry.bind('<FocusIn>', entry_click)
    search_bar_entry.grid(column=5, row=1, sticky=tkinter.E)
    search_btn = tkinter.Button(menu_window, text='GO', command=search)
    search_btn.grid(column=6, row=1, sticky=tkinter.E)

    # ds_btn = tkinter.Button(menu_window, text='Disconnect', command=dscon_bttn)
    # ds_btn.grid(column=5, row=1, sticky=tkinter.E, padx=50, columnspan=4)

    # DEL
    # DEL = tkinter.Button(menu_window, text='DELETE', command=DELE)
    # DEL.grid(column=6, row=1, sticky=tkinter.E, padx=25, columnspan=5)
    # DEL

    for x in range(10):
        tkinter.Grid.columnconfigure(frame, x, weight=1)

    for y in range(5):
        tkinter.Grid.rowconfigure(frame, y, weight=1)

    for x in range(10):
        tkinter.Grid.columnconfigure(wrapper1, x, weight=1)

def main():
    global cur_path, root, frame, ssh, sftp

    print(screen_width, screen_height, app_width, app_height)  # temp

    SELF_NAME = os.getlogin()
    SELF_IP = socket.gethostbyname(socket.gethostname())


    root = tkinter.Tk()
    x = int((screen_width - app_width) / 2)
    y = int((screen_height - app_height) / 2)
    print(f'x={x}, y={y}')
    root.geometry(f'{app_width}x{app_height}+{x}+{y}')# + MENU_BAR_HEIGHT}+{x}+{y}')
    root.iconbitmap('icon.ico')
    menubar = tkinter.Menu(root)
    account = tkinter.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Account', menu=account)
    pc_info = tkinter.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='PC info', menu=pc_info)
    pc_info.add_command(label='Click to copy:', command=None, state='disabled', activebackground='grey90')
    pc_info.add_separator()
    def copy_ip():
        pyperclip.copy(SELF_IP)
    def copy_name():
        pyperclip.copy(SELF_NAME)
    pc_info.add_command(label=f'IP: {SELF_IP}', command=copy_ip, activebackground='steelblue2', activeforeground='black')
    pc_info.add_command(label=f'Userame: {SELF_NAME}', command=copy_name, activebackground='steelblue2', activeforeground='black')
    root.config(menu=menubar)
    root.resizable(False, False)

    # root.bind("<Configure>", resize)

    email, mode, ssh, sftp, username = LoginRegister.main(root, app_width, app_height, account)
    print('main_window.py')
    print(email)  # DELETE
    print(mode)
    print(ssh)
    print(sftp)
    if email != None and mode != 'control' and ssh != None and sftp != None:  # (ADD) and chosen_ip != None:
        global cur_path
        # end_video_name = 'end-animation.mp4'
        # LoginRegister.play_video(end_video_name)
        root.protocol("WM_DELETE_WINDOW", close_window)
        root.geometry(f'{app_width}x{app_height}+{x}+{y}')
        # root.minsize(width=1070, height=700)

        # root.resizable(False, False)

        root.title('Remote File Explorer')
        # root.iconbitmap('icon.ico')

        # host = "192.168.56.1"
        # username = "yaniv-pc\yaniv"
        # # password = input('Enter your password: ')  # DELETE
        # ssh = manageSSH.connect_to_ssh(host, username, password)
        # sftp = ssh.open_sftp()

        # system_drive = os.getenv("SystemDrive")

        cur_path = rf'{system_drive}\Users\{username}\Desktop'
        print(cur_path)  # TEMP
        # cur_path = r'%userprofile%\Desktop'
        manageSSH.chdir(sftp, cur_path)
        items_list = sftp.listdir()
        # items_list = ['new', 'parallels crack', '20200111_162640.jpg', 'apple watch.txt', 'iphone 12 pro.png', 'iphone.txt', 'macbook.txt', 'macos crack.txt']
        icons_dict = get_icons_dict()
        # icons_dict = manageSERVER.get_icons_dict()
        create_frame(items_list)
        # items_list = sort_files_list(items_list)
        create_bttn(frame)

        def go_to_path():
            global cur_path
            new_path = simpledialog.askstring('Enter a path', 'Enter a valid path to go to:')
            print(new_path)
            if new_path == '' or new_path == None:
                pass
            else:
                while new_path.startswith('\\') or new_path.startswith('/') or new_path.startswith(' '):
                    new_path = new_path[1:]
                    print(new_path)  # TEMP
                new_path = new_path[0].upper() + new_path[1:]
                print(f'upper: {cur_path}')
                answr = manageSSH.chdir(sftp, new_path)
                if answr == 'path not found':
                    tkinter.messagebox.showerror(title="The specified path doesn't exist", message=f"{new_path}\ndoesn't exist. Please try a different one")
                else:
                    cur_path = new_path
                    print(f'new path:{cur_path}')  # TEMP
                    items_list = sftp.listdir()
                    update_frame(items_list)

        def acc_signout():
            discon_msg_box = tkinter.messagebox.askquestion(title='Disconnect & Sign Out', message='Are you sure you want to disconnect and sign out of your account?')
            if discon_msg_box == 'yes':
                manageSSH.disconnect_ssh(ssh)
                root.destroy()
                main()

        account.delete('Sign Out')
        account.add_command(label='Disconnect & Sign Out', command=acc_signout, activebackground='steelblue2', activeforeground='black')

        def go_to_desktop():
            global cur_path
            cur_path = rf'{system_drive}\Users\{username}\Desktop'
            manageSSH.chdir(sftp, cur_path)
            items_list = sftp.listdir()
            update_frame(items_list)

        def go_to_documents():
            global cur_path
            cur_path = rf'{system_drive}\Users\{username}\Documents'
            manageSSH.chdir(sftp, cur_path)
            items_list = sftp.listdir()
            update_frame(items_list)

        def go_to_downloads():
            global cur_path
            cur_path = rf'{system_drive}\Users\{username}\Downloads'
            manageSSH.chdir(sftp, cur_path)
            items_list = sftp.listdir()
            update_frame(items_list)

        def go_to_pictures():
            global cur_path
            cur_path = rf'{system_drive}\Users\{username}\Pictures'
            manageSSH.chdir(sftp, cur_path)
            items_list = sftp.listdir()
            update_frame(items_list)

        go_to = tkinter.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Go to...', menu=go_to)
        go_to.add_command(label='Desktop', command=go_to_desktop, activebackground='steelblue2', activeforeground='black')
        go_to.add_command(label='Documents', command=go_to_documents, activebackground='steelblue2', activeforeground='black')
        go_to.add_command(label='Downloads', command=go_to_downloads, activebackground='steelblue2', activeforeground='black')
        go_to.add_command(label='Pictures', command=go_to_pictures, activebackground='steelblue2', activeforeground='black')
        go_to.add_separator()
        go_to.add_command(label='Enter a path', command=go_to_path, activebackground='steelblue2', activeforeground='black')

        file_transfer = tkinter.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File Transfer', menu=file_transfer)
        file_transfer.add_command(label='Desktop', command=None, activebackground='steelblue2', activeforeground='black')

        def disconnect_func():  # add disconnecting from the machine (SSH)
            discon_msg_box = tkinter.messagebox.askquestion(title='Disconnect', message='Are you sure you want to disconnect?')
            if discon_msg_box == 'yes':
                manageSSH.disconnect_ssh(ssh)
                menubar.delete('Account')
                menubar.delete('Go to...')
                menubar.delete('Disconnect')
                account = tkinter.Menu(menubar, tearoff=0)
                menubar.add_cascade(label='Account', menu=account)
                LoginRegister.choose_mode_window(email)

        disconnect = tkinter.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Disconnect', menu=disconnect)
        disconnect.add_command(label='Disconnect', command=disconnect_func, activebackground='steelblue2', activeforeground='black')

        end_video_name = 'end-animation.mp4'
        LoginRegister.play_video(end_video_name)

        # #IN THE FUNC
        # for x in range(10):
        #     tkinter.Grid.columnconfigure(frame, x, weight=1)
        #
        # for y in range(5):
        #     tkinter.Grid.rowconfigure(frame, y, weight=1)

        root.mainloop()

if __name__ == '__main__':
    main()

# if __name__ == '__main__':
#     global frame, ssh, sftp
#
#     print(screen_width, screen_height, app_width, app_height)  # temp
#
#     root = tkinter.Tk()
#     x = int((screen_width - app_width) / 2)
#     y = int((screen_height - app_height) / 2)
#     print(f'x={x}, y={y}')
#     root.geometry(f'{app_width}x{app_height}+{x}+{y}')
#     root.iconbitmap('icon.ico')
#     # root.resizable(False, False)
#
#     # root.bind("<Configure>", resize)
#
#     email, mode, ssh, sftp = LoginRegister.main(root, app_width, app_height)
#     print('main_window.py')
#     print(email)  # DELETE
#     print(mode)
#     print(ssh)
#     print(sftp)
#     if email != None and mode != None and ssh != None and sftp != None:  # (ADD) and chosen_ip != None:
#         # end_video_name = 'end-animation.mp4'
#         # LoginRegister.play_video(end_video_name)
#         root.protocol("WM_DELETE_WINDOW", close_window)
#         root.geometry(f'{app_width}x{app_height}+{x}+{y}')
#         # root.minsize(width=1070, height=700)
#
#         # root.resizable(False, False)
#
#         root.title('Remote File Explorer')
#         # root.iconbitmap('icon.ico')
#
#         # host = "192.168.56.1"
#         # username = "yaniv-pc\yaniv"
#         # # password = input('Enter your password: ')  # DELETE
#         # password = 'Yanivn911911'
#         # ssh = manageSSH.connect_to_ssh(host, username, password)
#         # sftp = ssh.open_sftp()
#
#
#
#         manageSSH.chdir(sftp, cur_path)
#         items_list = sftp.listdir()
#         # items_list = ['new', 'parallels crack', '20200111_162640.jpg', 'apple watch.txt', 'iphone 12 pro.png', 'iphone.txt', 'macbook.txt', 'macos crack.txt']
#         icons_dict = get_icons_dict()
#         # icons_dict = manageSERVER.get_icons_dict()
#         create_frame(items_list)
#         # items_list = sort_files_list(items_list)
#         create_bttn(frame)
#
#         end_video_name = 'end-animation.mp4'
#         LoginRegister.play_video(end_video_name)
#
#         # #IN THE FUNC
#         # for x in range(10):
#         #     tkinter.Grid.columnconfigure(frame, x, weight=1)
#         #
#         # for y in range(5):
#         #     tkinter.Grid.rowconfigure(frame, y, weight=1)
#
#         root.mainloop()