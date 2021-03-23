#!/usr/bin/env python3
import os, sys
from FoodSubstitution.controls import Controller


def main():
    #######################################
    print("\n***** Current working dir : ", os.getcwd())
    print("\n***** PATH *****")
    for path in sys.path:
        print(path)
    print("")
    #######################################

    controller = Controller()
    controller.run_data_initialization()
    controller.run_main_menu()
       

if __name__ == '__main__':
    main()
