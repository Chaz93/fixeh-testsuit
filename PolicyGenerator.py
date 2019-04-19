
class PolicyGenerator(object):
    __filter_method = None
    __filter_class = None
    __filter_package = None
    __filter_stackkeyword = None
    __fixeh_head = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" \
                      "<fixeh>\n" \
    "   <remote-controller enable=\"false\" address=\"127.0.0.1\" port=\"7675\"/>\n" \
    "   <policy exclude=\"false\" search=\"false\" limit=\"-1\">\n"
    __method_fliter_format = '<policyentry kind = \"filter\" type = \"method\" value = \"%s\" %s/>\n'
    __class_fliter_format = '<policyentry kind = \"filter\" type = \"class\" value = \"%s\" %s/>\n'
    __package_fliter_format = '<policyentry kind = \"filter\" type = \"package\" value = \"%s\" %s/>\n'
    __exception_format = '<policyentry kind = \"exception\" value = \"%s\" %s maxcount=\"%s\"/>\n'
    __method_format = '<policyentry kind = \"method\" value = \"%s\" \"/>\n'
    __class_format = '<policyentry kind = \"class\" value = \"%s\" \"/>\n'
    __package_format = '<policyentry kind = \"package\" value = \"%s\" \"/>\n'
    __stackkeyword_format = 'stackkeyword=\"%s\"'
    __pattern_format = 'pattern=\"%s\"'
    __fixeh_end = "</policy>\n" \
    "</fixeh>"
    __exception = None
    __method = None
    __class = None
    __package = None
    __maxcount = str(-1)

    def __init__(self,tri_exception=None, tri_method=None, tri_class=None, tri_package=None, tri_maxcount=None):
        self.__exception = tri_exception
        self.__method = tri_method
        self.__class = tri_class
        self.__package = tri_package
        if tri_maxcount is None:
            __maxcount = str(-1)
        else:
            __maxcount = tri_maxcount

    def analyze_carsh_log(self,analyze_file,outformat_file):
        stackelement = None
        stacklocation = None
        with open(analyze_file,'r') as ana_fps:
            lines = ana_fps.readlines()
            for line in lines:
                if "Caused by" in line:
                    stackelement = "Found"
                    continue
                if stackelement is "Found":
                    stackelement = line.split('at ')[1].split('(')[0]
                    stacklocation = line.split('at ')[1].strip()
                    break
        if stacklocation is None or stackelement is None:
            print('wrong analyze crash file')
            exit(2)
        with open(outformat_file,"r") as tri_fps:
            lines = tri_fps.readlines()
            find_flag = False
            for line in lines:
                if stacklocation in line:
                    find_flag = True
                    continue
                if find_flag and 'triggering' in line:
                    method = line.split('exception on ')[1].split(' and such')[0].strip()
                    break
        if method is None:
            print('wrong analyze crash file')
            exit(2)
        self.__filter_method = method
        #self.__class = method[method.rfind(':') : ]
        #self.__package = self.__class[self.__class.rfind(':') : ]
        self.__stackkeyword = stackelement

    #just for trigger excepiton mode:
    def generator_methodfilter_policy(self):
        if self.__exception is None:
            print('triggerde Exception must be given!')
            exit(2) #2 stands for try to generate policy without key information
        method_string = ''
        if self.__method_fliter_format is not None:
            method_string += self.__method_format % (self.__method)
        class_string = ''
        if self.__class is not None:
            class_string += self.__class_format % (self.__class)
        package_string = ''
        if self.__package is not None:
            package_string += self.__package_format % (self.__package)
        if self.__filter_method is None:
            return self.__fixeh_head + self.__generator_exception_pattern() + self.__fixeh_end
        stackkeyword = ''
        if self.__stackkeyword is not None:
            stackkeyword = self.__stackkeyword_format % (self.__stackkeyword)
        return self.__fixeh_head + self.__method_fliter_format % (self.__filter_method, stackkeyword)\
               + self.__generator_exception_pattern() + self.__fixeh_end

    #every time only one method can be added
    def generator_increasement_methodfilters_policy(self,last_policy):
        policy = ''
        for line in last_policy.split('\n'):
            if 'maxcount' in line:
                if self.__filter_method is not None:
                    stackkeyword = ''
                    if self.__stackkeyword is not None:
                        stackkeyword = self.__stackkeyword_format % (self.__stackkeyword)
                    policy += self.__method_fliter_format % (self.__filter_method,stackkeyword)
            policy += line + '\n'
        return policy

    def __generator_exception_pattern(self,pattern=None):
        if self.__exception is None:
            return ''
        temp_pattern = ''
        if pattern is not None:
            temp_pattern = self.__pattern_format % pattern
        return self.__exception_format % (self.__exception,temp_pattern,self.__maxcount)

    def analyze_appium_error(self,appium_err_out_file,trigger_file):
        error = False
        method = None
        stackkeyword = None
        with open(appium_err_out_file,'r') as fps:
            if 'Traceback' in fps.read():
                error = True
        if error:
            with open(trigger_file,'r') as tf_fps:
                while True:
                    line = tf_fps.readline()
                    if line:
                        if 'triggering' in line:
                            method = line.split('exception on ')[1].strip()
                            line = tf_fps.readline()
                            while not '\tat ' in line:
                                line = tf_fps.readline()
                            stackkeyword = line.split('at ')[1].split('(')[0].strip()
                    else:break
            if method is None or stackkeyword is None:
                print('wrong get trigger_file key value')
                exit(2)
            self.__stackkeyword = stackkeyword
            self.__filter_method = method

        return error