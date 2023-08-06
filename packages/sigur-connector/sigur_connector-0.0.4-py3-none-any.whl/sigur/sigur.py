import logging
import re
from socket import AF_INET, SOCK_STREAM, socket, timeout


class SigurException(Exception):
    pass


class Sigur:
    def __init__(self, login, pwd, host='127.0.0.1', port=3312, logging_level=logging.INFO):
        self.login = login
        self.pwd = pwd
        self.BUFFER = 65565
        self.tcp_socket = None
        self.host = host
        self.port = port

        logger = logging.getLogger('Sigur')
        self.main_log_lvl = logging_level
        logger.setLevel(self.main_log_lvl)
        ch = logging.StreamHandler()
        ch.setLevel(self.main_log_lvl)
        formatter = logging.Formatter('[%(levelname)s] - %(filename)s - %(funcName)s - %(asctime)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        self.logger = logger
        self.ap_re = \
            re.compile(r'APINFO ID (?P<_id>\d+) NAME \"(?P<ap_name>.*)\" ZONEA \d+ ZONEB \d+ STATE (?P<state>\w+) \w+')

        self.create_socket()

    def create_socket(self):
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_socket.settimeout(10)
        try:
            self.tcp_socket.connect((self.host, self.port))
            self._login()
        except Exception:
            self.logger.exception('Connect error')
            raise Exception

    def _login(self):
        """Authorization

        """
        auth_str = '"LOGIN" 1.8 {} {}'.format(self.login, self.pwd)
        self.logger.debug(auth_str)
        answer = self._send(auth_str).strip()
        self.logger.debug(answer)
        if answer == 'OK':
            self.logger.info('Login success')
            return True
        else:
            self.logger.error('Login error')
            raise SigurException('Login error')
            return False

    def _send(self, data):
        """Send data and return answer

        """
        result = ''
        try:
            self.tcp_socket.send(str.encode(data + "\r\n"))
            while 1:
                data = bytes.decode(self.tcp_socket.recv(self.BUFFER))
                result += data
                self.logger.debug("We receive from socket - {}".format(data))
                if data == '': break
        except timeout:
            # timeout is normally
            self.logger.debug("End receive with timeout")
            return result.strip()

        except BrokenPipeError:
            # if connection is broken create connection again
            self.logger.info('Socket error')
            self.create_socket()
            self._send(data)

        except Exception:
            self.logger.exception('We have exception in send')
            raise

    def get_ap_list(self)->list:
        """ Get access point list from Sigur server

        :return: list of access point
        """
        result = self._send('GETAPLIST')
        if 'APLIST' not in result:
            raise SigurException('Wrong answer from server - ' + result)
        return [int(ap_id) for ap_id in result.replace('APLIST', '').strip().split()]

    def get_ap_state(self, ap_id: int)->dict:
        """

        :param ap_id: int access point id
        :return: dict  {'Name':...
                        'LinkState': ... ENUM('ONLINE', 'OFFLINE')
                        }
        """
        if not isinstance(ap_id, int):
            raise ValueError('ap_id must be integer')
        result = self._send('GETAPINFO {}'.format(ap_id))
        result.strip().split()
        # Sample result
        # APINFO ID 1 NAME "Door 1" ZONEA 18 ZONEB 0 STATE ONLINE_NORMAL CLOSED
        match_result = self.ap_re.match(result)
        if not match_result:
            raise SigurException('Wrong answer in get_ap_state - ' + ' '.join(result))
        match_result = match_result.groupdict()
        return {'Name': match_result['ap_name'],
                'LinkState': 'ONLINE' if 'ONLINE' in match_result['state'] else 'OFFLINE'
                }

if __name__ == '__main__':
    pass
