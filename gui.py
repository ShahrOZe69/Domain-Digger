
import PySimpleGUI as sg

def gui():
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [ [sg.Text('Domain Digger', font=('Courier 12',22), text_color='black',justification='center')],
            [sg.Text('Select an Input Option', font=('Courier 12',22), text_color='blue')],
                [sg.Combo(['IP List', 'Domain List', 'IP Range'],default_value='IP List',readonly=True,key='-in-',auto_size_text=True)],
                [sg.Button(button_text='Go',key='-go-')]]
    # Create the Window
    window = sg.Window('Domain Digger', layout,size=(500,200)).Finalize()
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (None, 'Close Window'): # if user closes window or clicks cancel
            break
        if event =='-go-':
            if values['-in-'] == 'Domain List' or values['-in-'] == 'IP List': 
                input = multiline_input()
                break
            elif values['-in-'] == 'IP Range':
                input = ip_input()
                break

    
    window.close()
    return input,values['-in-']

def ip_input():
    layout =  [[sg.Text(text='Start Range')],

            [sg.InputText(default_text='0',size=(4,2)),sg.Text(text='.'),
            sg.InputText(default_text='0',size=(4,2)),sg.Text(text='.'),
            sg.InputText(default_text='0',size=(4,2)),sg.Text(text='.'),
            sg.InputText(default_text='0',size=(4,2))],

            [sg.Text(text='End Range')],


            [sg.InputText(default_text='0',size=(4,2)),sg.Text(text='.'),
            sg.InputText(default_text='0',size=(4,2)),sg.Text(text='.'),
            sg.InputText(default_text='0',size=(4,2)),sg.Text(text='.'),
            sg.InputText(default_text='0',size=(4,2))],

                
                
                [sg.Button('Submit',key='-ok-')]]
    window = sg.Window('IP Range',layout)
    while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '-ok-':
            if all([i.isnumeric() and -1<int(i)<256 for i in values.values()]):
                break
            else:
                sg.Popup(custom_text='Please enter Valid IP')
                values = {}
                break


    window.close()
    if all(i==None for i in values.values()):
        return None
    return f'{values[0]}.{values[1]}.{values[2]}.{values[3]}',f'{values[4]}.{values[5]}.{values[6]}.{values[7]}'



def multiline_input():
    layout = [[sg.Text('Paste the List')],
    [sg.Multiline(key='-list-',size=(30,20))],
    [sg.Button('Submit',key='-ok-')]]
    window = sg.Window('Domain Digger', layout)
    while True:
        event,values = window.read()
        if event == '-ok-' or event == sg.WIN_CLOSED:
            break
    window.close()
    return values['-list-']


if __name__=='__main__':
    gui()

