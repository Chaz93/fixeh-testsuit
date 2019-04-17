import subprocess
import os
from time import gmtime, strftime

class Preparer(object):
    def __init__(self,err_log_file,base_dir,initial_dir):
        self.err_log_file = err_log_file
        if not os.path.exists(os.path.dirname(err_log_file)):
            os.makedirs(os.path.dirname(err_log_file))
        self.base_dir = base_dir
        self.initial_file = os.path.join(os.path.dirname(initial_dir),"initial.log")
        list = subprocess.Popen(['adb','shell','ls',self.base_dir+'/'],
                                stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        [stdout,stderr] = list.communicate()

        if stderr is not None and len(stderr) != 0:
            print("wrong cd storage :: %s \n" % stderr.decode('gbk'))
            return
        all_files = stdout.decode('gbk').split()
        if not os.path.exists(self.initial_file):
            with open(self.initial_file,'w') as fps:
                fps.write(stdout.decode('gbk'))
        else:
            with open(self.initial_file,'r') as rps:
                files = rps.read().split()
                for file in all_files:
                    if file in files:
                        continue
                    delete_path = os.path.join(self.base_dir,file)
                    deleter = subprocess.Popen(['adb','shell','rm','-r',delete_path],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    [_,stderr] = deleter.communicate()
                    if stderr is not None and len(stderr) != 0:
                        print("wrong delete storage :: %s \n" % stderr.decode('gbk'))
                        return

    def makedir(self,test_files):
        current_time = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
        for test_file in test_files:
            test_file = self.base_dir + "/" + test_file
            creator=subprocess.Popen(["adb","shell","mkdir",test_file],
                                     stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            (stdout,stderr) = creator.communicate()
            if stderr is not None and len(stderr) != 0:
                with open(self.err_log_file, 'a+') as fps:
                    fps.write("{time}:: err make dir: {dir_name}:: {err_message}".
                              format(time=current_time, dir_name=test_file,err_message=stderr.decode("gbk")) + "\n")

    def clear(self,test_files,ifdir=True):
        for test_file in test_files:
            current_time = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
            test_file = self.base_dir + "/" + test_file
            if ifdir:
                clear=subprocess.Popen(["adb", "shell", "rm", "-r",test_file],
                                       stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                (stdout, stderr) = clear.communicate()
                if stderr is not None and len(stderr) != 0:
                    with open(self.err_log_file, 'a+') as fps:
                        fps.write("{time}:: err clear: {dir_name}:: {err_message}".
                                  format(time=current_time, dir_name=test_file,err_message=stderr.decode("gbk")) + "\n")
            else:
                clear=subprocess.Popen(["adb", "shell", "rm",test_file],
                                       stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                (stdout, stderr) = clear.communicate()
                if stderr is not None and len(stderr) != 0:
                    with open(self.err_log_file, 'a+') as fps:
                        fps.write("{time}:: err clear: {dir_name}:: {err_message}".
                                  format(time=current_time, dir_name=test_file,err_message=stderr.decode("gbk")) + "\n")

    def copy(self,source_name, dest_dir, ifdir=True):
        current_time = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
        source_name = self.base_dir + "/" + source_name
        dest_dir = self.base_dir + "/" + dest_dir
        if ifdir:
            copy = subprocess.Popen(["adb", "shell", "cp","-r", source_name, dest_dir],
                                    stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            (stdout, stderr) = copy.communicate()
            if stderr is not None and len(stderr) != 0:
                with open(self.err_log_file, 'a+') as fps:
                    fps.write("{time}:: err copy1 dir: {source_name} to {dir_name}:: {err_message}".
                              format(time=current_time, source_name=source_name, dir_name=dest_dir,
                                     err_message=stderr.decode("gbk")) + "\n")
            return
        copy = subprocess.Popen(["adb", "shell", "cp", source_name, dest_dir],
                                stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        (stdout, stderr) = copy.communicate()
        if stderr is not None and len(stderr) != 0:
            with open(self.err_log_file, 'a+') as fps:
                fps.write("{time}:: err copy1 dir: {source_name} to {dir_name}:: {err_message}".
                          format( time=current_time, source_name=source_name,dir_name=dest_dir,
                                  err_message=stderr.decode("gbk")) + "\n")

    def push(self,source_name,tar_dir):
        current_time = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
        source_name = self.base_dir + "/" + source_name
        dest_dir = self.base_dir + "/" + tar_dir
        copy = subprocess.Popen(["adb", "push", source_name, dest_dir],
                                stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        (stdout, stderr) = copy.communicate()
        if stderr is not None and len(stderr) != 0:
            with open(self.err_log_file, 'a+') as fps:
                fps.write("{time}:: err push dir: {source_name} to {dir_name}:: {err_message}".
                          format( time=current_time, source_name=source_name,dir_name=dest_dir,
                                  err_message=stderr.decode("gbk")) + "\n")