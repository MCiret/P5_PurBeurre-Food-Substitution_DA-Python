#!/usr/bin/env python3

import control as ct


def main():
    if ct.load_data():
        print("ALL GOOD :-)")
    else:
        exit()


if __name__ == '__main__':
    main()
