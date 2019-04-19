import PolicyGenerator


if __name__ == '__main__':
   generator = PolicyGenerator.PolicyGenerator(tri_exception='java.io.IOException',tri_maxcount='2')
   #generator.analyze_carsh_log(analyze_file='1.log',outformat_file='2.log')
   policy = generator.generator_methodfilter_policy()
   print(policy)
   generator.analyze_appium_error(appium_err_out_file='test/0/LOG.log',trigger_file='test/0/trigger.log')
   policy = generator.generator_increasement_methodfilters_policy(last_policy=policy)
   print('*************************************************************')
   print(policy)
