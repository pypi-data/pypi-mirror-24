def main(*args):
    from pyconrad import PyConrad

    # PyConrad is a singleton class
    pyconrad = PyConrad()
    # setup PyConrad
    pyconrad.setup()
    # start CONRAD
    pyconrad.start_reconstruction_filter_pipeline()

if __name__ == '__main__':
     main()
