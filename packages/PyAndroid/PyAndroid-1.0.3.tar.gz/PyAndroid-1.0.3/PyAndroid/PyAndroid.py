# PYANDROID
# VERSION 1.0 BETA

# USES:
# android_version(e*)
# sdk_version(e) 
# android_name(e)
# processor_machine()
# ram_total(type_) 
# directory_size(directory) 
# min_sdk(version) 
# program() 
# device_brand(e) 
# device_model(e)
# device_time(e) 
# copy_build(path, +filename) 
# * e = +with_error

import re
import os, platform
import datetime 
try:
    f = open("/system/build.prop", 'r')

    # CHECK SYSTEM

    work = True
    if not os.path.exists('/system/build.prop'):
        if not platform.system() == 'Linux':
            print('PyDroid Error: PyAndroid work only on android.\nYour system is {}. '.format(platform.system()))
        else:
            print("PyDroid Error: PyAndroid can't read system folder (PERMISSIONS DENITED). ")
        work = False
        exit()

    # GET ANDROID VERSION

    def android_version(with_error=True):
        try:
            ver = 'Error'
            for line in open('/system/build.prop'):
                mth = re.search("ro.build.version.release=(.*)", line)
                if mth:
                    ver = mth.group(1)
            if ver == 'Error':
                if with_error == True:
                    ver = 'Error'
                else:
                    ver = None
            return ver
        except:
            if with_error == True:
                return 'Error'

    # ANDROID SDK VERSION

    def sdk_version(with_error = True):
        try:
            ver = 'Error'
            for line in open('/system/build.prop'):
                mth = re.search("ro.build.version.sdk=(.*)", line)
                if mth:
                    ver = mth.group(1)
            if ver == 'Error':
                if with_error == True:
                    ver = 'Error'
                else:
                    ver = None
            else:
                ver = int(ver)
            return ver
        except:
            if with_error == True:
                return 'Error'

    # GET ANDROID NAME

    def android_name(with_error = True):
        if type(sdk_version(with_error)) == int:
            try:
                v = sdk_version(with_error)
                name = 'Error'
                if v == 1 or v == 2:
                    name = 'Null'
                if v == 3:
                    name = 'Cupcake'
                if v == 4:
                    name = 'Donut'
                if v >= 5 and v <= 7:
                    name = 'Eclair'
                if v == 8:
                    name = 'Froyo'
                if v == 9 or v == 10:
                    name = 'Gingerbread'
                if v >= 11 and v <= 13:
                    name = 'Honeycomb'
                if v == 14 or v == 15:
                    name = 'Ice cream sandwich'
                if v >= 16 and v <= 18:
                    name = 'Jelly bean'
                if v == 19 or v == 20:
                    name = 'Kitkat'
                if v == 21 or v == 22:
                    name = 'Lollipop'
                if v == 23:
                    name = 'Marshmallow'
                if v == 24 or v == 25:
                    name = 'Nougat'
                if v == 26:
                    name = 'O'
                if v > 26:
                    name = 'Future...'
                if name == 'Error' and with_error == False:
                    pass
                else:
                    return name
            except:
                if with_error == True:
                    return 'Error'
                else:
                    pass
        else:
            if with_error == True:
                return 'Error'
            else:
                pass

    # GET PROCESSOR MACHINE

    def processor_machine():
        return platform.machine()
        
    # GET RAM INFORMATION

    def ram_total(type_):
        ins = type_  
        mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') # e.g. 4015976448
        mem_gib = mem_bytes/(1024.**3) # e.g. 3.74
        mem_mb = mem_gib * 1024   
        rammb = int(mem_mb)
        if ins == 'B':
            return mem_bytes
        if ins == 'KB':
            return int(mem_bytes / 1024)
        if ins == 'MB':
            return int(mem_bytes / 1024 / 1024)
        if ins == 'GB':
            return float(mem_bytes / 1024 / 1024 / 1024)
        if ins == 'TB':
            return float(mem_bytes / 1024 / 1024 / 1024 / 1024)
        if ins == 'PB':
            return float(mem_bytes / 1024 / 1024 / 1024 / 1024 / 1024)

    # GET DIRECTORY SIZE

    def directory_size(directory):
        a = os.popen('du -ks "{}"'.format(directory)).read() 
        a = str(a)
        try:
            ssscache = int(a[1]) 
        except:
            return 'Error'
            exit()
        b = -1
        c = '' 
        e = '' 
        d = False
        while d != True:
            b += 1
            try:
                c = int(a[b]) 
                e += str(c) 
            except:
                d = True
        return int(e) 

    # MIN ANDROID SDK REQUIRE FOR SCRIPT

    def min_sdk(version):
        if type(sdk_version(with_error = True)) == int:
            if sdk_version(with_error = True) < version:
                print('You require android {} or higher to run script.\nYou have android {} . '.format(converter(version), android_version())) 
                exit()
            else:
                pass
                return 1
        else:
            return 'Error' 

    # GET PYTHON3 IDE

    def program():
        prog = 'Unknown'
        if platform.python_version() == '3.2.2':
            prog = 'qpython3' 
        if platform.python_version() == '3.6.0':
            prog = 'Dcoder' 
        return prog

    # GET DEVICE BRAND

    def device_brand(with_error = True):
        try:
            brand = None
            for line in open('/system/build.prop'):
                mth = re.search("ro.product.brand=(.*)", line)
                if mth:
                    brand = mth.group(1)
            if brand == None and with_error == True:
                brand = 'Error'
            return brand   
        except:
            if with_error == True:
                return 'Error'

    # GET DEVICE CREATION TIME

    def device_time(with_error = True, date = True, autoconvert = True):
        try:
            if autoconvert == True:
                time = None
                for line in open('/system/build.prop'):
                    mth = re.search("ro.build.date.utc=(.*)", line)
                    if mth:
                        time = mth.group(1)
                if time == None and with_error == True:
                    time = 'Error'
                if date == True:
                    time = datetime.datetime.fromtimestamp(int(time)).strftime('%c')
                else:
                    time = int(time)
                return time
            else:
                time = None
                for line in open('/system/build.prop'):
                    mth = re.search("ro.build.date=(.*)", line)
                    if mth:
                        time = mth.group(1)
                if time == None and with_error == True:
                    time = 'Error'
                time = str(time)
                return time
        except:
            if with_error == True:
                return 'Error'

    # GET MODEL

    def device_model(with_error = True):
        try:
            mdl = None
            for line in open('/system/build.prop'):
                mth = re.search("ro.product.model=(.*)", line)
                if mth:
                    mdl = mth.group(1)
            if mdl == None and with_error == True:
                mdl = 'Error'
            return mdl
        except:
            if with_error == True:
                return 'Error'

    # COPY BUILD.PROP

    def build_copy(path, filename = 'build.prop'):
        try:
            if path[-10:-1] == 'build.prop' or path[-10:-1] == 'build.pro':
                path = str(path[0:-10])    
            if path[-1] == '/':
                path = str(path[0:-1])
            f = open('{}/{}'.format(path, filename), 'w+')
            for line in open('/system/build.prop'):
                f.write(line) 
            f.close()
            return str(path+'/'+filename)
        except:
            return 'Error'

    # CONVERT SDK TO ANDROID

    def converter(api):
        sdk = int(api) 
        if sdk == 1:
            android = '1.0' 
        if sdk == 2:
            android = '1.1' 
        if sdk == 3:
            android = '1.5' 
        if sdk == 4:
            android = '1.6' 
        if sdk == 5:
            android = '2.0'
        if sdk == 6:
            android = '2.0.1' 
        if sdk == 7:
            android = '2.1'
        if sdk == 8:
            android = '2.2' 
        if sdk == 9:
            android = '2.3' 
        if sdk == 10:
            android = '2.3.3' 
        if sdk == 11:
            android = '3.0' 
        if sdk == 12:
            android = '3.1' 
        if sdk == 13:
            android = '3.2' 
        if sdk == 14:
            android = '4.0' 
        if sdk == 15:
            android = '4.0.3' 
        if sdk == 16:
            android = '4.1' 
        if sdk == 17:
            android = '4.2' 
        if sdk == 18:
            android = '4.3' 
        if sdk == 19:
            android = '4.4' 
        if sdk == 20:
            android = '5.0 (dev) ' 
        if sdk == 21:
            android = '5.0' 
        if sdk == 22:
            android = '5.1' 
        if sdk == 23:
            android = '6.0' 
        if sdk == 24:
            android = '7.0' 
        if sdk == 25:
            android = '7.1' 
        if sdk == 26:
            android = '8.0' 
        if sdk >= 27:
            android = 'future... '
        return android

    # THE END OF VERSION 1.0
except:
    print('PyAndroid error. Please use only on android, if you see this and your os is android you can write to on olokelo@gmail.com')
