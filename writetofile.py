#C:\Users\teamw\OneDrive\Documents\william\Atom
#com is /dev/cu.usbmodem14201 on mac or COM3 on windows
import data_transfer
import os
import time
def d_sum(distancelist, indexfrom, indexto):
    num = 0.0
    count = indexfrom
    while count <= indexto:
        num = num + float(distancelist[count])
        count+=1
    return num
def writetocsv(datalist, filename, distancelist, trial):
    with open(filename, "a") as file:
        file.write("begin trial\n")
        file.write("A state change state=10 indicates the sensors is being activated.,A state change state=01 indicates the sensors is ceasing to be activated. \n")
        a = time.time()
        b = time.localtime(a)
        c = time.asctime(b)
        file.write("time=" + str(c) + "\n")
        file.write("Trial= " + str(trial) + "\n")
        file.write(",sensor,position (cm), time (microseconds), state change\n")
        counts = 1
        for el in datalist:
            if counts == 1:
                newline = "," + str(counts) + "," + str(0) + ","
            if counts > 1:
                newline = "," + str(counts) + "," + str(d_sum(distancelist,0,counts-2)) + ","

            #print("el is ")
            #print(el)
            if el != []:
                for subel in el:
                    newline = newline + str(subel[0]) + ","
                    #print(subel[1])
                    #print(subel)
                    newline = newline + "state= " + str(subel[1]) + ","
            newline = newline + "\n"
            file.write(newline)
            counts =counts + 1
        file.write("end trial\n")
def writetotxt(datalist, filename, distancelist, trial):
    with open(filename, "a") as file:
        file.write("begin trial\n")
        a = time.time()
        b = time.localtime(a)
        c = time.asctime(b)
        file.write("time=" + str(c) + "\n")
        file.write("Trial= " + str(trial) + "\n")
        counts = 1
        for el in datalist:
            for el in datalist:
                if counts == 1:
                    newline = "Sensor: " + str(counts) + ", Postion (cm): " + str(0) + ","
                if counts > 1:
                    newline = "Sensor: " + str(counts) + ", Postion (cm): " + str(d_sum(distancelist,0,counts-2)) + ","

            #print("el is ")
            #print(el)
            if el != []:
                for subel in el:
                    newline = newline + "Time= " + str(subel[0]) + ","
                    #print(subel[1])
                    #print(subel)
                    newline = newline + "state= " + str(subel[1]) + ","
            newline = newline + "\n"
            file.write(newline)
            counts =counts + 1
        file.write("end trial\n")
def convert_cmpermu_to_mpers(num):
    val = num/100 #convert cm to meters
    val = val*1000000 #convert microseconds to seconds
    return val
def convert_cmpermupw2_to_mperspw2(num):
    val = num
    val = val*1000000 #convert microseconds to seconds
    return val
def d_tot(distancelist):
    num = 0.0
    for el in distancelist:
        num = num + float(el)
    return num
def calc_v_avg(time_1_trigger, time_2_trigger, distance):
    num = 0.0
    num = float(distance) / (float(time_2_trigger) - float(time_1_trigger))
    #num is now in centimeter per microsecond
    return num
def calc_a_avg(time_1_trigger, time_2_trigger, velocity1, velocity2):
    num = 0.0
    num = (float(velocity2) - float(velocity1))/ (float(time_2_trigger) - float(time_1_trigger))
    #num is now in centimeter per microsecond squared
    return num
def gettime(datalist, sensor):
    sensor = int(sensor)
    try:
        if datalist[sensor-1][0][1] == '10':
            data = datalist[sensor-1][0][0]
        else:
            print("Error. Try again.")
            return "error"
        return data
    except:
        print("Houston we have a problem")
#############################################################################################################################################
if __name__ == '__main__':

    filename = ""
    exit = False
    z = 9600 #default baud
    trial = 1
    while not exit:
        counter = 0
        counter2 = 0
        print("***Welcome to the command line interface for CAV_PHOTO_GATE_MKI***")
        print("Please follow the instructions below! Thank You :)")
        print("Created by William White (2021) for SCI 513 - Computer Programming Project 1 in Fall Semester 2020")
        print("Under the tutiliege of Mr. Joseph Crnkovich of the Heights School")
        print("********************************************************************")
        print("Enter Quit or q in any input box to exit program")
###########################################################################################################################################
        validcomp = False
        while not validcomp:
            compinpt = input("Are you using a Mac or Windows (M/W):")
            valid = 0
            if compinpt.lower().startswith('m'):
                comp = True
                validcomp = True
                valid = 1
            if compinpt.lower().startswith('w'):
                comp = False
                validcomp = True
                valid = 1
            if compinpt.lower().startswith('q'):
                exit = True
                break
            if valid == 0:
                print("Invalid field!")
        if exit:
            break
##################################################################################################################################
        wannafile = str(input("Would you like to save the results of the experiment in a file? y/n: "))
        if wannafile.lower().startswith('y'):
            validfile = False

            while not validfile:
                isproblem = False
                filename = str(input("What will the name of the file be? Please use a .csv fileending. Please no periods in file name. EG example.csv: "))
                filename = filename.strip()
                if len(filename.split(".")) <= 1:
                    if filename.lower().startswith('q'):
                        exit = True
                        break
                if len(filename.split(".")) != 2:
                    print("Invalid filename please. Must have file ending and no periods except for file ending.")
                    isproblem = True
                    continue
                filenamel = filename.split(".")
                #print(filenamel)
                #print(str(filenamel[1] != "txt"))
                #print(str(filenamel[1] != "txt" or filenamel[1] != "csv"))
                if (filenamel[1] != "txt") and (filenamel[1] != "csv"):
                    print("Please use a .txt or .csv file. Only these files are recognized by this software.")
                    isproblem = True
                    continue
                if comp:
                    print("##############################################")
                    os.system("find " + filename + " >testfile123.txt")
                    print("##############################################")
                    print("please disregard text between # marks")
                if not comp:
                    print("##############################################")
                    os.system("dir " + filename + "/s >testfile123.txt")
                    print("##############################################")
                    print("please disregard text between # marks")
                fstr = ""
                with open("testfile123.txt", "r") as file:
                    fstr = file.readline()
                    for line in file:
                        #print("line = " + file.readline())
                        fstr = fstr + file.readline()
                isduplicate = False
                #print("this is fstr: " + fstr)
                if comp:
                    if fstr.find(filename) != -1:
                        print("A file of this name already exists.")
                        isduplicate = True
                if not comp:
                    if fstr.find("File") != -1:
                        print("A file of this name already exists.")
                        isduplicate = True
                if isduplicate == True:
                    overwrite = input("Would you like to overwrite this file? Warning this will destroy the current file! (y/n): ")
                    if overwrite.lower().startswith('y'):
                        print("You have choosen to over write")
                    if overwrite.lower().startswith('n'):
                        isproblem = True
                        continue
                    if overwrite.lower().startswith('q'):
                        exit = True
                        validfile = True
                        print("you have choosen to quit")
                        break
                    overwrite2 = input("Are you sure you want to overwrite this file? Warning this will destroy the current file! THIS CANNOT BE UNDONE (y/n): ")
                    if overwrite2.lower().startswith('y'):
                        print("You have choosen to over write")
                        validfile = True
                    if overwrite2.lower().startswith('n'):
                        print("Please choose a new file name")
                        isproblem = True
                    if overwrite2.lower().startswith('q'):
                        exit = True
                        validfile = True
                        print("you have choosen to quit")
                        break
                if not isproblem:
                    validfile = True
            if exit:
                break
            try:
                with open(filename, "w") as file:
                    file.write(filename + "\n")
                    print(filename + ' has been created.')
            except Exception as er:
                print(str(er) + " occured attempting to override")
                print("##############################################")
                os.system("cat >" + filename)
                print("##############################################")
                print("please disregard text between # marks")
        doesnothing = 0
        if wannafile.lower().startswith('y'):
            doesnothing = 1
        if wannafile.lower().startswith('q'):
            exit = True
            print("you have choosen to quit")
            break
        if doesnothing == 0:
            print("Warning! You have choosen to continue without saving your data in a file.")
        if exit:
            break
################################################################################################################################################################################

        print("Defaults are 1.50 cm distance between sensors, baud 9600, and port /dev/cu.usbmodem14201 on mac and COM3 on windows.")
        deflt = input("Would you like to use defaults? (y/n)")
        if deflt.lower().startswith('y'):
                if comp:
                    counter = 1
                    x = "/dev/cu.usbmodem14201"
                    counter = 1
                if not comp:
                    x = "COM3"
                    counter = 1

                if data_transfer.testserial(x, z) != "works":
                    counter = 0
                counter2 = 1
                a = 1.50
                b = 1.50
                c = 1.50
                d = 1.50
                e = 1.50
                f = 1.50
                g = 1.50
                h = 1.50
                distancelist = [a,b,c,d,e,f,g,h]
        if deflt.lower().startswith('q'):
            exit = True
            print("you have choosen to quit")
        if exit:
            break
#############################################################################################################################################################
        while(counter < 1):
            print("Please enter the port and baud rate for your Arduino")
            print("On a windows os the port is usally COMX where X is the port number.")
            print("On a Mac or Linux os the port is usally /dev/cu.usbmodem14X01 where 14X01 is the port number. X can be any number see below.")
            print("to find out what port it is:")
            if comp:
                print("On mac go to Apple Button> About This Mac > System Report > USB")
                print("Select communications device and the look for the location id")
                print("It should look like this:: Location ID:	0x14200000 / 28")
                print("The third number determines what the serial port should be.")
                print("In this case it would be /dev/cu.usbmodem14201")
                print("The third number determines the third number after usbmodem.")
            if not comp:
                print("For windows:")
                print("What your settings looks like depends on your version of windows.")
                print("Go to settings and find or search for device manager.")
                print("Look for a section that says ports. NOT USB")
                print("When you open it, you should see somthing invovling arduino and the COMX. X is a number. This is your port.")
                print("IF you dont see it your device is not plugged in. Plug it in and ports should apppear.")
            print("Default baud for the software on the Arduino is 9600")
            x = input("computer port: " )
            if (x.lower().startswith('q')):
                exit = True
                print("you have choosen to quit")
                break
            if data_transfer.testserial(x, z) == "works":
                counter = 2
            else:
                print("******************************************************")
                print("Invalid format or wrong port. Port must follow format.")
                print("******************************************************")

        if exit:
            break
##################################################################################################################################################################
        while counter2 < 1:
            try:
                print("Please enter the following data in centimeters. Decimals are usable and requested. Remember signinficant digits. Measure from the black bar in the middle of each sensor.")
                aa = input("Distance between Sensor 1 and 2: ")

                bb = input("Distance between Sensor 2 and 3: ")

                cc = input("Distance between Sensor 3 and 4: ")

                dd = input("Distance between Sensor 4 and 5: ")

                ee = input("Distance between Sensor 5 and 6: ")

                ff = input("Distance between Sensor 6 and 7: ")

                gg = input("Distance between Sensor 7 and 8: ")

                hh = input("Distance between Sensor 8 and 9: ")
                a = float(aa)
                b = float(bb)
                c = float(cc)
                d = float(dd)
                e = float(ee)
                f = float(ff)
                g = float(gg)
                h = float(hh)
                distancelist = [a,b,c,d,e,f,g,h]
                counter2 = 1
            except:
                print('Entries invalid! Please re-enter!')
        if exit:
            break
######################################################################################################################################################################
        count = 0
        xx = 'y'
        while count < 2:
            if count == 1:
                xx = str(input("would you like to run the experiment again with the same distances? y/n:"))
            if (xx.lower().startswith('y')):
                masterdata = data_transfer.getserial(x, int(z))
                timedata = data_transfer.gettimes(masterdata)
                try:
                        print("calcing")
                        resolved = timedata
                        timelist = [gettime(resolved, 1), gettime(resolved, 2),gettime(resolved, 3),gettime(resolved, 4),gettime(resolved, 5),gettime(resolved, 6),gettime(resolved, 7),gettime(resolved, 8), gettime(resolved, 9)]
                        va = convert_cmpermu_to_mpers(calc_v_avg(timelist[0], timelist[1], distancelist[0]))
                        vb = convert_cmpermu_to_mpers(calc_v_avg(timelist[1], timelist[2], distancelist[1]))
                        vc = convert_cmpermu_to_mpers(calc_v_avg(timelist[2], timelist[3], distancelist[2]))
                        vd = convert_cmpermu_to_mpers(calc_v_avg(timelist[3], timelist[4], distancelist[3]))
                        ve = convert_cmpermu_to_mpers(calc_v_avg(timelist[4], timelist[5], distancelist[4]))
                        vf = convert_cmpermu_to_mpers(calc_v_avg(timelist[5], timelist[6], distancelist[5]))
                        vg = convert_cmpermu_to_mpers(calc_v_avg(timelist[6], timelist[7], distancelist[6]))
                        vh = convert_cmpermu_to_mpers(calc_v_avg(timelist[7], timelist[8], distancelist[7]))
                        finalv = convert_cmpermu_to_mpers(calc_v_avg(timelist[0], timelist[-1], d_tot(distancelist)))
                        finala = convert_cmpermupw2_to_mperspw2(calc_a_avg(timelist[1], timelist[8], va, vh))
                        ab = convert_cmpermupw2_to_mperspw2(calc_a_avg(timelist[1], timelist[2], va, vb))
                        ac = convert_cmpermupw2_to_mperspw2(calc_a_avg(timelist[2], timelist[3], vb, vc))
                        ad = convert_cmpermupw2_to_mperspw2(calc_a_avg(timelist[3], timelist[4], vc, vd))
                        ae = convert_cmpermupw2_to_mperspw2(calc_a_avg(timelist[4], timelist[5], vd, ve))
                        af = convert_cmpermupw2_to_mperspw2(calc_a_avg(timelist[5], timelist[6], ve, vf))
                        ag = convert_cmpermupw2_to_mperspw2(calc_a_avg(timelist[6], timelist[7], vf, vg))
                        ah = convert_cmpermupw2_to_mperspw2(calc_a_avg(timelist[7], timelist[8], vg, vh))
                        print( "total distance of experiment = " + str(d_tot(distancelist)) + "cm")
                        print("average velocity 1 between sensor 1 and 2: " + str(va) + "m/s")
                        print("average velocity 2 between sensor 2 and 3: " + str(vb) + "m/s")
                        print("average velocity 3 between sensor 3 and 4: " + str(vc) + "m/s")
                        print("average velocity 4 between sensor 4 and 5: " + str(vd) + "m/s")
                        print("average velocity 5 between sensor 5 and 6: " + str(ve) + "m/s")
                        print("average velocity 6 between sensor 6 and 7: " + str(vf) + "m/s")
                        print("average velocity 7 between sensor 7 and 8: " + str(vg) + "m/s")
                        print("average velocity 8 between sensor 8 and 9: " + str(vh) + "m/s")
                        print("total average velocity " + str(finalv)  + "m/s")
                        print("average acceleration between velocities 2 and 3: " + str(ab) + "m/s")
                        print("average acceleration between velocities 3 and 4: " + str(ac) + "m/s")
                        print("average acceleration between velocities 4 and 5: " + str(ad) + "m/s")
                        print("average acceleration between velocities 5 and 6: " + str(ae) + "m/s")
                        print("average acceleration between velocities 6 and 7: " + str(af) + "m/s")
                        print("average acceleration between velocities 7 and 8: " + str(ag) + "m/s")
                        print("average acceleration between velocities 8 and 9: " + str(ah) + "m/s")
                        print("total average acceleration between velocities 2 and 9: " + str(finala)  + "m/s")

                except Exception as ers:
                    print("error:" + str(ers) + " has occured while trying to caclulate velocity and acceleration. Your data set maybe incomplete. Check your save file for experiment data.")
                if filename !=  "":
                    try:
                        print("saving......")
                        writetocsv(timedata, filename, distancelist, trial)
                        print("Complete. Data saved to " + filename + " .")
                    except Exception as er:
                        print("error:" + str(er) + "has occured while atttempting to save times to file. Please restart program and retry.")
                        print("If the error is access denied. Close the file window for the file you are trying to save to and continue the experiment.")
                trial = trial + 1
                count = 1
            if (xx.lower().startswith('n')):
                count = 2
                exit = True
                break
            if (xx.lower().startswith('q')):
                exit = True
                print("you have choosen to quit")
                break
            else:
                count = 1
####################################################################################################################################################
print("Goodbye and Goodluck and GODSPEED")
