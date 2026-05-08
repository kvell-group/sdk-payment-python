class KvellSettings:
    """
    Kvell - https://docs.kvell.group/
    """

    __pay_host: str = None
    __customer_host: str = None
    __api_host: str = None
    __baas_host: str = None

    __api_key: str = None
    __secret_key: str = None
    __private_key: str = None

    def __init__(
        self,
        pay_host: str = "https://pay.kvell.group",
        api_host: str = "https://api.pay.kvell.group",
        customer_host: str = "https://customer.pay.kvell.group",
        baas_host: str = "https://api.baas.kvell.group",
        api_key: str = "",
        secret_key: str = "",
        private_key: str = "",
    ):
        self.__pay_host = pay_host
        self.__api_host = api_host
        self.__customer_host = customer_host
        self.__baas_host = baas_host

        self.__api_key = api_key
        self.__secret_key = secret_key
        self.__private_key = private_key

    def get_pay_host(self) -> str:
        return self.__pay_host

    def get_api_host(self) -> str:
        return self.__api_host

    def get_baas_host(self) -> str:
        return self.__baas_host

    def get_api_key(self) -> str:
        return self.__api_key

    def get_secret_key(self) -> str:
        return self.__secret_key

    def get_private_key(self) -> str:
        return self.__private_key

    def get_customer_host(self) -> str:
        return self.__customer_host
