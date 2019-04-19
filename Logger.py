import subprocess
import os
#import psutil
import time

class Logger(object):
    def __init__(self, output_dir, app_package_name):
        self.output_dir = output_dir
        self.temp_output = os.path.join(output_dir, "temp.out")
        self.output = os.path.join(output_dir, "format-out.out")
        self.simple_output = os.path.join(output_dir,"simple-out.out")
        self.triggering_out = os.path.join(output_dir,"trigger.log")
        self.crash_out = os.path.join(output_dir,"crash-stack.log")
        self.logger = None
        self.app_package_name = app_package_name
        self.tag = os.path.split(output_dir)[1]

    def begin_log(self):
        log_cleaner = subprocess.Popen(['adb', 'logcat', '-c'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = log_cleaner.communicate()
        if stderr is not None and len(stderr) != 0:
            print('error clean log with message: %s', stderr.decode('gbk'))
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        with open(self.temp_output, "w+") as fps:
            self.logger = subprocess.Popen(["adb","shell","logcat"],stdout=fps, stderr=fps)


    #def close_old(self):
        #parent = psutil.Process(self.logger.pid)
        #children = parent.children(recursive=True)
        #for child in children:
        #    child.kill()
        #gone, still_alive = psutil.wait_procs(children,timeout=5)
        #parent.kill()
        #parent.wait(5)

    def close(self):
        l_pid=self.logger.pid
        self.logger.terminate()
        time.sleep(5)
        #if psutil.pid_exists(l_pid):
            #self.close_old()

    def get_pid(self):
        pid_catcher = subprocess.Popen(['adb','shell', 'ps', '|','grep', self.app_package_name],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr)=pid_catcher.communicate()
        if stderr is not None and len(stderr) != 0:
            print("fail to get pid with info: %s" % stderr.decode('gbk'))
            return None
        pid = stdout.decode('gbk').split()[1]
        return pid

    def generate_log_file(self,pid=None):

        crashstack = []
        trigger_stack = False
        trigger_exception = False
        with open(self.temp_output,'r') as temp_fps:
            while True:
                line = temp_fps.readline()
                if 'fixeh' in line:
                    pid = line.split(' ')[2]
                    break
                if not line:
                    print('fail to get pid!')
                    exit(2)
        with open(self.temp_output, 'r') as fps , open(self.output, 'a+') as out_fps,\
                open(self.simple_output,'a+') as sim_fps, open(self.triggering_out,'a+') as tri_fps:
            for line in fps.readlines():
                if pid in line:
                    out_fps.write(line)
                    if "I fixeh" in line:
                        sim_fps.write(line)
                        if "triggering" in line or trigger_stack:
                            if not trigger_stack:
                                tri_fps.write("Test"+self.tag +" :: "+ line)
                                trigger_stack = True
                                trigger_exception = True
                                continue
                            if trigger_exception:
                                if 'Exception' in line:
                                    tri_fps.write(line)
                                trigger_exception =  False
                                continue
                            if trigger_stack and '\tat' in line:
                                tri_fps.write(line)
                                continue
                            trigger_stack = False
                            #trigger_stack = not trigger_stack
                if "beginning of crash" in line:
                    if pid in line:
                        crashstack.append(line)
                    continue
                if len(crashstack) != 0:
                    if "AndroidRuntime" in line:
                        if pid in line:
                            crashstack.append(line)
                    else:
                        with open(self.crash_out,'a+') as cra_fps:
                            cra_fps.writelines(crashstack)
                            crashstack.clear()
                    continue

        os.remove(self.temp_output)