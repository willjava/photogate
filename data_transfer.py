#C:\Users\teamw\OneDrive\Documents\william\Atom
#com is /dev/cu.usbmodem14201 on mac or COM3 on windows
import os
import serial
import sys
def testserial(ardu_port, baud):
    try:
        ser = serial.Serial(ardu_port, baud)
        return "works"
    except:
        print("Error: Could not connect. Connect Arduino, Close Serial Moniter in Ardunio editors, and Verify that your port name and baud rate is correct. You entered port: " + ardu_port +  " baud: " + str(baud))
        print("Please check usb port monitor or check the Ardunio Editior to get the correct port.")
        return "fail"
def resolve_times_to_zero(timedatalist):
    firsttime = timedatalist[0][0][0]
    for el in timedatalist:
        for subel in el:
            if firsttime != subel[0]:
                temp = float(subel[0])
                temp = temp - float(firsttime)
                subel[0] = str(temp)
    timedatalist[0][0][0] = str(0.0)
    return timedatalist
def compare(l1, l2):
    returnlist= []
    #print(l1)
    #print(l2)
    if len(l1) == len(l2):
        counter = 1
        while counter < (len(l1)-1):
            if l1[counter] != l2[counter]:
                #print("STATE CHANGE --" + "LOCATION =" + str(counter) + "-- TIME=" + l2[-1])
                #print(counter)
                newlist = [str(l2[-1]), str(l1[counter]) + str(l2[counter]), counter]
                returnlist.append(newlist)
            counter += 1
    else:
        print("error")
        print(l1)
        print(l2)
        print()
        #print(returnlist)
    return returnlist
def getserial(ardu_port, baud):
    try:
        ser = serial.Serial(ardu_port, baud)
    except:
        print("Error: Could not connect. Connect Arduino, Close Serial Moniter in Ardunio editors, and Verify that your port name and baud rate is correct. You entered port: " + ardu_port +  " baud: " + str(baud))
        print("Please check usb port monitor or check the Ardunio Editior to get the correct port.")
        return []
    print("connected")
    print("When finished with experiment please press the reset button on the arduino located near the USB port to continue")
    count = 1
    count2 = 0
    masterdata = []
    while(count > 0):
        getData=str(ser.readline())
        #print(getData)
        #b',1204,0,0,0,1,1,1,1,1,1,42262556,\r\n'
        if getData.find("N") != -1 or getData.find("M") !=  -1:
            if count == 2:
                count = 0
            if count == 1:
                count = 2
                count2 = 1
        if getData.find("N") == -1 or getData.find("M") ==  -1:
            if count2 == 1:
                data = getData.split(",")
                if (data[0] == "b'") and (data[-1] == "\\r\\n'") and (data[-1].find("xec") == -1):
                    data.pop(0)
                    data.pop(-1)
                    masterdata.append(data)
                    #print(data)
                if (data[0] == "b'") and (data[-1].find("xec") != -1):
                    data.pop(0)
                    data[-1].rstrip("\\xec\\r\\n'")
                    masterdata.append(data)
                    #print(data)

    return masterdata
def gettimes(masterdata):
    loopnum = len(masterdata)
    previous = masterdata[0]
    counter = 1
    changelist = [[],[],[],[],[],[],[],[],[]]
    while counter < loopnum - 1:
        templist = compare(previous, masterdata[counter])
        #print(templist)
        for el in templist:
            if el[-1] == 1:
                changelist[0].append(el)
            if el[-1] == 2:
                changelist[1].append(el)
            if el[-1] == 3:
                changelist[2].append(el)
            if el[-1] == 4:
                changelist[3].append(el)
            if el[-1] == 5:
                changelist[4].append(el)
            if el[-1] == 6:
                changelist[5].append(el)
            if el[-1] == 7:
                changelist[6].append(el)
            if el[-1] == 8:
                changelist[7].append(el)
            if el[-1] == 9:
                changelist[8].append(el)
        previous = masterdata[counter]
        counter += 1;
    return changelist
def getsensordata(timedata, sensor):
    returnstr = ''
    prev = []
    count = 0
    for el in timedata[sensor]:
        if count == 0:
            returnstr = str(el[0]) + str(el[1]) + "Diff=N/A"
        returnstr = returnstr + str(el[0]) + str(el[1]) + "Diff=" + str(el[0] - prev[0]) + ","
        prev = el
    return returnstr
def print_return(datalist):
    for el in datalist:
        print(el)
if __name__ == '__main__':
    ardu_port = "/dev/cu.usbmodem14201"
    baud = 9600
    masterdata = getserial(ardu_port, baud)
    #os.system("cat > newfile.csv")
    if masterdata != []:

        #print("finished with getserial")
        #print(masterdata)
        timedata = gettimes(masterdata)
        #print("finished with gettimes")
        #resolved = resolve_times_to_zero(timedata)
        print_return(timedata)
