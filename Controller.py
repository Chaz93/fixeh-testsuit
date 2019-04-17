import PolicyGenerator
import getopt
import sys
import os
import subprocess


def usage() :
    pass


if __name__ == "__main__" :

    options, args = getopt.getopt(sys.argv[1:],'he:p:c:m:P:C:M:t:T',['help','excepiton=','package=','class=','method=',
                                                             'filter_package=','filter_class=','filter_method=',
                                                             'maxcount=','test_dir=','testcase='])
    policy_file = 'fixeh-policy.xml'
    dest_dir = '/data/local/tmp'
    crash_log = 'crash-stack.log'
    format_output = 'format-out.out'
    final_log = 'LOG.log'
    tri_maxcount = None
    tri_exception = None
    tri_package = None
    tri_class = None
    tri_method = None
    filter_package = None
    filter_class = None
    filter_method = None
    test_dir = None
    testcase = None


    try:
        for name,value in options:
            if name in('-h','--help'):
                usage()
            if name in ('-e','--exception'):
                tri_exception = value
            if name in ('-p','--package'):
                tri_package = value
            if name in ('-c','--class'):
                tri_class = value
            if name in ('-m','--method'):
                tri_method = value
            if name in ('-P','--filter_package'):
                filter_package = value
            if name in ('-C','--filter_class'):
                filter_class = value
            if name in ('-M','--filter__method'):
                filter_method = value
            if name is '--maxcount':
                tri_maxcount = value
            if name in ('-t','--test_dir'):
                test_dir = value
            if name in ('-T','--testcase'):
                testcase = os.path.join(os.getcwd(),value)
    except getopt.GetoptError:
        usage()
        exit(30) # get wrong opt parameter


    test_id = 0
    flag = True
    test_dir = os.path.join(os.getcwd,test_dir)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    assert(os.path.exists(test_dir))

    last_policy = None

    while flag:
        current_test_dir = os.path.join(test_dir,str(test_id))
        current_log = os.path.join(current_test_dir,final_log)
        policygenerator = PolicyGenerator.PolicyGenerator(tri_exception=tri_exception, tri_method=tri_method, tri_class=tri_class,
                                          tri_package=tri_package, tri_maxcount=tri_maxcount)
        if test_id == 0:
            last_policy = policygenerator.generator_methodfilter_policy()
        else:
            log_file = os.path.join(test_dir,str(test_id - 1),crash_log)
            format_file = os.path.join(test_id,str(test_id - 1),format_output)
            if not os.path.exists(log_file):
                print('end crash at %d turn' % test_id)
                exit(1)
            policygenerator.analyze_carsh_log(analyze_file=log_file, outformat_file=format_output)
            last_policy = policygenerator.generator_increasemetn_methodfilters_policy(last_policy=last_policy)

        current_policy_file=os.path.join(current_test_dir,policy_file)

        # copy to file
        with open(current_policy_file,'w') as fps:
            fps.writelines(last_policy)
        # push file
        pusher = subprocess.Popen(['adb','push',current_policy_file,dest_dir],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (stdout, stderr) = pusher.communicate()
        if stderr is not None and len(stderr) is not 0:
            print('wrong push fixeh-policy.xml')
            exit(4) #stands for something is error whild call subprocess

        with open(current_log,'w') as l_fps:
            appium_conductor = subprocess.Popen(['python',testcase],stdout=l_fps,stderr=l_fps)
            appium_conductor.communicate()

        if not os.path.exists(current_test_dir,crash_log):
            flag = False

