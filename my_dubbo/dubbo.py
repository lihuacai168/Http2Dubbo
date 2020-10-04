import ast
import json
import telnetlib


class Dubbo(telnetlib.Telnet):
    cmd_prefix = 'dubbo>'

    # 初始化Telnet连接
    def __init__(self, host=None, port=0):
        super().__init__(host, port)
        self.write(b'\n')
        self.read_until(self.cmd_prefix.encode())

    def _write_cmd(self, cmd: str = ""):
        self.write(cmd.encode() + b"\n")

    # 执行命令，并且返回结果，结果是list
    def _exec_cmd(self) -> list:
        res: bytes = self.read_until(Dubbo.cmd_prefix.encode())
        res: list = res.decode('utf-8').split('\r\n')
        if len(res) > 0:
            # ['"Name: Riksai, Age: 18, Gender: MALE"', 'elapsed: 0 ms.', 'dubbo>']
            # 去掉最后多余的'dubbo>'
            res.pop()
        return res

    @staticmethod
    def parser_arg(*args):
        """
        >>> parser_arg(1, 3, {"k": "v"})
        "(1, 3, {'k': 'v'})"
        :param args:
        :return:
        """
        return json.dumps(str(args).replace("[", '').replace(']', '')).replace('"', '')

    # 调用dubbo接口，返回结果，dict类型
    def invoke(self, service_name, method_name, *args) -> dict:
        params = self.parser_arg(*args)
        command_str = f"invoke {service_name}.{method_name}{params}"
        self._write_cmd(command_str)
        res: list = self._exec_cmd()
        if len(res) == 2:
            # ['{"status":true}', 'elapsed: 10 ms.']
            parsed_res = ast.literal_eval(
                res[0].replace("true", "True").replace("false", "False").replace("null", "None"))
            elapsed: list = res[1].replace(':', '').replace('.', '').split()
            elapsed: str = elapsed[1] + elapsed[2]
            return {'res': parsed_res, 'elapsed': elapsed}
        else:
            return {'res': res[0]}

    # 显示服务列表
    # ['com.example.service.Greetings']
    def ls(self, *args):
        """
        ls('Greetings')
        ['say', 'hello']
        :param args:
        :return:
        """
        base_cmd = ('ls',)
        return self.cmd(*(base_cmd + args))

    # 显示服务详细信息列表
    # ['com.example.service.Greetings -> dubbo://172.19.0.3:20880/com.example.service.Greetings?anyhost=true&application=producer-app&dubbo=2.5.3&interface=com.example.service.Greetings&methods=say,hello&pid=1&revision=1.0-SNAPSHOT&side=provider&timestamp=1601610125027']
    def ll(self, *args):
        """
        >>> ll('Greetings')
        ['java.lang.String say(java.lang.String)', 'java.lang.String hello(com.example.service.User)']

        >>> ll('com.example.service.Greetings')
        ['java.lang.String say(java.lang.String)', 'java.lang.String hello(com.example.service.User)']
        """
        return self.ls('-l', *args)

    def ps(self, *args):
        base_cmd = ('ps',)
        return self.cmd(*(base_cmd + args))

    # 执行通用命令
    def cmd(self, *args):
        self._write_cmd(' '.join(args))
        return self._exec_cmd()

    @staticmethod
    def parse_method(method_info: str) -> dict:
        """
        >>> parse_method('java.lang.String say(java.lang.String)')
        [{'method_name': 'say', 'return_type': 'java.lang.String', 'params': ['java.lang.String']}, {'method_name': 'hello', 'return_type': 'java.lang.String', 'params': ['com.example.service.User']}]

        :param method_info:
        :return:
        """
        if len(method_info.split()) != 2:
            return {"res": "parser error"}
        return_type, method_params = method_info.split()
        params_start: int = method_params.find('(')
        params_end: int = method_params.find(')')
        method_name: str = method_params[:params_start]
        params: list = method_params[params_start + 1:params_end].split(',')
        return {
            "method_name": method_name,
            "return_type": return_type,
            "params": params
        }

    def get_service_method(self, service_name: str) -> list:
        methods = []
        for i in self.ll(service_name):
            methods.append(Dubbo.parse_method(i))
        return methods


if __name__ == '__main__':
    interface = 'com.example.service.Greetings'
    method = 'hello'
    data = {"class": "com.example.service.User", "name": "Riksai", "age": 18, "gender": "MALE"}
    conn = Dubbo('localhost', 20880)
    print(conn.invoke(interface, method, data))
    print(conn.invoke(interface, 'say', 'Rikasai'))
    print(conn.ls())
    print(conn.ll())
    print(conn.ls('Greetings'))
    print(conn.ll('Greetings'))
    print(conn.get_service_method('com.example.service.Greetings'))
