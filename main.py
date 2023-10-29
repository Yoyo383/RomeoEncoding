"""
Author: Yoad Winter
Date: 28.10.23
Description: A program that encrypts and decrypts messages using an encryption table.
Note: In the logging I print encrypted and decrypted messages with triangular brackets like this: <msg>.
That is because they are not in the encryption table (unlike ' and ") and I wanted these messages to be
differentiated from words that aren't in the message.
"""

import sys
import os
import logging

LOG_FORMAT = '[%(levelname)s | %(asctime)s | %(processName)s] %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/romeo.log'

ENCRYPT_DICT = {
    'A': '56', 'B': '57', 'C': '58', 'D': '59', 'E': '40', 'F': '41', 'G': '42', 'H': '43', 'I': '44',
    'J': '45', 'K': '46', 'L': '47', 'M': '48', 'N': '49', 'O': '60', 'P': '61', 'Q': '62', 'R': '63',
    'S': '64', 'T': '65', 'U': '66', 'V': '67', 'W': '68', 'X': '69', 'Y': '10', 'Z': '11', 'a': '12',
    'b': '13', 'c': '14', 'd': '15', 'e': '16', 'f': '17', 'g': '18', 'h': '19', 'i': '30', 'j': '31',
    'k': '32', 'l': '33', 'm': '34', 'n': '35', 'o': '36', 'p': '37', 'q': '38', 'r': '39', 's': '90',
    't': '91', 'u': '92', 'v': '93', 'w': '94', 'x': '95', 'y': '96', 'z': '97', ' ': '98', ',': '99',
    '.': '100', ';': '101', "'": '102', '?': '103', '!': '104', ':': '105'
}


def read_file(filepath):
    """
    Reads a file's content and returns it. If the file doesn't exist, returns None.
    :param filepath: The path to the file.
    :type filepath: str
    :rtype: str | None
    :return: Content of file if it exists, otherwise None.
    """
    try:
        with open('encrypted_msg.txt', 'r') as file:
            content = file.read()
            logging.debug(f'Successfully read {filepath}.')
            return content
    except IOError:
        print(f'{filepath} not found.')
        logging.error(f'{filepath} not found.')


def write_to_file(filepath, string):
    """
    Writes a string to a file.
    :param filepath: The path to the file.
    :type filepath: str
    :param string: The string to be written.
    :type string: str
    :return: None
    """
    with open(filepath, 'w') as file:
        file.write(string)
        logging.debug(f'Successfully written <{string}> to {filepath}.')


def encrypt_msg(msg):
    """
    Encrypts the message and returns it.
    :param msg: The message to encrypt.
    :type msg: str
    :rtype: str
    :return: The encrypted message.
    """
    return ','.join([ENCRYPT_DICT[x] for x in msg])


def decrypt_msg(msg):
    """
    Decrypts the encrypted message and returns it.
    :param msg: The encrypted message.
    :type msg: str
    :rtype: str
    :return: The decrypted message.
    """
    values = list(ENCRYPT_DICT.values())
    keys = list(ENCRYPT_DICT.keys())

    return ''.join(keys[values.index(x)] for x in msg.split(','))


def encrypt():
    """
    Gets message from user, encrypts it, and puts it in encrypted_msg.txt
    :return: None
    """
    msg = input('Enter your message: ')
    logging.debug(f'User entered: {msg}')

    encrypted = encrypt_msg(msg)
    logging.info(f'Encrypted <{msg}> to <{encrypted}>')

    write_to_file('encrypted_msg.txt', encrypted)

    print('The encrypted message is saved in encrypted_msg.txt')
    logging.info('The encrypted message is saved in encrypted_msg.txt')


def decrypt():
    """
    Decrypts message from encrypted_msg.txt (if exists) and prints it.
    :return: None
    """
    msg = read_file('encrypted_msg.txt')
    if msg is None:
        return

    decrypted = decrypt_msg(msg)
    print(f'Decrypted message from encrypted_msg.txt is: {decrypted}')
    logging.info(f'Message in encrypted_msg.txt: {msg}')
    logging.info(f'Decrypted <{msg}> to <{decrypted}>')


def main():
    """
    The main function.
    :return: None
    """
    if len(sys.argv) < 2:
        print("Argument not found. Please specify 'encrypt' or 'decrypt' when running the program.")
        logging.warning('User did not enter an argument.')
        return

    if sys.argv[1] == 'encrypt':
        logging.debug('Started encrypting process.')
        encrypt()
        logging.debug('Finished encrypting process.')
    elif sys.argv[1] == 'decrypt':
        logging.debug('Started decrypting process.')
        decrypt()
        logging.debug('Finished decrypting process.')
    else:
        print("Argument not valid. Please specify 'encrypt' or 'decrypt' when running the program.")
        logging.warning(f"User entered '{sys.argv[1]}', invalid argument.")


if __name__ == '__main__':
    # initialize logging
    if not os.path.isdir(LOG_DIR):
        os.mkdir(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)

    # testing encrypt_msg and decrypt_msg
    assert (encrypt_msg('My bounty is as boundless as the sea, My love as deep; the more I give to thee, The more I '
                        'have, for both are infinite.')
            == ('48,96,98,13,36,92,35,91,96,98,30,90,98,12,90,98,13,36,92,'
                '35,15,33,16,90,90,98,12,90,98,91,19,16,98,90,16,12,99,98,'
                '48,96,98,33,36,93,16,98,12,90,98,15,16,16,37,101,98,91,'
                '19,16,98,34,36,39,16,98,44,98,18,30,93,16,98,91,36,98,91,'
                '19,16,16,99,98,65,19,16,98,34,36,39,16,98,44,98,19,12,93,'
                '16,99,98,17,36,39,98,13,36,91,19,98,12,39,16,98,30,35,17,'
                '30,35,30,91,16,100'))
    assert (decrypt_msg('59,36,35,102,91,98,94,12,90,91,16,98,96,36,92,39,98,33,36,93,16,98,36,35,98,90,36,34,16,13,'
                        '36,15,96,99,98,94,19,36,98,15,36,16,90,35,102,91,98,93,12,33,92,16,98,30,91,100')
            == "Don't waste your love on somebody, who doesn't value it.")

    main()
