import RPi.GPIO as GPIO
import telepot
from picamera import PiCamera
from time import sleep
from signal import pause
from gpiozero import MotionSensor
from telepot.loop import MessageLoop
import time

GPIO.setwarnings(False)

#Inisialisasi Variabel
pir = MotionSensor(4)
relay = 18
buzzer = 17
button = 15
camera = PiCamera()

GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#API Chat Bot Telegram
bot = telepot.Bot('833497859:AAEmyaXLqltkCM1sYq1a06jmI9v6M4Wq3hM')
  


        
def handle(msg):
    chat_id= msg['chat']['id']
    command = msg['text']
    #Tampilkan perintah yang diterima dari telegram
    print ('Got Command: %s'%command)


    
    def button_callback(channel):
        print("Button was pushed!")
        GPIO.output(buzzer, 0)
        time.sleep(1)
        GPIO.output(buzzer, 1)
        time.sleep(1)
        GPIO.output(buzzer, 0)
        take_photo()
        bot.sendMessage(chat_id=chat_id,text=("Ada tamu di depan pintu"))
        

    #Fungsi untuk mengambil gambar
    def take_photo():
        camera.capture('./capture.jpg')
        print('Photo has been taken')
        #Kirim foto ke telegram bot
        #bot.sendPhoto(chat_id=chat_id,photo=open('./capture.jpg','rb'))
        sleep(3)
    
    #Perintah untuk mengambil gambar
    if command == 'foto':
        take_photo()      
   
    #Perintah untuk membuka pintu   
    elif command == 'buka':
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(relay,GPIO.OUT)
        GPIO.output(relay,0) #relay nyala
        GPIO.output(relay,0) 
        #Kirim teks ke telegram bot
        bot.sendMessage(chat_id=chat_id,text=("Pintu Terbuka"))
        print("Pintu terbuka")

        sleep(2) #delay 2 detik
        GPIO.output(relay,1) #relay mati
        sleep(2) 
        GPIO.cleanup(relay)
        bot.sendMessage(chat_id=chat_id,text=("Pintu Tertutup"))
        print("Pintu tertutup")

        
    #Perintah untuk mematikan sensor PIR
    elif command == 'pirmati':
        #Menghentikan penggunaan kamera 
        pir.when_motion = camera.stop_preview()
        bot.sendMessage(chat_id=chat_id,text=("Sensor Infrared dimatikan"))
        print("PIR Dimatikan")
    
    #Perintah untuk menyalakan sensor PIR
    elif command == 'pirnyala':
        #Mengambil gambar saat ada gerakan terdeteksi
        pir.when_motion = take_photo
        bot.sendMessage(chat_id=chat_id,text=("Sensor Infrared dinyalakan"))
        print("PIR Dinyalakan")
        
    elif command == '/list':
        bot.sendMessage(chat_id=chat_id,text=("Perintah yang dqapat anda gunakan adalah : \n 1.buka - digunakan untuk membuka pintu \n 2.pirnyala - digunakan untuk menyalakan sensor inframerah \n 3.pirmati - digunakan untuk mematikan sensor inframerah"))
    
    #Perintah untuk menyalakan bell
    elif command == 'bell':
        GPIO.add_event_detect(button,GPIO.RISING,callback=button_callback)
        print('bel ditekan')
    


    
    else :
        bot.sendMessage(chat_id=chat_id,text=("Maaf, Perintah yang anda masukkan salah"))
        print("Maaf, Perintah yang anda masukkan salah, silahkan mengetik /list untuk melihat perintah yang dapat anda gunakan")


#Perintah untuk menerima imputan tombol
#GPIO.add_event_detect(button,GPIO.RISING,callback=button_callback) 

MessageLoop(bot,handle).run_as_thread()
print ('I am Listening....')
pause()
