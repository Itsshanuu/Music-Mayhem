##############################       Libraries      ######################################
from tkinter import *
import pygame
from tkinter import filedialog               # To Search Songs from pc files
from pygame import mixer
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
from idlelib.tooltip import Hovertip        # for tooltip
import random                               # for shuffling songs


root=Tk()                                #Initialize Tkinter
root.title('Musical  Mayhem')
root.geometry('300x500+500+100')
root.resizable(False,False)
root.config(bg='#A2C4C9')


pygame.mixer.init()                     # Initialize Pygame Mixer


def add_song():                         # adds only one song
    song_path=filedialog.askopenfilename(title="Select Audio File",filetype=(("MP3","*mp3"),("WAV","*wav")))
    songlist_items=songlist.get(0,END)
    if song_path is "":                      # No song selected
        pass
    elif song_path not in songlist_items:
        songlist.insert(END,song_path)
        
        
def add_many_songs():                   # adds one or more than one song
    song_paths=filedialog.askopenfilenames(title="Select Audio File",filetype=(("MP3","*mp3"),("WAV","*wav")))
    songlist_items=songlist.get(0,END)
    for song in song_paths:
        if song not in songlist_items:
            songlist.insert(END,song)
            
        
def delete_song():                     # Deletes only one selected song
    songlist.delete(ANCHOR)
    mixer.music.stop()
    
    
def delete_all_songs():                # Deletes all the songs in the list
    songlist.delete(0,END)
    mixer.music.stop()
        

def light_theme():
    root.config(bg='#A2C4C9')
    songlist.config(bg='#D0E0E3', fg='#000000')
    song_name_label.config(bg='#A2C4C9')
    song_name_show.config(bg='#A2C4C9',fg='#000000')
    song_slider_label.config(bg='#A2C4C9')
    song_start_show.config(bg='#A2C4C9',fg='#000000')
    song_end_show.config(bg='#A2C4C9',fg='#000000')
    controls_frame.config(bg='#A2C4C9')
    shuffle_button.config(bg='#A2C4C9',activebackground='#A2C4C9')
    back_button.config(bg='#A2C4C9',activebackground='#A2C4C9')
    play_button.config(bg='#A2C4C9',activebackground='#A2C4C9')
    pause_button.config(bg='#A2C4C9',activebackground='#A2C4C9')
    forward_button.config(bg='#A2C4C9',activebackground='#A2C4C9')
    volume_button.config(bg='#A2C4C9',activebackground='#A2C4C9')
    close_button.config(bg='#A2C4C9',activebackground='#A2C4C9')
    volume_frame.config(bg='#A2C4C9',fg='#000000')
    volume_label.config(bg='#A2C4C9',fg='#000000')


def dark_theme():
    root.config(bg='#434343')
    songlist.config(bg='#666666', fg='#FFFFFF')
    song_name_label.config(bg='#434343')
    song_name_show.config(bg='#434343',fg="#FFFFFF")
    song_slider_label.config(bg='#434343')
    song_start_show.config(bg='#434343',fg="#FFFFFF")
    song_end_show.config(bg='#434343',fg="#FFFFFF")
    controls_frame.config(bg='#434343')
    shuffle_button.config(bg='#434343',activebackground='#434343')
    back_button.config(bg='#434343',activebackground='#434343')
    play_button.config(bg='#434343',activebackground='#434343')
    pause_button.config(bg='#434343',activebackground='#434343')
    forward_button.config(bg='#434343',activebackground='#434343')
    volume_button.config(bg='#434343',activebackground='#434343')
    close_button.config(bg='#434343',activebackground='#434343')
    volume_frame.config(bg='#434343',fg='#FFFFFF')
    volume_label.config(bg='#434343',fg='#FFFFFF')
        
    
def play_time():
    current_time=mixer.music.get_pos()/1000
    converted_current_time=time.strftime('%H:%M:%S',time.gmtime(current_time))
    song=songlist.get(ACTIVE)
    song_playing=MP3(song)                          # loads the current song using mutagen
    #global song_length
    song_length=song_playing.info.length            # Finds length of song
    converted_song_length=time.strftime('%H:%M:%S',time.gmtime(song_length))
    song_start_show.grid()
    song_start_show.config(text=converted_current_time)
    song_end_show.grid()
    song_end_show.config(text=converted_song_length)
    
    slider_position=int(song_length)
    song_slider.config(to=slider_position)
    
    current_time +=1

    if int(song_slider.get()) == int(song_length):
        song_start_show.config(text=song_length)
        song_start_show.grid_remove()
        song_end_show.grid_remove()
        pause_button.grid_remove()
        play_button.grid()
        #forward()
    elif paused:
        pass
    elif int(song_slider.get()) == int(current_time):
        song_slider.config(value=int(current_time))
    else:
        cur_time=int(song_slider.get()+1)
        converted_cur_time = time.strftime('%H:%M:%S', time.gmtime(cur_time))
        song_start_show.config(text=converted_cur_time)

        next_time = int(song_slider.get()+1)
        song_slider.config(value=next_time)

    song_start_show.after(1000,play_time) 


global paused
paused=False


def play(is_paused):
    global paused
    paused=is_paused
    
    song=songlist.get(ACTIVE)
    selected_song=songlist.get(songlist.curselection())
    
    if song is '':
        pass
    elif paused:
        play_button.grid_remove()
        pause_button.grid()
        mixer.music.unpause()
        paused=False
    elif selected_song is '':
        pass
    else:
        mixer.music.load(selected_song)
        mixer.music.play(loops=0)
        play_button.grid_remove()
        pause_button.grid()
        song_name=selected_song.split('/')[-1].split('.')[0]
        song_name_show.grid()
        song_name_show.config(text=song_name)
        ToolTip = Hovertip(pause_button,'Pause')
        a=int(volume_slider.get()*100)
        volume_label.config(text=f"volume: {a}")
        mixer.music.set_volume(volume_slider.get())
        play_time()

        
def pause(is_paused):
    global paused
    paused=is_paused
    
    pause_button.grid_remove()
    play_button.grid()
    mixer.music.pause()
    paused=True


def forward():
    song_slider.config(value=0)
    next_song=songlist.curselection()
    next_song=next_song[0]+1
    song=songlist.get(next_song)
    if song is "":
        pass
    else:
        mixer.music.load(song)
        mixer.music.play(loops=0)
        songlist.selection_clear(0,END)
        songlist.activate(next_song)
        songlist.selection_set(next_song, last=None)
        song_name=song.split('/')[-1].split('.')[0]
        song_name_show.grid()
        song_name_show.config(text=song_name)
        play_button.grid_remove()
        pause_button.grid()


def back():
    song_slider.config(value=0)
    previous_song=songlist.curselection()
    previous_song=previous_song[0]-1
    song=songlist.get(previous_song)
    mixer.music.load(song)
    mixer.music.play(loops=0)
    songlist.selection_clear(0,END)
    songlist.activate(previous_song)
    songlist.selection_set(previous_song, last=None)
    song_name=song.split('/')[-1].split('.')[0]
    song_name_show.grid()
    song_name_show.config(text=song_name)
    play_button.grid_remove()
    pause_button.grid()
    play_time()
    

def shuffle():
    songlist_items=songlist.get(0,END)
    shuffled_items=random.sample(songlist_items,len(songlist_items))
    songlist.delete(0,END)
    for i in shuffled_items:
        songlist.insert(END,i)
        
        
def popup_close():
    popup_close.popup=Tk()
    popup_close.popup.title('Exit')
    popup_close.popup.geometry('250x150+520+250')
    popup_close.popup.resizable(False,False)

    Message=Label(popup_close.popup, text="Are you sure you want to exit?", font = ('arial',12))
    Message.pack(ipadx=10,anchor="w",ipady=30)

    yes_no_frame=Frame(popup_close.popup)
    yes_no_frame.pack(ipadx=10,ipady=10)

    yes_button = Button(yes_no_frame, text="Yes", borderwidth=1, command=exit)
    yes_button.grid(row=1,column=1,padx=10)

    no_button = Button(yes_no_frame, text="No", borderwidth=1, command=popup_close.popup.destroy)
    no_button.grid(row=1,column=2)
    
    
def exit():
    mixer.music.stop()
    popup_close.popup.destroy()
    root.destroy()


def volume(x):
    mixer.music.set_volume(volume_slider.get())
    current_volume=int(volume_slider.get()*100)
    volume_label.config(text=f"volume: {current_volume}")
    
    
def vol_show():
    volume_frame.pack()
    
    
def vol_close():
    volume_frame.pack_forget()


def slide(x):
    song=songlist.get(ACTIVE)
    mixer.music.load(song)
    mixer.music.play(loops=0,start=int(song_slider.get()))
    play_button.grid_remove()
    pause_button.grid()
    
    
###################################         Create Menu           ###########################
my_menu=Menu(root)
root.config(menu=my_menu)             # Display Menu

menu_options=Menu(my_menu,tearoff=0)
add_menu=Menu(my_menu,tearoff=0)
delete_menu=Menu(my_menu,tearoff=0)
theme_menu=Menu(my_menu,tearoff=0)

my_menu.add_cascade(label="Menu",menu=menu_options)

menu_options.add_cascade(label="Add Songs",menu=add_menu)
add_menu.add_cascade(label="Add One Song to Playlist",command=add_song)
add_menu.add_cascade(label="Add Many Songs to Playlist",command=add_many_songs)

menu_options.add_cascade(label="Delete Songs",menu=delete_menu)
delete_menu.add_cascade(label="Delete One Song from Playlist",command=delete_song)
delete_menu.add_cascade(label="Delete All Songs From Playlist",command=delete_all_songs)

menu_options.add_cascade(label="Select Theme",menu=theme_menu)
theme_menu.add_cascade(label="Light",command=light_theme)
theme_menu.add_cascade(label="Dark",command=dark_theme)

menu_options.add_cascade(label="Exit",command=popup_close)


##################################         Songs List Box           ###########################
songlist = Listbox(root, width=45,bg='#D0E0E3', fg='#000000')
songlist.pack(pady=20,padx=10)


##################################         Song Name Satus Label           ###########################
song_name_label = Frame(root,bg='#A2C4C9')
song_name_label.pack(padx=10, pady=10, anchor="w")

song_name_show=Label(song_name_label, text='', font = ('arial',10,'italic bold'),bg='#A2C4C9')
song_name_show.grid(row=1,column=0)
song_name_show.grid_remove()


##################################         Song Slider           ###########################
song_slider_label = Frame(root,bg='#A2C4C9')
song_slider_label.pack(padx=10, pady=10)

song_slider=ttk.Scale(song_slider_label, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=270)
song_slider.grid(row=0,column=0)

song_start_show=Label(song_slider_label, text='', font = ('arial',10,'italic bold'),bg='#A2C4C9')
song_start_show.grid(row=1,column=0,sticky="W",pady=10)
song_start_show.grid_remove()

song_end_show=Label(song_slider_label, text='', font = ('arial',10,'italic bold'),bg='#A2C4C9')
song_end_show.grid(row=1,column=0,sticky="E",pady=10)
song_end_show.grid_remove()

#please change the path#
##################################         Button Images           ###########################
play_img = PhotoImage(file="D:\Study\Coding Stuffs\Music Mayhem")
pause_img = PhotoImage(file="D:\Study\Coding Stuffs\Music Mayhem")
forward_img = PhotoImage(file="D:\Study\Coding Stuffs\Music Mayhem")
back_img = PhotoImage(file="D:\Study\Coding Stuffs\Music Mayhem")
shuffle_img = PhotoImage(file="D:\Study\Coding Stuffs\Music Mayhem")
volume_img = PhotoImage(file="D:\Study\Coding Stuffs\Music Mayhem")
close_img = PhotoImage(file="D:\Study\Coding Stuffs\Music Mayhem")

##################################         Resizing Button Images           ###########################
play_img = play_img.subsample(12,12)
pause_img = pause_img.subsample(12,12)
forward_img = forward_img.subsample(20,20)
back_img = back_img.subsample(20,20)
shuffle_img = shuffle_img.subsample(2,2)
volume_img = volume_img.subsample(2,2)
close_img = close_img.subsample(4,4)


##################################      Create Player Control Frame for Buttons        ###########################
controls_frame = Frame(root,bg='#A2C4C9')
controls_frame.pack(ipadx=10,ipady=10,padx=10)


##################################         Button Placements           ###########################
shuffle_button = Button(controls_frame, image=shuffle_img, borderwidth=0, command=shuffle,bg='#A2C4C9',activebackground='#A2C4C9')
shuffle_button.grid(row=0,column=0,padx=10)
ToolTip = Hovertip(shuffle_button,'Shuffle')

back_button = Button(controls_frame, image=back_img, borderwidth=0, command=back,bg='#A2C4C9',activebackground='#A2C4C9')
back_button.grid(row=0,column=1,padx=5)
ToolTip = Hovertip(back_button,'Previous Song')

play_button = Button(controls_frame, image=play_img, borderwidth=0, command=lambda: play(paused),bg='#A2C4C9',activebackground='#A2C4C9')
play_button.grid(row=0,column=2,padx=5)
ToolTip = Hovertip(play_button,'Play')

pause_button = Button(controls_frame, image=pause_img, borderwidth=0, command=lambda: pause(paused),bg='#A2C4C9',activebackground='#A2C4C9')
pause_button.grid(row=0,column=2,padx=5)
pause_button.grid_remove()

forward_button = Button(controls_frame, image=forward_img, borderwidth=0, command=forward,bg='#A2C4C9',activebackground='#A2C4C9')
forward_button.grid(row=0,column=3,padx=10)
ToolTip = Hovertip(forward_button,'Next Song')

volume_button = Button(controls_frame, image=volume_img, borderwidth=0, command=vol_show,bg='#A2C4C9',activebackground='#A2C4C9')
volume_button.grid(row=0,column=4,padx=10)
ToolTip = Hovertip(volume_button,'Volume')


##################################      Volume Frame        ###########################
volume_frame = LabelFrame(root,text="Volume",bg='#A2C4C9')
volume_frame.pack(padx=20)

volume_slider=ttk.Scale(volume_frame, from_=0, to=1, orient=HORIZONTAL, value=0.5, command=volume, length=150)
volume_slider.grid(pady=10,padx=10)

close_button = Button(volume_frame, image=close_img,command=vol_close, borderwidth=1,bg='#A2C4C9',activebackground='#A2C4C9')
close_button.grid(row=0,column=1,padx=10)
ToolTip = Hovertip(close_button,'Volume Frame Close')

volume_label=Label(volume_frame,text="volume: 50",bg='#A2C4C9')
volume_label.grid(row=1,column=0,padx=5)

volume_frame.pack_forget()


root.mainloop()                            # End