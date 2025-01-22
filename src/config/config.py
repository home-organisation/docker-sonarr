import tools

if __name__ == '__main__':

    tools.reconcile(desired=tools.get_env_parameter(), current=tools.get_db_parameter())
    tools.restart()