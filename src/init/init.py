import tools

if __name__ == '__main__':
    path = '/config/config.xml'

    env = tools.get_env_parameter()
    tools.reconcile(env, path)
