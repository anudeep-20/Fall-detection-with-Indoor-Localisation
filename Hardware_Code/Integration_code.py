import matplotlib.pyplot as plt
import serial ,time
from drawnow import drawnow
import winsound
from firebase import firebase

firebase_url = firebase.FirebaseApplication('https://falldetection-7f089-7fcfd.firebaseio.com', None)

#Change the COM-Ports accordingly from Device-Manager in your PC.
gyro_COM = "5"
accl_COM = "12"
bath_COM = "7"

bt_1_data = serial.Serial("COM"+ gyro_COM, 9600 ,timeout = .1)#Port of Bluetooth-3(Corresponding to Arduino-1 / Gyro) connected to Bluetooth-1
bt_2_data = serial.Serial("COM"+ accl_COM , 9600 , timeout = .1)#Port of Bluetooth-4(Corresponding to Arduino-2 / Acclerometer) connected to Bluetooth-2
bath_data = serial.Serial("COM"+ bath_COM , 9600 , timeout = .1)
gsm_data = serial.Serial("COM35" , 9600 , timeout = .1)#Port of GSM Module 

bt_1_data.flush()
bt_2_data.flush()
bath_data.flush()
gsm_data.flush()

def makeFig():
    if (char == 'x'):
        plt.plot(time_1, val_fsr , color = 'c' , label = 'Piezo_value' , linewidth = 1)
        plt.xlabel('Time')
        plt.ylabel('Piezo_analog_value')
    if (char != 'x') :
        plt.plot(time_1, val_1 , color = 'r' , label = 'x_angle' , linewidth = 0.5)
        plt.plot(time_1, val_2 , color = '#67C117' , label = 'y_angle' , linewidth = 0.5)
        plt.plot(time_1, val_3 , color = '#1735C1' , label = 'z_angle' , linewidth = 0.5)
        plt.plot(time_1, val_acc , color = 'k' , label = 'acc_angle' , linewidth = 1.5)
        plt.xlabel('Time')
    plt.grid(True)
    plt.legend(loc = 'upper center' , bbox_to_anchor = (0.5,1.1) , ncol = 4)
    

def gsm_func():
    print "Help...!!"  #Alert saying "HELP..!!"
    winsound.Beep(800,500)
    gsm_data.write('ATZ\r')
    time.sleep(0.5)
    gsm_data.write('AT+CMGF=1\r')
    time.sleep(0.5)
    gsm_data.write("ATD+918919029787;\r")#Type your phone number in place of +91xxxxxxxxxx(+91 is country code)
    time.sleep(20)
    gsm_data.write("ATH\r")
    time.sleep(0.5)
    gsm_data.write("Message from GSM\nI need your help" + "\r")
    time.sleep(0.5)
    gsm_data.write(chr(26))
    time.sleep(1)

plt.ion() 
fig=plt.figure()

x_diff = x_prev = 0
y_diff = y_prev = 0
z_diff = z_prev = 0
diff_fsr = 0
diff_acc = 0
acc_prev = 0
fsr_prev = '*'
char = '*'
isT = True

time_ref = time.time()
time_1 = [None]*100
val_1 = [None]*100
val_1[99] = 0
val_2 = [None]*100
val_2[99] = 0
val_3 = [None]*100
val_3[99] = 0
val_acc = [None]*100
val_acc[99] = 0
val_fsr = [None]*100

myData_bt_2 = []
q = a = p = 0

while True :
    try:
        if(bt_1_data.inWaiting() > 0 or bt_2_data.inWaiting() > 0 or bath_data.inWaiting()):
            myData_bt_1 = bt_1_data.readline()
            myData_bt_2 = bt_2_data.readline()
            fsr_data = bath_data.readline()
            myData_bt_1 = myData_bt_1.strip('\n')
            myData_bt_1 = myData_bt_1.strip('\r')
            myData_bt_2 = myData_bt_2.strip('\n')
            myData_bt_2 = myData_bt_2.strip('\r')
            fsr_data = fsr_data.strip('\n')
            fsr_data = fsr_data.strip('\r')

            if fsr_data == '':
                fsr_data = fsr_prev
                
            char = fsr_data[:1]
            
            if char == 'x':
                fsr_data = int(fsr_data[1:])

            if myData_bt_1 != '':  
                myData_bt_1 = myData_bt_1.split(",")
                heart_rate = myData_bt_1[3]
            
            if myData_bt_2 != '':
                myData_bt_2 = myData_bt_2.split(";")
                gps_lat = myData_bt_2[1]
                gps_lng = myData_bt_2[2]
                myData_bt_2 = myData_bt_2[0]
            
            if myData_bt_1 == '':
                x_diff = x_prev
                y_diff = y_prev
                z_diff = z_prev
                
            else:
                time_diff = abs(time.time()-time_ref)
                time_1.append(time_diff)
                time_1 = time_1[-100:]
          
                val_1.append(float(myData_bt_1[0]))
                val_1 = val_1[-100:]
                val_2.append(float(myData_bt_1[1]))
                val_2 = val_2[-100:]
                val_3.append(float(myData_bt_1[2]))
                val_3 = val_3[-100:]
                
                x_diff = abs(val_1[99] - val_1[98])
                y_diff = abs(val_2[99] - val_2[98])
                z_diff = abs(val_3[99] - val_3[98])
                
            if myData_bt_2 == '':
                diff_acc = acc_prev
            else:
                val_acc.append(float(myData_bt_2))
                val_acc = val_acc[-100:]
                diff_acc = abs(val_acc[99]-val_acc[98])   
             
            if ((x_diff > 40.0 or y_diff > 40.0 or z_diff > 40) and diff_acc > 40):
                q += 1
            if q==2:
                q = 0

            if (char == 'x') :
                if val_fsr == [None]*100 :
                    val_fsr.append(fsr_data)
                    val_fsr = val_fsr[-100:]
                    p = 0
                else:
                    val_fsr.append(fsr_data)
                    val_fsr = val_fsr[-100:]
                    diff_fsr = abs(val_fsr[99]-val_fsr[98])
                    p = 1
                if (diff_fsr > 300):
                    a += 1
                if a==2 :
                    a = 0

            if (char != 'x') :          
                if ((x_diff > 40.0 or y_diff > 40.0 or z_diff > 40) and diff_acc > 30 and q == 1):
                    bt_1_data.close()
                    bt_2_data.close()
                    bath_data.close()
                    firebase.patch(firebase_url+'/chennuruvineeth/Father/', {'HeartBeat':heart_rate})
                    firebase.patch(firebase_url+'/chennuruvineeth/Father/', {'ImpactFactor':diff_acc})
                    firebase.patch(firebase_url+'/chennuruvineeth/Father/', {'Location':str(gps_lat)+","+str(gps_lng)})
                    gsm_func()
                    bt_1_data = serial.Serial("COM" + gyro_COM , 9600 ,timeout = .1)
                    bt_2_data = serial.Serial("COM" + accl_COM , 9600 , timeout = .1)
                    bath_data = serial.Serial("COM" + bath_COM , 9600 , timeout = .1)
                    print "Its from gyro" # Alert saying that fall detected through the wearable band

            if (char == 'x') :
                if (diff_fsr > 250 and a == 1 and p != 0 ) :
                    bt_1_data.close()
                    bt_2_data.close()
                    bath_data.close()
                    firebase.patch(firebase_url+'/chennuruvineeth/Father/', {'HeartBeat':heart_rate})
                    firebase.patch(firebase_url+'/chennuruvineeth/Father/', {'ImpactFactor':diff_fsr})
                    firebase.patch(firebase_url+'/chennuruvineeth/Father/', {'Location':str(gps_lat)+","+str(gps_lng)})
                    gsm_func()
                    bt_1_data = serial.Serial("COM" + gyro_COM , 9600 ,timeout = .1)
                    bt_2_data = serial.Serial("COM" + accl_COM , 9600 , timeout = .1)
                    bath_data = serial.Serial("COM" + bath_COM , 9600 , timeout = .1)
                    print "Its from Bathroom" #Alert saying fall detected inside the bathroom

            x_prev = x_diff
            y_prev = y_diff
            z_prev = z_diff
            acc_prev = diff_acc
            fsr_prev = char + str(fsr_data)
                
            drawnow(makeFig)
            plt.pause(0.01)
    except ValueError or IndexError:
        continue
