from admin.common import Common


class SignMsg(Common):

    def __init__(self):
        super().__init__()

    def initEnv(self):
        pass

    def start(self):
        try:
            super().get_signing_info()

            msg = self.take_input("\n\nEnter the msg you want to sign: ", True)
            sig = self.sign(msg, self.seed)
            print("\n\n")
            print("msg: {}".format(msg))
            print("signature: {}".format(sig))
            print("\n\n")
        except Exception as e:
            print("\nError occurred: {}\n".format(repr(e)))
        except KeyboardInterrupt:
            print("\n\nExited\n")
