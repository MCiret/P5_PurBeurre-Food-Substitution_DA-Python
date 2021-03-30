#!/usr/bin/env python3
import os, sys
import foodsubstitution.controls as ct

def main():
    #######################################
    print("\n***** Current working dir : ", os.getcwd())
    print("\n***** PATH *****")
    for path in sys.path:
        print(path)
    print("")
    #######################################

    ct.FullControl().full_run()
    

if __name__ == '__main__':
    main()
